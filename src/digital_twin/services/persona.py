from sqlalchemy.orm import Session

from digital_twin.models.persona import Persona
from digital_twin.schemas.persona import PersonaCreate, PersonaUpdate


class PersonaService:
    @staticmethod
    def create_persona(db: Session, persona_create: PersonaCreate) -> Persona:
        db_persona = Persona(**persona_create.model_dump())
        db.add(db_persona)
        db.commit()
        db.refresh(db_persona)
        return db_persona

    @staticmethod
    def get_personas(db: Session) -> list[Persona]:
        return db.query(Persona).order_by(Persona.id.asc()).all()

    @staticmethod
    def get_persona(db: Session, id: int) -> Persona | None:
        return db.query(Persona).filter(Persona.id == id).first()

    @staticmethod
    def update_persona(db: Session, id: int, persona_update: PersonaUpdate) -> Persona | None:
        persona = db.query(Persona).filter(Persona.id == id).first()
        if not persona:
            return None
        update_data = persona_update.model_dump(exclude_unset=True)
        for k, v in update_data.items():
            setattr(persona, k, v)
        db.commit()
        db.refresh(persona)
        return persona

    @staticmethod
    def delete_persona(db: Session, id: int) -> bool:
        persona = db.query(Persona).filter(Persona.id == id).first()
        if not persona:
            return False
        db.delete(persona)
        return True

