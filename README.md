# Library Management System Documentation

## Table of Contents
1. [Introduction](#introduction)
2. [System Architecture](#system-architecture)
3. [Installation and Setup](#installation-and-setup)
4. [API Documentation](#api-documentation)
5. [Database Schema](#database-schema)
6. [Authentication and Authorization](#authentication-and-authorization)
7. [Error Handling](#error-handling)
8. [Development Guidelines](#development-guidelines)

## Introduction

The Library Management System is a comprehensive Django REST Framework-based solution that facilitates the management of a library's resources. The system enables users to browse, borrow, and return books while allowing administrators to manage the library's collection effectively.

### Key Features

The system provides several core functionalities:

- User authentication and role-based access control
- Complete book inventory management
- Automated book borrowing and returning system
- Fine calculation for overdue books
- Comprehensive API documentation
- Containerized deployment with Docker

### Technology Stack

- Backend Framework: Django / Django REST Framework
- Authentication: JWT (djangorestframework-simplejwt)
- Database: PostgreSQL 16
- API Documentation: drf-spectacular
- Containerization: Docker & Docker Compose
- Development Tools: Python 3.12, Git

## System Architecture

The system follows a modular architecture with four main applications:

1. Authentication (apps.authentication)
   - Handles user management and authentication
   - Implements role-based access control
   - Manages JWT token generation and validation

2. Books (apps.books)
   - Manages the library's book inventory
   - Handles CRUD operations for books
   - Tracks book availability

3. Circulation (apps.circulation)
   - Manages book borrowing and returning
   - Implements borrowing limits
   - Handles due date calculations

4. Fines (apps.fines)
   - Calculates overdue fines
   - Manages fine payments
   - Tracks fine history

## Installation and Setup

### Prerequisites

- Docker and Docker Compose
- Git

### Installation Steps

1. Clone the repository:
```bash
git clone <repository-url>
cd library-management-system
```

2. Create .env file:
```bash
cp .env.example .env
```

3. Build and start the containers:
```bash
docker-compose up --build
```

4. Run migrations:
```bash
docker-compose exec web python manage.py migrate
```

5. Create superuser:
```bash
docker-compose exec web python manage.py createsuperuser
```

## API Documentation

### Authentication Endpoints

#### Register New User
```http
POST /api/auth/register/
```

Request Body:
```json
{
    "username": "string",
    "password": "string",
    "email": "string",
    "role": "MEMBER"
}
```

Response (201 Created):
```json
{
    "id": "integer",
    "username": "string",
    "email": "string",
    "role": "string"
}
```

#### User Login
```http
POST /api/auth/login/
```

Request Body:
```json
{
    "username": "string",
    "password": "string"
}
```

Response (200 OK):
```json
{
    "access": "string",
    "refresh": "string"
}
```

### Book Management Endpoints

#### List All Books
```http
GET /api/books/
```

Response (200 OK):
```json
[
    {
        "id": "integer",
        "title": "string",
        "author": "string",
        "isbn": "string",
        "quantity": "integer",
        "available_quantity": "integer"
    }
]
```

#### Create New Book (Admin Only)
```http
POST /api/books/
```

Request Body:
```json
{
    "title": "string",
    "author": "string",
    "isbn": "string",
    "quantity": "integer"
}
```

### Circulation Endpoints

#### Borrow Book
```http
POST /api/circulation/borrow/
```

Request Body:
```json
{
    "book": "integer"
}
```

Response (201 Created):
```json
{
    "id": "integer",
    "book": "integer",
    "borrowed_date": "datetime",
    "due_date": "datetime",
    "status": "string"
}
```

#### Return Book
```http
PUT /api/circulation/return/{loan_id}/
```

Response (200 OK):
```json
{
    "id": "integer",
    "book": "integer",
    "returned_date": "datetime",
    "status": "RETURNED"
}
```

### Fines Endpoints

#### View User Fines
```http
GET /api/fines/my-fines/
```

Response (200 OK):
```json
[
    {
        "id": "integer",
        "loan": "integer",
        "amount": "decimal",
        "paid": "boolean",
        "created_at": "datetime"
    }
]
```

## Database Schema

### User Model
```python
class User(AbstractUser):
    role = models.CharField(max_length=10, choices=[
        ('ADMIN', 'Admin'),
        ('MEMBER', 'Member')
    ])
```

### Book Model
```python
class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    isbn = models.CharField(max_length=13, unique=True)
    quantity = models.IntegerField(default=1)
    available_quantity = models.IntegerField(default=1)
```

### BookLoan Model
```python
class BookLoan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrowed_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    returned_date = models.DateTimeField(null=True)
    status = models.CharField(max_length=20)
```

## Authentication and Authorization

The system uses JWT (JSON Web Tokens) for authentication. Each token has:
- Access Token validity: 1 hour
- Refresh Token validity: 1 day

### Role-Based Access Control

Two user roles are implemented:
1. Admin: Full access to all system features
2. Member: Limited access to borrowing-related features

## Error Handling

The system implements comprehensive error handling:

1. Authentication Errors (401):
   - Invalid credentials
   - Expired tokens
   - Missing authentication

2. Permission Errors (403):
   - Insufficient privileges
   - Role-based access violations

3. Business Logic Errors (400):
   - Borrowing limit exceeded
   - Book unavailability
   - Invalid operations

## Development Guidelines

### Code Style

- Follow PEP 8 standards for Python code
- Use meaningful variable and function names
- Include docstrings for all classes and methods
- Write comprehensive unit tests

### Git Workflow

1. Create feature branches from development
2. Use meaningful commit messages
3. Submit pull requests for review
4. Merge only after CI passes and review approval

### Testing

Run tests using:
```bash
docker-compose exec web python manage.py test
```

### API Documentation Access

The API documentation is available at:
- Swagger UI: http://localhost:8000/api/docs/
- ReDoc: http://localhost:8000/api/redoc/
- OpenAPI Schema: http://localhost:8000/api/schema/

### Environment Variables

Required environment variables:
- DJANGO_SECRET_KEY
- DJANGO_ALLOWED_HOSTS
- DATABASE_URL
- POSTGRES_DB
- POSTGRES_USER
- POSTGRES_PASSWORD
