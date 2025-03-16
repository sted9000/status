# N8N Workflow Monitor

This script fetches all workflows from an n8n server and retrieves their executions.

## Requirements

- Python 3.7+
- Required packages:
  - httpx
  - python-dotenv

## Setup

1. Copy the `.env.example` file to `.env`:
   ```
   cp .env.example .env
   ```

2. Edit the `.env` file with your n8n server details:
   ```
   N8N_HOST=http://your-n8n-host
   N8N_PORT=5678
   N8N_PATH=your-path  # Leave empty if n8n is at the root
   N8N_API_KEY=your_n8n_api_key_here
   N8N_API_VERSION=1
   ```

3. Install the required packages:
   ```
   pip install httpx python-dotenv
   ```

## Usage

Run the script:

```
python workflows.py
```

The script will:
1. Connect to your n8n server
2. Fetch all active workflows
3. For each workflow, retrieve all available executions
4. Print information about the workflows and executions

## Customization

- To fetch inactive workflows as well, modify the `active` parameter in the `get_all_workflows` function call in `main()`

## Output

The script returns a dictionary with:
- `workflows_count`: Number of workflows found
- `executions_count`: Number of executions
- `executions`: List of execution objects with workflow information

## Error Handling

The script includes basic error handling with print statements for errors. Check the console output for any issues that occur during execution. 