"""
Course management endpoints.
"""

from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core import security
from app.core.database import get_db
from app.models.user import User
from app.schemas.course import CourseResponse, CourseCreate, CourseUpdate, PaginatedResponse, CategoryResponse
from app.services.course_service import CourseService

router = APIRouter()


@router.get("/", response_model=PaginatedResponse[CourseResponse])
def read_courses(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(20, ge=1, le=100, description="Number of records per page"),
    category: str = Query(None, description="Filter by category"),
    search: str = Query(None, description="Search in course title and description"),
) -> Any:
    """
    Retrieve courses with optional filtering and pagination.
    
    Args:
        db: Database session
        page: Page number (1-based)
        size: Number of records per page
        category: Filter by category
        search: Search term
        
    Returns:
        PaginatedResponse[CourseResponse]: Paginated list of courses
    """
    course_service = CourseService(db)
    skip = (page - 1) * size
    
    # Get courses and total count
    courses = course_service.get_multi(
        skip=skip, 
        limit=size, 
        category=category, 
        search=search
    )
    
    # Get total count for pagination
    total = course_service.get_count(category=category, search=search)
    pages = (total + size - 1) // size  # Ceiling division
    
    return PaginatedResponse(
        items=courses,
        total=total,
        page=page,
        size=size,
        pages=pages,
        has_next=page < pages,
        has_previous=page > 1
    )


@router.get("/difficulty-levels")
def get_difficulty_levels(
    db: Session = Depends(get_db),
) -> Any:
    """
    Get all available difficulty levels from courses.
    
    Args:
        db: Database session
        
    Returns:
        List[str]: List of unique difficulty levels
    """
    from app.models.course import Course
    
    # Get unique difficulty levels from courses
    difficulty_levels = db.query(Course.difficulty_level).filter(
        Course.difficulty_level.isnot(None),
        Course.is_active == True
    ).distinct().all()
    
    # Extract the values and sort them
    levels = [level[0] for level in difficulty_levels if level[0]]
    levels.sort()
    
    return levels


@router.get("/categories/", response_model=List[CategoryResponse])
def read_categories(
    db: Session = Depends(get_db),
) -> Any:
    """
    Retrieve all active categories.
    
    Args:
        db: Database session
        
    Returns:
        List[CategoryResponse]: List of active categories
    """
    course_service = CourseService(db)
    categories = course_service.get_categories()
    return categories


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