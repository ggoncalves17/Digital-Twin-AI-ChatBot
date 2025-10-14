from fastapi import HTTPException
from sqlalchemy.orm import Session

from digital_twin.models.education import Education
from digital_twin.schemas.education import EducationCreate, EducationUpdate


def get_education_by_id(db: Session, education_id: int) -> Education:
    education = db.query(Education).filter(Education.id == education_id).first()
    if not education:
        raise HTTPException(status_code=404, detail="Education not found")
    return education

def create_new_education(db: Session, education: EducationCreate) -> Education:
    existing_education = db.query(Education).filter(Education.name == education.name).first()
    if existing_education:
        raise HTTPException(status_code=400, detail="Education already registered")

    new_education = Education(
        level=education.level,
        course=education.course,
        school=education.school,
        date_started=education.date_started,
        date_finished=education.date_finished,
        is_graduated=education.is_graduated,
        grade=education.grade,
        persona_id=education.persona_id,
    )
    db.add(new_education)
    db.commit()
    db.refresh(new_education)
    return new_education

def list_all_educations(db: Session) -> list[Education]:
    return db.query(Education).all()

def update_education(db: Session, education_id: int, update: EducationUpdate) -> Education:
    education = get_education_by_id(db, education_id)
    if not education:
        raise HTTPException(status_code=404, detail="Education not found")

    update_data = update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(education, field, value)

    db.commit()
    db.refresh(education)
    return education

def delete_education(db: Session, education_id: int) -> None:
    education = get_education_by_id(db, education_id)
    if not education:
        raise HTTPException(status_code=404, detail="Education not found")
    db.delete(education)
    db.commit()