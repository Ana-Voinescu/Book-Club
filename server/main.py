"""
Main FastAPI application for Book Club API.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from config import settings
from routes import auth_routes, book_routes

# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG
)

# Add session middleware for authentication
# This allows us to store user sessions
app.add_middleware(
    SessionMiddleware,
    secret_key=settings.SECRET_KEY,
    session_cookie=settings.SESSION_COOKIE_NAME,
    max_age=86400,  # 24 hours in seconds
    same_site="lax",
    https_only=False  # Set to True in production with HTTPS
)

# Configure CORS to allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_allowed_origins(),
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers
)


@app.get("/")
def root():
    """
    Root endpoint - confirms the API is running.
    """
    return {
        "message": "Book Club API is running!",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
def health_check():
    """
    Health check endpoint - useful for monitoring.
    """
    return {"status": "healthy"}


# Include routers
app.include_router(auth_routes.router)
app.include_router(book_routes.router)

# We'll add more routers in the next phases:
# - Groups endpoints
# - User profile endpoints


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
