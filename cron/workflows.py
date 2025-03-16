#!/usr/bin/env python3
import os
import httpx
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# N8N API Configuration
N8N_HOST = os.getenv("N8N_HOST", "http://localhost")
N8N_PORT = os.getenv("N8N_PORT", "5678")
N8N_PATH = os.getenv("N8N_PATH", "")
N8N_API_KEY = os.getenv("N8N_API_KEY")
N8N_API_VERSION = os.getenv("N8N_API_VERSION", "1")


class N8NClient:
    def __init__(self):
        if not N8N_API_KEY:
            raise ValueError("N8N_API_KEY environment variable is not set")
        
        # Construct the base URL
        self.base_url = f"{N8N_HOST}:{N8N_PORT}/{N8N_PATH}".rstrip("/")
        self.api_url = f"{self.base_url}/api/v{N8N_API_VERSION}"
        self.headers = {
            "accept": "application/json",
            "X-N8N-API-KEY": N8N_API_KEY
        }
        self.client = httpx.Client(timeout=30.0)
    
    def get_all_workflows(self, active=True):
        """
        Retrieve all workflows from the n8n instance.
        
        Args:
            active: If True, only return active workflows
            
        Returns:
            List of workflow objects
        """
        url = f"{self.api_url}/workflows"
        params = {"active": str(active).lower()}
        
        try:
            print(f"Fetching workflows with params: {params}")
            response = self.client.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            workflows = response.json()
            print(f"Retrieved {len(workflows)} workflows")
            return workflows
        except Exception as e:
            print(f"Error occurred while fetching workflows: {e}")
            raise
    
    def get_workflow_executions(self, workflow_id):
        """
        Retrieve executions for a specific workflow.
        
        Args:
            workflow_id: The ID of the workflow
            
        Returns:
            List of execution objects
        """
        url = f"{self.api_url}/executions"
        params = {
            "workflowId": workflow_id,
            "limit": 250  # Maximum allowed by the API
        }
        
        all_executions = []
        cursor = None
        page_count = 0
        
        try:
            print(f"Fetching executions for workflow {workflow_id}")
            
            while True:
                page_count += 1
                
                # Add cursor to params if we have one
                if cursor:
                    params["cursor"] = cursor
                
                response = self.client.get(url, headers=self.headers, params=params)
                response.raise_for_status()
                response_data = response.json()
                
                # Extract executions and next cursor
                executions = response_data.get("data", [])
                next_cursor = response_data.get("nextCursor")
                
                all_executions.extend(executions)
                print(f"Retrieved page {page_count} with {len(executions)} executions for workflow {workflow_id}")
                
                # If there's no next cursor, we've reached the end
                if not next_cursor:
                    break
                    
                # Update cursor for next iteration
                cursor = next_cursor
            
            print(f"Retrieved a total of {len(all_executions)} executions for workflow {workflow_id}")
            return all_executions
        except Exception as e:
            print(f"Error occurred while fetching executions for workflow {workflow_id}: {e}")
            raise


def main():
    """Main function to retrieve all workflows and their executions."""
    try:
        client = N8NClient()
        
        # Get all active workflows
        workflows = client.get_all_workflows(active=True)
        
        # Get executions for each workflow
        all_executions = []
        for workflow in workflows:
            workflow_id = workflow.get("id")
            workflow_name = workflow.get("name", "Unknown")
            
            if workflow_id:
                print(f"Processing workflow: {workflow_name} (ID: {workflow_id})")
                executions = client.get_workflow_executions(workflow_id)
                
                # Add workflow info to each execution for easier identification
                for execution in executions:
                    execution["workflowName"] = workflow_name
                
                all_executions.extend(executions)
            else:
                print(f"Skipping workflow with missing ID: {workflow_name}")
        
        # Print summary
        print(f"Total workflows: {len(workflows)}")
        print(f"Total executions: {len(all_executions)}")
        
        # Here you can add code to process the executions data
        # For example, store in a database, send notifications, etc.
        
        return {
            "workflows_count": len(workflows),
            "executions_count": len(all_executions),
            "executions": all_executions
        }
    
    except Exception as e:
        print(f"Error in main function: {e}")
        raise


if __name__ == "__main__":
    main()
