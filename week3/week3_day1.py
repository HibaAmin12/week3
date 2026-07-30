# from fastapi import FastAPI

# app = FastAPI()

# @app.get("/")
# async def home():
#     return {"message": "Hello FastAPI"}


##MULTIPLE ROUTES

# from fastapi import FastAPI

# app = FastAPI()

# @app.get("/")
# async def home():
#     return {"message": "Home Page"}

# @app.get("/about")
# async def about():
#     return {"message": "About Page"}

# @app.get("/contact")
# async def contact():
#     return {"message": "Contact Page"}

## PATH PARAMETERS
# from fastapi import FastAPI

# app = FastAPI()
# @app.get("/books/{book_id}")
# async def get_book(book_id: int):
#     return {
#         "book_id": book_id
#     }

## QUERY PRAMEtERS

# from fastapi import FastAPI

# app = FastAPI()

# @app.get("/search")
# async def search(name: str):
#     return {
#         "name": name
#     }

# @app.get("/search")
# async def search(name: str, age: int):
#     return {
#         "name": name,
#         "age": age
#     }


## PYDANTIC MODELS
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