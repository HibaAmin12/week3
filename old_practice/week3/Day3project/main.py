from fastapi import FastAPI, HTTPException, Depends, Header
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from datetime import date
import os

from database import engine, Base, get_db
from models import Task

# Load environment variables
load_dotenv()

API_KEY = os.getenv("API_KEY")

# Create FastAPI app
app = FastAPI()

# Create tables
Base.metadata.create_all(bind=engine)


# -----------------------------
# API Key Dependency
# -----------------------------
def verify_api_key(x_api_key: str = Header(None)):

    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Invalid API Key"
        )

    return x_api_key


# -----------------------------
# GET ALL TASKS (Public)
# -----------------------------
@app.get("/tasks")
def get_tasks(
    db: Session = Depends(get_db)
):

    tasks = db.query(Task).all()

    return tasks


# -----------------------------
# CREATE TASK (Protected)
# -----------------------------
@app.post("/tasks")
def create_task(
    title: str,
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key)
):

    task = Task(
        title=title,
        done=False,
        created_at=str(date.today())
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return task


# -----------------------------
# UPDATE TASK (Protected)
# -----------------------------
@app.put("/tasks/{task_id}")
def update_task(
    task_id: int,
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key)
):

    task = db.query(Task).filter(
        Task.id == task_id
    ).first()

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    task.done = True

    db.commit()
    db.refresh(task)

    return task


# -----------------------------
# DELETE TASK (Protected)
# -----------------------------
@app.delete("/tasks/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key)
):

    task = db.query(Task).filter(
        Task.id == task_id
    ).first()

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    db.delete(task)
    db.commit()

    return {
        "message": "Task Deleted Successfully"
    }