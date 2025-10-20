from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from digital_twin.database import get_db
from digital_twin.schemas.occupation import (
    Occupation,
    OccupationCreate,
    OccupationUpdate,
)
from digital_twin.services.occupation import OccupationService

router = APIRouter(prefix="/occupations", tags=["occupation"])


@router.post("/", response_model=Occupation)
def create_occupation(
    occupation: OccupationCreate, db: Annotated[Session, Depends(get_db)]
):
    occupation = OccupationService.create_occupation(db, occupation)
    
    if occupation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Persona id not found"
        )
    return occupation


@router.get("/", response_model=list[Occupation])
def get_occupations_by_persona(
    persona: Annotated[int, Query(description="Persona ID")],
    db: Annotated[Session, Depends(get_db)],
):
    occupation = OccupationService.get_occupations_by_persona(db, persona)

    if occupation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Persona id not found"
        )
    return occupation


@router.get("/{id}", response_model=Occupation)
def get_occupation(id: int, db: Annotated[Session, Depends(get_db)]):
    occupation = OccupationService.get_occupation(db, id)
    if not occupation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Occupation not found"
        )
    return occupation


@router.put("/{id}", response_model=Occupation)
def update_occupation(
    id: int,
    occupation_update: OccupationUpdate,
    db: Annotated[Session, Depends(get_db)],
):
    occupation = OccupationService.update_occupation(db, id, occupation_update)
    if not occupation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Occupation not found"
        )
    return occupation


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_occupation(id: int, db: Annotated[Session, Depends(get_db)]) -> None:
    success = OccupationService.delete_occupation(db, id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Occupation not found"
        )
