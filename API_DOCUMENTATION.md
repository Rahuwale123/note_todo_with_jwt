# API Documentation

This document provides comprehensive API documentation with curl commands and example responses for all endpoints.

## Table of Contents
1. [Authentication](#authentication)
2. [Organizations](#organizations)
3. [Notes](#notes)
4. [Todos](#todos)
5. [System](#system)

---

## Authentication

### User Signup

#### Create New Organization (ADMIN)
```bash
curl -X POST "http://localhost:8000/api/v1/auth/signup" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_admin",
    "password": "securepass123",
    "organization_name": "Acme Corporation"
  }'
```

**Response:**
```json
{
  "id": 1,
  "username": "john_admin",
  "role": "ADMIN",
  "organization_id": 1,
  "created_at": "2024-01-15T10:30:00",
  "updated_at": "2024-01-15T10:30:00"
}
```

#### Join Existing Organization (MEMBER)
```bash
curl -X POST "http://localhost:8000/api/v1/auth/signup" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "jane_member",
    "password": "securepass123",
    "organization_name": "Acme Corporation"
  }'
```

**Response:**
```json
{
  "id": 2,
  "username": "jane_member",
  "role": "MEMBER",
  "organization_id": 1,
  "created_at": "2024-01-15T11:00:00",
  "updated_at": "2024-01-15T11:00:00"
}
```

#### Signup with Non-existent Organization
```bash
curl -X POST "http://localhost:8000/api/v1/auth/signup" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "new_user",
    "password": "password123",
    "organization_name": "NonExistent Corp"
  }'
```

**Response:**
```json
{
  "id": 3,
  "username": "new_user",
  "role": "ADMIN",
  "organization_id": 2,
  "created_at": "2024-01-15T12:00:00",
  "updated_at": "2024-01-15T12:00:00"
}
```

**Note**: When signing up with a non-existent organization name, the user automatically becomes an ADMIN of the newly created organization.

#### Signup with Existing Username
```bash
curl -X POST "http://localhost:8000/api/v1/auth/signup" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_admin",
    "password": "differentpass123"
  }'
```

**Response:**
```json
{
  "detail": "Username already registered"
}
```

### User Login

#### Valid Credentials
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_admin",
    "password": "securepass123"
  }'
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

#### Invalid Credentials
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_admin",
    "password": "wrongpassword"
  }'
```

**Response:**
```json
{
  "detail": "Incorrect username or password",
  "headers": {
    "www-authenticate": "Bearer"
  }
}
```

### Get Current User Info
```bash
curl -X GET "http://localhost:8000/api/v1/auth/me" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
```json
{
  "id": 1,
  "username": "john_admin",
  "role": "ADMIN",
  "organization_id": 1,
  "created_at": "2024-01-15T10:30:00"
}
```

#### Without Valid Token (401 Unauthorized)
```bash
curl -X GET "http://localhost:8000/api/v1/auth/me"
```

**Response:**
```json
{
  "detail": "Not authenticated",
  "headers": {
    "www-authenticate": "Bearer"
  }
}
```

---

## Organizations

### Get My Organization
```bash
curl -X GET "http://localhost:8000/api/v1/organizations/me" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
```json
{
  "id": 1,
  "name": "Acme Corp",
  "created_at": "2024-01-15T10:30:00",
  "updated_at": "2024-01-15T10:30:00"
}
```

### Get Public Organization List
```bash
curl -X GET "http://localhost:8000/api/v1/organizations/public"
```

**Response:**
```json
[
  {
    "id": 1,
    "name": "Acme Corp",
    "created_at": "2024-01-15T10:30:00"
  },
  {
    "id": 2,
    "name": "Tech Solutions Inc",
    "created_at": "2024-01-15T11:00:00"
  }
]
```

### Search Organizations
```bash
curl -X GET "http://localhost:8000/api/v1/organizations/search?q=acme"
```

**Response:**
```json
[
  {
    "id": 1,
    "name": "Acme Corp",
    "created_at": "2024-01-15T10:30:00"
  }
]
```

### List Organization Users (ADMIN Only)
```bash
curl -X GET "http://localhost:8000/api/v1/organizations/1/users" \
  -H "Authorization: Bearer ADMIN_ACCESS_TOKEN"
```

**Response:**
```json
[
  {
    "id": 1,
    "username": "john_admin",
    "role": "ADMIN",
    "created_at": "2024-01-15T10:30:00"
  },
  {
    "id": 2,
    "username": "jane_member",
    "role": "MEMBER",
    "created_at": "2024-01-15T11:00:00"
  }
]
```

#### MEMBER Trying to Access (403 Forbidden)
```bash
curl -X GET "http://localhost:8000/api/v1/organizations/1/users" \
  -H "Authorization: Bearer MEMBER_ACCESS_TOKEN"
```

**Response:**
```json
{
  "detail": "Insufficient permissions. ADMIN role required."
}
```

### Update User Role (ADMIN Only)
```bash
curl -X PUT "http://localhost:8000/api/v1/organizations/1/users/2" \
  -H "Authorization: Bearer ADMIN_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "role": "ADMIN"
  }'
```

**Response:**
```json
{
  "message": "User jane_member role updated to ADMIN"
}
```

#### Cannot Change Own Role (400 Bad Request)
```bash
curl -X PUT "http://localhost:8000/api/v1/organizations/1/users/1" \
  -H "Authorization: Bearer ADMIN_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "role": "MEMBER"
  }'
```

**Response:**
```json
{
  "detail": "Cannot change your own role"
}
```

### Remove User from Organization (ADMIN Only)
```bash
curl -X DELETE "http://localhost:8000/api/v1/organizations/1/users/3" \
  -H "Authorization: Bearer ADMIN_ACCESS_TOKEN"
```

**Response:**
```json
{
  "message": "User bob_member removed from organization"
}
```

#### Cannot Remove Self (400 Bad Request)
```bash
curl -X DELETE "http://localhost:8000/api/v1/organizations/1/users/1" \
  -H "Authorization: Bearer ADMIN_ACCESS_TOKEN"
```

**Response:**
```json
{
  "detail": "Cannot remove yourself from the organization"
}
```

---

## Notes

### List All Notes
```bash
curl -X GET "http://localhost:8000/api/v1/notes" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
```json
[
  {
    "id": 1,
    "title": "Project Ideas",
    "content": "Build a new web application",
    "organization_id": 1,
    "created_by": 1,
    "created_at": "2024-01-15T10:30:00",
    "updated_at": "2024-01-15T10:30:00",
    "created_by_username": "john_admin"
  }
]
```

### List My Notes
```bash
curl -X GET "http://localhost:8000/api/v1/notes/my-notes" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
```json
[
  {
    "id": 1,
    "title": "Project Ideas",
    "content": "Build a new web application",
    "organization_id": 1,
    "created_by": 1,
    "created_at": "2024-01-15T10:30:00",
    "updated_at": "2024-01-15T10:30:00",
    "created_by_username": "john_admin"
  }
]
```

### Create Note
```bash
curl -X POST "http://localhost:8000/api/v1/notes" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Meeting Notes",
    "content": "Discussed project timeline and milestones"
  }'
