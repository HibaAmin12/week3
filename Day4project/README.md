# Notes API

A small CRUD REST API for managing user-owned notes with JWT authentication, role-based authorization, ownership-based access control, SQLAlchemy ORM, PostgreSQL database, Alembic migrations, and Dockerized deployment.

## Features

* JWT based authentication
* Password hashing
* User registration/login
* Role-based authorization (user/admin)
* Ownership-based note access control
* CRUD operations for notes
* Category relationship (One-to-Many)
* PostgreSQL database integration
* Alembic database migrations
* API versioning using `/api/v1`
* Docker and Docker Compose setup

---

# Project Structure

```
Day4project/
│
├── app/
│   ├── main.py                 # FastAPI application entry point
│   ├── database.py             # PostgreSQL connection + SQLAlchemy setup
│   ├── dependencies.py         # Database dependency functions
│   ├── models.py               # SQLAlchemy ORM models
│   ├── schemas.py              # Pydantic request/response schemas
│   ├── oauth2.py               # JWT token creation and verification
│   ├── utils.py                # Password hashing utilities
│   │
│   └── routers/
│       ├── auth.py             # Register/login routes
│       ├── notes.py            # Notes CRUD routes
│       ├── categories.py        # Category routes
│       └── admin.py             # Admin-only routes
│
├── alembic/
│   └── versions/               # Database migration files
│
├── Dockerfile                  # API container configuration
├── docker-compose.yml          # FastAPI + PostgreSQL services
├── alembic.ini                 # Alembic configuration
├── requirements.txt            # Python dependencies
├── README.md
└── .env.example
```

---

# Local Setup (Without Docker)

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

The `.env` file contains secrets and is not uploaded to GitHub.

Instead, `.env.example` is provided as a template.

---

# Docker Setup (Recommended)

The project uses Docker Compose to run:

```
FastAPI Container
        |
        |
        ↓
PostgreSQL Container
```

## Start Containers

Build and start the application:

```bash
sudo docker-compose up -d --build
```

Check running containers:

```bash
sudo docker ps
```

Expected:

```
day4project_api_1
day4project_db_1
```

---

## Database Configuration in Docker

Inside Docker, the database host is the PostgreSQL service name, not localhost.

Example:

```
DATABASE_URL=postgresql://postgres:123456@db:5432/notesdb
```

Where:

* postgres = database username
* 123456 = database password
* db = PostgreSQL service name in docker-compose.yml
* 5432 = PostgreSQL port
* notesdb = database name

---

# Database Migration

Run migrations inside API container:

Enter container:

```bash
sudo docker exec -it day4project_api_1 bash
```

Apply migrations:

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

Using Docker:

```
http://127.0.0.1:8000/docs
```

Swagger documentation:

```
http://127.0.0.1:8000/docs
```

---

# API Endpoints

## Authentication

### Register User

```
POST /api/v1/auth/register
```

Creates a new user account.

### Login

```
POST /api/v1/auth/login
```

Returns JWT access token.

---

# Notes API

All note endpoints require JWT authentication.

Token format:

```
Authorization: Bearer <token>
```

## Create Note

```
POST /api/v1/notes
```

Creates a note for the logged-in user.

Response:

```
201 Created
```

## Get My Notes

```
GET /api/v1/notes
```

Returns only notes owned by the current user.

## Get Single Note

```
GET /api/v1/notes/{id}
```

Users can only access their own notes.

Other users' notes return:

```
404 Not Found
```

## Update Note

```
PUT /api/v1/notes/{id}
```

## Delete Note

```
DELETE /api/v1/notes/{id}
```

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
* hashed_password
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

1. User registers an account.
2. Password is hashed using bcrypt.
3. User logs in with username and password.
4. Server verifies credentials.
5. JWT token is generated.
6. Token is sent in request headers:

```
Authorization: Bearer <token>
```

7. Protected routes verify JWT before allowing access.

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
* PostgreSQL integration
* Docker deployment setup

---

# Technologies Used

* Python
* FastAPI
* SQLAlchemy ORM
* PostgreSQL
* Alembic
* Pydantic
* JWT Authentication
* Passlib / bcrypt
* Docker
* Docker Compose
* Uvicorn
