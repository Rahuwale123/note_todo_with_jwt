-- Initial database setup script for PostgreSQL
-- This script runs when the PostgreSQL container starts for the first time

-- Create database if it doesn't exist
-- Note: PostgreSQL creates the database automatically via POSTGRES_DB environment variable

-- Grant privileges to postgres user
GRANT ALL PRIVILEGES ON DATABASE fastapi_backend TO postgres;

-- Enable UUID extension (useful for future enhancements)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
