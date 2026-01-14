"""
Database connection and session management.
Sets up SQLAlchemy to work with the existing SQLite database.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import settings

# Create database engine
# check_same_thread=False is needed for SQLite to work with FastAPI
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Create a SessionLocal class for database sessions
# Each request will use its own session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all database models
Base = declarative_base()


def get_db():
    """
    Dependency function to get database session.

    Usage in FastAPI:
        @app.get("/example")
        def example(db: Session = Depends(get_db)):
            # use db here
            pass

    This ensures:
    - Each request gets its own database session
    - Session is properly closed after the request
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
