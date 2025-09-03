from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class TodoBase(BaseModel):
    title: str
    completed: bool = False


class TodoCreate(TodoBase):
    pass


class TodoUpdate(BaseModel):
    title: Optional[str] = None
    completed: Optional[bool] = None


class TodoResponse(TodoBase):
    id: int
    organization_id: int
    created_by: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class TodoWithUser(TodoResponse):
    created_by_username: str
