from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, func, Enum
from database import Base


priority_enum = Enum("low", "medium", "high", name="priority_enum", native_enum=False)
status_enum = Enum("pending", "in_progress", "completed", name="status_enum", native_enum=False) #Enum dois etre déclarer avant de créer le model

class Task(Base):
    __tablename__ = "task"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255), unique=True, nullable=False)
    priority = Column(priority_enum, nullable=False)
    status = Column(status_enum, nullable=False)
    active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, server_default=func.now())