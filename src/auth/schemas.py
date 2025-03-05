from datetime import datetime
import re
from typing import Annotated
import uuid
from pydantic import BaseModel, EmailStr, Field, field_validator


class UserMixin(BaseModel):
    email: EmailStr = Field(..., examples=["john.doe@example.com"])


class PasswordMixin(BaseModel):
    password: str = Field(
        ...,
        min_length=8,
        max_length=32,
        examples=["Password@123"],
        description="Password must be 8-32 characters long.",
    )

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        if not re.search(r"[A-Z]", value):
            raise ValueError("Password must contain at least one uppercase letter.")
        if not re.search(r"[a-z]", value):
            raise ValueError("Password must contain at least one lowercase letter.")
        if not re.search(r"\d", value):
            raise ValueError("Password must contain at least one number.")
        if not re.search(r"[@#$%^&+=!*]", value):
            raise ValueError(
                "Password must contain at least one special character (@#$%^&+=!*)."
            )
        if not re.match(r"^[A-Za-z\d@#$%^&+=!*]+$", value):
            raise ValueError("Password contains invalid characters.")
        return value


class UserRegister(UserMixin, PasswordMixin):
    pass


class UserLogin(UserMixin, PasswordMixin):
    pass


class UserResponse(BaseModel):
    id: uuid.UUID = Field(..., examples=["550e8400-e29b-41d4-a716-446655440000"])
    email: EmailStr = Field(..., examples=["john.doe@example.com"])
    created_at: datetime = Field(..., examples=["2024-02-26T12:34:56.789Z"])
    updated_at: datetime = Field(..., examples=["2024-02-26T12:45:00.123Z"])

    class Config:
        from_attributes = True


class UserRegisterResponse(BaseModel):
    user: UserResponse
    message: str = "User registered successfully"


class UserLoginResponse(BaseModel):
    user: UserResponse
    access_token: str = "<access_token>"
