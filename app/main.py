"""
Main entry point of the Notes API application.

This module:
1. Creates the FastAPI application.
2. Registers all API routers.
"""

from fastapi import FastAPI

from app.routers import admin, auth, notes

# Create the FastAPI application.
app = FastAPI(
    title="Notes API",
    description=(
        "A Notes Management API built with FastAPI, "
        "SQLAlchemy, Alembic, and JWT Authentication."
    ),
    version="1.0.0",
)

# Register application routers.
app.include_router(auth.router)
app.include_router(notes.router)
app.include_router(admin.router)


@app.get("/", tags=["Root"])
def root():
    """
    Root endpoint used to verify that the API is running.
    """

    return {
        "message": "Welcome to the Notes API!"
    }