"""
Base model classes and common patterns for the digital twin API.
"""

from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime, timezone
from typing import Optional, Dict, Any
from uuid import UUID, uuid4

class TimestampedModel(BaseModel):
    """Base model with automatic timestamp fields."""
    
    model_config = ConfigDict(
        # Enable validation on assignment
        validate_assignment=True,
        # Use enum values in serialization
        use_enum_values=True,
        # Allow extra fields but validate them
        extra='forbid',
        # Enable JSON schema generation
        json_schema_extra={
            "examples": []
        }
    )
    
    id: UUID = Field(default_factory=uuid4, description="Unique identifier")
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Creation timestamp"
    )
    updated_at: Optional[datetime] = Field(
        default=None,
        description="Last update timestamp"
    )
    
    def update_timestamp(self) -> None:
        """Update the updated_at timestamp."""
        self.updated_at = datetime.now(timezone.utc)
    
    def to_dict(self, exclude_none: bool = True) -> Dict[str, Any]:
        """Convert model to dictionary with options."""
        return self.model_dump(
            exclude_none=exclude_none,
            by_alias=True
        )

class ContactInfoModel(BaseModel):
    """Contact information model."""
    
    phone: Optional[str] = Field(None, pattern=r'^\+?[1-9]\d{1,14}$')
    email: str = Field(..., description="Email address")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "phone": "+1234567890",
                "email": "customer@example.com"
            }
        }
    )