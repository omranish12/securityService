# Auth Service

A backend authentication service built with FastAPI and PostgreSQL. It provides user registration, login with JWT access tokens, authenticated user profile retrieval, and session-aware logout.

## Features

- User registration with user information
- Login with access token issuance
- JWT-based authentication
- Authenticated user profile endpoint
- User session tracking during login
- Session closure during logout
- Password hashing using Argon2id
- PostgreSQL database integration

## Tech Stack

- **Language:** Python
- **Framework:** FastAPI
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy
- **Authentication:** JWT access tokens
- **Password Hashing:** Argon2id
- **API Documentation:** Swagger UI / OpenAPI
- **Testing:** pytest

## Project Structure

```text
auth_service/
├── app/
│   ├── api/
│   │   ├── auth.py
│   │   ├── dependencies.py
│   │   └── router.py
│   ├── core/
│   │   ├── config.py
│   │   ├── exceptions.py
│   │   └── security.py
│   ├── db/
│   │   ├── base.py
│   │   └── session.py
│   ├── models/
│   │   ├── user.py
│   │   └── user_sessions.py
│   ├── repositories/
│   │   ├── user_repository.py
│   │   └── user_session_repository.py
│   ├── schemas/
│   │   ├── auth.py
│   │   └── user.py
│   ├── services/
│   │   └── auth_service.py
│   └── main.py
├── tests/
│   └── test_auth.py
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/omranish12/securityService.git
cd securityService
```

### 2. Create a Virtual Environment

Windows:

```cmd
python -m venv .venv
.venv\Scripts\activate
```

Linux / macOS:

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file based on `.env.example` and configure the required database connection and authentication settings.

Never commit the real `.env` file or expose database credentials and token-signing secrets.

### 5. Configure PostgreSQL

Create a PostgreSQL database and configure the connection string according to the environment variables expected by the application.

Ensure that the required database tables and schema are created before using the API.

### 6. Run the Application

```bash
uvicorn app.main:app --reload
```

The API documentation is available at:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## API Endpoints

All authentication endpoints use the `/auth` prefix, except for the profile endpoint.

### 1. Register a User

`POST /auth/register`

Registers a new user.

Example request:

```json
{
  "username": "shadi",
  "email": "shadi@example.com",
  "password": "StrongPassword123",
  "first_name": "Shadi",
  "last_name": "Omrani"
}
```

The exact request fields depend on `RegisterRequest`.

**Success response:** `201 Created`

```json
{
  "id": "user-id",
  "username": "shadi",
  "email": "shadi@example.com",
  "first_name": "Shadi",
  "last_name": "Omrani",
  "is_active": true
}
```

A registration validation error is returned with `400 Bad Request`.

### 2. Login

`POST /auth/login`

Authenticates a user and issues an access token. The request also includes the `login_system` information defined by `LoginRequest`.

Example response:

```json
{
  "access_token": "<access-token>",
  "token_type": "bearer"
}
```

Invalid credentials or login errors represented by `ValueError` return `401 Unauthorized`.

### 3. Get User Profile

`GET /profile`

Returns the profile of the authenticated user.

Authentication is handled through the `get_current_user` dependency.

The exact authentication header format depends on the implementation of `get_current_user`.

### 4. Logout

`GET /auth/logout`

Closes the session associated with the provided access token.

The current implementation expects a request header named `token`:

```http
token: <access-token>
```

A successful response:

```json
{
  "message": "Logout successful."
}
```

> **Implementation note:** Consider changing logout to `POST /auth/logout` and using the standard `Authorization: Bearer <token>` header. Also ensure invalid or expired tokens are handled safely.

## Testing

Run the test suite with:

```bash
pytest
```

The available automated tests are located in the `tests/` directory.

## Security Considerations

- Passwords should be stored as secure hashes, not plaintext.
- JWT signing secrets and database credentials should be provided through environment variables.
- Access tokens should have a defined expiration time.
- Protected endpoints must validate the token before accessing user data.
- Logout should invalidate or close the associated session according to the application's session-management design.
- Sensitive values must never be committed to the repository.

## Potential Improvements

- Refresh-token support
- Rate limiting for login attempts
- Email verification and password reset
- Role-based access control
- Database migrations
- Docker-based development setup
- Improved token revocation and logout semantics

## Author

**Shadi Omrani**  
Backend Software Engineer
