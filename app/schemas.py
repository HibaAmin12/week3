"""
Pydantic schemas for the Notes API.

This file contains:
1. Note Schemas
2. Category Schemas
3. User Schemas
4. Authentication Schemas
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


# ==========================================================
# Note Schemas
# ==========================================================

class NoteBase(BaseModel):
    """
    Common fields shared by NoteCreate and NoteUpdate.
    """

    title: str
    body: str
    category_id: Optional[int] = None


class NoteCreate(NoteBase):
    """
    Schema used when creating a new note.
    """

    pass


class NoteUpdate(NoteBase):
    """
    Schema used when updating an existing note.
    """

    pass


class NoteResponse(NoteBase):
    """
    Schema returned to the client.
    """

    id: int
    owner_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ==========================================================
# Category Schemas
# ==========================================================

class CategoryBase(BaseModel):
    """
    Common fields shared by Category schemas.
    """

    name: str


class CategoryCreate(CategoryBase):
    """
    Schema used when creating a category.
    """

    pass


class CategoryUpdate(CategoryBase):
    """
    Schema used when updating a category.
    """

    pass


class CategoryResponse(CategoryBase):
    """
    Schema returned to the client.
    """

    id: int

    model_config = ConfigDict(from_attributes=True)


# ==========================================================
# User Schemas
# ==========================================================

class UserBase(BaseModel):
    """
    Common user fields.
    """

    username: str


class UserCreate(UserBase):
    """
    Schema used when registering a new user.
    """

    password: str
    role: str = "user"


class UserLogin(BaseModel):
    """
    Schema used for user login.
    """

    username: str
    password: str


class UserResponse(UserBase):
    """
    Schema returned to the client.
    """

    id: int
    role: str

    model_config = ConfigDict(from_attributes=True)


# ==========================================================
# JWT Authentication Schemas
# ==========================================================

class Token(BaseModel):
    """
    JWT token returned after successful login.
    """

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """
    Data extracted from the JWT payload.
    """

    username: Optional[str] = None
    role: Optional[str] = None