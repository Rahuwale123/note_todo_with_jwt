from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base, TimestampMixin


class Todo(Base, TimestampMixin):
    __tablename__ = "todos"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    completed = Column(Boolean, default=False, nullable=False)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    organization = relationship("Organization", back_populates="todos")
    created_by_user = relationship("User", back_populates="todos")
    
    def __repr__(self):
        return f"<Todo(id={self.id}, title='{self.title}', completed={self.completed})>"
