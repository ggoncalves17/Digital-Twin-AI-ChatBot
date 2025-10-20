from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from digital_twin.database import get_db
from digital_twin.schemas.education import Education, EducationCreate, EducationUpdate
from digital_twin.services.education import EducationService
from digital_twin.utils.lakehouse_export import export_data

router = APIRouter(prefix="/educations", tags=["education"])


@router.post("/", response_model=Education)
def create_education(
    education: EducationCreate, db: Annotated[Session, Depends(get_db)]
):
    new_education = EducationService.create_education(db, education)

    if new_education is None:
        export_data(
            "endpoints",
            {
                "event": "education_create",
                "status": "error",
                "description": f"Persona with ID {education.persona_id} does not exist",
            },
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Persona id not found"
        )

    export_data(
        "endpoints",
        {
            "event": "education_create",
            "status": "success",
            "education_id": new_education.id,
            "persona_id": new_education.persona_id,
        },
    )
    return new_education


@router.get("/", response_model=list[Education])
def get_educations_by_persona(
    persona: Annotated[int, Query(description="Persona ID")],
    db: Annotated[Session, Depends(get_db)],
):
    education = EducationService.get_educations_by_persona(db, persona)

    if education is None:
        export_data(
            "endpoints",
                {
                    "event": "education_get_by_persona",
                    "status": "error",
                    "description": f"Persona with ID {persona} does not exist",
                }
            )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Persona id not found"
        )

    export_data(
        "endpoints",
        {
            "event": "education_get_by_persona",
            "status": "success",
            "persona_id": persona,
            "items": len(education),
        }
    )
    return education


@router.get("/{id}", response_model=Education)
def get_education(id: int, db: Annotated[Session, Depends(get_db)]):
    education = EducationService.get_education(db, id)

    if not education:
        export_data(
            "endpoints",
            {
                "event": "education_get_by_id",
                "status": "error",
                "description": f"Education with ID {id} does not exist",
            }
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Education not found"
        )

    export_data(
        "endpoints",
        {
            "event": "education_get_by_id",
            "status": "success",
            "education_id": id,
        }
    )
    return education


@router.put("/{id}", response_model=Education)
def update_education(
    id: int, education_update: EducationUpdate, db: Annotated[Session, Depends(get_db)]
):
    education = EducationService.update_education(db, id, education_update)

    if not education:
        export_data(
            "endpoints",
            {
                "event": "education_update",
                "status": "error",
                "description": f"Education with ID {id} does not exist",
            }
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Education not found"
        )

    export_data(
        "endpoints",
        {
            "event": "education_update",
            "status": "success",
            "education_id": id,
        }
    )
    return education


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_education(id: int, db: Annotated[Session, Depends(get_db)]) -> None:
    success = EducationService.delete_education(db, id)

    if not success:
        export_data(
            "endpoints",
            {
                "event": "education_delete",
                "status": "error",
                "description": f"Education with ID {id} does not exist",
            }
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Education not found"
        )

    export_data(
        "endpoints",
        {
            "event": "education_delete",
            "status": "success",
            "education_id": id,
        }
    )
