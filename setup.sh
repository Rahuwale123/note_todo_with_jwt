#!/bin/bash

echo "🚀 Setting up FastAPI Backend with PostgreSQL and Alembic..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

# Check if Docker Compose is available
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose and try again."
    exit 1
fi

echo "✅ Docker and Docker Compose are available"

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p logs

# Build and start services
echo "🐳 Building and starting Docker services..."
docker-compose up --build -d

# Wait for PostgreSQL to be ready
echo "⏳ Waiting for PostgreSQL to be ready..."
sleep 30

# Check if PostgreSQL is ready
echo "🔍 Checking PostgreSQL connection..."
until docker-compose exec postgres_db pg_isready -U postgres; do
    echo "⏳ PostgreSQL is not ready yet, waiting..."
    sleep 5
done

echo "✅ PostgreSQL is ready!"

# Run Alembic migrations
echo "🔄 Running database migrations..."
docker-compose exec fastapi_app alembic upgrade head

echo "✅ Database migrations completed!"

# Check if FastAPI is running
echo "🔍 Checking FastAPI application..."
sleep 10

if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ FastAPI is running successfully!"
    echo "🌐 API Documentation: http://localhost:8000/docs"
    echo "🔗 Health Check: http://localhost:8000/health"
else
    echo "❌ FastAPI is not responding. Check logs with: docker-compose logs fastapi_app"
fi

echo ""
echo "🎉 Setup completed!"
echo ""
echo "📋 Available commands:"
echo "  Start services: docker-compose up -d"
echo "  Stop services:  docker-compose down"
echo "  View logs:      docker-compose logs -f"
echo "  Run migrations: docker-compose exec fastapi_app alembic upgrade head"
echo "  Create migration: docker-compose exec fastapi_app alembic revision --autogenerate -m 'description'"
echo ""
echo "🔗 API Endpoints:"
echo "  - Health: http://localhost:8000/health"
echo "  - Docs:   http://localhost:8000/docs"
echo "  - Signup: http://localhost:8000/api/v1/auth/signup"
echo "  - Login:  http://localhost:8000/api/v1/auth/login"
echo ""
echo "🗄️  Database:"
echo "  - PostgreSQL: localhost:5432"
echo "  - Database:  fastapi_backend"
echo "  - Username:  postgres"
echo "  - Password:  QWer12@*"
