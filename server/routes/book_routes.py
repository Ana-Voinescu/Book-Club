"""
Book routes: browsing, purchasing, rating, and commenting on books.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Request, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from database import get_db
from models import Book, User, UserBooksRead, BookRating, BookComment
from schemas import (
    BookResponse,
    BookWithUserData,
    RatingCreate,
    RatingResponse,
    CommentCreate,
    CommentResponse,
    MessageResponse
)
from auth import get_current_user_id, require_auth

router = APIRouter(prefix="/api/books", tags=["Books"])


@router.get("", response_model=List[BookWithUserData])
def get_all_books(
    request: Request,
    q: Optional[str] = Query(None, description="Search query for book title or author"),
    db: Session = Depends(get_db)
):
    """
    Get all books. Optionally filter by search query.

    - **q**: Search query (searches in title and author)
    - Returns list of books with user-specific data if authenticated
    """
    user_id = get_current_user_id(request)

    # Base query
    query = db.query(Book)

    # Apply search filter if provided
    if q:
        search_term = f"%{q}%"
        query = query.filter(
            (Book.title.ilike(search_term)) | (Book.author.ilike(search_term))
        )

    books = query.all()

    # Enrich books with user-specific data
    result = []
    for book in books:
        # Calculate average rating
        avg_rating = db.query(func.avg(BookRating.stars)).filter(
            BookRating.book_id == book.book_id
        ).scalar()

        total_ratings = db.query(func.count(BookRating.stars)).filter(
            BookRating.book_id == book.book_id
        ).scalar()

        # Check if user has purchased this book
        is_purchased = False
        user_rating = None

        if user_id:
            is_purchased = db.query(UserBooksRead).filter(
                UserBooksRead.user_id == user_id,
                UserBooksRead.book_id == book.book_id
            ).first() is not None

            rating = db.query(BookRating).filter(
                BookRating.user_id == user_id,
                BookRating.book_id == book.book_id
            ).first()

            if rating:
                user_rating = rating.stars

        # Create response object
        book_data = BookWithUserData(
            book_id=book.book_id,
            title=book.title,
            author=book.author,
            release_year=book.release_year,
            summary=book.summary,
            bookmark_price=book.bookmark_price,
            cover_image=book.cover_image,
            pdf_url=book.pdf_url,
            is_purchased=is_purchased,
            user_rating=user_rating,
            average_rating=float(avg_rating) if avg_rating else None,
            total_ratings=total_ratings or 0
        )

        result.append(book_data)

    return result


@router.get("/{book_id}", response_model=BookWithUserData)
def get_book_by_id(
    book_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Get detailed information about a specific book.

    - **book_id**: The ID of the book
    - Returns book details with user-specific data if authenticated
    """
    user_id = get_current_user_id(request)

    # Get book
    book = db.query(Book).filter(Book.book_id == book_id).first()

    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )

    # Calculate average rating
    avg_rating = db.query(func.avg(BookRating.stars)).filter(
        BookRating.book_id == book_id
    ).scalar()

    total_ratings = db.query(func.count(BookRating.stars)).filter(
        BookRating.book_id == book_id
    ).scalar()

    # Check if user has purchased this book
    is_purchased = False
    user_rating = None

    if user_id:
        is_purchased = db.query(UserBooksRead).filter(
            UserBooksRead.user_id == user_id,
            UserBooksRead.book_id == book_id
        ).first() is not None

        rating = db.query(BookRating).filter(
            BookRating.user_id == user_id,
            BookRating.book_id == book_id
        ).first()

        if rating:
            user_rating = rating.stars

    return BookWithUserData(
        book_id=book.book_id,
        title=book.title,
        author=book.author,
        release_year=book.release_year,
        summary=book.summary,
        bookmark_price=book.bookmark_price,
        cover_image=book.cover_image,
        pdf_url=book.pdf_url,
        is_purchased=is_purchased,
        user_rating=user_rating,
        average_rating=float(avg_rating) if avg_rating else None,
        total_ratings=total_ratings or 0
    )


