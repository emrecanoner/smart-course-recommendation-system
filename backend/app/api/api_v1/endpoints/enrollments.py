"""
Enrollment management endpoints.
"""

from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core import security
from app.core.database import get_db
from app.models.user import User
from app.schemas.enrollment import (
    EnrollmentResponse, 
    EnrollmentCreate, 
    EnrollmentWithCourse, 
    EnrollmentUpdate,
    EnrollmentStats
)
from app.services.enrollment_service import EnrollmentService

router = APIRouter()


@router.get("/", response_model=List[EnrollmentWithCourse])
def read_user_enrollments(
    db: Session = Depends(get_db),
    current_user: User = Depends(security.get_current_user),
) -> Any:
    """
    Retrieve user's enrolled courses.
    
    Args:
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        List[EnrollmentWithCourse]: List of user's enrolled courses
    """
    enrollment_service = EnrollmentService(db)
    enrollments = enrollment_service.get_user_enrollments(current_user.id)
    
    # Add course details to each enrollment
    result = []
    for enrollment in enrollments:
        enrollment_dict = {
            "id": enrollment.id,
            "user_id": enrollment.user_id,
            "course_id": enrollment.course_id,
            "is_active": enrollment.is_active,
            "deleted_date": enrollment.deleted_date,
            "enrollment_date": enrollment.enrollment_date,
            "completion_percentage": enrollment.completion_percentage,
            "last_accessed": enrollment.last_accessed,
            "is_completed": enrollment.is_completed,
            "completion_date": enrollment.completion_date,
            "created_at": enrollment.created_at,
            "updated_at": enrollment.updated_at,
            "course": {
                "id": enrollment.course.id,
                "title": enrollment.course.title,
                "description": enrollment.course.description,
                "short_description": enrollment.course.short_description,
                "skills": enrollment.course.skills,
                "instructor": enrollment.course.instructor,
                "duration_hours": enrollment.course.duration_hours,
                "difficulty_level": enrollment.course.difficulty_level,
                "rating": enrollment.course.rating,
                "rating_count": enrollment.course.rating_count,
                "enrollment_count": enrollment.course.enrollment_count,
                "is_free": enrollment.course.is_free,
                "price": enrollment.course.price,
                "category": {
                    "id": enrollment.course.category.id if enrollment.course.category else None,
                    "name": enrollment.course.category.name if enrollment.course.category else None,
                } if enrollment.course.category else None,
            }
        }
        result.append(enrollment_dict)
    
    return result


@router.post("/", response_model=EnrollmentResponse)
def create_enrollment(
    *,
    db: Session = Depends(get_db),
    enrollment_in: EnrollmentCreate,
    current_user: User = Depends(security.get_current_user),
) -> Any:
    """
    Enroll in a course.
    
    Args:
        db: Database session
        enrollment_in: Enrollment creation data
        current_user: Current authenticated user
        
    Returns:
        EnrollmentResponse: Created enrollment
    """
    enrollment_service = EnrollmentService(db)
    
    # Check if already enrolled
    if enrollment_service.is_enrolled(current_user.id, enrollment_in.course_id):
        raise HTTPException(
            status_code=400,
            detail="Already enrolled in this course"
        )
    
    enrollment = enrollment_service.create(obj_in=enrollment_in, user_id=current_user.id)
    return enrollment


@router.get("/check/{course_id}")
def check_enrollment(
    *,
    db: Session = Depends(get_db),
    course_id: int,
    current_user: User = Depends(security.get_current_user),
) -> Any:
    """
    Check if user is enrolled in a course.
    
    Args:
        db: Database session
        course_id: Course ID to check
        current_user: Current authenticated user
        
    Returns:
        dict: Enrollment status
    """
    enrollment_service = EnrollmentService(db)
    is_enrolled = enrollment_service.is_enrolled(current_user.id, course_id)
    
    return {"is_enrolled": is_enrolled}


@router.put("/progress/{course_id}")
def update_progress(
    *,
    db: Session = Depends(get_db),
    course_id: int,
    completion_percentage: float,
    current_user: User = Depends(security.get_current_user),
) -> Any:
    """
    Update course progress.
    
    Args:
        db: Database session
        course_id: Course ID
        completion_percentage: Completion percentage (0.0 to 100.0)
        current_user: Current authenticated user
        
    Returns:
        dict: Success message and updated enrollment
    """
    enrollment_service = EnrollmentService(db)
    
    # Check if enrolled
    if not enrollment_service.is_enrolled(current_user.id, course_id):
        raise HTTPException(
            status_code=404,
            detail="Not enrolled in this course"
        )
    
    enrollment = enrollment_service.update_progress(
        current_user.id, 
        course_id, 
        completion_percentage
    )
    
    if not enrollment:
        raise HTTPException(
            status_code=404,
            detail="Enrollment not found"
        )
    
    return {
        "message": "Progress updated successfully",
        "enrollment": enrollment
    }


@router.delete("/{course_id}")
def unenroll_from_course(
    *,
    db: Session = Depends(get_db),
    course_id: int,
    current_user: User = Depends(security.get_current_user),
) -> Any:
    """
    Unenroll from a course.
    
    Args:
        db: Database session
        course_id: Course ID to unenroll from
        current_user: Current authenticated user
        
    Returns:
        dict: Success message
    """
    enrollment_service = EnrollmentService(db)
    
    # Check if enrolled
    if not enrollment_service.is_enrolled(current_user.id, course_id):
        raise HTTPException(
            status_code=404,
            detail="Not enrolled in this course"
        )
    
    enrollment = enrollment_service.unenroll(current_user.id, course_id)
    
    if not enrollment:
        raise HTTPException(
            status_code=404,
            detail="Enrollment not found"
        )
    
    return {"message": "Successfully unenrolled from course"}


@router.get("/stats", response_model=EnrollmentStats)
def get_user_stats(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(security.get_current_user),
) -> Any:
    """
    Get user enrollment statistics.
    
    Args:
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        EnrollmentStats: User enrollment statistics
    """
    enrollment_service = EnrollmentService(db)
    stats = enrollment_service.get_user_stats(current_user.id)
    return stats
