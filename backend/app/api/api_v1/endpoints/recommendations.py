"""
Recommendation system endpoints.
"""

from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core import security
from app.core.database import get_db
from app.models.user import User
from app.schemas.recommendation import RecommendationResponse, RecommendationRequest
from app.services.recommendation_service import RecommendationService

router = APIRouter()


@router.get("/", response_model=List[RecommendationResponse])
def get_recommendations(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(security.get_current_user),
    limit: int = Query(10, ge=1, le=50, description="Number of recommendations to return"),
    algorithm: str = Query("hybrid", description="Recommendation algorithm to use"),
) -> Any:
    """
    Get personalized course recommendations for the current user.
    
    Args:
        db: Database session
        current_user: Current authenticated user
        limit: Number of recommendations to return
        algorithm: Recommendation algorithm to use
        
    Returns:
        List[RecommendationResponse]: List of recommended courses
    """
    recommendation_service = RecommendationService(db)
    
    try:
        recommendations = recommendation_service.get_recommendations(
            user_id=current_user.id,
            limit=limit,
            algorithm=algorithm
        )
        return recommendations
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate recommendations: {str(e)}"
        )


@router.post("/", response_model=List[RecommendationResponse])
def create_recommendations(
    *,
    db: Session = Depends(get_db),
    recommendation_request: RecommendationRequest,
    current_user: User = Depends(security.get_current_user),
) -> Any:
    """
    Generate recommendations based on specific criteria.
    
    Args:
        db: Database session
        recommendation_request: Recommendation request parameters
        current_user: Current authenticated user
        
    Returns:
        List[RecommendationResponse]: List of recommended courses
    """
    recommendation_service = RecommendationService(db)
    
    try:
        recommendations = recommendation_service.generate_recommendations(
            user_id=current_user.id,
            request=recommendation_request
        )
        return recommendations
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate recommendations: {str(e)}"
        )


@router.post("/feedback")
def submit_recommendation_feedback(
    *,
    db: Session = Depends(get_db),
    course_id: int,
    feedback_type: str = Query(..., description="Type of feedback: like, dislike, view, enroll"),
    current_user: User = Depends(security.get_current_user),
) -> Any:
    """
    Submit feedback for a recommendation to improve future recommendations.
    
    Args:
        db: Database session
        course_id: Course ID
        feedback_type: Type of feedback (like, dislike, view, enroll)
        current_user: Current authenticated user
        
    Returns:
        dict: Success message
    """
    recommendation_service = RecommendationService(db)
    
    try:
        recommendation_service.record_feedback(
            user_id=current_user.id,
            course_id=course_id,
            feedback_type=feedback_type
        )
        return {"message": "Feedback recorded successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to record feedback: {str(e)}"
        )


@router.get("/similar/{course_id}", response_model=List[RecommendationResponse])
def get_similar_courses(
    *,
    db: Session = Depends(get_db),
    course_id: int,
    limit: int = Query(5, ge=1, le=20, description="Number of similar courses to return"),
) -> Any:
    """
    Get courses similar to the specified course.
    
    Args:
        db: Database session
        course_id: Course ID
        limit: Number of similar courses to return
        
    Returns:
        List[RecommendationResponse]: List of similar courses
    """
    recommendation_service = RecommendationService(db)
    
    try:
        similar_courses = recommendation_service.get_similar_courses(
            course_id=course_id,
            limit=limit
        )
        return similar_courses
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to find similar courses: {str(e)}"
        )