```

**Response:**
```json
{
  "id": 2,
  "title": "Meeting Notes",
  "content": "Discussed project timeline and milestones",
  "organization_id": 1,
  "created_by": 1,
  "created_at": "2024-01-15T12:00:00",
  "updated_at": "2024-01-15T12:00:00"
}
```

### Get Specific Note
```bash
curl -X GET "http://localhost:8000/api/v1/notes/1" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
```json
{
  "id": 1,
  "title": "Project Ideas",
  "content": "Build a new web application",
  "organization_id": 1,
  "created_by": 1,
  "created_at": "2024-01-15T10:30:00",
  "updated_at": "2024-01-15T10:30:00",
  "created_by_username": "john_admin"
}
```

### Update Note (ADMIN Only)
```bash
curl -X PUT "http://localhost:8000/api/v1/notes/1" \
  -H "Authorization: Bearer ADMIN_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated Project Ideas",
    "content": "Build a new web application with modern tech stack"
  }'
```

**Response:**
```json
{
  "id": 1,
  "title": "Updated Project Ideas",
  "content": "Build a new web application with modern tech stack",
  "organization_id": 1,
  "created_by": 1,
  "created_at": "2024-01-15T10:30:00",
  "updated_at": "2024-01-15T12:30:00"
}
```

#### MEMBER Trying to Update Note (403 Forbidden)
```bash
curl -X PUT "http://localhost:8000/api/v1/notes/1" \
  -H "Authorization: Bearer MEMBER_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated Title",
    "content": "Updated content"
  }'
```

**Response:**
```json
{
  "detail": "Insufficient permissions. ADMIN role required."
}
```

### Delete Note (ADMIN Only)
```bash
curl -X DELETE "http://localhost:8000/api/v1/notes/1" \
  -H "Authorization: Bearer ADMIN_ACCESS_TOKEN"
```

