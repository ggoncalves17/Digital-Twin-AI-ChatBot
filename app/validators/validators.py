"""
Custom validators for e-commerce data models.
"""

from pydantic import field_validator, ValidationInfo
from typing import Any, List
import re
from datetime import datetime, timezone

class CommonValidators:
    """Collection of reusable validators."""
    
    @staticmethod
    def validate_phone_number(phone: str) -> str:
        """Validate phone number format."""
        if not phone:
            raise ValueError("Phone number cannot be empty")
        
        # Remove all non-digit characters except +
        clean_phone = re.sub(r'[^\d+]', '', phone)
        
        # Basic international format validation
        if not re.match(r'^\+?[1-9]\d{8,14}$', clean_phone):
            raise ValueError("Invalid phone number format")
        
        return clean_phone
    
    @staticmethod
    def validate_future_date(date_value: datetime) -> datetime:
        """Validate that date is in the future."""
        now = datetime.now(timezone.utc)
        if date_value.tzinfo is None:
            date_value = date_value.replace(tzinfo=timezone.utc)
        
        if date_value <= now:
            raise ValueError("Date must be in the future")
        
        return date_value