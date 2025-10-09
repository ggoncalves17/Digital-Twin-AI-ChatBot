"""
Ficheiro com a configuração do SQLAlchemy, modelos, repositórios e serviços.
"""

from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.sql import func
from datetime import date
from typing import Optional
import os

# Database configuration
DATABASE_URL = "postgresql://postgres:123@localhost/digital_twin_db"

# Create engine
engine = create_engine(DATABASE_URL, echo=True)  # echo=True shows generated SQL

# Create session factory
SessionLocal = sessionmaker(bind=engine)

# Base class for models
Base = declarative_base()

class User(Base):
    """User model with comprehensive profile information."""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False, unique=True, index=True)
    date_of_birth = Column(Date, nullable=True)
    password = Column(String(255), nullable=False)
    total_messages = Column(Integer, default=0)
    
    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', name='{self.full_name}')>"
    
    @property
    def full_name(self):
        """Get user's full name."""
        return f"{self.first_name} {self.last_name}"
    
    @property
    def age(self):
        """Calculate user's age from date of birth."""
        if self.date_of_birth:
            today = date.today()
            return today.year - self.date_of_birth.year - (
                (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
            )
        return None
    

# Repository Pattern Implementation

class BaseRepository:
    """Base repository with common CRUD operations."""
    
    def __init__(self, db: Session, model_class):
        self.db = db
        self.model_class = model_class
    
    def create(self, **kwargs):
        """Create a new record."""
        instance = self.model_class(**kwargs)
        self.db.add(instance)
        self.db.commit()
        self.db.refresh(instance)
        return instance
    
    def get_by_id(self, id: int):
        """Get record by ID."""
        return self.db.query(self.model_class).filter(self.model_class.id == id).first()
    
    def get_all(self, skip: int = 0, limit: int = 100):
        """Get all records with pagination."""
        return self.db.query(self.model_class).offset(skip).limit(limit).all()
    
    def update(self, id: int, **kwargs):
        """Update record by ID."""
        instance = self.get_by_id(id)
        if instance:
            for key, value in kwargs.items():
                setattr(instance, key, value)
            self.db.commit()
            self.db.refresh(instance)
        return instance
    
    def delete(self, id: int) -> bool:
        """Delete record by ID."""
        instance = self.get_by_id(id)
        if instance:
            self.db.delete(instance)
            self.db.commit()
            return True
        return False

class UserRepository(BaseRepository):
    """User-specific repository operations."""
    
    def __init__(self, db: Session):
        super().__init__(db, User)
    
    def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email address."""
        return self.db.query(User).filter(User.email == email).first()
    
    def get_active_users(self):
        """Get all active users."""
        return self.db.query(User).filter(User.is_active == True).all()
    
    def search_users(self, search_term: str):
        """Search users by name or email."""
        search = f"%{search_term}%"
        return self.db.query(User).filter(
            User.first_name.ilike(search) |
            User.last_name.ilike(search) |
            User.email.ilike(search)
        ).all()
    
def create_tables():
    """Create all tables."""
    Base.metadata.create_all(bind=engine)
    print("✅ All tables created successfully")

def get_db():
    """Database session dependency."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Example usage and testing
def main():
    """Demonstrate SQLAlchemy models usage."""
    # Create tables
    create_tables()

if __name__ == "__main__":
    main()