**Response:**
```json
{
  "message": "Note deleted successfully"
}
```

#### MEMBER Trying to Delete Note (403 Forbidden)
```bash
curl -X DELETE "http://localhost:8000/api/v1/notes/1" \
  -H "Authorization: Bearer MEMBER_ACCESS_TOKEN"
```

**Response:**
```json
{
  "detail": "Insufficient permissions. ADMIN role required."
}
```

---

## Todos

### List All Todos
```bash
curl -X GET "http://localhost:8000/api/v1/todos" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
```json
[
  {
    "id": 1,
    "title": "Review proposal",
    "completed": false,
    "organization_id": 1,
    "created_by": 1,
    "created_at": "2024-01-15T10:30:00",
    "updated_at": "2024-01-15T10:30:00",
    "created_by_username": "john_admin"
  }
]
```

### List My Todos
```bash
curl -X GET "http://localhost:8000/api/v1/todos/my-todos" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
```json
[
  {
    "id": 1,
    "title": "Review proposal",
    "completed": false,
    "organization_id": 1,
    "created_by": 1,
    "created_at": "2024-01-15T10:30:00",
    "updated_at": "2024-01-15T10:30:00",
    "created_by_username": "john_admin"
  }
]
```

### Create Todo
```bash
curl -X POST "http://localhost:8000/api/v1/todos" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Schedule meeting",
    "completed": false
  }'
```

**Response:**
```json
{
  "id": 2,
  "title": "Schedule meeting",
  "completed": false,
  "organization_id": 1,
  "created_by": 1,
  "created_at": "2024-01-15T12:00:00",
  "updated_at": "2024-01-15T12:00:00"
}
```

### Get Specific Todo
```bash
curl -X GET "http://localhost:8000/api/v1/todos/1" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Response:**
```json
{
  "id": 1,
  "title": "Review proposal",
  "completed": false,
  "organization_id": 1,
  "created_by": 1,
  "created_at": "2024-01-15T10:30:00",
  "updated_at": "2024-01-15T10:30:00",
  "created_by_username": "john_admin"
}
```

### Update Todo (All Users)
```bash
curl -X PUT "http://localhost:8000/api/v1/todos/1" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Review proposal",
    "completed": true
  }'
```

**Response:**
```json
{
  "id": 1,
  "title": "Review proposal",
  "completed": true,
  "organization_id": 1,
  "created_by": 1,
  "created_at": "2024-01-15T10:30:00",
  "updated_at": "2024-01-15T12:30:00"
}
```

### Delete Todo (ADMIN Only)
```bash
curl -X DELETE "http://localhost:8000/api/v1/todos/1" \
  -H "Authorization: Bearer ADMIN_ACCESS_TOKEN"
```

**Response:**
```json
{
  "message": "Todo deleted successfully"
}
```

#### MEMBER Trying to Delete Todo (403 Forbidden)
```bash
curl -X DELETE "http://localhost:8000/api/v1/todos/1" \
  -H "Authorization: Bearer MEMBER_ACCESS_TOKEN"
```

**Response:**
```json
{
  "detail": "Insufficient permissions. ADMIN role required."
}
```

---

## System

### Health Check
```bash
curl -X GET "http://localhost:8000/health"
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T12:00:00"
}
```

### API Documentation
```bash
curl -X GET "http://localhost:8000/docs"
```

**Response:** Swagger UI documentation page

### OpenAPI Schema
```bash
curl -X GET "http://localhost:8000/openapi.json"
```

**Response:** OpenAPI specification in JSON format

---

## Authentication Notes

- **Access Token**: Include in `Authorization: Bearer <token>` header for protected endpoints
- **Token Expiration**: Tokens expire after 24 hours
- **Role-Based Access**: Some endpoints require specific user roles (ADMIN/MEMBER)
- **Organization Isolation**: Users can only access data from their own organization

## Error Responses

### Common HTTP Status Codes
- **200**: Success
- **201**: Created
- **400**: Bad Request (validation errors)
- **401**: Unauthorized (invalid/missing token)
- **403**: Forbidden (insufficient permissions)
- **404**: Not Found
- **422**: Unprocessable Entity (data validation errors)

### Error Response Format
```json
{
  "detail": "Error message description"
}
```

## Rate Limiting

Currently, no rate limiting is implemented. Consider implementing rate limiting for production use.

## CORS

CORS is enabled for all origins. Configure specific origins for production use.
