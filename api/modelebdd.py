from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, func, Enum
import enum
from database import Base


class PriorityEnum(str, enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"

class StatusEnum(str, enum.Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"


class Task(Base):
    __tablename__ = "task"
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    name = Column(String(100), nullable=False)
    description = Column(String(255), unique=True, nullable=False)
    priority = Column(Enum(PriorityEnum), nullable=False)
    status = Column(Enum(StatusEnum), nullable=False)
    active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, server_default=func.now())