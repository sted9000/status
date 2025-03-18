#!/bin/bash

# Set the script directory as the working directory
cd "$(dirname "$0")"

# Create logs directory if it doesn't exist
mkdir -p logs

# Get current timestamp for log file
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
LOG_FILE="logs/workflow_status_${TIMESTAMP}.log"

# Function to log messages
log_message() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    log_message "ERROR: Python 3 is not installed"
    exit 1
fi

# Check if required environment variables are set
required_vars=("N8N_HOST" "N8N_API_KEY" "N8N_API_VERSION" "SUPABASE_URL" "SUPABASE_KEY" "TOOL_NAME")
missing_vars=()

for var in "${required_vars[@]}"; do
    if [ -z "${!var}" ]; then
        missing_vars+=("$var")
    fi
done

if [ ${#missing_vars[@]} -ne 0 ]; then
    log_message "ERROR: Missing required environment variables: ${missing_vars[*]}"
    exit 1
fi

# Run the Python script
log_message "Starting workflow status check..."
python3 workflows.py >> "$LOG_FILE" 2>&1

# Check the exit status
if [ $? -eq 0 ]; then
    log_message "Workflow status check completed successfully"
else
    log_message "ERROR: Workflow status check failed"
    exit 1
fi

# Clean up old log files (keep last 7 days)
find logs -name "workflow_status_*.log" -type f -mtime +7 -delete

exit 0 