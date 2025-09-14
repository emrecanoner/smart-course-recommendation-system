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
    """
    user_service = UserService(db)
    user = user_service.update(db_obj=current_user, obj_in=user_in)
    return user


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
