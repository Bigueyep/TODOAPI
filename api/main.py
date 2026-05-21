from fastapi import FastAPI, Response, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from api.database import Base, engine, get_db #ajouter api. pour eviter conflit lors du dockercompose
from api.modelebdd import Task, PriorityEnum, StatusEnum
from typing import Optional
import datetime #pour les champs de date et heure

from sqlalchemy.exc import IntegrityError


app = FastAPI()

Base.metadata.create_all(bind=engine)

class TaskCreate(BaseModel): #ne pas mettre la date car elle est auto générée par la base de données id aussi
    name: str
    description: str
    priority: PriorityEnum = Field(
        description= "priorité de la tâche",
        example="low"
    )
    status: StatusEnum = Field(
        description= "status",
        example="pending"
    )
    active: bool = True
    parentid: Optional[int] = None

    model_config = {
        "from_attributes": True, #meilleur gestion du json pour la libraire pydantic avec datetime
        "arbitrary_types_allowed": True
    }

class TaskRead(BaseModel):
    id: int
    created_at: datetime.datetime
    name: str
    description: str
    priority: PriorityEnum
    status: StatusEnum
    active: bool
    parentid: Optional[int] = None

    model_config = {
        "from_attributes": True,
        "arbitrary_types_allowed": True
    }

@app.post("/task/")
def root():
    return {"message": "BDD ok"}
@app.post("/task", response_model=TaskRead)
def create_task(
    task: TaskCreate,
    db: Session= Depends(get_db)
):
    db_task = Task(
        name=task.name,
        description=task.description,
        priority=task.priority,
        status=task.status,
        active=task.active,
        parent_id=task.parentid
    )
    try:
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="DB Error")
    if task.parentid:
        parent_task = db.query(Task).filter(Task.id == task.parentid).first()
        if not parent_task:
            raise HTTPException(status_code=404, detail="Parent task not found")
    return db_task 
@app.get("/task/{id}")
def get_task(id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == id).first() #envoie requete a bdd pour lecture de la tache avec id correspondant
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    print(task)
    return task
@app.get("/tasks/{name}")
def get_task_by_name(name: str, db: Session = Depends(get_db)): #same mais par nom
    task = db.query(Task).filter(Task.name == name).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task
@app.delete("/tasks/{id}")
def delete_task(id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return task
@app.get("/tasks", response_model=list[TaskRead])#formater la reponse en se basant sur TaskREAd
def get_tasks(
    priority: Optional[PriorityEnum] = None,
    status: Optional[StatusEnum] = None,
    active: Optional[bool] = None,
    name: Optional[str] = None,
    parentid: Optional[int] = None,
    db: Session = Depends(get_db)

): #lister taches
    query = db.query(Task)

    if priority:
        query = query.filter(Task.priority == priority)

    if status:
        query = query.filter(Task.status == status)

    if active is not None:
        query = query.filter(Task.active == active)
    
    if name:
        query = query.filter(Task.name == name)

    if parentid is not None:
        query = query.filter(Task.parent_id == parentid)
    
    tasks = query.all()

    return tasks
@app.put("/task/{id}")
def update_task(id: int, task_update: TaskCreate, db: Session = Depends(get_db)): #changer la tache
    task = db.query(Task).filter(Task.id == id).first()
    if task_update.parentid:
        parent_task = db.query(Task).filter(Task.id == task_update.parentid).first()
        if not parent_task:
            raise HTTPException(status_code=404, detail="Parent task not found")
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    for key, value in task_update().items():
        setattr(task, key, value)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Update Error (DB-issue)")

