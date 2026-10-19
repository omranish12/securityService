from fastapi import Header, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.security import decode_access_token
from app.repositories.user_repository import UserRepository
from app.repositories.user_session_repository import UserSessionRepository

 
def get_current_user(
    token: str = Header(...),
    db: Session = Depends(get_db)
):
    try:
        payload = decode_access_token(token)

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )
    user_id = payload.get("sub")
    session_id = payload.get("sid")

    if not user_id or not session_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token."
        )
    user_repository = UserRepository(db)
    user = user_repository.get_by_id(user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found."
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User account is inactive."
        )
    user_session_repository = UserSessionRepository(db)

    session = user_session_repository.get_active_session(
        user_id,
        int(session_id)
    )

    if session is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session is no longer active."
        )
    return user