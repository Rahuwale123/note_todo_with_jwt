from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from datetime import datetime

Base = declarative_base()


class TimestampMixin:
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
