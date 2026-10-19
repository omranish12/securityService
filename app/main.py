from fastapi import Depends, FastAPI
from sqlalchemy import inspect, text
from sqlalchemy.orm import Session

from app.api.router import api_router
from app.db.session import engine, get_db
from app.models.user import User
from app.repositories.user_repository import UserRepository


app = FastAPI(
    title="AquaSky Auth Service",
    version="1.0.0",
)


app.include_router(api_router)


@app.get("/health")
def health_check():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))

    return {
        "status": "ok",
        "database": "connected",
        "result": result.scalar(),
    }


@app.get("/test/user-model")
def test_user_model():
    inspector = inspect(engine)

    tables = inspector.get_table_names(
        schema="security"
    )

    return {
        "model_table": User.__tablename__,
        "model_schema": User.__table_args__["schema"],
        "database_table_exists": "users" in tables,
    }


@app.get("/test/user")
def test_get_user(
    username: str,
    db: Session = Depends(get_db),
):
    repository = UserRepository(db)

    user = repository.get_by_username(username)

    if user is None:
        return {
            "found": False,
            "message": "User not found",
        }

    return {
        "found": True,
        "id": str(user.id),
        "username": user.username,
        "email": user.email,
        "is_active": user.is_active,
        "is_locked": user.is_locked,
    }