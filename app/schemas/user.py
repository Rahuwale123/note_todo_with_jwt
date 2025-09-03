from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from app.models.user import UserRole


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str
    organization_name: str


class UserUpdate(BaseModel):
    username: Optional[str] = None
    role: Optional[UserRole] = None


class UserInDB(UserBase):
    id: int
    role: UserRole
    organization_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class UserResponse(UserBase):
    id: int
    role: UserRole
    organization_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
    user_id: Optional[int] = None
    organization_id: Optional[int] = None
    role: Optional[UserRole] = None
