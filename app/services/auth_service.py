from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)
from app.models.user import User
from app.models.user_sessions import UserSession
from app.repositories.user_repository import UserRepository
from app.repositories.user_session_repository import UserSessionRepository
from app.schemas.auth import LoginRequest, RegisterRequest


class AuthService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def register(self, request: RegisterRequest) -> User:
        existing_user = self.user_repository.get_by_username(
            request.username
        )

        if existing_user is not None:
            raise ValueError("Username already exists.")

        if request.email is not None:
            existing_email = self.user_repository.get_by_email(
                request.email
            )

            if existing_email is not None:
                raise ValueError("Email already exists.")

        user = User(
            username=request.username,
            email=request.email,
            password_hash=hash_password(request.password),
            first_name=request.first_name,
            last_name=request.last_name,
        )

        return self.user_repository.create(user)

    def login(
        self,
        request: LoginRequest,
        login_system: str,
        user_session_repository: UserSessionRepository,
    ) -> str:

        user = self.user_repository.get_by_username(
            request.username
        )
        login_system=request.login_system

        if user is None:
            raise ValueError("Invalid username or password.")

        if not user.is_active:
            raise ValueError("User account is inactive.")

        if user.is_locked:
            raise ValueError("User account is locked.")

        if not verify_password(
            request.password,
            user.password_hash,
        ):
            raise ValueError("Invalid username or password.")

        # Update last successful login time
        self.user_repository.update_last_login(user)

        # Create a new login session
        session = UserSession(
            nid_user=user.id,
            login_state="LOGIN",
            login_system=login_system,
        )

        user_session_repository.create(session)

        # Create JWT
        access_token = create_access_token(
            str(user.id),
            session.nid_session
        )

        # Commit all login changes in one transaction
        self.user_repository.db.commit()

        return access_token