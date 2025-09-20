"""
Recommendation service for AI-powered course recommendations.
"""

from typing import Any, Dict, List, Optional, Union
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc
import logging
import os
import sys

from app.models.course import Course
from app.models.recommendation import Recommendation, RecommendationLog
from app.models.interaction import UserInteraction
from app.schemas.recommendation import RecommendationRequest, RecommendationResponse

# Import AI recommendation engine
try:
    # Add AI-ML path to sys.path
    ai_ml_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'ai-ml', 'inference')
    if ai_ml_path not in sys.path:
        sys.path.append(ai_ml_path)
    
    from recommendation_engine import AIRecommendationEngine
    AI_AVAILABLE = True
except ImportError as e:
    logging.warning(f"AI recommendation engine not available: {e}")
    AI_AVAILABLE = False

logger = logging.getLogger(__name__)


class RecommendationService:
    """Service class for recommendation operations."""
    
    def __init__(self, db: Session):
        self.db = db
        self.ai_engine = None
        
        # Initialize AI engine if available
        if AI_AVAILABLE:
            try:
                self.ai_engine = AIRecommendationEngine(db)
                logger.info("AI recommendation engine initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize AI engine: {e}")
                self.ai_engine = None
    
    def get_recommendations(
        self, 
        user_id: int, 
        limit: int = 10, 
        algorithm: str = "hybrid"
    ) -> List[RecommendationResponse]:
        """
        Get personalized recommendations for a user.
        
        Args:
            user_id: User ID
            limit: Number of recommendations to return
            algorithm: Algorithm to use (collaborative, content-based, hybrid)
            
        Returns:
            List[RecommendationResponse]: List of recommendations
        """
        # Use AI engine if available
        if self.ai_engine:
            try:
                logger.info(f"Using AI engine for recommendations for user {user_id}")
                return self.ai_engine.get_recommendations(user_id, limit, algorithm)
            except Exception as e:
                logger.error(f"AI engine failed, falling back to basic recommendations: {e}")
        
        # Fallback to basic recommendations
        logger.info(f"Using basic recommendations for user {user_id}")
        return self._get_basic_recommendations(user_id, limit)
    
    def _get_basic_recommendations(
        self, 
        user_id: int, 
        limit: int
    ) -> List[RecommendationResponse]:
        """
        Get basic recommendations as fallback.
        
        Args:
            user_id: User ID
            limit: Number of recommendations to return
            
        Returns:
            List[RecommendationResponse]: List of recommendations
        """
        # Get user's interaction history
        user_interactions = self.db.query(UserInteraction).filter(
            UserInteraction.user_id == user_id
        ).all()
        
        # Get courses the user hasn't interacted with
        interacted_course_ids = [interaction.course_id for interaction in user_interactions]
        
        # Get popular courses that user hasn't seen
        recommendations = self.db.query(Course).filter(
            and_(
                Course.is_active == True,
                ~Course.id.in_(interacted_course_ids)
            )
        ).order_by(desc(Course.rating)).limit(limit).all()
        
        # Convert to response format
        result = []
        for course in recommendations:
            result.append(RecommendationResponse(
                course_id=course.id,
                title=course.title,
                description=course.description,
                short_description=course.short_description,
                instructor=course.instructor,
                duration_hours=course.duration_hours,
                difficulty_level=course.difficulty_level,
                rating=course.rating,
                rating_count=course.rating_count,
                enrollment_count=course.enrollment_count,
                is_free=course.is_free,
                price=course.price,
                confidence_score=0.8,  # Placeholder confidence score
                recommendation_reason=f"Popular course with {course.rating:.1f} rating",
                category_name=course.category.name if course.category else None
            ))
        
        return result
    
    def generate_recommendations(
        self, 
        user_id: int, 
        request: RecommendationRequest
    ) -> List[RecommendationResponse]:
        """
        Generate recommendations based on specific criteria.
        
        Args:
            user_id: User ID
            request: Recommendation request parameters
            
        Returns:
            List[RecommendationResponse]: List of recommendations
        """
        # Build query based on request parameters
        query = self.db.query(Course).filter(Course.is_active == True)
        
        if request.categories:
            from app.models.course import Category
            query = query.join(Category).filter(Category.name.in_(request.categories))
        
        if request.difficulty_level:
            query = query.filter(Course.difficulty_level == request.difficulty_level)
        
        if request.max_duration_hours:
            query = query.filter(Course.duration_hours <= request.max_duration_hours)
        
        if request.content_type:
            query = query.filter(Course.content_type == request.content_type)
        
        # Get recommendations
        courses = query.order_by(desc(Course.rating)).limit(request.limit).all()
        
        # Convert to response format
        result = []
        for course in courses:
            result.append(RecommendationResponse(
                course_id=course.id,
                title=course.title,
                description=course.description,
                short_description=course.short_description,
                instructor=course.instructor,
                duration_hours=course.duration_hours,
                difficulty_level=course.difficulty_level,
                rating=course.rating,
                rating_count=course.rating_count,
                enrollment_count=course.enrollment_count,
                is_free=course.is_free,
                price=course.price,
                confidence_score=0.7,  # Placeholder confidence score
                recommendation_reason=f"Matches your criteria",
                category_name=course.category.name if course.category else None
            ))
        
        return result
    
    def get_similar_courses(
        self, 
        course_id: int, 
        limit: int = 5
    ) -> List[RecommendationResponse]:
        """
        Get courses similar to the specified course.
        
        Args:
            course_id: Course ID
            limit: Number of similar courses to return
            
        Returns:
            List[RecommendationResponse]: List of similar courses
        """
        # Use AI engine if available
        if self.ai_engine:
            try:
                logger.info(f"Using AI engine for similar courses for course {course_id}")
                return self.ai_engine.get_similar_courses(course_id, limit)
            except Exception as e:
                logger.error(f"AI engine failed for similar courses, falling back to basic: {e}")
        
        # Fallback to basic similar courses
        return self._get_basic_similar_courses(course_id, limit)
    
    def _get_basic_similar_courses(
        self, 
        course_id: int, 
        limit: int
    ) -> List[RecommendationResponse]:
        """
        Get basic similar courses as fallback.
        
        Args:
            course_id: Course ID
            limit: Number of similar courses to return
            
        Returns:
            List[RecommendationResponse]: List of similar courses
        """
        # Get the target course
        target_course = self.db.query(Course).filter(Course.id == course_id).first()
        if not target_course:
            return []
        
        # Find similar courses based on category and difficulty
        similar_courses = self.db.query(Course).filter(
            and_(
                Course.is_active == True,
                Course.id != course_id,
                Course.category_id == target_course.category_id,
                Course.difficulty_level == target_course.difficulty_level
            )
        ).order_by(desc(Course.rating)).limit(limit).all()
        
        # Convert to response format
        result = []
        for course in similar_courses:
            result.append(RecommendationResponse(
                course_id=course.id,
                title=course.title,
                description=course.description,
                short_description=course.short_description,
                instructor=course.instructor,
                duration_hours=course.duration_hours,
                difficulty_level=course.difficulty_level,
                rating=course.rating,
                rating_count=course.rating_count,
                enrollment_count=course.enrollment_count,
                is_free=course.is_free,
                price=course.price,
                confidence_score=0.6,  # Placeholder confidence score
                recommendation_reason=f"Similar to {target_course.title}",
                category_name=course.category.name if course.category else None
            ))
        
        return result
    
    def record_feedback(
        self, 
        user_id: int, 
        course_id: int, 
        feedback_type: str
    ) -> None:
        """
        Record user feedback for a recommendation.
        
        Args:
            user_id: User ID
            course_id: Course ID
            feedback_type: Type of feedback
        """
        # Use AI engine if available
        if self.ai_engine:
            try:
                self.ai_engine.record_user_feedback(user_id, course_id, feedback_type)
                return
            except Exception as e:
                logger.error(f"AI engine failed to record feedback, using basic method: {e}")
        
        # Fallback to basic feedback recording
        self._record_basic_feedback(user_id, course_id, feedback_type)
    
    def _record_basic_feedback(
        self, 
        user_id: int, 
        course_id: int, 
        feedback_type: str
    ) -> None:
        """
        Record user feedback using basic method.
        
        Args:
            user_id: User ID
            course_id: Course ID
            feedback_type: Type of feedback
        """
        # Create user interaction record
        interaction = UserInteraction(
            user_id=user_id,
            course_id=course_id,
            interaction_type=feedback_type
        )
        self.db.add(interaction)
        
        # Update recommendation feedback if exists
        recommendation = self.db.query(Recommendation).filter(
            and_(
                Recommendation.user_id == user_id,
                Recommendation.course_id == course_id,
                Recommendation.is_active == True
            )
        ).first()
        
        if recommendation:
            recommendation.user_feedback = feedback_type
            self.db.add(recommendation)
        
        self.db.commit()
    
    def log_recommendation_request(
        self,
        user_id: Optional[int],
        algorithm: str,
        number_of_recommendations: int,
        processing_time_ms: int,
        recommendations_generated: int,
        error_occurred: bool = False,
        error_message: Optional[str] = None
    ) -> None:
        """
        Log recommendation request for analytics.
        
        Args:
            user_id: User ID (optional for anonymous users)
            algorithm: Algorithm used
            number_of_recommendations: Number requested
            processing_time_ms: Processing time in milliseconds
            recommendations_generated: Number actually generated
            error_occurred: Whether an error occurred
            error_message: Error message if any
        """
        log_entry = RecommendationLog(
            user_id=user_id,
            algorithm_used=algorithm,
            number_of_recommendations=number_of_recommendations,
            processing_time_ms=processing_time_ms,
            recommendations_generated=recommendations_generated,
            error_occurred=error_occurred,
            error_message=error_message
        )
        self.db.add(log_entry)
        self.db.commit()
