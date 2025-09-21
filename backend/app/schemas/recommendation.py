"""
Recommendation schemas for recommendation system.
"""

from typing import Optional, List
from pydantic import BaseModel


class RecommendationRequest(BaseModel):
    """Schema for recommendation request."""
    limit: int = 10
    algorithm: str = "hybrid"
    category: Optional[str] = None
    difficulty_level: Optional[str] = None
    max_duration_hours: Optional[int] = None
    content_type: Optional[str] = None


class RecommendationResponse(BaseModel):
    """Schema for recommendation response."""
    course_id: int
    title: str
    description: Optional[str] = None
    short_description: Optional[str] = None
    instructor: Optional[str] = None
    duration_hours: Optional[int] = None
    difficulty_level: Optional[str] = None
    rating: float
    rating_count: int
    enrollment_count: int
    is_free: bool
    price: Optional[float] = None
    confidence_score: float
    recommendation_reason: Optional[str] = None
    category_name: Optional[str] = None

    class Config:
        from_attributes = True


class RecommendationFeedback(BaseModel):
    """Schema for recommendation feedback."""
    course_id: int
    feedback_type: str  # like, dislike, view, enroll, ignore
    rating: Optional[float] = None
    time_spent_minutes: Optional[int] = None
    progress_percentage: Optional[float] = None
