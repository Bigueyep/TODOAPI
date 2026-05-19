from fastapi import FastAPI, requests, Response, responses
from pydantic import BaseModel
from database import Base, engine
from modelebdd import Task
app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.post("/task/")
def root():
    return {"message": "BDD ok"}
def create_task():
    return task
@app.get("/task/{id}")
def get_task(id: int):
    print(task)
    return task
@app.delete("/tasks")
def delete_task():
    return task
@app.get("/tasks")
def get_tasks(id: int, response: Response): #permet de retourner une erreur si non trouver
    return task
@app.put("/task")
def update_task():
    return task
