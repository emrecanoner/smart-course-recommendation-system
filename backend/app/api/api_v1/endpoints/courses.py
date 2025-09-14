"""
Course management endpoints.
"""

from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core import security
from app.core.database import get_db
from app.models.user import User
from app.schemas.course import CourseResponse, CourseCreate, CourseUpdate
from app.services.course_service import CourseService

router = APIRouter()


@router.get("/", response_model=List[CourseResponse])
def read_courses(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    category: str = Query(None, description="Filter by category"),
    search: str = Query(None, description="Search in course title and description"),
) -> Any:
    """
    Retrieve courses with optional filtering and pagination.
    
    Args:
        db: Database session
        skip: Number of records to skip
        limit: Number of records to return
        category: Filter by category
        search: Search term
        
    Returns:
        List[CourseResponse]: List of courses
    """
    course_service = CourseService(db)
    courses = course_service.get_multi(
        skip=skip, 
        limit=limit, 
        category=category, 
        search=search
    )
    return courses


@router.get("/{course_id}", response_model=CourseResponse)
def read_course(
    *,
    db: Session = Depends(get_db),
    course_id: int,
) -> Any:
    """
    Get course by ID.
    
    Args:
        db: Database session
        course_id: Course ID
        
    Returns:
        CourseResponse: Course information
        
    Raises:
        HTTPException: If course not found
    """
    course_service = CourseService(db)
    course = course_service.get(id=course_id)
    if not course:
        raise HTTPException(
            status_code=404,
            detail="The course with this ID does not exist in the system",
        )
    return course


@router.post("/", response_model=CourseResponse)
def create_course(
    *,
    db: Session = Depends(get_db),
    course_in: CourseCreate,
    current_user: User = Depends(security.get_current_user),
) -> Any:
    """
    Create new course (admin only).
    
    Args:
        db: Database session
        course_in: Course creation data
        current_user: Current authenticated user
        
    Returns:
        CourseResponse: Created course information
        
    Raises:
        HTTPException: If user is not admin
    """
    # TODO: Add admin role check
    course_service = CourseService(db)
    course = course_service.create(obj_in=course_in)
    return course


@router.put("/{course_id}", response_model=CourseResponse)
def update_course(
    *,
    db: Session = Depends(get_db),
    course_id: int,
    course_in: CourseUpdate,
    current_user: User = Depends(security.get_current_user),
) -> Any:
    """
    Update course (admin only).
    
    Args:
        db: Database session
        course_id: Course ID
        course_in: Course update data
        current_user: Current authenticated user
        
    Returns:
        CourseResponse: Updated course information
        
    Raises:
        HTTPException: If course not found or user is not admin
    """
    # TODO: Add admin role check
    course_service = CourseService(db)
    course = course_service.get(id=course_id)
    if not course:
        raise HTTPException(
            status_code=404,
            detail="The course with this ID does not exist in the system",
        )
    
    course = course_service.update(db_obj=course, obj_in=course_in)
    return course
