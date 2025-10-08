"""
User management endpoints.
"""

from fastapi import APIRouter, HTTPException, status, Query
from typing import List, Optional
from datetime import datetime
import uuid

from app.models.users import (User, UserRegistration, UserListResponse, UserLogin, ErrorResponse)

router = APIRouter()

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
    # response_model=User,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new User",
    description="Register a new user with automatic validation",
    responses={
        201: {"description": "User created successfully"},
        400: {"model": ErrorResponse, "description": "Invalid User data"},
        #409: {"model": ErrorResponse, "description": "User with given email already exists"},
        422: {"description": "Validation error"}
    }
)
async def create_User(user_data: UserRegistration) -> str:
    """
    Create a new User
    
    - **first_name**: User first name (1-150 characters)
    - **last_name**: User last name (1-100 characters)
    - **email**: Valid email address
    - **password**: Password (8-100 characters, mix of upper, lower, digit, special)
    - **date_of_birth**: Optional date in YYYY-MM-DD format, user must be at least 13 years old
    """

    # Check for duplicate email
    if user_data.email:
        existing_User = next((b for b in users_db if b.email == user_data.email), None)
        if existing_User:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"User with email '{user_data.email}' already exists"
            )
    
    # Create new User
    new_User = User(
        id=get_next_id(),
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        email=user_data.email,
        password=user_data.password,
        date_of_birth=user_data.date_of_birth,
        total_messages=user_data.total_messages,
        created_at=datetime.now()  # se TimestampedModel tiver este campo
    )
    
    users_db.append(new_User)
    return "User registered successfully."



# TODO: ENCRIPTAR AS PASSWORDS e IMPLEMENTAR JWT -------------------------------------------------------------------------------------------------------
@router.post(
        "/login",
        summary="User Authentication",
        description="Authenticate a user and return a token",
)
async def login_user(user_data: UserLogin) -> str:

    """Authenticate user and return a token."""

    existing_user = next((user for user in users_db if (user.email == user_data.email and user.password == user_data.password)), None)

    if existing_user:
        return "User authenticated successfully."
    else:
        return "Invalid credentials."

@router.get(
    "/",
    response_model=UserListResponse,
    summary="Get users with filtering and pagination",
    description="Retrieve users with optional filtering by birth year"
)
async def get_users(
    skip: int = Query(0, ge=0, description="Number of users to skip"),
    limit: int = Query(10, ge=1, le=100, description="Maximum number of users to return"),
    year: Optional[int] = Query(None, ge=1900, le=2024, description="Filter by birth year")
) -> UserListResponse:
    """
    Get a list of users with optional filtering.
    
    Supports pagination and filtering by:
    - **year**: Birth year
    """
    # Apply filters
    filtered_users = users_db.copy()
    
    if year:
        filtered_users = [b for b in filtered_users if b.date_of_birth == year]
    
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