"""
User management endpoints.
"""

from fastapi import APIRouter, HTTPException, status, Query, Path
from typing import List, Optional
from datetime import datetime
import uuid

from models.users import (
    User, UserRegistration, UserUpdate, UserPreferences, UserListResponse,
    UserStatus, UserLogin, ErrorResponse
)

# Create router
router = APIRouter(prefix="/users", tags=["users"])

# In-memory storage (for demo purposes)
users_db: List[User] = []
next_id = 1

def get_next_id() -> int:
    """Get next available ID."""
    global next_id
    current = next_id
    next_id += 1
    return current

@router.post(
    "/register",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new User",
    description="Register a new user with automatic validation",
    responses={
        201: {"description": "User created successfully"},
        400: {"model": ErrorResponse, "description": "Invalid User data"},
        422: {"description": "Validation error"}
    }
)
async def create_User(User: UserRegistration) -> User:
    """
    Create a new User
    
    - **first_name**: User first name (1-100 characters)
    - **last_name**: User last name (1-100 characters)
    - **email**: Valid email address
    - **phone**: Optional phone number
    - **password**: Password (8-100 characters, mix of upper, lower, digit, special)
    - **date_of_birth**: Optional date in YYYY-MM-DD format, user must be at least 13 years old
    - **terms_accepted**: Must be True
    """
    # Check for duplicate email
    if User.email:
        existing_User = next((b for b in users_db if b.email == User.email), None)
        if existing_User:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"User with email {User.email} already exists"
            )
    
    # Create new User
    new_User = User(
        id=get_next_id(),
        **User.model_dump(),
        created_at=datetime.now()
    )
    
    users_db.append(new_User)
    return new_User

@router.get(
    "/",
    response_model=UserListResponse,
    summary="Get users with filtering and pagination",
    description="Retrieve users with optional filtering by genre, author, or publication year"
)
async def get_users(
    skip: int = Query(0, ge=0, description="Number of users to skip"),
    limit: int = Query(10, ge=1, le=100, description="Maximum number of users to return"),
    genre: Optional[UserGenre] = Query(None, description="Filter by genre"),
    author: Optional[str] = Query(None, min_length=1, description="Filter by author name"),
    year: Optional[int] = Query(None, ge=1000, le=2024, description="Filter by publication year")
) -> UserListResponse:
    """
    Get a list of users with optional filtering.
    
    Supports pagination and filtering by:
    - **genre**: User genre
    - **author**: Author name (partial match)
    - **year**: Publication year
    """
    # Apply filters
    filtered_users = users_db.copy()
    
    if genre:
        filtered_users = [b for b in filtered_users if b.genre == genre]
    
    if author:
        author_lower = author.lower()
        filtered_users = [b for b in filtered_users if author_lower in b.author.lower()]
    
    if year:
        filtered_users = [b for b in filtered_users if b.publication_year == year]
    
    # Pagination
    total = len(filtered_users)
    paginated_users = filtered_users[skip:skip + limit]
    has_next = skip + limit < total
    
    return UserListResponse(
        users=paginated_users,
        total=total,
        page=(skip // limit) + 1,
        limit=limit,
        has_next=has_next
    )

@router.get(
    "/{User_id}",
    response_model=User,
    summary="Get a specific User",
    description="Retrieve a User by its ID",
    responses={
        200: {"description": "User found"},
        404: {"model": ErrorResponse, "description": "User not found"}
    }
)
async def get_User(
    User_id: int = Path(..., gt=0, description="User ID")
) -> User:
    """Get a specific User by ID."""
    User = next((b for b in users_db if b.id == User_id), None)
    if not User:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {User_id} not found"
        )
    return User

@router.put(
    "/{User_id}",
    response_model=User,
    summary="Update a User",
    description="Update an existing User with new information",
    responses={
        200: {"description": "User updated successfully"},
        404: {"model": ErrorResponse, "description": "User not found"},
        400: {"model": ErrorResponse, "description": "Invalid update data"}
    }
)
async def update_User(
    User_id: int = Path(..., gt=0, description="User ID"),
    User_update: UserUpdate = ...
) -> User:
    """Update an existing User."""
    User_index = next((i for i, b in enumerate(users_db) if b.id == User_id), None)
    if User_index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {User_id} not found"
        )
    
    # Check ISBN uniqueness if updating
    if User_update.isbn:
        existing_User = next((b for b in users_db if b.isbn == User_update.isbn and b.id != User_id), None)
        if existing_User:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"User with ISBN {User_update.isbn} already exists"
            )
    
    # Update User
    existing_User = users_db[User_index]
    update_data = User_update.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(existing_User, field, value)
    
    existing_User.updated_at = datetime.now()
    
    return existing_User

@router.delete(
    "/{User_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a User",
    description="Remove a User from the library",
    responses={
        204: {"description": "User deleted successfully"},
        404: {"model": ErrorResponse, "description": "User not found"}
    }
)
async def delete_User(
    User_id: int = Path(..., gt=0, description="User ID")
):
    """Delete a User from the library."""
    User_index = next((i for i, b in enumerate(users_db) if b.id == User_id), None)
    if User_index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {User_id} not found"
        )
    
    users_db.pop(User_index)
    return None

# Statistics endpoints
@router.get(
    "/stats/summary",
    summary="Get library statistics",
    description="Get summary statistics about the User library"
)
async def get_library_stats():
    """Get library statistics."""
    if not users_db:
        return {
            "total_users": 0,
            "genres": {},
            "average_pages": 0,
            "publication_year_range": None
        }
    
    # Calculate statistics
    total_users = len(users_db)
    
    # Genre distribution
    genre_counts = {}
    for User in users_db:
        genre_counts[User.genre] = genre_counts.get(User.genre, 0) + 1
    
    # Average pages
    total_pages = sum(User.pages for User in users_db)
    average_pages = round(total_pages / total_users) if total_users > 0 else 0
    
    # Publication year range
    years = [User.publication_year for User in users_db]
    year_range = {
        "earliest": min(years),
        "latest": max(years)
    }
    
    return {
        "total_users": total_users,
        "genres": genre_counts,
        "average_pages": average_pages,
        "publication_year_range": year_range
    }