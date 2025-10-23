from sqlalchemy.orm import Session

from digital_twin.models.education import Education
from digital_twin.schemas.education import EducationCreate, EducationUpdate
from digital_twin.services.persona import PersonaService


class EducationService:
    """Hobby abstraction layer between ORM and API endpoints."""

    @staticmethod
    def create_education(db: Session, education: EducationCreate) -> Education | None:
        new_education = Education(**education.model_dump())

        try:
            db.add(new_education)
            db.commit()
            db.refresh(new_education)

            return new_education
        except:
            return None

    @staticmethod
    def get_education(db: Session, id: int) -> Education | None:
        return db.query(Education).filter(Education.id == id).first()

    @staticmethod
    def get_educations_by_persona(db: Session, persona_id: int) -> list[Education] | None:
        if not PersonaService.get_persona(db, persona_id):
            return None
        return db.query(Education).filter(Education.persona_id == persona_id).all()

    @staticmethod
    def update_education(db: Session, id: int, update: EducationUpdate) -> Education | None:
        education = db.query(Education).filter(Education.id == id).first()
        if education:
            for k, v in update.model_dump(exclude_unset=True).items():
                setattr(education, k, v)
            db.commit()
            db.refresh(education)

        return education

    @staticmethod
    def delete_education(db: Session, id: int) -> bool:
        education = db.query(Education).filter(Education.id == id).first()
        if not education:
            return False

        db.delete(education)
        db.commit()
        return True

