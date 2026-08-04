"""
Shared dependencies used across the application.
"""

from app.database import SessionLocal


def get_db():
    """
    Provide a database session for each request.

    A new session is created before the request starts
    and is automatically closed after the request finishes.
    """

    # Create a new database session.
    db = SessionLocal()

    try:
        # Make the session available to the route.
        yield db

    finally:
        # Always close the session to free resources.
        db.close()