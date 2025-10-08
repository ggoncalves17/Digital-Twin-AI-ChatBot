"""
User-related data models for the digital twin API.
"""

from pydantic import BaseModel, Field, field_validator, EmailStr
from typing import List, Optional
from datetime import date, datetime, timezone
from enum import Enum
import re
from .base import TimestampedModel

class User(TimestampedModel):
    """Main User model."""
    
    # Personal Information
    id: int = Field(..., description="Unique user ID")
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    date_of_birth: Optional[date] = None
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=100)
    
    # Account metrics
    total_messages: int = Field(default=0, ge=0)
    
    @field_validator('first_name', 'last_name')
    @classmethod
    def validate_names(cls, v: str) -> str:
        """Validate name fields."""
        v = v.strip()
        if not v:
            raise ValueError("Name cannot be empty")
        
        # Allow letters, spaces, hyphens, and apostrophes
        if not re.match(r"^[a-zA-Z\s'-]+$", v):
            raise ValueError("Name contains invalid characters")
        
        return v.title()  # Capitalize properly
    
    @field_validator('date_of_birth')
    @classmethod
    def validate_date_of_birth(cls, v: Optional[date]) -> Optional[date]:
        """Validate date of birth."""
        if v is None:
            return v
        
        today = date.today()
        age = today.year - v.year - ((today.month, today.day) < (v.month, v.day))
        
        if age < 13:
            raise ValueError("User must be at least 13 years old")
        if age > 120:
            raise ValueError("Invalid date of birth")
        
        return v
    
    @property
    def full_name(self) -> str:
        """Get User's full name."""
        return f"{self.first_name} {self.last_name}"
    
    @property
    def age(self) -> Optional[int]:
        """Calculate User's age."""
        if not self.date_of_birth:
            return None
        
        today = date.today()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )
    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "first_name": "John",
                "last_name": "Doe",
                "date_of_birth": "1990-01-01",
                "preferences": {
                    "persona": "none",
                    "language": "en",
                    "timezone": "UTC"
                },
                "total_messages": 42,
                "email_verified": True,
                "phone_verified": False,
                "identity_verified": False
            }
        }

class UserRegistration(BaseModel):
    """User registration request model."""
    
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=100)
    date_of_birth: Optional[date] = None
    total_messages: int = Field(default=0, ge=0)
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        """Validate password strength."""
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        
        checks = [
            (r'[a-z]', "Password must contain lowercase letters"),
            (r'[A-Z]', "Password must contain uppercase letters"), 
            (r'\d', "Password must contain numbers"),
            (r'[!@#$%^&*(),.?":{}|<>]', "Password must contain special characters")
        ]
        
        for pattern, message in checks:
            if not re.search(pattern, v):
                raise ValueError(message)
        
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "first_name": "John",
                "last_name": "Doe",
                "email": "johndoe@email.com",
                "password": "StrongP@ssw0rd!",
                "date_of_birth": "1990-01-01",
            }
        }

class UserLogin(BaseModel):
    """User login request model."""
    
    email: EmailStr
    password: str = Field(..., min_length=1)
    # remember_me: bool = False
    class Config:
        json_schema_extra = {
            "example": {
                "email": "johndoe@email.com",
                "password": "StrongP@ssw0rd!",
                # "remember_me": False
            }
        }

class UserListResponse(BaseModel):
    """Response model for user list with pagination."""
    users: List[User]
    total: int = Field(..., description="Total number of users")
    page: int = Field(..., description="Current page number")
    limit: int = Field(..., description="Items per page")
    has_next: bool = Field(..., description="Whether there are more pages")
    
    class Config:
        json_schema_extra = {
            "example": {
                "users": [
                    {
                        "id": 1,
                        "first_name": "John",
                        "last_name": "Doe",
                        "phone": "+1234567890",
                        "date_of_birth": "1990-01-01",
                        "preferences": {
                            "persona": "none",
                            "language": "en",
                            "timezone": "UTC"
                        }
                    }
                ],
                "total": 25,
                "page": 1,
                "limit": 10,
                "has_next": True
            }
        }

class ErrorResponse(BaseModel):
    """Standard error response model."""
    
    detail: str = Field(..., description="Error message")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), description="Error timestamp")
    class Config:
        json_schema_extra = {
            "example": {
                "detail": "User not found",
                "timestamp": "2023-10-01T12:00:00Z"
            }
        }