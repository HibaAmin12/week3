"""
Utility functions used across the application.

This module provides helper functions for:
1. Hashing passwords
2. Verifying passwords
"""

from passlib.context import CryptContext

# Configure bcrypt as the password hashing algorithm.
pwd_context = CryptContext( schemes=["bcrypt"],deprecated="auto",)


def hash_password(password: str) -> str:
    """
    Hash a plain text password before storing it in the database.

    Args:
        password: Plain text password provided by the user.

    Returns:
        Hashed password.
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str,) -> bool:
    """
    Verify whether the entered password matches the stored hash.

    Args:
        plain_password: Password entered by the user.
        hashed_password: Password stored in the database.

    Returns:
        True if the password is correct, otherwise False.
    """
    return pwd_context.verify(plain_password, hashed_password,)