from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class NoteBase(BaseModel):
    title: str
    content: str


class NoteCreate(NoteBase):
    pass


class NoteUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None


class NoteResponse(NoteBase):
    id: int
    organization_id: int
    created_by: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class NoteWithUser(NoteResponse):
    created_by_username: str
