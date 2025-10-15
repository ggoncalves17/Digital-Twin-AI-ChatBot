from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from digital_twin.database import get_db
from digital_twin.schemas.education import Education, EducationCreate, EducationUpdate
from digital_twin.services.education import EducationService

router = APIRouter(prefix="/educations", tags=["education"])


@router.post("/", response_model=Education)
def create_education(
    education: EducationCreate, db: Annotated[Session, Depends(get_db)]
):
    
    new_education = EducationService.create_education(db, education)

    if new_education is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Persona id not found"
        )

    return new_education


@router.get("/", response_model=list[Education])
def get_educations_by_persona(
    persona: Annotated[int, Query(description="Persona ID")],
    db: Annotated[Session, Depends(get_db)],
):
    education = EducationService.get_educations_by_persona(db, persona)
    
    if education is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Persona id not found"
        )
    return education


@router.get("/{id}", response_model=Education)
def get_education(id: int, db: Annotated[Session, Depends(get_db)]):
    education = EducationService.get_education(db, id)
    if not education:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Education not found"
        )
    return education


@router.put("/{id}", response_model=Education)
def update_education(
    id: int, education_update: EducationUpdate, db: Annotated[Session, Depends(get_db)]
):
    education = EducationService.update_education(db, id, education_update)
    if not education:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Education not found"
        )
    return education


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_education(id: int, db: Annotated[Session, Depends(get_db)]) -> None:
    success = EducationService.delete_education(db, id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Education not found"
        )
