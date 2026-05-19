from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, func, Enum
from database import Base

class Task(Base):
    __tablename__ = "task"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255), unique=True, nullable=False)
    priority = Column(Enum("low", "medium", "high"), nullable=False)
    status = Column(Enum("pending", "in_progress", "completed"), nullable=False)
    active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, server_default=func.now())