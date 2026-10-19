from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    username: str = Field(
        min_length=3,
        max_length=100,
    )

    email: EmailStr | None = None

    password: str = Field(
        min_length=8,
        max_length=128,
    )

    first_name: str | None = Field(
        default=None,
        max_length=100,
    )

    last_name: str | None = Field(
        default=None,
        max_length=100,
    )
    
class LoginRequest(BaseModel):
    username: str
    password: str
    login_system: str

class ProfileRequest():
    token:str