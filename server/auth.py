"""
Authentication utilities for password hashing and session management.
"""

import bcrypt
from typing import Optional
from fastapi import Request, HTTPException, status


def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt.

    Args:
        password: Plain text password

    Returns:
        Hashed password as a string
    """
    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against its hash.

    Args:
        plain_password: Plain text password to verify
        hashed_password: Hashed password from database

    Returns:
        True if password matches, False otherwise
    """
    return bcrypt.checkpw(
        plain_password.encode('utf-8'),
        hashed_password.encode('utf-8')
    )


def create_session(request: Request, user_id: int):
    """
    Create a user session by storing user_id in the session.

    Args:
        request: FastAPI request object
        user_id: ID of the authenticated user
    """
    request.session["user_id"] = user_id


def get_current_user_id(request: Request) -> Optional[int]:
    """
    Get the current user's ID from the session.

    Args:
        request: FastAPI request object

    Returns:
        User ID if authenticated, None otherwise
    """
    return request.session.get("user_id")


def require_auth(request: Request) -> int:
    """
    Require authentication. Raises HTTPException if not authenticated.

    Args:
        request: FastAPI request object

    Returns:
        User ID if authenticated

    Raises:
        HTTPException: If user is not authenticated
    """
    user_id = get_current_user_id(request)
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    return user_id


def destroy_session(request: Request):
    """
    Destroy the user session (logout).

    Args:
        request: FastAPI request object
    """
    request.session.clear()
