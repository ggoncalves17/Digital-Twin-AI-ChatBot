"""
Education data models.
"""

from datetime import date
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator
from enum import Enum
from typing import ClassVar, Optional
from typing_extensions import Self

class EducationLevel(str, Enum):

    """Education levels enumeration."""

    HIGHSCHOOL = "Highschool"
    BACHELOR = "Bachelor"
    MASTER = "Master"
    PHD = "PhD"

class EducationBase(BaseModel):

    """Base education model with common fields."""

    level : EducationLevel = Field(..., description="Education level")
    course : str = Field(..., min_length=1, max_length=100, description="Name of the course")
    school : str = Field(..., min_length=1, max_length=100, description="Name of the school")
    date_started : date = Field(..., description="Date when the course started")
    date_finished : Optional[date] = Field(None, description="Date when the course finished")
    is_graduated: bool = Field(..., description="Indicates whether the user has graduated")

    @field_validator('course')
    def validate_course(cls, v : str) -> str:
        if not v.strip():
            raise ValueError("Course name cannot be empty.")
        return v.strip()

    @field_validator('school')
    def validate_school(cls, v : str) -> str:
        if not v.strip():
            raise ValueError("School name cannot be empty.")
        return v.strip()

    @model_validator(mode='after')
    def validate_is_graduated(self) -> Self:
        if self.is_graduated is True and not self.date_finished:
            raise ValueError("If the user is graduated, 'date_finished' must be specified.")
        return self
    
    @model_validator(mode='after')
    def check_dates(self) -> Self:
        if self.date_finished and self.date_finished < self.date_started:
            raise ValueError("'date_finished' must be after 'date_started'.")
        return self

    model_config: ClassVar[ConfigDict] = ConfigDict(validate_assignment=True)
    
class EducationCreate(EducationBase):
    """Model for creating a new education."""
    pass

class EducationUpdate(BaseModel):
    """Model for updating an existing education."""

    level: Optional[EducationLevel] = Field(None, description="Education level")
    course: Optional[str] = Field(None, min_length=1, max_length=100, description="Name of the course")
    school: Optional[str] = Field(None, min_length=1, max_length=100, description="Name of the school")
    date_started: Optional[date] = Field(None, description="Date when the course started")
    date_finished: Optional[date] = Field(None, description="Date when the course finished")
    is_graduated: Optional[bool] = Field(None, description="Indicates whether the user has graduated")

    @field_validator('course')
    def validate_course(cls, v : str) -> str:
        if v is not None and not v.strip():
            raise ValueError("Course name cannot be empty.")
        return v.strip()

    @field_validator('school')
    def validate_school(cls, v : str) -> str:
        if v is not None and not v.strip():
            raise ValueError("School name cannot be empty.")
        return v.strip()

    @model_validator(mode='after')
    def check_dates(self) -> Self:
        if self.date_started is not None and self.date_finished is not None and self.date_finished < self.date_started:
            raise ValueError("'date_finished' must be after 'date_started'.")
        return self

class Education(EducationBase):
    """Model for education responses."""

    id: int = Field(..., description="Unique education ID")

    model_config = ConfigDict(
        from_attributes = True,
        json_schema_extra = {
            "examples": [
                {
                    "level": "Bachelor",
                    "course": "Computer Science",
                    "school": "Harvard University",
                    "date_started": "2022-10-01",
                    "date_finished": "2025-07-01",
                    "is_graduated": True,
                    "id": 1
                },
            ]
        }
    )