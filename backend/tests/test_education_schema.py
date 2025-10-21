
from dataclasses import Field
from datetime import date
from turtle import position
from digital_twin.schemas.education import EducationBase, EducationLevel, EducationUpdate

def test_education_schema():
    education = EducationBase(
        level=EducationLevel.BACHELOR,
        course="Computer Science",
        school="Tech University",
        date_started=date(2016, 1, 1),
        date_finished=date(2020, 1, 1),
        is_graduated=True,
        grade=14.5
        )
    assert education.level == EducationLevel.BACHELOR
    assert education.course == "Computer Science"
    assert education.school == "Tech University"
    assert education.date_started == date(2016, 1, 1)
    assert education.date_finished == date(2020, 1, 1)
    assert education.is_graduated == True
    assert education.grade == 14.5

def test_invalid_name_raises_error():
    import pytest
    with pytest.raises(ValueError):
        EducationBase(
        level=EducationLevel.BACHELOR,
        course="Philosophy",
        school="Philosophy University",
        date_started=date(2016, 1, 1),
        is_graduated=True,
        grade=14.5
        )

def test_update_occupation_schema():
    education_update = EducationUpdate(
        course="Data Science",
    )
    assert education_update.course == "Data Science"
    assert education_update.level == None 
    assert education_update.school == None
    assert education_update.date_started == None
    assert education_update.date_finished == None
    assert education_update.is_graduated == None
    assert education_update.grade == None