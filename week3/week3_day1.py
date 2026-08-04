from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def home():
    return {"message": "Hello FastAPI"}


#MULTIPLE ROUTES

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def home():
    return {"message": "Home Page"}

@app.get("/about")
async def about():
    return {"message": "About Page"}

@app.get("/contact")
async def contact():
    return {"message": "Contact Page"}

# PATH PARAMETERS
from fastapi import FastAPI

app = FastAPI()
@app.get("/books/{book_id}")
async def get_book(book_id: int):
    return {
        "book_id": book_id
    }

# QUERY PRAMEtERS

from fastapi import FastAPI

app = FastAPI()

@app.get("/search")
async def search(name: str):
    return {
        "name": name
    }

@app.get("/search")
async def search(name: str, age: int):
    return {
        "name": name,
        "age": age
    }


# PYDANTIC MODELS
from fastapi import FastAPI,status
from pydantic import BaseModel

app = FastAPI()


class Book(BaseModel):
    title: str
    price: float


@app.post("/books")
async def create_book(book: Book):
    return book

@app.put("/books/{book_id}")
async def update_book(book_id: int, book: Book):
    return {
        "book_id": book_id,
        "book": book
    }
@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int):
    return

# Build Complete Task API
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
import asyncio
app = FastAPI()


class Task(BaseModel):
    title: str
    completed: bool


tasks = {
    1: {"title": "Learn FastAPI", "completed": False},
    2: {"title": "Practice Python", "completed": True},
}


@app.get("/api/v1/tasks")
async def get_tasks():
    return tasks


@app.get("/api/v1/tasks/{task_id}")
async def get_task(task_id: int):

    if task_id not in tasks:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return tasks[task_id]


@app.post("/api/v1/tasks", status_code=status.HTTP_201_CREATED)
async def create_task(task: Task):

    new_id = max(tasks.keys()) + 1

    tasks[new_id] = task.model_dump()

    return {
        "id": new_id,
        **tasks[new_id]
    }


@app.put("/api/v1/tasks/{task_id}")
async def update_task(task_id: int, task: Task):

    if task_id not in tasks:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    tasks[task_id] = task.model_dump()

    return tasks[task_id]


@app.patch("/api/v1/tasks/{task_id}")
async def patch_task(task_id: int, task: Task):

    if task_id not in tasks:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    tasks[task_id] = task.model_dump()

    return tasks[task_id]


@app.delete("/api/v1/tasks/{task_id}",
            status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: int):

    if task_id not in tasks:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    del tasks[task_id]



@app.get("/slow")
async def slow():

    await asyncio.sleep(2)

    return {
        "message": "Finished after 2 seconds"
    }