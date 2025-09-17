"""
Course schemas for course management.
"""

from typing import Optional, List, Generic, TypeVar
from pydantic import BaseModel
from datetime import datetime

T = TypeVar('T')


class CategoryBase(BaseModel):
    """Base category schema."""
    name: str
    description: Optional[str] = None
    parent_id: Optional[int] = None


class CategoryCreate(CategoryBase):
    """Schema for category creation."""
    pass


class CategoryUpdate(BaseModel):
    """Schema for category updates."""
    name: Optional[str] = None
    description: Optional[str] = None
    parent_id: Optional[int] = None
    is_active: Optional[bool] = None


class CategoryResponse(CategoryBase):
    """Schema for category response."""
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CourseBase(BaseModel):
    """Base course schema."""
    title: str
    description: Optional[str] = None
    short_description: Optional[str] = None
    skills: Optional[str] = None
    instructor: Optional[str] = None
    duration_hours: Optional[int] = None
    difficulty_level: Optional[str] = None
    language: str = "en"
    content_type: Optional[str] = None
    has_certificate: bool = False
    is_free: bool = True
    price: Optional[float] = None
    category_id: Optional[int] = None


class CourseCreate(CourseBase):
    """Schema for course creation."""
    pass


class CourseUpdate(BaseModel):
    """Schema for course updates."""
    title: Optional[str] = None
    description: Optional[str] = None
    short_description: Optional[str] = None
    skills: Optional[str] = None
    instructor: Optional[str] = None
    duration_hours: Optional[int] = None
    difficulty_level: Optional[str] = None
    language: Optional[str] = None
    content_type: Optional[str] = None
    has_certificate: Optional[bool] = None
    is_free: Optional[bool] = None
    price: Optional[float] = None
    category_id: Optional[int] = None
    is_active: Optional[bool] = None
    is_featured: Optional[bool] = None


class CourseResponse(CourseBase):
    """Schema for course response."""
    id: int
    rating: float
    rating_count: int
    enrollment_count: int
    completion_rate: float
    is_active: bool
    is_featured: bool
    created_at: datetime
    updated_at: datetime
    published_at: Optional[datetime] = None
    category: Optional[CategoryResponse] = None

    class Config:
        from_attributes = True


class PaginatedResponse(BaseModel, Generic[T]):
    """Generic paginated response schema."""
    items: List[T]
    total: int
    page: int
    size: int
    pages: int
    has_next: bool
    has_previous: bool
