# FastAPI Backend API Documentation

## Base URL
```
http://localhost:8000
```

## Authentication Endpoints

### 1. User Signup
**POST** `/api/v1/auth/signup`

**Request:**
```bash
curl -X POST "http://localhost:8000/api/v1/auth/signup" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "password": "securepassword123"
  }'
```

**Response:**
```json
{
  "id": 1,
  "username": "john_doe",
  "role": "ADMIN",
  "organization_id": 1,
  "created_at": "2024-01-15T10:30:00",
  "updated_at": "2024-01-15T10:30:00"
}
```

### 2. User Login
**POST** `/api/v1/auth/login`

**Request:**
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "password": "securepassword123"
  }'
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

## Organization Endpoints

### 3. Get My Organization
**GET** `/api/v1/organizations/me`

**Request:**
```bash
curl -X GET "http://localhost:8000/api/v1/organizations/me" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
```json
{
  "id": 1,
  "name": "Organization for john_doe",
  "created_at": "2024-01-15T10:30:00",
  "updated_at": "2024-01-15T10:30:00"
}
```

### 4. Get Organization Users
**GET** `/api/v1/organizations/{organization_id}/users`

**Request:**
```bash
curl -X GET "http://localhost:8000/api/v1/organizations/1/users" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
```json
[
  {
    "id": 1,
    "username": "john_doe",
    "role": "ADMIN",
    "created_at": "2024-01-15T10:30:00"
  },
  {
    "id": 2,
    "username": "jane_smith",
    "role": "MEMBER",
    "created_at": "2024-01-15T11:00:00"
  }
]
```

## Notes Endpoints

### 5. Get All Notes
**GET** `/api/v1/notes`

**Request:**
```bash
curl -X GET "http://localhost:8000/api/v1/notes" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
```json
[
  {
    "id": 1,
    "title": "Project Meeting Notes",
    "content": "Discussed Q1 goals and timeline",
    "organization_id": 1,
    "created_by": 1,
    "created_at": "2024-01-15T10:30:00",
    "updated_at": "2024-01-15T10:30:00",
    "created_by_username": "john_doe"
  },
  {
    "id": 2,
    "title": "Client Requirements",
    "content": "New feature requests from client",
    "organization_id": 1,
    "created_by": 2,
    "created_at": "2024-01-15T11:00:00",
    "updated_at": "2024-01-15T11:00:00",
    "created_by_username": "jane_smith"
  }
]
```

### 6. Create Note
**POST** `/api/v1/notes`

**Request:**
```bash
curl -X POST "http://localhost:8000/api/v1/notes" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "New Project Idea",
    "content": "This is a great idea for our next project"
  }'
```

**Response:**
```json
{
  "id": 3,
  "title": "New Project Idea",
  "content": "This is a great idea for our next project",
  "organization_id": 1,
  "created_by": 1,
  "created_at": "2024-01-15T12:00:00",
  "updated_at": "2024-01-15T12:00:00"
}
```

### 7. Get Note by ID
**GET** `/api/v1/notes/{note_id}`

**Request:**
```bash
curl -X GET "http://localhost:8000/api/v1/notes/1" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
```json
{
  "id": 1,
  "title": "Project Meeting Notes",
  "content": "Discussed Q1 goals and timeline",
  "organization_id": 1,
  "created_by": 1,
  "created_at": "2024-01-15T10:30:00",
  "updated_at": "2024-01-15T10:30:00",
  "created_by_username": "john_doe"
}
```

### 8. Update Note
**PUT** `/api/v1/notes/{note_id}`

**Request:**
```bash
curl -X PUT "http://localhost:8000/api/v1/notes/1" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated Project Meeting Notes",
    "content": "Discussed Q1 goals, timeline, and budget"
  }'
```

**Response:**
```json
{
  "id": 1,
  "title": "Updated Project Meeting Notes",
  "content": "Discussed Q1 goals, timeline, and budget",
  "organization_id": 1,
  "created_by": 1,
  "created_at": "2024-01-15T10:30:00",
  "updated_at": "2024-01-15T12:30:00"
}
```

