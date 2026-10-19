from pydantic import BaseModel
from datetime import datetime
from uuid import UUID


class UserProfileResponse(BaseModel):
    id: UUID
    username: str
    email: str | None
    first_name: str | None
    last_name: str | None
    is_active: bool
    is_locked: bool
    created_at: datetime
    last_login_at: datetime | None