# Status Update API

A simple FastAPI server with HTTP Basic Authentication that provides a status update endpoint and saves data to a Supabase database.

## Setup

1. Configure environment variables:
   
   The application uses a `.env` file for configuration. A default file is provided with the following content:
   ```
   AUTH_USERNAME=admin
   AUTH_PASSWORD=password
   
   # Supabase credentials
   SUPABASE_URL=your_supabase_url_here
   SUPABASE_KEY=your_supabase_key_here
   ```
   
   You should modify these values for production use. Make sure to add your actual Supabase URL and API key.

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Run the server:
```bash
python main.py
```

Alternatively, you can use uvicorn directly:
```bash
uvicorn main:app --reload
```

The server will start on http://localhost:8000

## Authentication

The API uses HTTP Basic Authentication. The default credentials (defined in the `.env` file) are:
- Username: `admin`
- Password: `password`

For security in production environments, you should change these credentials in the `.env` file.

## Database Schema

The application uses a Supabase database with the following schema:

```sql
CREATE TABLE services (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    platform VARCHAR(255) NOT NULL,
    client_id INTEGER NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (client_id) REFERENCES clients(id) ON DELETE CASCADE
);

CREATE TABLE service_updates (
    id SERIAL PRIMARY KEY,
    service_id INTEGER NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(50) NOT NULL,
    message TEXT,
    tool_name VARCHAR(100) NOT NULL,
    FOREIGN KEY (service_id) REFERENCES services(id) ON DELETE CASCADE
);
```

## API Endpoints

### GET /

Returns a simple welcome message.

### POST /status/update

Updates the status and saves it to the Supabase database.

**Request Body:**
```json
{
  "service_id": 1,
  "status": "online",
  "message": "System is running smoothly",
  "tool_name": "monitoring-service"
}
```

The `message` field is optional.

**Response:**
```json
{
  "message": "Status updated successfully",
  "service_id": 1,
  "status": "online",
  "message": "System is running smoothly",
  "tool_name": "monitoring-service",
  "updated_by": "admin"
}
```

## Interactive API Documentation

FastAPI provides automatic interactive API documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc 