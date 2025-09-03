from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base, TimestampMixin


class Note(Base, TimestampMixin):
    __tablename__ = "notes"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    organization = relationship("Organization", back_populates="notes")
    created_by_user = relationship("User", back_populates="notes")
    
    def __repr__(self):
        return f"<Note(id={self.id}, title='{self.title}')>"
