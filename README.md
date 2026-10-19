# Auth Service

A small authentication service that stores users in PostgreSQL and provides user registration, login with token issuance, and password change.

> **Before publishing:** replace every `TODO` below with the real value from your code, and delete any feature or endpoint your service does not actually have.

## Features

- User registration (users stored in PostgreSQL)
- Login that returns an access token
- Password change for an authenticated user
- TODO: password hashing algorithm (e.g. bcrypt / argon2)
- TODO: token type and expiry (e.g. JWT, 60 minutes)

## Tech Stack

- Python, TODO: framework (e.g. FastAPI)
- PostgreSQL
- TODO: ORM / DB driver (e.g. SQLAlchemy, psycopg2)
- TODO: testing tool (e.g. pytest)

## Project Structure

```
auth-service/
├── app/            # application code (TODO: adjust to your layout)
├── tests/          # automated tests
├── .env.example    # example configuration (no real secrets)
├── .gitignore
├── requirements.txt
└── README.md
```

## Getting Started

### 1. Clone and install

```bash
git clone https://github.com/USERNAME/auth-service.git
cd auth-service
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure

Copy the example file and fill in your own values:

```bash
cp .env.example .env
```

Example `.env.example` (TODO: match the variable names your code reads):

```
DATABASE_URL=postgresql://USER:PASSWORD@localhost:5432/auth_db
SECRET_KEY=change-me
TOKEN_EXPIRE_MINUTES=60
```

Never commit the real `.env` file.

### 3. Create the database

```bash
createdb auth_db
```

TODO: describe how tables are created (migrations, or automatically on startup).

### 4. Run

```bash
# TODO: replace with your real start command, for example:
uvicorn app.main:app --reload
```

## API

TODO: adjust paths, field names and status codes to match your code.

### Register

`POST /auth/register`

```json
{
  "email": "user@example.com",
  "password": "StrongPassword123"
}
```

Response `201 Created`:

```json
{
  "id": 1,
  "email": "user@example.com"
}
```

### Login

`POST /auth/login`

```json
{
  "email": "user@example.com",
  "password": "StrongPassword123"
}
```

Response `200 OK`:

```json
{
  "access_token": "<token>",
  "token_type": "bearer"
}
```

Wrong credentials return `401 Unauthorized`.

### Change password

`POST /auth/change-password`

Header: `Authorization: Bearer <token>`

```json
{
  "old_password": "StrongPassword123",
  "new_password": "EvenStrongerPassword456"
}
```

Response `200 OK`.

## Tests

```bash
pytest
```

TODO: list what the tests cover (successful login, wrong password, duplicate user, password change).

## Security Notes

- Passwords are stored only as hashes, never as plain text. (TODO: confirm)
- The token signing key is read from the environment, not from the source code. (TODO: confirm)
- Passwords are never returned in responses or written to logs. (TODO: confirm)

## Possible Improvements

- Refresh tokens
- Rate limiting on login
- Email verification and password reset
- Dockerfile and docker-compose for one-command setup

## Author

Shadi Omrani, Backend Software Engineer