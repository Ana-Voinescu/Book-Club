"""
SQLAlchemy models representing the database tables.
These classes map to the existing tables in bookclub.db.
"""

from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, CheckConstraint
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime


class User(Base):
    """
    Users table - stores user account information.
    """
    __tablename__ = "Users"

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False)
    email = Column(Text, nullable=False, unique=True)
    password_hash = Column(Text, nullable=False)
    bookmark_count = Column(Integer, nullable=False, default=0)

    # Relationships
    ratings = relationship("BookRating", back_populates="user")
    comments = relationship("BookComment", back_populates="user")
    books_read = relationship("UserBooksRead", back_populates="user")
    groups = relationship("UserGroup", back_populates="user")
    posts = relationship("GroupPost", back_populates="user")


class Book(Base):
    """
    Books table - stores book information.
    """
    __tablename__ = "Books"

    book_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(Text, nullable=False)
    author = Column(Text, nullable=False)
    release_year = Column(Integer)
    summary = Column(Text)
    bookmark_price = Column(Integer, nullable=False, default=0)
    cover_image = Column(Text)
    pdf_url = Column(Text)

    # Relationships
    ratings = relationship("BookRating", back_populates="book")
    comments = relationship("BookComment", back_populates="book")
    users_read = relationship("UserBooksRead", back_populates="book")
    groups = relationship("Group", back_populates="current_book")
    group_history = relationship("GroupReadingHistory", back_populates="book")
    posts = relationship("GroupPost", back_populates="book")


class Group(Base):
    """
    Groups table - stores reading group information.
    """
    __tablename__ = "Groups"

    group_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False)
    cover_image = Column(Text)
    current_book_id = Column(Integer, ForeignKey("Books.book_id"))
    created_at = Column(Text, nullable=False, default=lambda: datetime.utcnow().isoformat())

    # Relationships
    current_book = relationship("Book", back_populates="groups")
    members = relationship("UserGroup", back_populates="group")
    reading_history = relationship("GroupReadingHistory", back_populates="group")
    posts = relationship("GroupPost", back_populates="group")


class BookRating(Base):
    """
    BookRatings table - stores user ratings for books.
    """
    __tablename__ = "BookRatings"

    user_id = Column(Integer, ForeignKey("Users.user_id"), primary_key=True)
    book_id = Column(Integer, ForeignKey("Books.book_id"), primary_key=True)
    stars = Column(Integer, nullable=False)

    # Check constraint: stars must be between 1 and 5
    __table_args__ = (
        CheckConstraint('stars BETWEEN 1 AND 5', name='check_stars_range'),
    )

    # Relationships
    user = relationship("User", back_populates="ratings")
    book = relationship("Book", back_populates="ratings")


class BookComment(Base):
    """
    BookComments table - stores user comments on books.
    """
    __tablename__ = "BookComments"

    comment_id = Column(Integer, primary_key=True, autoincrement=True)
    book_id = Column(Integer, ForeignKey("Books.book_id"), nullable=False)
    user_id = Column(Integer, ForeignKey("Users.user_id"), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    book = relationship("Book", back_populates="comments")
    user = relationship("User", back_populates="comments")


class UserBooksRead(Base):
    """
    UserBooksRead table - tracks which books users have purchased/read.
    """
    __tablename__ = "UserBooksRead"

    user_id = Column(Integer, ForeignKey("Users.user_id"), primary_key=True)
    book_id = Column(Integer, ForeignKey("Books.book_id"), primary_key=True)

    # Relationships
    user = relationship("User", back_populates="books_read")
    book = relationship("Book", back_populates="users_read")


class UserGroup(Base):
    """
    UserGroups table - tracks which users are members of which groups.
    """
    __tablename__ = "UserGroups"

    user_id = Column(Integer, ForeignKey("Users.user_id"), primary_key=True)
    group_id = Column(Integer, ForeignKey("Groups.group_id"), primary_key=True)

    # Relationships
    user = relationship("User", back_populates="groups")
    group = relationship("Group", back_populates="members")


class GroupReadingHistory(Base):
    """
    GroupReadingHistory table - tracks books that groups have read.
    """
    __tablename__ = "GroupReadingHistory"

    group_id = Column(Integer, ForeignKey("Groups.group_id"), primary_key=True)
    book_id = Column(Integer, ForeignKey("Books.book_id"), primary_key=True)

    # Relationships
    group = relationship("Group", back_populates="reading_history")
    book = relationship("Book", back_populates="group_history")


class GroupPost(Base):
    """
    GroupPosts table - stores discussion posts within groups.
    """
    __tablename__ = "GroupPosts"

    post_id = Column(Integer, primary_key=True, autoincrement=True)
    group_id = Column(Integer, ForeignKey("Groups.group_id"), nullable=False)
    book_id = Column(Integer, ForeignKey("Books.book_id"))
    user_id = Column(Integer, ForeignKey("Users.user_id"), nullable=False)
    content = Column(Text, nullable=False)

    # Relationships
    group = relationship("Group", back_populates="posts")
    book = relationship("Book", back_populates="posts")
    user = relationship("User", back_populates="posts")
