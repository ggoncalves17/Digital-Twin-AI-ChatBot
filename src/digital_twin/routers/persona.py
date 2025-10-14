from fastapi import APIRouter

from digital_twin.schemas.persona import Persona, PersonaCreate, PersonaUpdate

router = APIRouter(prefix="/personas")

# Mock database
persona_db: list[Persona] = list()
next_id: int = 1


def get_next_id() -> int:
    global next_id
    current = next_id
    next_id += 1
    return current


def get_persona_from_id(id: int) -> Persona | None:
    return next((p for p in persona_db if p.id == id), None)


@router.get("/")
def get_all_personas() -> list[Persona]:
    return persona_db


@router.get("/{id}")
def get_persona(id: int) -> Persona:
    persona = get_persona_from_id(id)
    if not persona:
        raise ValueError(f"Persona with ID {id} not found")
    return persona


@router.post("/")
def add_persona(new_persona: PersonaCreate) -> Persona:
    persona = Persona(id=get_next_id(), **new_persona.model_dump())
    persona_db.append(persona)
    return persona


@router.put("/{id}")
def update_persona(id: int, update_persona: PersonaUpdate) -> Persona:
    persona = get_persona_from_id(id)
    if not persona:
        raise ValueError(f"Persona with ID {id} not found")
    for k, v in update_persona.model_dump(exclude_unset=True).items():
        setattr(persona, k, v)
    return persona


@router.delete("/{id}")
def delete_persona(id: int):
    persona = get_persona_from_id(id)
    if not persona:
        raise ValueError(f"Persona with ID {id} not found")
    persona_db.remove(persona)
    return
