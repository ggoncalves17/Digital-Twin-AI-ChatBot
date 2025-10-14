from datetime import date, datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session

from digital_twin.models.persona import Persona
from digital_twin.schemas.persona import PersonaCreate, PersonaUpdate


def input_date(prompt: str) -> date:
    while True:
        try:
            d = input(prompt)
            return datetime.strptime(d, "%Y-%m-%d").date()
        except ValueError:
            print("Invalid format. Use YYYY-MM-DD.")


def get_persona_by_id(db: Session, persona_id: int) -> Persona:
    persona = db.query(Persona).filter(Persona.id == persona_id).first()
    if not persona:
        raise HTTPException(status_code=404, detail="Persona not found")
    return persona

def create_new_persona(db: Session, persona: PersonaCreate) -> Persona:
    existing_persona = db.query(Persona).filter(Persona.name == persona.name).first()
    if existing_persona:
        raise HTTPException(status_code=400, detail="Persona already registered")

    new_persona = Persona(
        name=persona.name,
        birthdate=persona.birthdate,
        gender=persona.gender,
        nationality=persona.nationality
    )
    db.add(new_persona)
    db.commit()
    db.refresh(new_persona)
    return new_persona

def list_all_personas(db: Session) -> list[Persona]:
    return db.query(Persona).all()

def update_persona(db: Session, persona_id: int, update: PersonaUpdate) -> Persona:
    persona = get_persona_by_id(db, persona_id)
    if not persona:
        raise HTTPException(status_code=404, detail="Persona not found")

    update_data = update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(persona, field, value)

    db.commit()
    db.refresh(persona)
    return persona

def delete_persona(db: Session, persona_id: int) -> None:
    persona = get_persona_by_id(db, persona_id)
    if not persona:
        raise HTTPException(status_code=404, detail="Persona not found")
    db.delete(persona)
    db.commit()