"""
Database configuration for the Notes API.

This module is responsible for:
1. Reading the database connection URL from the .env file.
2. Creating the SQLAlchemy engine.
3. Managing database sessions.
4. Providing the Base class for all ORM models.
"""

import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Load variables from the .env file.
load_dotenv()

# PostgreSQL database connection string.
DATABASE_URL = os.getenv("DATABASE_URL")

# Create the SQLAlchemy engine.
engine = create_engine(DATABASE_URL)

# Create a database session factory.
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# Base class for all SQLAlchemy models.
Base = declarative_base()