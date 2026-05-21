from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, func, Enum, ForeignKey
from sqlalchemy.orm import relationship
import enum
from api.database import Base


class PriorityEnum(str, enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"

LABELS = {
    PriorityEnum.low == "low",
    PriorityEnum.medium == "medium",
    PriorityEnum.high == "high"
}

class StatusEnum(str, enum.Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"

LABELS = {
    StatusEnum.pending =="pending",
    StatusEnum.in_progress== "in_progress",
    StatusEnum.completed == "completed"
}


class Task(Base):
    __tablename__ = "task"
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    name = Column(String(100), nullable=False)
    description = Column(String(255), nullable=False)
    priority = Column(Enum(PriorityEnum), nullable=False)
    status = Column(Enum(StatusEnum), nullable=False)
    active = Column(Boolean, default=True)
    parent_id = Column(Integer, ForeignKey("task.id"), nullable=True)
    subtasks = relationship("Task", backref="parent", remote_side=[id])