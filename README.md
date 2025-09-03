# FastAPI Backend - Multi-tenant API with Role-Based Access Control

A secure, scalable FastAPI backend providing a multi-tenant API for managing users, organizations, notes, and todos with JWT authentication and role-based access control.

## 🚀 Features

- **JWT Authentication**: Secure user signup/login with JWT tokens
- **Multi-tenant Architecture**: Organizations with isolated data
- **Role-Based Access Control**: ADMIN and MEMBER roles with different permissions
- **CRUD Operations**: Full CRUD for notes and todos
- **Database Migrations**: Alembic for schema management
- **Docker Support**: Containerized with MySQL database
- **Comprehensive Testing**: Pytest test suite
- **API Documentation**: Auto-generated OpenAPI docs

## 🏗️ Architecture

```
backend/
│── alembic/                 # Database migrations
│── app/
│   ├── api/                 # API endpoints
│   │   ├── auth.py          # Authentication
│   │   ├── organizations.py # Organization management
│   │   ├── notes.py         # Notes CRUD
│   │   └── todos.py         # Todos CRUD
│   ├── core/                # Core configuration
│   │   ├── config.py        # Settings
│   │   └── security.py      # JWT & password utilities
│   ├── models/              # SQLAlchemy models
│   ├── schemas/             # Pydantic schemas
│   ├── deps.py              # Dependencies & middleware
│   └── main.py              # FastAPI application
│── tests/                   # Test suite
│── Dockerfile               # Container configuration
│── docker-compose.yml       # Multi-service orchestration
│── requirements.txt         # Python dependencies
└── README.md               # This file
```

## 🛠️ Tech Stack

- **Framework**: FastAPI
- **Database**: MySQL 8.0
- **ORM**: SQLAlchemy 2.0
- **Migrations**: Alembic
- **Authentication**: JWT (PyJWT) + bcrypt
- **Containerization**: Docker + Docker Compose
- **Testing**: Pytest + HTTPX

## 📋 Prerequisites

- Docker and Docker Compose
- Python 3.11+ (for local development)
- MySQL 8.0+ (for local development)

## 🚀 Quick Start

### Using Docker (Recommended)

1. **Clone and navigate to the project:**
   ```bash
   cd backend
   ```

2. **Start the services:**
   ```bash
   docker-compose up -d
   ```

3. **Access the API:**
   - API: http://localhost:8000
   - Interactive docs: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

### Local Development

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials
   ```

3. **Run database migrations:**
   ```bash
   alembic upgrade head
   ```

4. **Start the development server:**
   ```bash
   uvicorn app.main:app --reload
   ```

## 🗄️ Database Schema

### Tables

- **organizations**: Multi-tenant organizations
- **users**: Users with roles and organization membership
- **notes**: Organization-scoped notes
- **todos**: Organization-scoped todos

### Key Relationships

- Users belong to one organization
- Notes and todos are scoped to organizations
- Role-based permissions (ADMIN/MEMBER)

## 🔐 Authentication & Authorization

### JWT Token Structure
```json
{
  "sub": "username",
  "user_id": 123,
  "organization_id": 456,
  "role": "ADMIN",
  "exp": 1640995200
}
```

### Role Permissions

| Role | Notes | Todos | Organization |
|------|-------|-------|--------------|
| ADMIN | Full CRUD | Full CRUD | Manage members |
| MEMBER | Read/Create | Read/Create/Update | Read-only |

## 📡 API Endpoints

### Authentication
- `POST /api/v1/auth/signup` - User registration
- `POST /api/v1/auth/login` - User login

### Organizations
- `GET /api/v1/organizations/me` - Get current org
- `GET /api/v1/organizations/{id}/users` - List org members (ADMIN)

### Notes
- `GET /api/v1/notes` - List org notes
- `POST /api/v1/notes` - Create note
- `GET /api/v1/notes/{id}` - Get note
- `PUT /api/v1/notes/{id}` - Update note (ADMIN)
- `DELETE /api/v1/notes/{id}` - Delete note (ADMIN)

### Todos
- `GET /api/v1/todos` - List org todos
- `POST /api/v1/todos` - Create todo
- `GET /api/v1/todos/{id}` - Get todo
- `PUT /api/v1/todos/{id}` - Update todo
- `DELETE /api/v1/todos/{id}` - Delete todo (ADMIN)

## 🧪 Testing

Run the test suite:
```bash
pytest tests/
```

Run with coverage:
```bash
pytest tests/ --cov=app --cov-report=html
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | MySQL connection string | `mysql+mysqlconnector://app_user:app_password@localhost:3306/app_db` |
| `JWT_SECRET_KEY` | JWT signing secret | `your-super-secret-jwt-key-change-in-production` |
| `JWT_ALGORITHM` | JWT algorithm | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiry time | `1440` (24 hours) |

### Database Configuration

The application uses MySQL with the following default settings:
- Database: `app_db`
- User: `app_user`
- Password: `app_password`
- Host: `mysql_db` (Docker) or `localhost` (local)

## 📊 Database Migrations

### Create a new migration:
```bash
alembic revision --autogenerate -m "Description of changes"
```

### Apply migrations:
```bash
alembic upgrade head
```

### Rollback migrations:
```bash
alembic downgrade -1
```

## 🐳 Docker Commands

### Build and start:
```bash
docker-compose up --build
```

### View logs:
```bash
docker-compose logs -f fastapi_app
```

### Stop services:
```bash
docker-compose down
```

### Clean up volumes:
```bash
docker-compose down -v
```

## 🔒 Security Features

- **Password Hashing**: bcrypt for secure password storage
- **JWT Tokens**: Secure authentication with configurable expiry
- **Role-Based Access**: Fine-grained permission control
- **Organization Isolation**: Data isolation between tenants
- **SQL Injection Protection**: SQLAlchemy ORM with parameterized queries

## 📈 Performance Considerations

- Connection pooling for database connections
- Efficient database queries with proper indexing
- JWT token validation without database hits
- Optimized SQLAlchemy relationships

## 🚨 Production Deployment

### Security Checklist
- [ ] Change default JWT secret key
- [ ] Use strong database passwords
- [ ] Enable HTTPS/TLS
- [ ] Configure proper CORS origins
- [ ] Set up monitoring and logging
- [ ] Use production-grade MySQL instance

### Environment Variables
```bash
JWT_SECRET_KEY=your-production-secret-key
DATABASE_URL=mysql+mysqlconnector://user:pass@host:port/db
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## 📝 License

This project is licensed under the MIT License.

## 🆘 Support

For issues and questions:
1. Check the API documentation at `/docs`
2. Review the test cases for usage examples
3. Open an issue on GitHub

## 🔄 API Versioning

The API is versioned under `/api/v1/`. Future versions will maintain backward compatibility where possible.

---

**Built with ❤️ using FastAPI and modern Python practices**
