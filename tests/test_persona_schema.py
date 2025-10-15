
from dataclasses import Field
from datetime import date
from turtle import position
from digital_twin.schemas.education import Education, EducationBase, EducationLevel
from digital_twin.schemas.hobby import HobbyFrequency, HobbyType, HobbyBase
from digital_twin.schemas.occupation import OccupationBase
from digital_twin.schemas.persona import GenderEnum, PersonaBase, PersonaCreate, PersonaUpdate, Persona

def test_valid_persona_schema():
    hobby = HobbyBase(
        name="Running",
        type=HobbyType.SPORTS_FITNESS,
        freq=HobbyFrequency.OFTEN
    )
    occupation = OccupationBase(
        position="Software Engineer",
        workplace="Tech Corp",
        date_started=date(2020, 1, 1),
        date_finished=date(2022, 1, 1)
    )    
    education = EducationBase(
        level=EducationLevel.BACHELOR,
        course="Computer Science",
        school="Tech University",
        date_started=date(2016, 1, 1),
        date_finished=date(2020, 1, 1),
        is_graduated=True,
        grade=14.5
    )
    persona = PersonaBase(
        name="John Doe",
        birthdate=date(1990, 1, 1),
        gender=GenderEnum.MALE,
        nationality="American",
        # education=[education],
        # hobbies=[hobby],
        # occupations=[occupation]
    )
    assert persona.name == "John Doe"
    # assert persona.gender == "Male"
    # assert persona.nationality == "American"
    # assert persona.education == "Bachelor's Degree"
    # assert persona.occupation == "Software Engineer"
    # assert persona.hobbies == ["Reading", "Traveling"]


def test_invalid_name_raises_error():
    import pytest
    with pytest.raises(ValueError):
        PersonaBase(name="  ", gender="Male", nationality="American", education="Bachelor's Degree")

def test_update_persona_schema():
    persona_update = PersonaUpdate(
        name="Jane Doe",
    )
    assert persona_update.name == "Jane Doe"
    assert persona_update.gender == None
    assert persona_update.nationality == None
    assert persona_update.education == None
