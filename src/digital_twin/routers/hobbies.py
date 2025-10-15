from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from digital_twin.database import get_db
from digital_twin.schemas.hobby import Hobby, HobbyCreate, HobbyUpdate
from digital_twin.services.hobby import HobbyService

router = APIRouter(prefix="/hobbies", tags=["hobbies"])


@router.post("/", response_model=Hobby)
def create_hobby(hobby: HobbyCreate, db: Annotated[Session, Depends(get_db)]):
    return HobbyService.create_hobby(db, hobby)


@router.get("/", response_model=list[Hobby])
def get_hobbies(persona: Annotated[int, Query(description="Persona ID")], db: Annotated[Session, Depends(get_db)]):
    return HobbyService.get_hobbies_by_persona(db, persona)


@router.get("/{id}", response_model=Hobby)
def get_hobby(id: int, db: Annotated[Session, Depends(get_db)]):
    hobby = HobbyService.get_hobby(db, id)
    if not hobby:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Hobby not found"
        )
    return hobby


@router.put("/{id}", response_model=Hobby)
def update_hobby(
    id: int, hobby_update: HobbyUpdate, db: Annotated[Session, Depends(get_db)]
):
    hobby = HobbyService.update_hobby(db, id, hobby_update)
    if not hobby:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Hobby not found"
        )
    return hobby


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_hobby(id: int, db: Annotated[Session, Depends(get_db)]) -> None:
    success = HobbyService.delete_hobby(db, id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Hobby not found"
        )
