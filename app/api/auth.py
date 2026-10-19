from fastapi import APIRouter, Depends, HTTPException, status,Header
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repositories.user_repository import UserRepository
from app.repositories.user_session_repository import UserSessionRepository
from app.schemas.auth import LoginRequest, RegisterRequest 
from app.services.auth_service import AuthService
from app.core.security import decode_access_token
from app.schemas.user import UserProfileResponse
from app.api.dependencies import get_current_user
from app.models.user import User
router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(
    request: RegisterRequest,
    db: Session = Depends(get_db),
):
    repository = UserRepository(db)
    service = AuthService(repository)

    try:
        user = service.register(request)

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )

    return {
        "id": str(user.id),
        "username": user.username,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "is_active": user.is_active,
    }

@router.post("/login")
def login(
    request: LoginRequest,
    db: Session = Depends(get_db),
):
    user_repository = UserRepository(db)
    user_session_repository = UserSessionRepository(db)

    service = AuthService(user_repository)

    try:
        access_token = service.login(
            request=request,
            login_system=request.login_system,
            user_session_repository=user_session_repository,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
        )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }

@router.get("/profile", response_model=UserProfileResponse)
def profile(
    current_user: User = Depends(get_current_user)
):
    return current_user

@router.get("/logout")
def logout(
    token: str = Header(...),
    db: Session = Depends(get_db)
):
    user_session_repository = UserSessionRepository(db)

    payload = decode_access_token(token)

    user_id = payload.get("sub")
    session_id = payload.get("sid")

    user_session_repository.close_session(
        user_id,
        session_id
    )

    return {
        "message": "Logout successful."
    }
