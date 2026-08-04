"""
Database models for the Notes API.

This module defines the database schema using SQLAlchemy ORM.
"""

from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


# ==========================================================
# User Model
# ==========================================================

class User(Base):
    """
    Represents a registered user of the application.
    """

    __tablename__ = "users"

    # Primary key.
    id = Column(Integer, primary_key=True, index=True)

    # Username must be unique.
    username = Column(String, unique=True, nullable=False)

    # Store the hashed password instead of the plain password.
    hashed_password = Column(String, nullable=False)

    # User role (user/admin).
    role = Column(String, default="user", nullable=False)

    # One user can own multiple notes.
    notes = relationship(
        "Note",
        back_populates="owner",
        cascade="all, delete-orphan",
    )


# ==========================================================
# Category Model
# ==========================================================

class Category(Base):
    """
    Represents a note category.
    """

    __tablename__ = "categories"

    # Primary key.
    id = Column(Integer, primary_key=True, index=True)

    # Category name must be unique.
    name = Column(String, unique=True, nullable=False)

    # One category can contain many notes.
    notes = relationship(
        "Note",
        back_populates="category",
    )


# ==========================================================
# Note Model
# ==========================================================

class Note(Base):
    """
    Represents a note created by a user.
    """

    __tablename__ = "notes"

    # Primary key.
    id = Column(Integer, primary_key=True, index=True)

    # Note title.
    title = Column(String, nullable=False)

    # Note content.
    body = Column(String, nullable=False)

    # Foreign key referencing the owner of the note.
    owner_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
    )

    # Optional category assigned to the note.
    category_id = Column(
        Integer,
        ForeignKey("categories.id"),
        nullable=True,
    )

    # Timestamp when the note is created.
    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )
    # Last updated timestamp.
    updated_at = Column(
    DateTime,
    nullable=True,
)

    # Relationship to the owner.
    owner = relationship(
        "User",
        back_populates="notes",
    )

    # Relationship to the category.
    category = relationship(
        "Category",
        back_populates="notes",
    )