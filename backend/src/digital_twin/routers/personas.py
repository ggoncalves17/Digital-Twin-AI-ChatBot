from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from digital_twin.database import get_db
from digital_twin.schemas.persona import Persona, PersonaCreate, PersonaUpdate
from digital_twin.services.persona import PersonaService
from digital_twin.utils.lakehouse_export import export_data

router = APIRouter(prefix="/personas", tags=["persona"])


@router.get("/", response_model=list[Persona])
def get_all_personas(db: Annotated[Session, Depends(get_db)]):
    personas = PersonaService.get_personas(db)
    export_data(
        "endpoints",
        {
            "event": "personas_get_all",
            "status": "success",
            "items": len(personas),
        },
    )
    return personas


@router.get("/{id}", response_model=Persona)
def get_persona(id: int, db: Annotated[Session, Depends(get_db)]):
    persona = PersonaService.get_persona(db, id)

    if not persona:
        export_data(
            "endpoints",
            {
                "event": "persona_get_by_id",
                "status": "error",
                "description": f"Persona with ID {id} does not exist",
            },
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Persona not found"
        )

    export_data(
        "endpoints",
        {
            "event": "persona_get_by_id",
            "status": "success",
            "persona_id": id,
        },
    )
    return persona


@router.post("/", response_model=Persona)
def add_persona(new_persona: PersonaCreate, db: Annotated[Session, Depends(get_db)]):
    persona = PersonaService.create_persona(db, new_persona)

    if not persona:
        export_data(
            "endpoints",
            {
                "event": "persona_create",
                "status": "error",
                "description": "DB integrity error",
            },
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Integrity error"
        )

    export_data(
        "endpoints",
        {
            "event": "persona_create",
            "status": "success",
            "persona_id": persona.id,
        },
    )
    return persona


@router.put("/{id}", response_model=Persona)
def update_persona(
    id: int, update_persona: PersonaUpdate, db: Annotated[Session, Depends(get_db)]
):
    persona = PersonaService.update_persona(db, id, update_persona)

    if not persona:
        export_data(
            "endpoints",
            {
                "event": "persona_update",
                "status": "error",
                "description": f"Persona with ID {id} does not exist",
            },
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Persona not found"
        )

    export_data(
        "endpoints",
        {
            "event": "persona_update",
            "status": "success",
            "persona_id": id,
        },
    )
    return persona


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_persona(id: int, db: Annotated[Session, Depends(get_db)]):
    success = PersonaService.delete_persona(db, id)

    if not success:
        export_data(
            "endpoints",
            {
                "event": "persona_delete",
                "status": "error",
                "description": f"Persona with ID {id} does not exist",
            },
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Persona not found"
        )

    export_data(
        "endpoints",
        {
            "event": "persona_delete",
            "status": "success",
            "persona_id": id,
        },
    )
