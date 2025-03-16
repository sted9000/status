from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets
from pydantic import BaseModel
from typing import Optional
import os
from dotenv import load_dotenv
from supabase import create_client, Client
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

app = FastAPI()
security = HTTPBasic()

# Get credentials from environment variables
USERNAME = os.getenv("AUTH_USERNAME")
PASSWORD = os.getenv("AUTH_PASSWORD")

# Initialize Supabase client
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)

class StatusUpdate(BaseModel):
    service_id: int
    status: str
    message: Optional[str] = None
    tool_name: str

def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, USERNAME)
    correct_password = secrets.compare_digest(credentials.password, PASSWORD)
    
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

@app.get("/")
def read_root():
    return {"message": "Status update API"}

@app.post("/status/update")
def update_status(status_update: StatusUpdate, username: str = Depends(authenticate)):
    try:
        # Check if service_id exists
        service = supabase.table("services").select("id").eq("id", status_update.service_id).execute()
        
        if not service.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Service with ID {status_update.service_id} not found"
            )
        
        # Insert status update into service_updates table
        data = {
            "service_id": status_update.service_id,
            "status": status_update.status,
            "message": status_update.message,
            "tool_name": status_update.tool_name,
            # updated_at will be set by default in the database
        }
        
        result = supabase.table("service_updates").insert(data).execute()
        
        if not result.data:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to save status update"
            )
        
        return {
            "message": "Status updated successfully",
            "service_id": status_update.service_id,
            "status": status_update.status,
            "message": status_update.message,
            "tool_name": status_update.tool_name,
            "updated_by": username
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating status: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 