# Testing Authentication Endpoints

Use these examples to test the authentication system using the interactive API docs.

## Setup

1. Make sure your server is running:
   ```bash
   uvicorn main:app --reload
   ```

2. Open the API docs in your browser:
   ```
   http://127.0.0.1:8000/docs
   ```

## Test Sequence

### 1. Register a New User

**Endpoint:** `POST /api/auth/register`

Click "Try it out" and use this example:

```json
{
  "name": "Test User",
  "email": "test@example.com",
  "password": "password123"
}
```

**Expected Response (201 Created):**
```json
{
  "user_id": 1,
  "name": "Test User",
  "email": "test@example.com",
  "bookmark_count": 0
}
```

Note: Password is NOT returned (security!)

---

### 2. Get Current User

**Endpoint:** `GET /api/auth/me`

Click "Try it out" and execute.

**Expected Response (200 OK):**
```json
{
  "user_id": 1,
  "name": "Test User",
  "email": "test@example.com",
  "bookmark_count": 0
}
```

This confirms you're logged in from the registration.

---

### 3. Logout

**Endpoint:** `POST /api/auth/logout`

Click "Try it out" and execute.

**Expected Response (200 OK):**
```json
{
  "message": "Logged out successfully"
}
```

---

### 4. Try Getting Current User Again

**Endpoint:** `GET /api/auth/me`

Click "Try it out" and execute.

**Expected Response (401 Unauthorized):**
```json
{
  "detail": "Not authenticated"
}
```

This confirms logout worked!

---

### 5. Login

**Endpoint:** `POST /api/auth/login`

Click "Try it out" and use:

```json
{
  "email": "test@example.com",
  "password": "password123"
}
```

**Expected Response (200 OK):**
```json
{
  "user_id": 1,
  "name": "Test User",
  "email": "test@example.com",
  "bookmark_count": 0
}
```

---

### 6. Test Wrong Password

**Endpoint:** `POST /api/auth/login`

Use wrong password:

```json
{
  "email": "test@example.com",
  "password": "wrongpassword"
}
```

**Expected Response (401 Unauthorized):**
```json
{
  "detail": "Invalid email or password"
}
```

---

## Common Issues

**Issue:** "Not authenticated" errors
**Solution:** Sessions are browser-based. Make sure you're testing in the same browser tab sequentially.

**Issue:** "Email already registered"
**Solution:** Either use a different email or check your database - the user was already created.

**Issue:** Server errors (500)
**Solution:** Check the terminal where uvicorn is running for error details.
