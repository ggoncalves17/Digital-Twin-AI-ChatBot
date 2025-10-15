from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, joinedload

from digital_twin.models.persona import Persona
from digital_twin.schemas.persona import PersonaCreate, PersonaUpdate


class PersonaService:
    """Persona abstraction layer between ORM and API endpoints."""

    @staticmethod
    def create_persona(db: Session, persona: PersonaCreate) -> Persona | None:
        new_persona = Persona(**persona.model_dump())
        try:
            db.add(new_persona)
        except IntegrityError:
            return None
        db.commit()
        db.refresh(new_persona)
        return new_persona

    @staticmethod
    def get_persona(db: Session, id: int) -> Persona | None:
        return (
            db.query(Persona)
            .options(
                joinedload(Persona.educations),
                joinedload(Persona.occupations),
                joinedload(Persona.hobbies),
            )
            .filter(Persona.id == id)
            .first()
        )

    @staticmethod
    def get_personas(db: Session) -> list[Persona]:
        return db.query(Persona).order_by(Persona.id).all()

    @staticmethod
    def update_persona(db: Session, id: int, update: PersonaUpdate) -> Persona | None:
        persona = db.query(Persona).filter(Persona.id == id).first()
        if not persona:
            return None

        for k, v in update.model_dump(exclude_unset=True).items():
            setattr(persona, k, v)

        db.commit()
        db.refresh(persona)
        return persona

    @staticmethod
    def delete_persona(db: Session, persona_id: int) -> bool:
        persona = db.query(Persona).filter(Persona.id == id).first()
        if not persona:
            return False
        db.delete(persona)
        db.commit()
        return True
