"""
Enrollment schemas for enrollment management.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class EnrollmentBase(BaseModel):
    """Base enrollment schema."""
    course_id: int


class EnrollmentCreate(EnrollmentBase):
    """Schema for enrollment creation."""
    pass


class EnrollmentUpdate(BaseModel):
    """Schema for enrollment updates."""
    completion_percentage: Optional[float] = None
    last_accessed: Optional[datetime] = None
    is_completed: Optional[bool] = None
    completion_date: Optional[datetime] = None


class EnrollmentResponse(EnrollmentBase):
    """Schema for enrollment response."""
    id: int
    user_id: int
    is_active: bool
    deleted_at: Optional[datetime]
    enrollment_date: datetime
    completion_percentage: float
    last_accessed: Optional[datetime]
    is_completed: bool
    completion_date: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class EnrollmentWithCourse(EnrollmentResponse):
    """Schema for enrollment with course details."""
    course: Optional[dict] = None  # Will be populated with course details


class EnrollmentStats(BaseModel):
    """Schema for enrollment statistics."""
    total_enrollments: int
    completed_courses: int
    in_progress_courses: int
    completion_rate: float  # Percentage
    total_study_time: Optional[float] = None  # In hours
