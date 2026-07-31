# import os
# from dotenv import load_dotenv
# from fastapi import FastAPI, Header, HTTPException, Depends

# app = FastAPI()
# load_dotenv()

# API_KEY = os.getenv("API_KEY")

# def verify_api_key(x_api_key: str = Header()):
#     if x_api_key != API_KEY:
#         raise HTTPException(status_code=401, detail="Invalid API Key")

# @app.get("/")
# def home():
#     return {"message": "Public Endpoint"}

# @app.post("/tasks", dependencies=[Depends(verify_api_key)])
# def create_task():
#     return {"message": "Task Created"}

# from fastapi import FastAPI, Header, HTTPException, Depends
# from database import get_connection

# app = FastAPI()


# @app.get("/tasks")
# def get_tasks():

#     connection = get_connection()
#     cursor = connection.cursor()

#     cursor.execute("SELECT * FROM tasks")

#     rows = cursor.fetchall()

#     connection.close()

#     return rows


# @app.post("/tasks")
# def create_task(title: str):

#     connection = get_connection()
#     cursor = connection.cursor()

#     cursor.execute(
#         """
#         INSERT INTO tasks(title, done, created_at)
#         VALUES (?, ?, ?)
#         """,
#         (title, False, "2026-07-31")
#     )

#     connection.commit()

#     connection.close()

#     return {
#         "message": "Task Created"
#     }

# @app.put("/tasks/{task_id}")
# def update_task(task_id: int):

#     connection = get_connection()
#     cursor = connection.cursor()

#     cursor.execute(
#         """
#         UPDATE tasks
#         SET done = ?
#         WHERE id = ?
#         """,
#         (True, task_id)
#     )

#     connection.commit()

#     connection.close()

#     return {
#         "message": "Task Updated"
#     }

# @app.delete("/tasks/{task_id}")
# def delete_task(task_id: int):

#     connection = get_connection()
#     cursor = connection.cursor()

#     cursor.execute(
#         """
#         DELETE FROM tasks
#         WHERE id = ?
#         """,
#         (task_id,)
#     )

#     connection.commit()

#     if cursor.rowcount == 0:
#         connection.close()
#         raise HTTPException(
#             status_code=404,
#             detail="Task not found"
#         )

#     connection.close()

#     return {
#         "message": "Task Deleted"
#     }


from fastapi import FastAPI, Depends, Header, HTTPException
from dotenv import load_dotenv
import os

from database import get_connection


app = FastAPI()


# Load environment variable
load_dotenv()

API_KEY = os.getenv("API_KEY")


# API Key verification dependency
def verify_api_key(x_api_key: str = Header(None)):

    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Invalid API Key"
        )

    return x_api_key


# Public endpoint
@app.get("/tasks")
def get_tasks():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM tasks")

    rows = cursor.fetchall()

    connection.close()

    return rows


# Protected POST
@app.post("/tasks")
def create_task(
    title: str,
    api_key: str = Depends(verify_api_key)
):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO tasks(title, done, created_at)
        VALUES (?, ?, ?)
        """,
        (title, False, "2026-07-31")
    )

    connection.commit()
    connection.close()

    return {
        "message": "Task Created"
    }


# Protected PUT
@app.put("/tasks/{task_id}")
def update_task(
    task_id: int,
    api_key: str = Depends(verify_api_key)
):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE tasks
        SET done = ?
        WHERE id = ?
        """,
        (True, task_id)
    )

    connection.commit()

    if cursor.rowcount == 0:
        connection.close()
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    connection.close()

    return {
        "message": "Task Updated"
    }


# Protected DELETE
@app.delete("/tasks/{task_id}")
def delete_task(
    task_id: int,
    api_key: str = Depends(verify_api_key)
):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM tasks
        WHERE id = ?
        """,
        (task_id,)
    )

    connection.commit()

    if cursor.rowcount == 0:
        connection.close()
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    connection.close()

    return {
        "message": "Task Deleted"
    }
