"""
Pydantic schemas for request/response validation.
These define the structure of data sent to and from the API.
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime


# ============================================================================
# User Schemas
# ============================================================================

class UserCreate(BaseModel):
    """Schema for user registration."""
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=6)


class UserLogin(BaseModel):
    """Schema for user login."""
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """Schema for user data in responses."""
    user_id: int
    name: str
    email: str
    bookmark_count: int

    class Config:
        from_attributes = True  # Allows conversion from SQLAlchemy models


# ============================================================================
# Book Schemas
# ============================================================================

class BookBase(BaseModel):
    """Base book schema with common fields."""
    title: str
    author: str
    release_year: Optional[int] = None
    summary: Optional[str] = None
    bookmark_price: int = 0
    cover_image: Optional[str] = None
    pdf_url: Optional[str] = None


class BookResponse(BookBase):
    """Schema for book data in responses."""
    book_id: int

    class Config:
        from_attributes = True


class BookWithUserData(BookResponse):
    """Book response with user-specific data (is_purchased, user_rating)."""
    is_purchased: bool = False
    user_rating: Optional[int] = None
    average_rating: Optional[float] = None
    total_ratings: int = 0


# ============================================================================
# Rating Schemas
# ============================================================================

class RatingCreate(BaseModel):
    """Schema for creating/updating a book rating."""
    stars: int = Field(..., ge=1, le=5, description="Rating from 1 to 5 stars")


class RatingResponse(BaseModel):
    """Schema for rating data in responses."""
    user_id: int
    book_id: int
    stars: int

    class Config:
        from_attributes = True


# ============================================================================
# Comment Schemas
# ============================================================================

class CommentCreate(BaseModel):
    """Schema for creating a book comment."""
    content: str = Field(..., min_length=1, max_length=1000)


class CommentResponse(BaseModel):
    """Schema for comment data in responses."""
    comment_id: int
    book_id: int
    user_id: int
    content: str
    created_at: datetime
    user_name: str  # Will be populated from joined User data

    class Config:
        from_attributes = True


# ============================================================================
# Group Schemas
# ============================================================================

class GroupBase(BaseModel):
    """Base group schema."""
    name: str
    cover_image: Optional[str] = None
    current_book_id: Optional[int] = None


class GroupResponse(GroupBase):
    """Schema for group data in responses."""
    group_id: int
    created_at: str
    member_count: int = 0
    current_book: Optional[BookResponse] = None

    class Config:
        from_attributes = True


# ============================================================================
# Group Post Schemas
# ============================================================================

class PostCreate(BaseModel):
    """Schema for creating a group post."""
    content: str = Field(..., min_length=1, max_length=2000)
    book_id: Optional[int] = None


class PostResponse(BaseModel):
    """Schema for post data in responses."""
    post_id: int
    group_id: int
    user_id: int
    content: str
    book_id: Optional[int] = None
    user_name: str  # Will be populated from joined User data

    class Config:
        from_attributes = True


# ============================================================================
# Generic Response Schemas
# ============================================================================

class MessageResponse(BaseModel):
    """Generic message response."""
    message: str


class ErrorResponse(BaseModel):
    """Error response schema."""
    detail: str
