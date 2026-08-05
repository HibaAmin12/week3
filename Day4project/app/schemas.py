"""
Pydantic schemas for the Notes API.

Contains:
1. Note Schemas
2. Category Schemas
3. User Schemas
4. Authentication Schemas
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


# ==========================================================
# Note Schemas
# ==========================================================

class NoteBase(BaseModel):

    title: str = Field(min_length=1)
    body: str = Field(min_length=1)
    category_id: Optional[int] = None



class NoteCreate(NoteBase):
    pass



class NoteUpdate(BaseModel):

    title: Optional[str] = Field(
        default=None,
        min_length=1
    )

    body: Optional[str] = Field(
        default=None,
        min_length=1
    )

    category_id: Optional[int] = None



class NoteResponse(NoteBase):

    id: int
    owner_id: int

    created_at: datetime
    updated_at: Optional[datetime] = None


    model_config = ConfigDict(
        from_attributes=True
    )



# ==========================================================
# Category Schemas
# ==========================================================

class CategoryBase(BaseModel):

    name: str = Field(min_length=1)



class CategoryResponse(CategoryBase):

    id: int


    model_config = ConfigDict(
        from_attributes=True
    )



# ==========================================================
# User Schemas
# ==========================================================

class UserBase(BaseModel):

    username: str



class UserCreate(UserBase):

    password: str
    role: str = "user"



class UserLogin(BaseModel):

    username: str
    password: str



class UserResponse(UserBase):

    id: int
    role: str


    model_config = ConfigDict(
        from_attributes=True
    )



# ==========================================================
# JWT Schemas
# ==========================================================

class Token(BaseModel):

    access_token: str
    token_type: str



class TokenData(BaseModel):

    user_id: Optional[int] = None
    role: Optional[str] = None