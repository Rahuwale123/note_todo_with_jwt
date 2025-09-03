from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from app.schemas.user import UserResponse


class OrganizationBase(BaseModel):
    name: str


class OrganizationCreate(OrganizationBase):
    pass


class OrganizationUpdate(OrganizationBase):
    pass


class OrganizationResponse(OrganizationBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class OrganizationWithUsers(OrganizationResponse):
    users: List[UserResponse]
