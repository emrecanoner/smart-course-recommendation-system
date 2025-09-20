"""
Analytics endpoints for data warehouse and reporting.
"""

from typing import Dict, List, Optional, Any
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
import logging

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.services.analytics_service import AnalyticsService
from app.services.interaction_tracking_service import InteractionTrackingService
from app.services.user_preference_service import UserPreferenceService

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/track/course-view")
async def track_course_view(
    course_id: int,
    session_id: Optional[str] = None,
    device_type: Optional[str] = None,
    referrer: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Track when a user views a course.
    
    Args:
        course_id: Course ID
        session_id: Session ID
        device_type: Device type
        referrer: Referrer URL
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Dict: Tracking result
    """
    try:
        tracking_service = InteractionTrackingService(db)
        success = tracking_service.track_course_view(
            user_id=current_user.id,
            course_id=course_id,
            session_id=session_id,
            device_type=device_type,
            referrer=referrer
        )
        
        if success:
            return {
                "message": "Course view tracked successfully",
                "user_id": current_user.id,
                "course_id": course_id,
                "timestamp": "now"
            }
        else:
            raise HTTPException(status_code=400, detail="Failed to track course view")
            
    except Exception as e:
        logger.error(f"Error tracking course view: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/track/course-like")
async def track_course_like(
    course_id: int,
    session_id: Optional[str] = None,
    device_type: Optional[str] = None,
    referrer: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """Track when a user likes a course."""
    try:
        tracking_service = InteractionTrackingService(db)
        success = tracking_service.track_course_like(
            user_id=current_user.id,
            course_id=course_id,
            session_id=session_id,
            device_type=device_type,
            referrer=referrer
        )
        
        if success:
            return {
                "message": "Course like tracked successfully",
                "user_id": current_user.id,
                "course_id": course_id
            }
        else:
            raise HTTPException(status_code=400, detail="Failed to track course like")
            
    except Exception as e:
        logger.error(f"Error tracking course like: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/track/course-unlike")
async def track_course_unlike(
    course_id: int,
    session_id: Optional[str] = None,
    device_type: Optional[str] = None,
    referrer: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """Track when a user unlikes/unfavorites a course."""
    try:
        tracking_service = InteractionTrackingService(db)
        success = tracking_service.track_course_unlike(
            user_id=current_user.id,
            course_id=course_id,
            session_id=session_id,
            device_type=device_type,
            referrer=referrer
        )
        
        if success:
            return {
                "message": "Course unlike tracked successfully",
                "user_id": current_user.id,
                "course_id": course_id
            }
        else:
            raise HTTPException(status_code=400, detail="Failed to track course unlike")
            
    except Exception as e:
        logger.error(f"Error tracking course unlike: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/track/course-enroll")
async def track_course_enroll(
    course_id: int,
    session_id: Optional[str] = None,
    device_type: Optional[str] = None,
    referrer: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """Track when a user enrolls in a course."""
    try:
        tracking_service = InteractionTrackingService(db)
        success = tracking_service.track_course_enroll(
            user_id=current_user.id,
            course_id=course_id,
            session_id=session_id,
            device_type=device_type,
            referrer=referrer
        )
        
        if success:
            return {
                "message": "Course enrollment tracked successfully",
                "user_id": current_user.id,
                "course_id": course_id
            }
        else:
            raise HTTPException(status_code=400, detail="Failed to track course enrollment")
            
    except Exception as e:
        logger.error(f"Error tracking course enrollment: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/track/course-unenroll")
async def track_course_unenroll(
    course_id: int,
    session_id: Optional[str] = None,
    device_type: Optional[str] = None,
    referrer: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """Track when a user unenrolls from a course."""
    try:
        tracking_service = InteractionTrackingService(db)
        success = tracking_service.track_course_unenroll(
            user_id=current_user.id,
            course_id=course_id,
            session_id=session_id,
            device_type=device_type,
            referrer=referrer
        )
        
        if success:
            return {
                "message": "Course unenrollment tracked successfully",
                "user_id": current_user.id,
                "course_id": course_id
            }
        else:
            raise HTTPException(status_code=400, detail="Failed to track course unenrollment")
            
    except Exception as e:
        logger.error(f"Error tracking course unenrollment: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/track/course-complete")
async def track_course_complete(
    course_id: int,
    completion_percentage: float,
    session_id: Optional[str] = None,
    device_type: Optional[str] = None,
    referrer: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """Track when a user completes a course."""
    try:
        tracking_service = InteractionTrackingService(db)
        success = tracking_service.track_course_complete(
            user_id=current_user.id,
            course_id=course_id,
            completion_percentage=completion_percentage,
            session_id=session_id,
            device_type=device_type,
            referrer=referrer
        )
        
        if success:
            return {
                "message": "Course completion tracked successfully",
                "user_id": current_user.id,
                "course_id": course_id,
                "completion_percentage": completion_percentage
            }
        else:
            raise HTTPException(status_code=400, detail="Failed to track course completion")
            
    except Exception as e:
        logger.error(f"Error tracking course completion: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/track/course-rate")
async def track_course_rate(
    course_id: int,
    rating: float,
    session_id: Optional[str] = None,
    device_type: Optional[str] = None,
    referrer: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """Track when a user rates a course."""
    try:
        if not (1.0 <= rating <= 5.0):
            raise HTTPException(status_code=400, detail="Rating must be between 1.0 and 5.0")
        
        tracking_service = InteractionTrackingService(db)
        success = tracking_service.track_course_rate(
            user_id=current_user.id,
            course_id=course_id,
            rating=rating,
            session_id=session_id,
            device_type=device_type,
            referrer=referrer
        )
        
        if success:
            return {
                "message": "Course rating tracked successfully",
                "user_id": current_user.id,
                "course_id": course_id,
                "rating": rating
            }
        else:
            raise HTTPException(status_code=400, detail="Failed to track course rating")
            
    except Exception as e:
        logger.error(f"Error tracking course rating: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/user/interaction-summary")
async def get_user_interaction_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """Get user's interaction summary."""
    try:
        tracking_service = InteractionTrackingService(db)
        summary = tracking_service.get_user_interaction_summary(current_user.id)
        
        return {
            "user_id": current_user.id,
            "summary": summary
        }
        
    except Exception as e:
        logger.error(f"Error getting user interaction summary: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/user/preferences")
async def get_user_preferences(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """Get user's preferences."""
    try:
        pref_service = UserPreferenceService(db)
        preferences = pref_service.get_user_preferences(current_user.id)
        
        return {
            "user_id": current_user.id,
            "preferences": preferences
        }
        
    except Exception as e:
        logger.error(f"Error getting user preferences: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/user/preferences")
async def update_user_preferences(
    preferences: Dict[str, Any],
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """Update user's explicit preferences."""
    try:
        pref_service = UserPreferenceService(db)
        success = pref_service.update_explicit_preferences(current_user.id, preferences)
        
        if success:
            return {
                "message": "Preferences updated successfully",
                "user_id": current_user.id
            }
        else:
            raise HTTPException(status_code=400, detail="Failed to update preferences")
            
    except Exception as e:
        logger.error(f"Error updating user preferences: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/user/learn-preferences")
async def learn_user_preferences(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """Learn user preferences from interactions."""
    try:
        pref_service = UserPreferenceService(db)
        learned_prefs = pref_service.learn_from_interactions(current_user.id)
        
        return {
            "message": "Preferences learned from interactions",
            "user_id": current_user.id,
            "learned_preferences": learned_prefs
        }
        
    except Exception as e:
        logger.error(f"Error learning user preferences: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/user/learning-profile")
async def get_user_learning_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """Get user's learning profile from analytics."""
    try:
        analytics_service = AnalyticsService(db)
        
        # Update profile first
        analytics_service.update_user_learning_profile(current_user.id)
        
        # Get updated profile
        profile = analytics_service.generate_user_report(current_user.id)
        
        return {
            "user_id": current_user.id,
            "learning_profile": profile
        }
        
    except Exception as e:
        logger.error(f"Error getting user learning profile: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/user/insights")
async def get_user_insights(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """Get AI-driven insights about user."""
    try:
        pref_service = UserPreferenceService(db)
        insights = pref_service.get_preference_insights(current_user.id)
        
        return {
            "user_id": current_user.id,
            "insights": insights
        }
        
    except Exception as e:
        logger.error(f"Error getting user insights: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/course/{course_id}/interaction-stats")
async def get_course_interaction_stats(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """Get interaction statistics for a course."""
    try:
        tracking_service = InteractionTrackingService(db)
        stats = tracking_service.get_course_interaction_stats(course_id)
        
        return {
            "course_id": course_id,
            "interaction_stats": stats
        }
        
    except Exception as e:
        logger.error(f"Error getting course interaction stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/system/analytics")
async def get_system_analytics(
    days: int = Query(30, ge=1, le=365),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """Get system-wide analytics (admin only)."""
    try:
        # Check if user is admin
        if not current_user.is_superuser:
            raise HTTPException(status_code=403, detail="Only administrators can access system analytics")
        
        analytics_service = AnalyticsService(db)
        analytics = analytics_service.get_system_analytics(days)
        
        return analytics
        
    except Exception as e:
        logger.error(f"Error getting system analytics: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/system/update-all-profiles")
async def update_all_user_profiles(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """Update analytics profiles for all users (admin only)."""
    try:
        # Check if user is admin
        if not current_user.is_superuser:
            raise HTTPException(status_code=403, detail="Only administrators can update all profiles")
        
        analytics_service = AnalyticsService(db)
        
        # Get all users
        from app.models.user import User
        users = db.query(User).all()
        
        updated_count = 0
        for user in users:
            try:
                analytics_service.update_user_learning_profile(user.id)
                updated_count += 1
            except Exception as e:
                logger.error(f"Error updating profile for user {user.id}: {e}")
        
        return {
            "message": f"Updated profiles for {updated_count} users",
            "total_users": len(users),
            "updated_count": updated_count
        }
        
    except Exception as e:
        logger.error(f"Error updating all user profiles: {e}")
        raise HTTPException(status_code=500, detail=str(e))
