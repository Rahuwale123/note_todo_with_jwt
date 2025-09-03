from sqlalchemy import Column, Integer, String, Enum, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.models.base import Base, TimestampMixin
import enum


class UserRole(str, enum.Enum):
    ADMIN = "ADMIN"
    MEMBER = "MEMBER"


class User(Base, TimestampMixin):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.MEMBER, nullable=False)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    
    organization = relationship("Organization", back_populates="users")
    notes = relationship("Note", back_populates="created_by_user")
    todos = relationship("Todo", back_populates="created_by_user")
    
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', role='{self.role}')>"
