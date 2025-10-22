from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from digital_twin.database import get_db
from digital_twin.schemas.hobby import Hobby, HobbyCreate, HobbyUpdate
from digital_twin.services.hobby import HobbyService
from digital_twin.utils.lakehouse_export import export_data

router = APIRouter(prefix="/hobbies", tags=["hobby"])


@router.post("/", response_model=Hobby)
def create_hobby(hobby: HobbyCreate, db: Annotated[Session, Depends(get_db)]):
    new_hobby = HobbyService.create_hobby(db, hobby)

    if new_hobby is None:
        export_data(
            "endpoints",
            {
                "event": "hobby_create",
                "status": "error",
                "description": f"Persona with ID {hobby.persona_id} does not exist",
            }
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Persona id not found"
        )

    export_data(
        "endpoints",
        {
            "event": "hobby_create",
            "status": "success",
            "hobby_id": new_hobby.id,
            "persona_id": new_hobby.persona_id,
        }
    )
    return new_hobby


@router.get("/", response_model=list[Hobby])
def get_hobbies(
    persona: Annotated[int, Query(description="Persona ID")],
    db: Annotated[Session, Depends(get_db)],
):
    hobby = HobbyService.get_hobbies_by_persona(db, persona)

    if hobby is None:
        export_data(
            "endpoints",
            {
                "event": "hobby_get_by_persona",
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
            "event": "hobby_get_by_persona",
            "status": "success",
            "persona_id": persona,
            "items": len(hobby),
        }
    )
    return hobby


@router.get("/{id}", response_model=Hobby)
def get_hobby(id: int, db: Annotated[Session, Depends(get_db)]):
    hobby = HobbyService.get_hobby(db, id)

    if not hobby:
        export_data(
            "endpoints",
            {
                "event": "hobby_get_by_id",
                "status": "error",
                "description": f"Hobby with ID {id} does not exist",
            }
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Hobby not found"
        )

    export_data(
        "endpoints",
        {
            "event": "hobby_get_by_id",
            "status": "success",
            "hobby_id": id,
        }
    )
    return hobby


@router.put("/{id}", response_model=Hobby)
def update_hobby(
    id: int, hobby_update: HobbyUpdate, db: Annotated[Session, Depends(get_db)]
):
    hobby = HobbyService.update_hobby(db, id, hobby_update)

    if not hobby:
        export_data(
            "endpoints",
            {
                "event": "hobby_update",
                "status": "error",
                "description": f"Hobby with ID {id} does not exist",
            }
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Hobby not found"
        )

    export_data(
        "endpoints",
        {
            "event": "hobby_update",
            "status": "success",
            "hobby_id": id,
        }
    )
    return hobby


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_hobby(id: int, db: Annotated[Session, Depends(get_db)]) -> None:
    success = HobbyService.delete_hobby(db, id)

    if not success:
        export_data(
            "endpoints",
            {
                "event": "hobby_delete",
                "status": "error",
                "description": f"Hobby with ID {id} does not exist",
            }
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Hobby not found"
        )

    export_data(
        "endpoints",
        {
            "event": "hobby_delete",
            "status": "success",
            "hobby_id": id,
        }
    )
