"""
Database models for Notes API.
"""

from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


# ==========================================================
# User Model
# ==========================================================

class User(Base):

    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    username = Column(
        String,
        unique=True,
        nullable=False
    )

    hashed_password = Column(
        String,
        nullable=False
    )

    role = Column(
        String,
        default="user",
        nullable=False
    )


    # One user can have many notes
    notes = relationship(
        "Note",
        back_populates="owner",
        cascade="all, delete-orphan"
    )



# ==========================================================
# Category Model
# ==========================================================

class Category(Base):

    __tablename__ = "categories"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    # Category name
    name = Column(
        String,
        unique=True,
        nullable=False
    )


    # One category can have many notes
    notes = relationship(
        "Note",
        back_populates="category"
    )



# ==========================================================
# Note Model
# ==========================================================

class Note(Base):

    __tablename__ = "notes"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    title = Column(
        String,
        nullable=False
    )


    body = Column(
        String,
        nullable=False
    )


    # Note belongs to user
    owner_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )


    # Note optionally belongs to category
    category_id = Column(
        Integer,
        ForeignKey("categories.id"),
        nullable=True
    )


    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )


    updated_at = Column(
        DateTime,
        nullable=True
    )


    # Relationship with User
    owner = relationship(
        "User",
        back_populates="notes"
    )


    # Relationship with Category
    category = relationship(
        "Category",
        back_populates="notes"
    )