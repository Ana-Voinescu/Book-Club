# Book Club Backend Server

FastAPI backend for the Book Club application.

## Setup Instructions

### 1. Create Virtual Environment

Open a terminal in the project root directory and run:

```bash
python -m venv venv
```

### 2. Activate Virtual Environment

**Windows:**
```bash
venv\Scripts\activate
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

You should see `(venv)` at the beginning of your terminal prompt.

### 3. Install Dependencies

```bash
cd server
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Copy the example environment file:

```bash
copy .env.example .env    # Windows
cp .env.example .env      # Mac/Linux
```

Edit `.env` and update the `SECRET_KEY` to a random string.

### 5. Run the Server

From the `server` directory:

```bash
uvicorn main:app --reload
```

The API will be available at: `http://127.0.0.1:8000`

### 6. View API Documentation

Once the server is running, visit:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Project Structure

```
server/
├── main.py           # FastAPI application entry point
├── models.py         # SQLAlchemy database models
├── database.py       # Database connection and session
├── config.py         # Configuration settings
├── schemas.py        # Pydantic schemas for request/response validation
├── auth.py           # Authentication utilities
├── requirements.txt  # Python dependencies
├── .env              # Environment variables (not committed)
├── .env.example      # Example environment variables
└── README.md         # This file
```

## Next Steps

After setup, we'll create:
1. Database models (models.py)
2. Database connection (database.py)
3. Configuration (config.py)
4. Main application (main.py)
5. Authentication system
6. API endpoints for books, groups, users
