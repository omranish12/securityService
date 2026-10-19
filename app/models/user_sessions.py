from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class UserSession(Base):
    __tablename__ = "user_sessions"
    __table_args__ = {"schema": "security"}

    nid_session: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    nid_user: Mapped[str] = mapped_column(
        ForeignKey("security.users.id", ondelete="CASCADE"),
        nullable=False,
    )

    login_state: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="LOGIN",
    )

    login_system: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    last_activity_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    logout_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )