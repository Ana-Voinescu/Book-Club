"""
Authentication routes: register, login, logout, get current user.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from database import get_db
from models import User
from schemas import UserCreate, UserLogin, UserResponse, MessageResponse
from auth import hash_password, verify_password, create_session, get_current_user_id, require_auth, destroy_session

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, request: Request, db: Session = Depends(get_db)):
    """
    Register a new user.

    This endpoint:
    1. Checks if email already exists
    2. Hashes the password
    3. Creates the user in the database
    4. Creates a session (logs them in automatically)
    5. Returns the user data
    """
    # Check if email already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Hash the password
    hashed_pw = hash_password(user_data.password)

    # Create new user
    new_user = User(
        name=user_data.name,
        email=user_data.email,
        password_hash=hashed_pw,
        bookmark_count=0
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Create session (auto-login after registration)
    create_session(request, new_user.user_id)

    return new_user


@router.post("/login", response_model=UserResponse)
def login(credentials: UserLogin, request: Request, db: Session = Depends(get_db)):
    """
    Login a user.

    This endpoint:
    1. Finds user by email
    2. Verifies password
    3. Creates a session
    4. Returns the user data
    """
    # Find user by email
    user = db.query(User).filter(User.email == credentials.email).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Verify password
    if not verify_password(credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Create session
    create_session(request, user.user_id)

    return user


@router.post("/logout", response_model=MessageResponse)
def logout(request: Request):
    """
    Logout the current user.

    This endpoint:
    1. Destroys the session
    2. Returns a success message
    """
    destroy_session(request)
    return {"message": "Logged out successfully"}


@router.get("/me", response_model=UserResponse)
def get_current_user(request: Request, db: Session = Depends(get_db)):
    """
    Get the current authenticated user's data.

    This endpoint:
    1. Checks if user is authenticated
    2. Returns their user data

    Returns 401 if not authenticated.
    """
    user_id = require_auth(request)

    user = db.query(User).filter(User.user_id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return user
