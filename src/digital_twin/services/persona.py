from datetime import date, datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.digital_twin.models.persona import Persona
from src.digital_twin.schemas.persona import PersonaUpdate

# Mock database
DBPersona: list[Persona] = list()

def input_date(prompt: str) -> date:
    while True:
        try:
            d = input(prompt)
            return datetime.strptime(d, "%Y-%m-%d").date()
        except ValueError:
            print("Formato inválido. Usa YYYY-MM-DD.")


def get_persona_by_id(db: Session, persona_id: int) -> Persona:
    persona = db.query(DBPersona).filter(DBPersona.id == persona_id).first()
    if not persona:
        raise HTTPException(status_code=404, detail="Persona não encontrada")
    return persona

def create_new_persona(db: Session, persona: Persona) -> Persona:
    existing_persona = db.query(DBPersona).filter(DBPersona.name == persona.name).first()
    if existing_persona:
        raise HTTPException(status_code=400, detail="Persona com esse nome já registada")

    new_persona = DBPersona(
        name=persona.name,
        birthdate=persona.birthdate,
        gender=persona.gender,
        nationality=persona.nationality,
        educations=persona.educations or [],
        occupations=persona.occupations or [],
        hobbies=persona.hobbies or [],
    )
    db.add(new_persona)
    db.commit()
    db.refresh(new_persona)
    return new_persona

def list_all_personas(db: Session) -> list[Persona]:
    return db.query(DBPersona).all()

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