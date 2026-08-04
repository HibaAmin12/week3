"""
Database configuration for the Notes API.

This module is responsible for:
1. Creating the database engine.
2. Managing database sessions.
3. Providing the Base class for SQLAlchemy models.
"""

# Import SQLAlchemy components.
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# SQLite database file.
DATABASE_URL = "sqlite:///./notes.db"

# Create the SQLAlchemy engine.
# The engine is responsible for connecting the application
# to the SQLite database.
engine = create_engine(
    DATABASE_URL,
    # SQLite allows only one thread by default.
    # Setting check_same_thread=False allows FastAPI
    # to handle database access across multiple requests.
    connect_args={"check_same_thread": False}
)

# Create a database session factory.
# Every request will receive its own independent session.
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class for all SQLAlchemy models.
# Every model (User, Note, Category) will inherit from this class.
Base = declarative_base()


