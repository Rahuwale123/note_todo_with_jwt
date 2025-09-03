from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.models.base import Base, TimestampMixin


class Organization(Base, TimestampMixin):
    __tablename__ = "organizations"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    
    users = relationship("User", back_populates="organization")
    notes = relationship("Note", back_populates="organization")
    todos = relationship("Todo", back_populates="organization")
    
    def __repr__(self):
        return f"<Organization(id={self.id}, name='{self.name}')>"
