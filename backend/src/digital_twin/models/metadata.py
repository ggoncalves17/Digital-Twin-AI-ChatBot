from sqlalchemy import String, JSON 
from sqlalchemy.sql import func
from digital_twin.models import Base
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column

# Define table

class Table(Base):
    """SQLAlchemy model for the tables Table."""

    __tablename__ = "tables"

    table_id: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    schema_name: Mapped[str] = mapped_column(String,nullable=False)
    location: Mapped[str] = mapped_column(String,nullable=False)
    format: Mapped[str] = mapped_column(String,nullable=False)
    schema_definition: Mapped[dict] = mapped_column(JSON, nullable=True)
    partitions: Mapped[list] = mapped_column(JSON, nullable=False)
    properties: Mapped[dict] = mapped_column(JSON, nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<Table(id={self.id}, name='{self.name}', schema_name='{self.schema_name}')>"


