# Notes API 

A small CRUD REST API for managing user-owned notes with JWT authentication, role-based authorization, ownership-based access control, SQLAlchemy ORM, PostgreSQL database, and Alembic migrations.

## Features

* JWT based authentication
* Password hashing
* User registration/login
* Role-based authorization (user/admin)
* Ownership-based note access
* CRUD operations for notes
* Category relationship (One-to-Many)
* PostgreSQL database integration
* Alembic database migrations
* API versioning using `/api/v1`

---

## Project Structure

```
Day4project/
│
├── app/
│   ├── main.py                 # FastAPI application entry point
│   ├── database.py             # PostgreSQL connection + SQLAlchemy setup
│   ├── dependencies.py         # Database dependency functions
│   ├── models.py               # SQLAlchemy ORM models (User, Note, Category)
│   ├── schemas.py              # Pydantic request/response schemas
│   ├── oauth2.py               # JWT token creation and verification
│   ├── utils.py                # Password hashing utilities
│   │
│   └── routers/
│       ├── auth.py             # User login/authentication routes
│       ├── notes.py            # Notes CRUD routes
│       ├── categories.py       # Category routes
│       └── admin.py            # Admin-only routes
│
├── alembic/
│   ├── env.py
│   ├── script.py.mako
│   └── versions/               # Database migration files
│
├── alembic.ini                 # Alembic configuration
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
└── .env.example                # Environment variables template
```

---

# Setup Instructions

## 1. Create Virtual Environment

```bash
python3 -m venv venv

source venv/bin/activate
```

## 2. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file inside the project folder:

```
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/notesdb
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

I Don't upload  my`.env` file to GitHub.

Instead i upload this one  `.env.example` 

---

# Database Setup

This project uses PostgreSQL.

Create database:

```bash
sudo -u postgres psql
```

Inside PostgreSQL:

```sql
CREATE DATABASE notesdb;
```

Run migrations:

```bash
alembic upgrade head
```

Check migration status:

```bash
alembic current
```

View migration history:

```bash
alembic history
```

---

# Run Application

Start FastAPI server:

```bash
uvicorn app.main:app --reload
```

API documentation:

```
http://127.0.0.1:8000/docs
```

---

# Test Users

For testing authentication:

| Username | Password | Role  |
| -------- | -------- | ----- |
| Hiba     | 123456    | user  |
| Ali      | 654321   | user  |
| admin    | admin    | admin |

---

# API Endpoints

## Authentication

### Login

```
POST /api/v1/auth/login
```

Returns JWT access token.

---

# Notes API

All note endpoints require JWT authentication.

## Create Note

```
POST /api/v1/notes
```

Creates a note for the logged-in user.

Success:

```
201 Created
```

---

## Get My Notes

```
GET /api/v1/notes
```

Returns only the current user's notes.

---

## Get Single Note

```
GET /api/v1/notes/{id}
```

A user can only access their own notes.

Another user's note returns:

```
404 Not Found
```

---

## Update Note

```
PUT /api/v1/notes/{id}
```

Updates only owned notes.

---

## Delete Note

```
DELETE /api/v1/notes/{id}
```

Deletes only owned notes.

Success:

```
204 No Content
```

---

# Admin Endpoint

## View All Notes

```
GET /api/v1/admin/notes
```

Only users with:

```
role = admin
```

can access this endpoint.

Non-admin users receive:

```
403 Forbidden
```

---

# Database Models

## User

Stores application users.

Fields:

* id
* username
* hashed password
* role

## Note

A note belongs to exactly one user.

Fields:

* id
* title
* body
* owner_id
* category_id
* created_at
* updated_at

## Category

One category can contain multiple notes.

Relationship:

```
User 1 -------- * Note

Category 1 ---- * Note
```

---

# Authentication Flow

1. User logs in with username and password.
2. Server verifies password.
3. JWT token is generated.
4. Token is sent in Authorization header:

```
Authorization: Bearer <token>
```

5. Protected routes verify the token before allowing access.

---

# Git Workflow

Development was completed using Git feature branch workflow.

Branch:

```
feature/notes-api
```

Changes were committed incrementally:

* Database models
* Alembic migrations
* CRUD endpoints
* JWT authentication
* Ownership authorization
* Admin authorization
* PostgreSQL migration

---

# Technologies Used

* Python
* FastAPI
* SQLAlchemy ORM
* PostgreSQL
* Alembic
* Pydantic
* JWT Authentication
* Uvicorn
