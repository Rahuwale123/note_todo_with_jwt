# FastAPI Backend Project - Complete Documentation

## Table of Contents
1. [Project Overview](#project-overview)
2. [Architecture & Tech Stack](#architecture--tech-stack)
3. [Database Design](#database-design)
4. [Authentication System](#authentication-system)
5. [Authorization & RBAC](#authorization--rbac)
6. [API Endpoints](#api-endpoints)
7. [Project Structure](#project-structure)
8. [Configuration](#configuration)
9. [Docker Setup](#docker-setup)
10. [Deployment](#deployment)

---

## Project Overview

This is a **multi-tenant FastAPI backend** that provides a secure, role-based API for managing users, organizations, notes, and todos. The system implements **organization-scoped data isolation** where users can only access data within their organization.

### Key Features
- **JWT-based Authentication** with secure password hashing
- **Role-Based Access Control (RBAC)** with ADMIN and MEMBER roles
- **Multi-organization Support** with complete data isolation
- **CRUD Operations** for notes and todos
- **Organization Management** with user role management
- **Dockerized Setup** with MySQL database
- **Database Migrations** using Alembic
- **Comprehensive API Documentation** with OpenAPI/Swagger

---

## Architecture & Tech Stack

### Backend Framework
- **FastAPI**: Modern, fast web framework for building APIs
- **Python 3.11**: Programming language
- **Uvicorn**: ASGI server for running FastAPI

### Database & ORM
- **MySQL 8.0**: Primary database
- **SQLAlchemy 2.0**: ORM for database operations
- **Alembic**: Database migration tool

### Authentication & Security
- **JWT (PyJWT)**: Token-based authentication
- **bcrypt**: Password hashing
- **HTTPBearer**: Token extraction from requests

### Development & Deployment
- **Docker & Docker Compose**: Containerization
- **Pytest**: Testing framework
- **HTTPX**: HTTP client for testing

---

## Database Design

### Database Schema

#### Organizations Table
```sql
CREATE TABLE organizations (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

#### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('ADMIN', 'MEMBER') DEFAULT 'MEMBER' NOT NULL,
    organization_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (organization_id) REFERENCES organizations(id)
);
```

#### Notes Table
```sql
CREATE TABLE notes (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    content TEXT,
    organization_id INTEGER NOT NULL,
    created_by INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (organization_id) REFERENCES organizations(id),
    FOREIGN KEY (created_by) REFERENCES users(id)
);
```

#### Todos Table
```sql
CREATE TABLE todos (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    completed BOOLEAN DEFAULT FALSE,
    organization_id INTEGER NOT NULL,
    created_by INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (organization_id) REFERENCES organizations(id),
    FOREIGN KEY (created_by) REFERENCES users(id)
);
```

### Relationships
- **One-to-Many**: Organization → Users
- **One-to-Many**: Organization → Notes
- **One-to-Many**: Organization → Todos
- **One-to-Many**: User → Notes (created_by)
- **One-to-Many**: User → Todos (created_by)

---

## Authentication System

### JWT Token Structure
```json
{
    "sub": "username",
    "user_id": 1,
    "organization_id": 5,
    "role": "ADMIN",
    "exp": 1640995200
}
```

### Password Security
- **Hashing Algorithm**: bcrypt
- **Salt Rounds**: Default (12 rounds)
- **Storage**: Only hashed passwords stored in database

### Token Management
- **Algorithm**: HS256
- **Expiration**: 24 hours (1440 minutes)
- **Secret Key**: Configurable via environment variables
- **Token Type**: Bearer token in Authorization header

### Authentication Flow
1. **Signup**: User provides username, password, organization_name
2. **Organization Logic**: 
   - If organization exists → User becomes MEMBER
   - If organization doesn't exist → New organization created, user becomes ADMIN
3. **Login**: Username/password validation → JWT token generation
4. **Token Usage**: Bearer token in Authorization header for protected endpoints

---

## Authorization & RBAC

### Role Definitions

#### ADMIN Role
- **Full CRUD** access to notes and todos
- **User Management**: Can update user roles, remove users
- **Organization Access**: Can manage organization members
- **Content Management**: Can update/delete any content in organization

#### MEMBER Role
- **Read Access**: Can view all notes and todos in organization
- **Create Access**: Can create new notes and todos
- **Update Access**: Can update their own todos (mark complete)
- **Limited Access**: Cannot delete content, cannot manage users

### Permission Matrix

| Action | ADMIN | MEMBER |
|--------|-------|--------|
| View Notes | ✅ | ✅ |
| Create Notes | ✅ | ✅ |
| Update Notes | ✅ | ❌ |
| Delete Notes | ✅ | ❌ |
| View Todos | ✅ | ✅ |
| Create Todos | ✅ | ✅ |
| Update Todos | ✅ | ✅ (own only) |
| Delete Todos | ✅ | ❌ |
| Manage Users | ✅ | ❌ |
| View Organization | ✅ | ✅ |

### Data Isolation
- **Organization Scoped**: All queries filtered by user's organization_id
- **Cross-Organization Access**: Completely blocked
- **User Context**: Every request validated against user's organization

---

## API Endpoints

### Authentication Endpoints

#### POST /api/v1/auth/signup
- **Purpose**: Register new user
- **Input**: username, password, organization_name
- **Logic**: Create organization if doesn't exist, assign ADMIN role; otherwise assign MEMBER role
- **Response**: User details

#### POST /api/v1/auth/login
- **Purpose**: Authenticate user and get JWT token
- **Input**: username, password
- **Response**: JWT access token

#### GET /api/v1/auth/me
- **Purpose**: Get current user information
- **Authentication**: Required (Bearer token)
- **Response**: User details (id, username, role, organization_id, created_at)

### Organization Endpoints

#### GET /api/v1/organizations/me
- **Purpose**: Get current user's organization details
- **Authentication**: Required
- **Response**: Organization information

#### GET /api/v1/organizations/public
- **Purpose**: List all public organizations (for signup)
- **Authentication**: Not required
- **Response**: List of organizations with id, name, created_at

#### GET /api/v1/organizations/search?q={name}
- **Purpose**: Search organizations by name
- **Authentication**: Not required
- **Response**: Filtered list of organizations

#### GET /api/v1/organizations/{id}/users
- **Purpose**: List organization members
- **Authentication**: Required (ADMIN only)
- **Response**: List of users in organization

#### PUT /api/v1/organizations/{id}/users/{user_id}
- **Purpose**: Update user role in organization
- **Authentication**: Required (ADMIN only)
- **Input**: role (ADMIN/MEMBER)
- **Response**: Success message

#### DELETE /api/v1/organizations/{id}/users/{user_id}
- **Purpose**: Remove user from organization
- **Authentication**: Required (ADMIN only)
- **Response**: Success message

### Notes Endpoints

#### GET /api/v1/notes/
- **Purpose**: List all notes in organization
- **Authentication**: Required
- **Response**: List of notes with creator information

#### GET /api/v1/notes/my-notes
- **Purpose**: List current user's notes
- **Authentication**: Required
- **Response**: List of user's own notes

#### POST /api/v1/notes/
- **Purpose**: Create new note
- **Authentication**: Required
- **Input**: title, content
- **Response**: Created note details

#### GET /api/v1/notes/{id}
- **Purpose**: Get specific note
- **Authentication**: Required
- **Response**: Note details with creator information

#### PUT /api/v1/notes/{id}
- **Purpose**: Update note
- **Authentication**: Required (ADMIN only)
- **Input**: title, content (optional)
- **Response**: Updated note details

#### DELETE /api/v1/notes/{id}
- **Purpose**: Delete note
- **Authentication**: Required (ADMIN only)
- **Response**: Success message

### Todos Endpoints

#### GET /api/v1/todos/
- **Purpose**: List all todos in organization
- **Authentication**: Required
- **Response**: List of todos with creator information

#### GET /api/v1/todos/my-todos
- **Purpose**: List current user's todos
- **Authentication**: Required
- **Response**: List of user's own todos

#### POST /api/v1/todos/
- **Purpose**: Create new todo
- **Authentication**: Required
- **Input**: title, completed (optional)
- **Response**: Created todo details

#### GET /api/v1/todos/{id}
- **Purpose**: Get specific todo
- **Authentication**: Required
- **Response**: Todo details with creator information

#### PUT /api/v1/todos/{id}
- **Purpose**: Update todo
- **Authentication**: Required
- **Input**: title, completed (optional)
- **Response**: Updated todo details

#### DELETE /api/v1/todos/{id}
- **Purpose**: Delete todo
- **Authentication**: Required (ADMIN only)
- **Response**: Success message

---

## Project Structure

```
task1/
├── app/                          # Main application package
│   ├── __init__.py
│   ├── main.py                   # FastAPI application entry point
│   ├── database.py               # Database configuration
│   ├── deps.py                   # FastAPI dependencies
│   ├── api/                      # API route handlers
│   │   ├── __init__.py
│   │   ├── auth.py               # Authentication endpoints
│   │   ├── organizations.py      # Organization management
│   │   ├── notes.py              # Notes CRUD operations
│   │   └── todos.py              # Todos CRUD operations
│   ├── core/                     # Core application settings
│   │   ├── __init__.py
│   │   ├── config.py             # Application configuration
│   │   └── security.py           # Security utilities
│   ├── models/                   # SQLAlchemy models
│   │   ├── __init__.py
│   │   ├── base.py               # Base model and mixins
│   │   ├── user.py               # User model
│   │   ├── organization.py       # Organization model
│   │   ├── note.py               # Note model
│   │   └── todo.py               # Todo model
│   └── schemas/                  # Pydantic schemas
│       ├── __init__.py
│       ├── user.py               # User data schemas
│       ├── organization.py       # Organization data schemas
│       ├── note.py               # Note data schemas
│       └── todo.py               # Todo data schemas
├── alembic/                      # Database migrations
│   ├── __init__.py
│   ├── env.py                    # Alembic environment
│   ├── script.py.mako            # Migration template
│   └── versions/
│       └── 001_initial.py        # Initial migration
├── tests/                        # Test suite
│   ├── __init__.py
│   └── test_auth.py              # Authentication tests
├── mysql/                        # MySQL initialization
│   └── init/
│       └── 01-init.sql           # Database initialization
├── docker-compose.yml            # Docker services configuration
├── docker-compose.override.yml   # Development overrides
├── Dockerfile                    # FastAPI application container
├── alembic.ini                   # Alembic configuration
├── requirements.txt              # Python dependencies
├── start.py                      # Development server script
├── setup.sh                      # Linux/Mac setup script
├── setup.bat                     # Windows setup script
├── .gitignore                    # Git ignore rules
├── README.md                     # Project setup instructions
├── API_DOCUMENTATION.md          # API usage documentation
├── ROLE_BASED_SYSTEM_DOCUMENTATION.md  # RBAC system documentation
└── PROJECT_DOCUMENTATION.md      # This comprehensive documentation
```

---

## Configuration

### Environment Variables
```bash
# Database Configuration
DATABASE_URL=mysql+mysqlconnector://root:QWer12@*@localhost:3306/fastapi_backend

# JWT Configuration
JWT_SECRET_KEY=your-super-secret-jwt-key-change-in-production
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# Application Configuration
API_V1_STR=/api/v1
PROJECT_NAME=FastAPI Backend
BACKEND_CORS_ORIGINS=["http://localhost:3000", "http://localhost:8080"]
```

### Database Configuration
- **Host**: localhost (development) / mysql_db (Docker)
- **Port**: 3306
- **Database**: fastapi_backend
- **Username**: root
- **Password**: QWer12@* (URL encoded for special characters)
- **Connection Pool**: Pre-ping enabled, 300-second recycle

### Security Configuration
- **JWT Secret**: Configurable via environment
- **Token Expiry**: 24 hours
- **Password Hashing**: bcrypt with default salt rounds
- **CORS**: Configured for frontend development

---

## Docker Setup

### Services Configuration

#### MySQL Database Service
```yaml
mysql_db:
  image: mysql:8.0
  container_name: fastapi_mysql
  environment:
    MYSQL_ROOT_PASSWORD: QWer12@*
    MYSQL_DATABASE: fastapi_backend
    MYSQL_USER: root
    MYSQL_PASSWORD: QWer12@*
  ports:
    - "3306:3306"
  volumes:
    - mysql_data:/var/lib/mysql
    - ./mysql/init:/docker-entrypoint-initdb.d
```

#### FastAPI Application Service
```yaml
fastapi_app:
  build: .
  container_name: fastapi_backend
  ports:
    - "8000:8000"
  environment:
    - DATABASE_URL=mysql+mysqlconnector://root:QWer12@*@mysql_db:3306/fastapi_backend
    - JWT_SECRET_KEY=your-super-secret-jwt-key-change-in-production
  depends_on:
    - mysql_db
  volumes:
    - ./app:/app/app
```

### Dockerfile Configuration
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## Deployment

### Development Setup
1. **Clone Repository**: Get the project code
2. **Run Setup Script**: 
   - Linux/Mac: `./setup.sh`
   - Windows: `setup.bat`
3. **Access Application**: http://localhost:8000
4. **API Documentation**: http://localhost:8000/docs

### Production Considerations
1. **Environment Variables**: Set secure JWT secret key
2. **Database Security**: Use strong passwords, enable SSL
3. **CORS Configuration**: Update allowed origins
4. **SSL/TLS**: Enable HTTPS for production
5. **Monitoring**: Add logging and health checks
6. **Backup Strategy**: Implement database backups

### Health Checks
- **Application Health**: GET /health
- **Database Health**: Connection pool monitoring
- **Docker Health**: Container status monitoring

---

## Key Implementation Details

### Authentication Flow
1. **User Registration**: Username, password, organization_name
2. **Organization Logic**: Auto-create or join existing
3. **Role Assignment**: ADMIN for new org, MEMBER for existing
4. **JWT Generation**: Include user_id, organization_id, role
5. **Token Validation**: Verify signature, expiry, user existence

### Authorization Implementation
1. **Dependency Injection**: FastAPI Depends for auth checks
2. **Role Validation**: require_admin_role dependency
3. **Organization Scoping**: All queries filtered by organization_id
4. **Permission Checks**: Role-based endpoint access

### Data Isolation Strategy
1. **Query Filtering**: Every database query includes organization_id filter
2. **User Context**: Current user's organization_id used for all operations
3. **Cross-Organization Prevention**: Explicit checks in all endpoints
4. **Admin Override**: Admins can only access their own organization

### Error Handling
1. **HTTP Status Codes**: Proper status codes for different scenarios
2. **Error Messages**: Clear, descriptive error messages
3. **Validation**: Pydantic schema validation
4. **Security**: No sensitive information in error responses

This documentation provides a complete understanding of the FastAPI backend project, covering all aspects from architecture to deployment. The system is designed to be secure, scalable, and maintainable with proper separation of concerns and clear data isolation.
