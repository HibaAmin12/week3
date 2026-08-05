"""
Authentication routes.

This module provides endpoints for:
1. User registration
2. User login
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import models, schemas
from app.dependencies import get_db
from app.oauth2 import create_access_token
from app.utils import hash_password, verify_password


router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Authentication"],
)



# ==========================================================
# Register User
# ==========================================================

@router.post(
    "/register",
    response_model=schemas.UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db),
):
    """
    Register a new user.
    """


    existing_user = (
        db.query(models.User)
        .filter(
            models.User.username == user.username
        )
        .first()
    )


    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists.",
        )


    hashed_password = hash_password(
        user.password
    )


    new_user = models.User(
        username=user.username,
        hashed_password=hashed_password,
        role=user.role,
    )


    db.add(new_user)
    db.commit()
    db.refresh(new_user)


    return new_user



# ==========================================================
# User Login
# ==========================================================

@router.post(
    "/login",
    response_model=schemas.Token,
    status_code=status.HTTP_200_OK,
)
def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """
    Authenticate a user and return JWT access token.
    """


    user = (
        db.query(models.User)
        .filter(
            models.User.username == user_credentials.username
        )
        .first()
    )


    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password.",
        )


    if not verify_password(
        user_credentials.password,
        user.hashed_password,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password.",
        )


    # Create JWT token
    # sub contains user id (standard JWT claim)
    access_token = create_access_token(
        data={
            "sub": str(user.id),
            "role": user.role,
        },
    )


    return {
        "access_token": access_token,
        "token_type": "bearer",
    }