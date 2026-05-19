from fastapi import FastAPI, Response, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import Base, engine, get_db
from modelebdd import Task
import modelebdd

app = FastAPI()

Base.metadata.create_all(bind=engine)

class TaskCreate(BaseModel):
    name: str
    description: str
    priority: str
    status: str
    active: bool = True

    class Config:
        orm_mode = True 



@app.post("/task/")
def root():
    return {"message": "BDD ok"}
@app.post("/task")
def create_task(task:TaskCreate, db: Session = Depends(get_db)): #créé une tache dans la bdd
    return task
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
@app.get("/tasks", response_model=list[TaskCreate])#formater la reponse en se basant sur TaskCreate
def get_tasks(db: Session = Depends(get_db)): #lister taches
    tasks = db.query(Task).all()
    return tasks
@app.put("/task/{id}")
def update_task(id: int, task_update: TaskCreate, db: Session = Depends(get_db)): #changer la tache
    task = db.query(Task).filter(Task.id == id).first()
    for key, value in task_update.dict().items():
        setattr(task, key, value)
    db.commit()
    return task
