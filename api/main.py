from fastapi import FastAPI, requests, Response, responses
#from psycopg2 import connect
from pydantic import BaseModel
#import dotenv
app = FastAPI()

task = [
    {"id": 1,
    "title": "Task 1",
    "description": "This is task 1",
    "completed": False},
    {"id": 2,
    "title": "Task 2",
    "description": "This is task 2",
    "completed": False},
    {"id": 3,
    "title": "Task 3",
    "description": "This is task 3",
    "completed": False},
]
@app.post("/task/")
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
