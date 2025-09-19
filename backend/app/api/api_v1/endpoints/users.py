"""
User management endpoints.
"""

from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core import security
from app.core.database import get_db
from app.models.user import User
from app.schemas.user import UserResponse, UserUpdate
from app.services.user_service import UserService

router = APIRouter()


@router.get("/me", response_model=UserResponse)
def read_user_me(
    current_user: User = Depends(security.get_current_user),
) -> Any:
    """
    Get current user information.
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        UserResponse: Current user information
    """
    return current_user


@router.put("/me", response_model=UserResponse)
def update_user_me(
    *,
    db: Session = Depends(get_db),
    user_in: UserUpdate,
    current_user: User = Depends(security.get_current_user),
) -> Any:
    """
    Update current user information.
    
    Args:
        db: Database session
        user_in: User update data
        current_user: Current authenticated user
        
    Returns:
        UserResponse: Updated user information
        
    Raises:
        HTTPException: If email or username already exists
    """
    user_service = UserService(db)
    try:
        user = user_service.update(db_obj=current_user, obj_in=user_in)
        
        # Convert datetime fields to ISO format strings for response
        user_data = {
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "full_name": user.full_name,
            "is_active": user.is_active,
            "bio": user.bio,
            "learning_goals": user.learning_goals,
            "preferred_categories": user.preferred_categories,
            "skill_level": user.skill_level,
            "time_commitment": user.time_commitment,
            "created_at": user.created_at.isoformat() if user.created_at else None,
            "updated_at": user.updated_at.isoformat() if user.updated_at else None,
            "last_login": user.last_login.isoformat() if user.last_login else None,
        }
        return user_data
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.get("/{user_id}", response_model=UserResponse)
def read_user_by_id(
    user_id: int,
    current_user: User = Depends(security.get_current_user),
    db: Session = Depends(get_db),
) -> Any:
    """
    Get user by ID.
    
    Args:
        user_id: User ID
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        UserResponse: User information
        
    Raises:
        HTTPException: If user not found or access denied
    """
    user_service = UserService(db)
    user = user_service.get(id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this ID does not exist in the system",
        )
    
    # Users can only access their own information
    if user == current_user:
        return user
    
    raise HTTPException(
        status_code=400,
        detail="Not enough permissions"
    )
