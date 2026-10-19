from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.user_sessions import UserSession
from datetime import datetime, timezone


class UserSessionRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, session: UserSession) -> UserSession:
        self.db.add(session)
        self.db.flush()
        return session
    

    def close_session(self, user_id, session_id) -> UserSession | None:

        session = self.db.get(
            UserSession,
            session_id
        )

        if session is None:
            return None

        session.login_state = "LOGOUT"
        session.logout_at = datetime.now(timezone.utc)
        session.last_activity_at = datetime.now(timezone.utc)

        self.db.commit()

        return session
    
    def get_active_session(self, user_id, session_id):
        
        statement = select(UserSession).where(
            UserSession.nid_session == session_id,
            UserSession.nid_user == user_id,
            UserSession.login_state == "LOGIN"
        )

        return self.db.scalar(statement)