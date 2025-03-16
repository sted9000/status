# Service Status Dashboard

A Vue.js application that connects to a Supabase database and displays real-time updates for services.

## Features

- View and filter clients, services, and service updates
- Real-time updates using Supabase's real-time subscriptions
- Responsive design for desktop and mobile devices

## Project Setup

```sh
npm install
```

### Configuration

Create a `.env` file in the root directory with the following variables:

```
VITE_SUPABASE_URL=your_supabase_url
VITE_SUPABASE_ANON_KEY=your_supabase_anon_key
```

Replace `your_supabase_url` and `your_supabase_anon_key` with your actual Supabase project URL and anonymous key.

### Compile and Hot-Reload for Development

```sh
npm run dev
```

### Compile and Minify for Production

```sh
npm run build
```

### Lint with ESLint

```sh
npm run lint
```

## Database Schema

The application is designed to work with the following Supabase database schema:

```sql
-- Create clients table
CREATE TABLE clients (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create services table
CREATE TABLE services (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    platform VARCHAR(255) NOT NULL,
    client_id INTEGER NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (client_id) REFERENCES clients(id) ON DELETE CASCADE
);

-- Create service updates table
CREATE TABLE service_updates (
    id SERIAL PRIMARY KEY,
    service_id INTEGER NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(50) NOT NULL,
    message TEXT,
    tool_name VARCHAR(100) NOT NULL,
    FOREIGN KEY (service_id) REFERENCES services(id) ON DELETE CASCADE
);

-- Add indexes for better query performance
CREATE INDEX idx_services_client_id ON services(client_id);
CREATE INDEX idx_service_updates_service_id ON service_updates(service_id);
CREATE INDEX idx_service_updates_status ON service_updates(status);
```

## Usage

1. Navigate to the Dashboard page
2. View clients, services, and service updates
3. Click on a client to filter services by that client
4. Click on a service to filter service updates by that service
5. Use the status and tool filters to further filter service updates
6. Click the "Reset Filters" button to clear all filters
