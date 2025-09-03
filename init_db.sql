-- PostgreSQL Database Initialization Script
-- Run this manually if you need to set up the database outside of Docker

-- Create database if it doesn't exist
-- Note: You need to run this as a superuser (postgres)
-- CREATE DATABASE fastapi_backend;

-- Connect to the database
\c fastapi_backend;

-- Create extensions if needed
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Grant necessary permissions
GRANT ALL PRIVILEGES ON DATABASE fastapi_backend TO postgres;
GRANT ALL PRIVILEGES ON SCHEMA public TO postgres;

-- Set timezone
SET timezone = 'UTC';

-- Verify connection
SELECT current_database(), current_user, version();
