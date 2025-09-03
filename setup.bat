@echo off
echo 🚀 Setting up FastAPI Backend with PostgreSQL and Alembic...

REM Check if Docker is running
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker is not running. Please start Docker and try again.
    pause
    exit /b 1
)

REM Check if Docker Compose is available
docker-compose --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker Compose is not installed. Please install Docker Compose and try again.
    pause
    exit /b 1
)

echo ✅ Docker and Docker Compose are available

REM Create necessary directories
echo 📁 Creating necessary directories...
if not exist "logs" mkdir "logs"

REM Build and start services
echo 🐳 Building and starting Docker services...
docker-compose up --build -d

REM Wait for PostgreSQL to be ready
echo ⏳ Waiting for PostgreSQL to be ready...
timeout /t 30 /nobreak >nul

REM Check if PostgreSQL is ready
echo 🔍 Checking PostgreSQL connection...
:postgres_check
docker-compose exec postgres_db pg_isready -U postgres >nul 2>&1
if %errorlevel% neq 0 (
    echo ⏳ PostgreSQL is not ready yet, waiting...
    timeout /t 5 /nobreak >nul
    goto postgres_check
)

echo ✅ PostgreSQL is ready!

REM Run Alembic migrations
echo 🔄 Running database migrations...
docker-compose exec fastapi_app alembic upgrade head

echo ✅ Database migrations completed!

REM Check if FastAPI is running
echo 🔍 Checking FastAPI application...
timeout /t 10 /nobreak >nul

echo 🎉 Setup completed!
echo.
echo 📋 Available commands:
echo   Start services: docker-compose up -d
echo   Stop services:  docker-compose down
echo   View logs:      docker-compose logs -f
echo   Run migrations: docker-compose exec fastapi_app alembic upgrade head
echo   Create migration: docker-compose exec fastapi_app alembic revision --autogenerate -m "description"
echo.
echo 🔗 API Endpoints:
echo   - Health: http://localhost:8000/health
echo   - Docs:   http://localhost:8000/docs
echo   - Signup: http://localhost:8000/api/v1/auth/signup
echo   - Login:  http://localhost:8000/api/v1/auth/login
echo.
echo 🗄️  Database:
echo   - PostgreSQL: localhost:5432
echo   - Database:  fastapi_backend
echo   - Username:  postgres
echo   - Password:  QWer12@*
echo.
pause