@router.post("/{book_id}/purchase", response_model=MessageResponse)
def purchase_book(
    book_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Purchase/bookmark a book. Requires authentication.

    - **book_id**: The ID of the book to purchase
    - Deducts bookmark_price from user's bookmark_count
    - Adds book to user's library
    """
    user_id = require_auth(request)

    # Check if book exists
    book = db.query(Book).filter(Book.book_id == book_id).first()
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )

    # Check if user already owns this book
    already_purchased = db.query(UserBooksRead).filter(
        UserBooksRead.user_id == user_id,
        UserBooksRead.book_id == book_id
    ).first()

    if already_purchased:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You already own this book"
        )

    # Get user
    user = db.query(User).filter(User.user_id == user_id).first()

    # Check if user has enough bookmarks
    if user.bookmark_count < book.bookmark_price:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Insufficient bookmarks. You have {user.bookmark_count}, need {book.bookmark_price}"
        )

    # Deduct bookmarks
    user.bookmark_count -= book.bookmark_price

    # Add book to user's library
    user_book = UserBooksRead(user_id=user_id, book_id=book_id)
    db.add(user_book)

    db.commit()

    return {"message": f"Successfully purchased '{book.title}'"}


@router.post("/{book_id}/rate", response_model=RatingResponse)
def rate_book(
    book_id: int,
    rating_data: RatingCreate,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Rate a book (1-5 stars). Requires authentication.

    - **book_id**: The ID of the book to rate
    - **stars**: Rating from 1 to 5
    - Creates new rating or updates existing one
    """
    user_id = require_auth(request)

    # Check if book exists
    book = db.query(Book).filter(Book.book_id == book_id).first()
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )

    # Check if rating already exists
    existing_rating = db.query(BookRating).filter(
        BookRating.user_id == user_id,
        BookRating.book_id == book_id
    ).first()

    if existing_rating:
        # Update existing rating
        existing_rating.stars = rating_data.stars
        db.commit()
        db.refresh(existing_rating)
        return existing_rating
    else:
        # Create new rating
        new_rating = BookRating(
            user_id=user_id,
            book_id=book_id,
            stars=rating_data.stars
        )
        db.add(new_rating)
        db.commit()
        db.refresh(new_rating)
        return new_rating


@router.get("/{book_id}/comments", response_model=List[CommentResponse])
def get_book_comments(
    book_id: int,
    db: Session = Depends(get_db)
):
    """
    Get all comments for a book.

    - **book_id**: The ID of the book
    - Returns list of comments with user names
    """
    # Check if book exists
    book = db.query(Book).filter(Book.book_id == book_id).first()
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )

    # Get comments with user data
    comments = db.query(BookComment, User.name).join(
        User, BookComment.user_id == User.user_id
    ).filter(
        BookComment.book_id == book_id
    ).order_by(BookComment.created_at.desc()).all()

    # Format response
    result = []
    for comment, user_name in comments:
        result.append(CommentResponse(
            comment_id=comment.comment_id,
            book_id=comment.book_id,
            user_id=comment.user_id,
            content=comment.content,
            created_at=comment.created_at,
            user_name=user_name
        ))

    return result


@router.post("/{book_id}/comments", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
def add_book_comment(
    book_id: int,
    comment_data: CommentCreate,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Add a comment to a book. Requires authentication.

    - **book_id**: The ID of the book
    - **content**: The comment text
    """
    user_id = require_auth(request)

    # Check if book exists
    book = db.query(Book).filter(Book.book_id == book_id).first()
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )

    # Get user name for response
    user = db.query(User).filter(User.user_id == user_id).first()

    # Create comment
    new_comment = BookComment(
        book_id=book_id,
        user_id=user_id,
        content=comment_data.content
    )

    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)

    return CommentResponse(
        comment_id=new_comment.comment_id,
        book_id=new_comment.book_id,
        user_id=new_comment.user_id,
        content=new_comment.content,
        created_at=new_comment.created_at,
        user_name=user.name
    )
