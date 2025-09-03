# Role-Based Access Control (RBAC) System Documentation

## Table of Contents
1. [System Overview](#system-overview)
2. [User Roles](#user-roles)
3. [Signup Process](#signup-process)
4. [Organization Management](#organization-management)
5. [Permission Matrix](#permission-matrix)
6. [API Endpoints by Role](#api-endpoints-by-role)
7. [Security Implementation](#security-implementation)
8. [Database Schema](#database-schema)
9. [Usage Examples](#usage-examples)
10. [Error Handling](#error-handling)
11. [Essential APIs](#essential-apis)

## System Overview

This FastAPI backend implements a **Role-Based Access Control (RBAC)** system with **multi-tenant organization support**. Users belong to organizations and have different permission levels based on their assigned roles.

### Key Features
- ✅ **Two distinct user roles**: ADMIN and MEMBER
- ✅ **Multi-tenant architecture**: Complete data isolation between organizations
- ✅ **Automatic role assignment**: Based on signup type
- ✅ **Organization-based data access**: Users only see their organization's data
- ✅ **JWT authentication**: Secure token-based authentication
- ✅ **Permission enforcement**: Role-based access control on all endpoints
- ✅ **Organization discovery**: Easy signup with organization names
- ✅ **Personal content filtering**: Users can view their own content separately

## User Roles

### 1. ADMIN Role 🏢
**Description**: Organization owners with full system access
**Permissions**:
- ✅ Create, Read, Update, Delete (CRUD) on all resources
- ✅ Manage organization users (change roles, remove users)
- ✅ Full access to notes and todos
- ✅ Can delete any content within their organization
- ✅ View organization user list

**Use Cases**:
- Company founders
- Team leaders
- Project managers
- System administrators

### 2. MEMBER Role 👥
**Description**: Regular users with limited permissions
**Permissions**:
- ✅ Create and Read resources
- ✅ Update their own content (todos only)
- ✅ View personal content (my-notes, my-todos)
- ❌ Cannot delete any content
- ❌ Cannot update notes
- ❌ Cannot view organization user list
- ❌ Cannot manage other users

**Use Cases**:
- Team members
- Employees
- Regular users
- Content contributors

## Signup Process

### How Signup Works

The signup system now **always requires an organization name** and automatically determines user roles based on whether the organization exists or not. This gives users full control over their organization names.

#### 1. ADMIN Signup (New Organization) 🆕

**Request Format:**
```bash
curl -X POST "http://localhost:8000/api/v1/auth/signup" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_admin",
    "password": "securepass123",
    "organization_name": "Acme Corporation"
  }'
```

**What Happens:**
1. System checks if "Acme Corporation" exists
2. Since it doesn't exist, creates new organization with that exact name
3. Assigns `ADMIN` role to the user
4. User becomes the owner of "Acme Corporation"

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

#### 2. MEMBER Signup (Join Existing Organization) ➕

**Request Format:**
```bash
curl -X POST "http://localhost:8000/api/v1/auth/signup" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "jane_member",
    "password": "securepass123",
    "organization_name": "Acme Corporation"
  }'
```

**What Happens:**
1. System checks if "Acme Corporation" exists
2. Since it exists, assigns `MEMBER` role to the user
3. User joins the existing "Acme Corporation" organization

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

### Organization Name Requirements

**Rules for Organization Names:**
- **Always Required**: Every signup must include `organization_name`
- **Unique**: Organization names must be unique across the system
- **Case-Sensitive**: "Acme Corp" and "acme corp" are different organizations
- **Professional**: Users can create meaningful, professional organization names

**Example Organization Names:**
```json
{
  "username": "ceo_sarah",
  "password": "ceopass123",
  "organization_name": "Tech Solutions Inc"
}

{
  "username": "dev_mike",
  "password": "devpass123",
  "organization_name": "Tech Solutions Inc"
}
```

**Result:**
- `ceo_sarah` becomes ADMIN of "Tech Solutions Inc"
- `dev_mike` becomes MEMBER of "Tech Solutions Inc"

### Organization Selection for Members

**How Members Choose Their Organization:**

1. **Organization Discovery**: Members can see all available organizations
2. **Search by Name**: Members can search for organizations by name
3. **Direct Organization Name**: Members specify the exact organization name during signup

**Example Organization Selection:**
```json
{
  "username": "new_team_member",
  "password": "memberpass123",
  "organization_name": "Tech Solutions Inc"  // Joins existing organization
}
```

**Important Notes:**
- **Exact Match Required**: Organization name must match exactly (case-sensitive)
- **No Auto-Creation**: If organization doesn't exist, user becomes ADMIN of new org
- **Professional Names**: Users can create meaningful company names instead of auto-generated ones

## Essential APIs

### 🎯 **Organization Discovery (HIGH PRIORITY)**

#### Get Public Organization List
```bash
GET /api/v1/organizations/public
```
**Purpose**: Show available organizations during signup
**Use Case**: Dropdown/autocomplete in signup form
**Response**:
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

#### Search Organizations by Name
```bash
GET /api/v1/organizations/search?q=acme
```
**Purpose**: Help users find organizations by name
**Use Case**: User knows company name but not exact spelling
**Response**:
```json
[
  {
    "id": 1,
    "name": "Acme Corp",
    "created_at": "2024-01-15T10:30:00"
  }
]
```

### 👥 **User Management (MEDIUM PRIORITY)**

#### Update User Role
```bash
PUT /api/v1/organizations/{id}/users/{user_id}
```
**Purpose**: Allow admins to change user roles
**Use Case**: Promote member to admin, demote admin to member
**Request Body**:
```json
{
  "role": "ADMIN"
}
```

#### Remove User from Organization
```bash
DELETE /api/v1/organizations/{id}/users/{user_id}
```
**Purpose**: Remove users from organization
**Use Case**: Fire employees, remove inactive users

### 📝 **Content Management (MEDIUM PRIORITY)**

#### Get User's Own Notes
```bash
GET /api/v1/notes/my-notes
```
**Purpose**: Show users their own notes
**Use Case**: Personal dashboard, "My Content" tab

#### Get User's Own Todos
```bash
GET /api/v1/todos/my-todos
```
**Purpose**: Show users their own todos
**Use Case**: Personal dashboard, "My Content" tab

## Organization Management

### Organization Structure

```
Organization (ID: 1, Name: "Acme Corp")
├── Users
│   ├── john_admin (ADMIN) - Owner
│   ├── jane_member (MEMBER) - Team Member
│   └── bob_member (MEMBER) - Team Member
├── Notes
│   ├── Project Ideas
│   ├── Meeting Notes
│   └── Client Requirements
└── Todos
    ├── Review proposal
    ├── Schedule meeting
    └── Prepare presentation
```

### Organization Operations

#### Get My Organization
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

#### List Organization Users (ADMIN Only)
```bash
curl -X GET "http://localhost:8000/api/v1/organizations/1/users" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
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

## Permission Matrix

### Complete Permission Breakdown

| **Resource** | **Operation** | **ADMIN** | **MEMBER** | **Notes** |
|--------------|---------------|-----------|------------|-----------|
| **Notes** | Create | ✅ | ✅ | All users can create notes |
| **Notes** | Read | ✅ | ✅ | All users can read notes |
| **Notes** | Update | ✅ | ❌ | Only admins can edit notes |
| **Notes** | Delete | ✅ | ❌ | Only admins can delete notes |
| **My Notes** | Read | ✅ | ✅ | All users can see their own notes |
| **Todos** | Create | ✅ | ✅ | All users can create todos |
| **Todos** | Read | ✅ | ✅ | All users can read todos |
| **Todos** | Update | ✅ | ✅ | All users can update todos |
| **Todos** | Delete | ✅ | ❌ | Only admins can delete todos |
| **My Todos** | Read | ✅ | ✅ | All users can see their own todos |
| **Organization** | View Details | ✅ | ✅ | All users can see their org |
| **Organization** | List Users | ✅ | ❌ | Only admins can see user list |
| **Organization** | Public List | ✅ | ✅ | All users can see available orgs |
| **Organization** | Search | ✅ | ✅ | All users can search orgs |
| **Users** | Manage Roles | ✅ | ❌ | Only admins can change roles |
| **Users** | Remove Users | ✅ | ❌ | Only admins can remove users |

### Permission Enforcement Examples

#### 1. MEMBER Trying to Update Note (403 Forbidden)
```bash
curl -X PUT "http://localhost:8000/api/v1/notes/1" \
  -H "Authorization: Bearer MEMBER_TOKEN" \
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

#### 2. MEMBER Trying to Delete Todo (403 Forbidden)
```bash
curl -X DELETE "http://localhost:8000/api/v1/todos/1" \
  -H "Authorization: Bearer MEMBER_TOKEN"
```

**Response:**
```json
{
  "detail": "Insufficient permissions. ADMIN role required."
}
```

#### 3. MEMBER Trying to View Organization Users (403 Forbidden)
```bash
curl -X GET "http://localhost:8000/api/v1/organizations/1/users" \
  -H "Authorization: Bearer MEMBER_TOKEN"
```

**Response:**
```json
{
  "detail": "Insufficient permissions. ADMIN role required."
}
```

## API Endpoints by Role

### Authentication Endpoints
| **Endpoint** | **Method** | **Role Required** | **Description** |
|--------------|------------|-------------------|-----------------|
| `/api/v1/auth/signup` | POST | None | User registration |
| `/api/v1/auth/login` | POST | None | User authentication |
| `/api/v1/auth/me` | GET | Any Authenticated | Get current user info |

### Organization Endpoints
| **Endpoint** | **Method** | **Role Required** | **Description** |
|--------------|------------|-------------------|-----------------|
| `/api/v1/organizations/me` | GET | Any Authenticated | Get user's organization |
| `/api/v1/organizations/public` | GET | None | List all organizations |
| `/api/v1/organizations/search` | GET | None | Search organizations by name |
| `/api/v1/organizations/{id}/users` | GET | ADMIN | List organization users |
| `/api/v1/organizations/{id}/users/{user_id}` | PUT | ADMIN | Update user role |
| `/api/v1/organizations/{id}/users/{user_id}` | DELETE | ADMIN | Remove user from org |

### Notes Endpoints
| **Endpoint** | **Method** | **Role Required** | **Description** |
|--------------|------------|-------------------|-----------------|
| `/api/v1/notes` | GET | Any Authenticated | List all notes |
| `/api/v1/notes/my-notes` | GET | Any Authenticated | List user's own notes |
| `/api/v1/notes` | POST | Any Authenticated | Create new note |
| `/api/v1/notes/{id}` | GET | Any Authenticated | Get specific note |
| `/api/v1/notes/{id}` | PUT | ADMIN | Update note |
| `/api/v1/notes/{id}` | DELETE | ADMIN | Delete note |

### Todos Endpoints
| **Endpoint** | **Method** | **Role Required** | **Description** |
|--------------|------------|-------------------|-----------------|
| `/api/v1/todos` | GET | Any Authenticated | List all todos |
| `/api/v1/todos/my-todos` | GET | Any Authenticated | List user's own todos |
| `/api/v1/todos` | POST | Any Authenticated | Create new todo |
| `/api/v1/todos/{id}` | GET | Any Authenticated | Get specific todo |
| `/api/v1/todos/{id}` | PUT | Any Authenticated | Update todo |
| `/api/v1/todos/{id}` | DELETE | ADMIN | Delete todo |

## Security Implementation

### JWT Token Structure
```json
{
  "sub": "username",
  "user_id": 123,
  "organization_id": 1,
  "role": "ADMIN",
  "exp": 1705312800
}
```

### Security Features
1. **Token Expiration**: 24 hours (configurable)
2. **Password Hashing**: bcrypt with salt
3. **Role Validation**: Server-side role checking
4. **Organization Isolation**: Data access restricted by org
5. **Permission Middleware**: Automatic role enforcement

### Authentication Flow
```
1. User submits credentials → /api/v1/auth/login
2. Server validates credentials
3. Server generates JWT with user info
4. Client stores JWT token
5. Client includes JWT in Authorization header
6. Server validates JWT and extracts user info
7. Server checks permissions based on user role
8. Server allows/denies access accordingly
```

## Database Schema

### User Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('ADMIN', 'MEMBER') DEFAULT 'MEMBER',
    organization_id INTEGER NOT NULL,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    FOREIGN KEY (organization_id) REFERENCES organizations(id)
);
```

### Organization Table
```sql
CREATE TABLE organizations (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL
);
```

### Notes Table
```sql
CREATE TABLE notes (
    id INTEGER PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    organization_id INTEGER NOT NULL,
    created_by INTEGER NOT NULL,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    FOREIGN KEY (organization_id) REFERENCES organizations(id),
    FOREIGN KEY (created_by) REFERENCES users(id)
);
```

### Todos Table
```sql
CREATE TABLE todos (
    id INTEGER PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    completed BOOLEAN DEFAULT FALSE,
    organization_id INTEGER NOT NULL,
    created_by INTEGER NOT NULL,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    FOREIGN KEY (organization_id) REFERENCES organizations(id),
    FOREIGN KEY (created_by) REFERENCES users(id)
);
```

## Usage Examples

### Complete Workflow Example

#### Step 1: Create Organization (First Admin)
```bash
# Admin creates new organization
curl -X POST "http://localhost:8000/api/v1/auth/signup" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "company_ceo",
    "password": "ceopass123",
    "organization_name": "Tech Solutions Inc"
  }'
```

#### Step 2: Add Team Members
```bash
# Add first team member
curl -X POST "http://localhost:8000/api/v1/auth/signup" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "developer1",
    "password": "devpass123",
    "organization_name": "Tech Solutions Inc"
  }'

# Add second team member
curl -X POST "http://localhost:8000/api/v1/auth/signup" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "designer1",
    "password": "designpass123",
    "organization_name": "Tech Solutions Inc"
  }'
```

#### Step 3: Login and Get Token
```bash
# Admin login
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "company_ceo",
    "password": "ceopass123"
  }'

# Response contains access token
# {
#   "access_token": "eyJhbGciOiJIUzI1NiIs...",
#   "token_type": "bearer"
# }
```

#### Step 3.5: Get Current User Info
```bash
# Get user details using the token
curl -X GET "http://localhost:8000/api/v1/auth/me" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# Response:
# {
#   "id": 1,
#   "username": "company_ceo",
#   "role": "ADMIN",
#   "organization_id": 1,
#   "created_at": "2024-01-15T10:30:00"
# }
```

#### Step 4: Use API with Role-Based Access
```bash
# Admin can create notes
curl -X POST "http://localhost:8000/api/v1/notes" \
  -H "Authorization: Bearer ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Project Requirements",
    "content": "Build a new web application"
  }'

# Admin can view organization users
curl -X GET "http://localhost:8000/api/v1/organizations/1/users" \
  -H "Authorization: Bearer ADMIN_TOKEN"

# Members can create todos
curl -X POST "http://localhost:8000/api/v1/todos" \
  -H "Authorization: Bearer MEMBER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Review code changes"
  }'

# Members can view their own content
curl -X GET "http://localhost:8000/api/v1/notes/my-notes" \
  -H "Authorization: Bearer MEMBER_TOKEN"

curl -X GET "http://localhost:8000/api/v1/todos/my-todos" \
  -H "Authorization: Bearer MEMBER_TOKEN"
```

#### Step 5: Organization Discovery
```bash
# Get all available organizations
curl -X GET "http://localhost:8000/api/v1/organizations/public"

# Search for specific organization
curl -X GET "http://localhost:8000/api/v1/organizations/search?q=tech"
```

#### Step 6: User Management (Admin Only)
```bash
# Change user role
curl -X PUT "http://localhost:8000/api/v1/organizations/1/users/2" \
  -H "Authorization: Bearer ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "role": "ADMIN"
  }'

# Remove user from organization
curl -X DELETE "http://localhost:8000/api/v1/organizations/1/users/3" \
  -H "Authorization: Bearer ADMIN_TOKEN"
```

## Error Handling

### Common Error Responses

#### 401 Unauthorized
```json
{
  "detail": "Could not validate credentials",
  "headers": {
    "www-authenticate": "Bearer"
  }
}
```

#### 403 Forbidden (Role Insufficient)
```json
{
  "detail": "Insufficient permissions. ADMIN role required."
}
```

#### 403 Forbidden (Organization Access)
```json
{
  "detail": "Access denied. You can only access your organization's data."
}
```

#### 404 Not Found
```json
{
  "detail": "Organization not found"
}
```

#### 400 Bad Request
```json
{
  "detail": "Username already registered"
}
```

#### 400 Bad Request (Self-Operation)
```json
{
  "detail": "Cannot change your own role"
}
```

## Best Practices

### For Admins
1. **Share Organization Name**: Provide organization name to new team members
2. **Monitor Users**: Regularly check organization user list
3. **Manage Content**: Review and moderate notes and todos
4. **Security**: Keep admin credentials secure
5. **User Management**: Use role updates instead of removing users when possible

### For Members
1. **Get Organization Name**: Ask your admin for the organization name
2. **Respect Permissions**: Don't attempt unauthorized operations
3. **Collaborate**: Create and contribute content within your role limits
4. **Personal Content**: Use my-notes and my-todos for personal organization
5. **Report Issues**: Contact admin for permission-related problems

### For Developers
1. **Role Validation**: Always check user roles before sensitive operations
2. **Organization Scoping**: Ensure data isolation between organizations
3. **Error Handling**: Provide clear error messages for permission issues
4. **Testing**: Test both ADMIN and MEMBER user scenarios
5. **API Design**: Use intuitive endpoints like my-notes, my-todos

## Frontend Integration Tips

### Signup Form
- **Organization Selection**: Use `/api/v1/organizations/public` for dropdown
- **Search**: Implement search with `/api/v1/organizations/search?q={name}`
- **Validation**: Check if organization exists before allowing signup

### Dashboard
- **Content Tabs**: Separate "All Content" and "My Content" views
- **Role Indicators**: Show user role and permissions clearly
- **Admin Panel**: Only show user management for ADMIN users

### Navigation
- **Conditional Menus**: Hide admin features from MEMBER users
- **Permission Checks**: Disable buttons for unauthorized actions
- **User Feedback**: Show clear messages for permission errors

## Conclusion

This enhanced RBAC system provides:
- **User-friendly signup** with organization names instead of IDs
- **Complete organization discovery** with public listing and search
- **Personal content filtering** with my-notes and my-todos
- **Advanced user management** with role updates and user removal
- **Secure multi-tenant architecture** with clear role separation
- **Automatic permission enforcement** and organization-based data isolation

The system now makes it incredibly easy for users to:
- **Join existing organizations** by simply typing the organization name
- **Discover available organizations** through public listing and search
- **Manage their personal content** separately from team content
- **Administer team members** with role changes and removals

This approach gives you a **solid, production-ready RBAC system** that's both powerful and user-friendly, perfect for modern web applications! 🎉
