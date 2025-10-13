"""
Hobby data models
"""
from enum import Enum
from typing import ClassVar

from pydantic import BaseModel, ConfigDict, Field, field_validator


class HobbyType(str, Enum):
    """Enumeration of possible types of hobbies"""

    SPORTS_FITNESS = "sports_fitness"          # includes gym, running, football, yoga, etc.
    ARTS_CRAFTS = "arts_crafts"                # includes drawing, painting, knitting, pottery, etc.
    MUSIC_PERFORMANCE = "music_performance"    # includes playing instruments, singing, dancing
    GAMING_TECH = "gaming_tech"                # includes video games, coding, electronics
    FOOD_COOKING = "food_cooking"              # includes cooking, baking, mixology
    TRAVEL_OUTDOORS = "travel_outdoors"        # includes travel, hiking, camping, nature walks
    READING_LEARNING = "reading_learning"      # includes reading, studying, personal development
    COLLECTING_BUILDING = "collecting_building"# includes collecting items, model building, puzzles
    OTHER = "other"                            # fallback for anything else


class HobbyFrequency(str, Enum):
    """Enumeration of possible frequencies of engaging in a hobby"""

    OFTEN = "often"
    SOMETIMES = "sometimes"
    RARELY = "rarely"


class HobbyBase(BaseModel):
    """Data model representing a hobby"""

    type : HobbyType = Field(..., description="Type of the hobby")
    name : str = Field(..., min_length=1, max_length=100, description="Name of the hobby")
    freq : HobbyFrequency = Field(..., description="Frequency of engaging in the hobby")
    

    @field_validator('name')
    @classmethod
    def validate_name(cls, v: str) -> str:
        if v is not None and not v.strip():
            raise ValueError("Hobby name cannot be empty.")
        return v.strip() if v else v
    

class HobbyCreation(HobbyBase):
    """Data model for creating a new hobby"""

    pass


class HobbyUpdate(BaseModel):
    """Model for updating an existing hobby."""

    type: HobbyType | None = Field(None, description="Type of the hobby")
    name: str | None = Field(None, min_length=1, max_length=100, description="Name of the hobby")
    freq: HobbyFrequency | None = Field(None, description="Frequency of engaging in the hobby")

    @field_validator('name')
    @classmethod
    def validate_name(cls, v : str) -> str:
        if not v.strip():
            raise ValueError("Hobby name cannot be empty.")
        return v.strip()


class Hobby(HobbyBase):
    """Data model representing a hobby with an ID"""
    id : int = Field(..., gt=0, description="Unique identifier for the hobby")

    model_config: ClassVar[ConfigDict] = ConfigDict(
        from_attributes = True,
        json_schema_extra = {
            "example": {
                "id": 1,
                "type": "sports_fitness",
                "name": "Running",
                "freq": "often"
            }
        }
    )
