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
from digital_twin.utils.lakehouse_export import export_data

router = APIRouter(prefix="/occupations", tags=["occupation"])


@router.post("/", response_model=Occupation)
def create_occupation(
    occupation: OccupationCreate, db: Annotated[Session, Depends(get_db)]
):
    new_occupation = OccupationService.create_occupation(db, occupation)

    if new_occupation is None:
        export_data(
            "endpoints",
            {
                "event": "occupation_create",
                "status": "error",
                "description": f"Persona with ID {occupation.persona_id} does not exist",
            }
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Persona id not found"
        )

    export_data(
        "endpoints",
        {
            "event": "occupation_create",
            "status": "success",
            "occupation_id": new_occupation.id,
            "persona_id": new_occupation.persona_id,
        }
    )
    return new_occupation


@router.get("/", response_model=list[Occupation])
def get_occupations_by_persona(
    persona: Annotated[int, Query(description="Persona ID")],
    db: Annotated[Session, Depends(get_db)],
):
    occupation = OccupationService.get_occupations_by_persona(db, persona)

    if occupation is None:
        export_data(
            "endpoints",
            {
                "event": "occupation_get_by_persona",
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
            "event": "occupation_get_by_persona",
            "status": "success",
            "persona_id": persona,
            "items": len(occupation),
        }
    )
    return occupation


@router.get("/{id}", response_model=Occupation)
def get_occupation(id: int, db: Annotated[Session, Depends(get_db)]):
    occupation = OccupationService.get_occupation(db, id)

    if not occupation:
        export_data(
            "endpoints",
            {
                "event": "occupation_get_by_id",
                "status": "error",
                "description": f"Occupation with ID {id} does not exist",
            }
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Occupation not found"
        )

    export_data(
        "endpoints",
        {
            "event": "occupation_get_by_id",
            "status": "success",
            "occupation_id": id,
        }
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
        export_data(
            "endpoints",
            {
                "event": "occupation_update",
                "status": "error",
                "description": f"Occupation with ID {id} does not exist",
            }
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Occupation not found"
        )

    export_data(
        "endpoints",
        {
            "event": "occupation_update",
            "status": "success",
            "occupation_id": id,
        }
    )
    return occupation


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_occupation(id: int, db: Annotated[Session, Depends(get_db)]) -> None:
    success = OccupationService.delete_occupation(db, id)

    if not success:
        export_data(
            "endpoints",
            {
                "event": "occupation_delete",
                "status": "error",
                "description": f"Occupation with ID {id} does not exist",
            }
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Occupation not found"
        )

    export_data(
        "endpoints",
        {
            "event": "occupation_delete",
            "status": "success",
            "occupation_id": id,
        }
    )
