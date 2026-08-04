"""
JWT Authentication utilities.

This module is responsible for:
1. Creating JWT access tokens.
2. Verifying JWT tokens.
3. Returning the currently authenticated user.
"""

import os
from datetime import datetime, timedelta, timezone
from typing import Optional

from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app import models
from app.dependencies import get_db
from app.schemas import TokenData

# Load environment variables.
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

# FastAPI expects the JWT token from this login endpoint.
oauth2_scheme = OAuth2PasswordBearer( tokenUrl="/api/v1/auth/login",)


def create_access_token(data: dict):
    """
    Create a JWT access token.
    """

    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES,
    )

    to_encode.update({"exp": expire})

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )


def verify_access_token(
    token: str,
    credentials_exception,
):
    """
    Verify the JWT access token.
    """

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )

        username: Optional[str] = payload.get("username")
        role: Optional[str] = payload.get("role")

        if username is None:
            raise credentials_exception

        return TokenData(
            username=username,
            role=role,
        )

    except JWTError:
        raise credentials_exception


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    """
    Return the currently authenticated user.
    """

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token_data = verify_access_token(
        token,
        credentials_exception,
    )

    user = (
        db.query(models.User)
        .filter(models.User.username == token_data.username)
        .first()
    )

    if user is None:
        raise credentials_exception

    return user