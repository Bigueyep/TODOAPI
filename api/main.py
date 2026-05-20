from fastapi import FastAPI, Response, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import Base, engine, get_db
from modelebdd import Task, PriorityEnum, StatusEnum
from typing import Optional
import datetime #pour les champs de date et heure
import modelebdd


app = FastAPI()

Base.metadata.create_all(bind=engine)

class TaskCreate(BaseModel): #ne pas mettre la date car elle est auto générée par la base de données id aussi
    name: str
    description: str
    priority: PriorityEnum
    status: StatusEnum
    active: bool = True

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

    model_config = {
        "from_attributes": True,
        "arbitrary_types_allowed": True
    }

@app.post("/task/")
def root():
    return {"message": "BDD ok"}
@app.post("/task", response_model=TaskRead)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    db_task = Task(
        name=task.name,
        description=task.description,
        priority=task.priority,
        status=task.status,
        active=task.active
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task 
@app.get("/task/{id}")
def get_task(id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == id).first() #envoie requete a bdd pour lecture de la tache avec id correspondant
    print(task)
    return task
@app.get("/tasks/{name}")
def get_task_by_name(name: str, db: Session = Depends(get_db)): #same mais par nom
    task = db.query(Task).filter(Task.name == name).first()
    return task
@app.delete("/tasks/{id}")
def delete_task(id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == id).first()
    db.delete(task)
    db.commit()
    return task
@app.get("/tasks", response_model=list[TaskRead])#formater la reponse en se basant sur TaskREAd
def get_tasks(
    priority: Optional[PriorityEnum] = None,
    status: Optional[StatusEnum] = None,
    active: Optional[bool] = None,
    name: Optional[str] = None,
    db: Session = Depends(get_db)

): #lister taches
    query = db.query(Task)

    if priority:
        query = query.filter(priority == PriorityEnum)

    if status:
        query = query.filter(status == StatusEnum)

    if active is not None:
        query = query.filter(active == Task.active)
    
    if name:
        query = query.filter(name == Task.name)
    
    tasks = query.all()

    return tasks
@app.put("/task/{id}")
def update_task(id: int, task_update: TaskCreate, db: Session = Depends(get_db)): #changer la tache
    task = db.query(Task).filter(Task.id == id).first()
    for key, value in task_update.dict().items():
        setattr(task, key, value)
    db.commit()
    return task
