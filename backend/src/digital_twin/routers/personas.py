from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.logger import logger
from sqlalchemy.orm import Session

from digital_twin.database import get_db
from digital_twin.schemas.persona import Persona, PersonaCreate, PersonaUpdate
from digital_twin.services.persona import PersonaService

router = APIRouter(prefix="/personas", tags=["persona"])


@router.get("/", response_model=list[Persona])
def get_all_personas(db: Annotated[Session, Depends(get_db)]):
    return PersonaService.get_personas(db)


@router.get("/{id}", response_model=Persona)
def get_persona(id: int, db: Annotated[Session, Depends(get_db)]):
    persona = PersonaService.get_persona(db, id)
    if not persona:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Persona not found"
        )
    return persona


@router.post("/", response_model=Persona)
def add_persona(new_persona: PersonaCreate, db: Annotated[Session, Depends(get_db)]):
    logger.info(new_persona)
    return PersonaService.create_persona(db, new_persona)


@router.put("/{id}", response_model=Persona)
def update_persona(
    id: int, update_persona: PersonaUpdate, db: Annotated[Session, Depends(get_db)]
):
    persona = PersonaService.update_persona(db, id, update_persona)
    logger.info(persona)
    if not persona:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Persona not found"
        )
    return persona


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_persona(id: int, db: Annotated[Session, Depends(get_db)]):
    success = PersonaService.delete_persona(db, id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Persona not found"
        )
