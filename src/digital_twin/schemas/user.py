"""
User data models
"""

import re
from datetime import date
from typing import Annotated, ClassVar, Optional

from pydantic import AfterValidator, BaseModel, ConfigDict, EmailStr, Field


def validate_birthdate(v: date) -> date:
    if date.today() < v:
        raise ValueError("Birthdate cannot be in the future.")
    return v


def validate_password(v):
    if not re.search(r"[A-Z]", v):
        raise ValueError("Password must contain at least one uppercase letter")
    if not re.search(r"[a-z]", v):
        raise ValueError("Password must contain at least one lowercase letter")
    if not re.search(r"\d", v):
        raise ValueError("Password must contain at least one digit")
    return v


class UserBase(BaseModel):
    """Base User schema."""

    name: str = Field(min_length=1, max_length=100, description="User's name")
    birthdate: Annotated[date, AfterValidator(validate_birthdate)] = Field(
        description="User's birthdate"
    )
    email: EmailStr


class UserCreate(UserBase):
    """User creation schema."""

    password: Annotated[str, AfterValidator(validate_password)] = Field(
        min_length=8, description="User's Password"
    )


class UserUpdate(BaseModel):
    """User update schema."""

    name: Optional[str] = Field(min_length=1, max_length=100, description="User's name")


class User(UserBase):
    """User response schema."""

    id: Annotated[int, Field(description="Unique User ID")]

    model_config: ClassVar[ConfigDict] = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "name": "John Doe",
                "birthdate": "2000-01-31",
                "email": "john.doe@gmail.com",
            }
        },
    )