### 9. Delete Note
**DELETE** `/api/v1/notes/{note_id}`

**Request:**
```bash
curl -X DELETE "http://localhost:8000/api/v1/notes/1" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
```json
{
  "message": "Note deleted successfully"
}
```

## Todos Endpoints

### 10. Get All Todos
**GET** `/api/v1/todos`

**Request:**
```bash
curl -X GET "http://localhost:8000/api/v1/todos" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
```json
[
  {
    "id": 1,
    "title": "Review project proposal",
    "completed": false,
    "organization_id": 1,
    "created_by": 1,
    "created_at": "2024-01-15T10:30:00",
    "updated_at": "2024-01-15T10:30:00",
    "created_by_username": "john_doe"
  },
  {
    "id": 2,
    "title": "Schedule team meeting",
    "completed": true,
    "organization_id": 1,
    "created_by": 2,
    "created_at": "2024-01-15T11:00:00",
    "updated_at": "2024-01-15T11:00:00",
    "created_by_username": "jane_smith"
  }
]
```

### 11. Create Todo
**POST** `/api/v1/todos`

**Request:**
```bash
curl -X POST "http://localhost:8000/api/v1/todos" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Prepare presentation slides"
  }'
```

**Response:**
```json
{
  "id": 3,
  "title": "Prepare presentation slides",
  "completed": false,
  "organization_id": 1,
  "created_by": 1,
  "created_at": "2024-01-15T12:00:00",
  "updated_at": "2024-01-15T12:00:00"
}
```

### 12. Get Todo by ID
**GET** `/api/v1/todos/{todo_id}`

**Request:**
```bash
curl -X GET "http://localhost:8000/api/v1/todos/1" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
```json
{
  "id": 1,
  "title": "Review project proposal",
  "completed": false,
  "organization_id": 1,
  "created_by": 1,
  "created_at": "2024-01-15T10:30:00",
  "updated_at": "2024-01-15T10:30:00",
  "created_by_username": "john_doe"
}
```

### 13. Update Todo
**PUT** `/api/v1/todos/{todo_id}`

**Request:**
```bash
curl -X PUT "http://localhost:8000/api/v1/todos/1" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Review project proposal",
    "completed": true
  }'
```

**Response:**
```json
{
  "id": 1,
  "title": "Review project proposal",
  "completed": true,
  "organization_id": 1,
  "created_by": 1,
  "created_at": "2024-01-15T10:30:00",
  "updated_at": "2024-01-15T12:30:00"
}
```

### 14. Delete Todo
**DELETE** `/api/v1/todos/{todo_id}`

**Request:**
```bash
curl -X DELETE "http://localhost:8000/api/v1/todos/1" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
```json
{
  "message": "Todo deleted successfully"
}
```

## System Endpoints

### 15. Health Check
**GET** `/health`

**Request:**
```bash
curl -X GET "http://localhost:8000/health"
```

**Response:**
```json
{
  "status": "healthy"
}
```

### 16. Root Endpoint
**GET** `/`

**Request:**
```bash
curl -X GET "http://localhost:8000/"
```

**Response:**
```json
{
  "message": "FastAPI Backend API",
  "version": "1.0.0",
  "docs": "/docs",
  "redoc": "/redoc"
}
```

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Username already registered"
}
```

### 401 Unauthorized
```json
{
  "detail": "Could not validate credentials",
  "headers": {
    "www-authenticate": "Bearer"
  }
}
```

### 403 Forbidden
```json
{
  "detail": "Insufficient permissions. ADMIN role required."
}
```

### 404 Not Found
```json
{
  "detail": "Note not found"
}
```

## Authentication Notes

- All protected endpoints require the `Authorization: Bearer YOUR_ACCESS_TOKEN` header
- The access token is obtained from the `/api/v1/auth/login` endpoint
- Tokens expire after 24 hours (1440 minutes)
- Only ADMIN users can update/delete notes and todos
- Users can only access data from their own organization

## Rate Limiting

Currently no rate limiting is implemented. All endpoints are available without restrictions.

## CORS

The API allows requests from:
- `http://localhost:3000` (Frontend development)
- `http://localhost:8000` (API documentation)
