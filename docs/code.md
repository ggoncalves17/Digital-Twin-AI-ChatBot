# Code best-practices

## Type hinting
Use type hinting as much as possible, to avoid developer mistakes and aid code linters.

## Linting and formatting
Use `ruff` to lint and format code.
```bash
# Optional: sort imports
ruff check --select I --fix <file>

# Format file 
ruff format <file>

# Check for errors (use --fix to apply safe fixes)
ruff check [--fix] <file>

# If '.' is supplied instead of a file, ruff will recurse through all python files
```

## SQLAlchemy

### Use type hints to create models
```python
from datetime import datetime

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase): ...


class User(Base):
    __tablename__: str = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column() # NOT NULL

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())         # NOT NULL
    updated_at: Mapped[datetime | None] = mapped_column(server_onupdate=func.now()) # NULLABLE
```
