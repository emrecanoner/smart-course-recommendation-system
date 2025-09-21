"""
AI-powered recommendation engine for course recommendations.
"""

import os
import sys
import logging
import numpy as np
import pandas as pd
from typing import List, Dict, Optional, Tuple
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import text

# Add backend path for imports
backend_path = os.path.join(os.path.dirname(__file__), '..', '..', 'backend')
if backend_path not in sys.path:
    sys.path.append(backend_path)

from app.models.course import Course
from app.models.interaction import UserInteraction
from app.models.enrollment import Enrollment
from app.schemas.recommendation import RecommendationResponse

logger = logging.getLogger(__name__)


class AIRecommendationEngine:
    """
    AI-powered recommendation engine that uses multiple algorithms
    to provide personalized course recommendations.
    """
    
    def __init__(self, db: Session):
        self.db = db
        self.min_interactions_for_ai = 5  # Minimum interactions needed for AI recommendations
        self.min_enrollments_for_ai = 2   # Minimum enrollments needed for AI recommendations
        
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
        try:
            # Check if user has enough data for AI recommendations
            if not self._has_sufficient_data(user_id):
                logger.info(f"User {user_id} has insufficient data for AI recommendations")
                return self._get_fallback_recommendations(user_id, limit)
            
            # Get user profile and preferences
            user_profile = self._get_user_profile(user_id)
            
            # Generate recommendations based on algorithm
            if algorithm == "collaborative":
                recommendations = self._collaborative_filtering(user_id, limit, user_profile)
            elif algorithm == "content":
                recommendations = self._content_based_filtering(user_id, limit, user_profile)
            elif algorithm == "hybrid":
                recommendations = self._hybrid_recommendations(user_id, limit, user_profile)
            else:
                recommendations = self._hybrid_recommendations(user_id, limit, user_profile)
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Error generating AI recommendations for user {user_id}: {e}")
            return self._get_fallback_recommendations(user_id, limit)
    
    def _has_sufficient_data(self, user_id: int) -> bool:
        """
        Check if user has sufficient data for AI recommendations.
        
        Args:
            user_id: User ID
            
        Returns:
            bool: True if user has sufficient data
        """
        # Count user interactions
        interaction_count = self.db.query(UserInteraction).filter(
            UserInteraction.user_id == user_id
        ).count()
        
        # Count user enrollments
        enrollment_count = self.db.query(Enrollment).filter(
            Enrollment.user_id == user_id,
            Enrollment.deleted_date.is_(None)
        ).count()
        
        # Check if user has enough data
        has_sufficient_interactions = interaction_count >= self.min_interactions_for_ai
        has_sufficient_enrollments = enrollment_count >= self.min_enrollments_for_ai
        
        logger.info(f"User {user_id} data check: interactions={interaction_count}, enrollments={enrollment_count}")
        
        return has_sufficient_interactions or has_sufficient_enrollments
    
    def _get_user_profile(self, user_id: int) -> Dict:
        """
        Get user profile and preferences from analytics.
        
        Args:
            user_id: User ID
            
        Returns:
            Dict: User profile data
        """
        try:
            # Get user learning profile from analytics
            profile_query = text("""
                SELECT 
                    preferred_categories,
                    preferred_difficulty_levels,
                    preferred_content_types,
                    preferred_durations,
                    learning_goals,
                    skills_developed,
                    engagement_score,
                    learning_velocity,
                    total_courses_viewed,
                    total_courses_enrolled,
                    total_courses_completed,
                    total_courses_rated,
                    total_courses_liked,
                    total_courses_unliked
                FROM analytics.user_learning_profile 
                WHERE user_id = :user_id
            """)
            
            result = self.db.execute(profile_query, {"user_id": user_id}).fetchone()
            
            if result:
                return {
                    'preferred_categories': result.preferred_categories or [],
                    'preferred_difficulty_levels': result.preferred_difficulty_levels or {},
                    'preferred_content_types': result.preferred_content_types or {},
                    'preferred_durations': result.preferred_durations or {},
                    'learning_goals': result.learning_goals or [],
                    'skills_developed': result.skills_developed or [],
                    'engagement_score': result.engagement_score or 0,
                    'learning_velocity': result.learning_velocity or 0,
                    'total_courses_viewed': result.total_courses_viewed or 0,
                    'total_courses_enrolled': result.total_courses_enrolled or 0,
                    'total_courses_completed': result.total_courses_completed or 0,
                    'total_courses_rated': result.total_courses_rated or 0,
                    'total_courses_liked': result.total_courses_liked or 0,
                    'total_courses_unliked': result.total_courses_unliked or 0
                }
            else:
                return self._get_basic_user_profile(user_id)
                
        except Exception as e:
            logger.error(f"Error getting user profile for user {user_id}: {e}")
            return self._get_basic_user_profile(user_id)
    
    def _get_basic_user_profile(self, user_id: int) -> Dict:
        """
        Get basic user profile from interactions.
        
        Args:
            user_id: User ID
            
        Returns:
            Dict: Basic user profile
        """
        # Get user's interaction history
        interactions = self.db.query(UserInteraction).filter(
            UserInteraction.user_id == user_id
        ).all()
        
        # Get user's enrollment history
        enrollments = self.db.query(Enrollment).filter(
            Enrollment.user_id == user_id,
            Enrollment.deleted_date.is_(None)
        ).all()
        
        # Analyze preferences from interactions
        categories = {}
        difficulty_levels = {}
        content_types = {}
        durations = {}
        
        for interaction in interactions:
            course = interaction.course
            if course:
                # Category preference
                if course.category:
                    categories[course.category.name] = categories.get(course.category.name, 0) + 1
                
                # Difficulty preference
                if course.difficulty_level:
                    difficulty_levels[course.difficulty_level] = difficulty_levels.get(course.difficulty_level, 0) + 1
                
                # Content type preference
                if course.content_type:
                    content_types[course.content_type] = content_types.get(course.content_type, 0) + 1
                
                # Duration preference
                if course.duration_hours:
                    duration_range = self._get_duration_range(course.duration_hours)
                    durations[duration_range] = durations.get(duration_range, 0) + 1
        
        return {
            'preferred_categories': list(categories.keys())[:5],
            'preferred_difficulty_levels': difficulty_levels,
            'preferred_content_types': content_types,
            'preferred_durations': durations,
            'learning_goals': [],
            'skills_developed': [],
            'engagement_score': len(interactions) * 0.5,
            'learning_velocity': len([e for e in enrollments if e.is_completed]) * 0.5,
            'total_courses_viewed': len([i for i in interactions if i.interaction_type == 'view']),
            'total_courses_enrolled': len(enrollments),
            'total_courses_completed': len([e for e in enrollments if e.is_completed]),
            'total_courses_rated': len([i for i in interactions if i.interaction_type == 'rate']),
            'total_courses_liked': len([i for i in interactions if i.interaction_type == 'like']),
            'total_courses_unliked': len([i for i in interactions if i.interaction_type == 'unlike'])
        }
    
    def _get_duration_range(self, duration_hours: float) -> str:
        """Get duration range category."""
        if duration_hours <= 2:
            return "short"
        elif duration_hours <= 8:
            return "medium"
        else:
            return "long"
    
    def _collaborative_filtering(self, user_id: int, limit: int, user_profile: Dict) -> List[RecommendationResponse]:
        """
        Collaborative filtering based on similar users.
        
        Args:
            user_id: User ID
            limit: Number of recommendations
            user_profile: User profile data
            
        Returns:
            List[RecommendationResponse]: Recommendations
        """
        try:
            # Find similar users based on interaction patterns
            similar_users_query = text("""
                WITH user_similarity AS (
                    SELECT 
                        u2.user_id,
                        COUNT(*) as common_interactions,
                        AVG(ABS(u1.engagement_score - u2.engagement_score)) as engagement_diff
                    FROM analytics.user_learning_profile u1
                    JOIN analytics.user_learning_profile u2 ON u1.user_id != u2.user_id
                    WHERE u1.user_id = :user_id
                    AND u1.preferred_categories && u2.preferred_categories
                    GROUP BY u2.user_id
                    HAVING COUNT(*) >= 2
                    ORDER BY common_interactions DESC, engagement_diff ASC
                    LIMIT 10
                )
                SELECT DISTINCT c.*
                FROM courses c
                JOIN enrollments e ON c.id = e.course_id
                JOIN user_similarity us ON e.user_id = us.user_id
                WHERE c.is_active = true
                AND c.id NOT IN (
                    SELECT course_id FROM user_interactions WHERE user_id = :user_id
                )
                ORDER BY c.rating DESC, c.enrollment_count DESC
                LIMIT :limit
            """)
            
            results = self.db.execute(similar_users_query, {
                "user_id": user_id,
                "limit": limit
            }).fetchall()
            
            recommendations = []
            for i, course in enumerate(results):
                confidence = max(0.6, 0.9 - (i * 0.05))  # Decreasing confidence
                recommendations.append(self._create_recommendation_response(
                    course, confidence, "Recommended by users with similar interests"
                ))
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Error in collaborative filtering: {e}")
            return []
    
    def _content_based_filtering(self, user_id: int, limit: int, user_profile: Dict) -> List[RecommendationResponse]:
        """
        Content-based filtering based on user preferences.
        
        Args:
            user_id: User ID
            limit: Number of recommendations
            user_profile: User profile data
            
        Returns:
            List[RecommendationResponse]: Recommendations
        """
        try:
            # Build query based on user preferences
            query = self.db.query(Course).filter(Course.is_active == True)
            
            # Exclude courses user has already interacted with
            interacted_courses = self.db.query(UserInteraction.course_id).filter(
                UserInteraction.user_id == user_id
            ).subquery()
            query = query.filter(~Course.id.in_(interacted_courses))
            
            # Apply preference filters
            if user_profile['preferred_categories']:
                from app.models.course import Category
                query = query.join(Category).filter(
                    Category.name.in_(user_profile['preferred_categories'])
                )
            
            if user_profile['preferred_difficulty_levels']:
                preferred_difficulties = list(user_profile['preferred_difficulty_levels'].keys())
                query = query.filter(Course.difficulty_level.in_(preferred_difficulties))
            
            if user_profile['preferred_content_types']:
                preferred_content_types = list(user_profile['preferred_content_types'].keys())
                query = query.filter(Course.content_type.in_(preferred_content_types))
            
            # Order by rating and enrollment count
            courses = query.order_by(Course.rating.desc(), Course.enrollment_count.desc()).limit(limit).all()
            
            recommendations = []
            for i, course in enumerate(courses):
                confidence = max(0.7, 0.95 - (i * 0.03))  # High confidence for content-based
                recommendations.append(self._create_recommendation_response(
                    course, confidence, "Matches your learning preferences"
                ))
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Error in content-based filtering: {e}")
            return []
    
    def _hybrid_recommendations(self, user_id: int, limit: int, user_profile: Dict) -> List[RecommendationResponse]:
        """
        Hybrid recommendations combining multiple approaches.
        
        Args:
            user_id: User ID
            limit: Number of recommendations
            user_profile: User profile data
            
        Returns:
            List[RecommendationResponse]: Recommendations
        """
        try:
            # Get recommendations from both approaches
            collaborative_recs = self._collaborative_filtering(user_id, limit // 2, user_profile)
            content_recs = self._content_based_filtering(user_id, limit // 2, user_profile)
            
            # Combine and deduplicate
            all_recommendations = {}
            
            # Add collaborative recommendations with weight
            for rec in collaborative_recs:
                all_recommendations[rec.course_id] = rec
                rec.confidence_score *= 0.8  # Slight weight reduction for collaborative
            
            # Add content-based recommendations with weight
            for rec in content_recs:
                if rec.course_id in all_recommendations:
                    # Average confidence scores
                    existing_rec = all_recommendations[rec.course_id]
                    existing_rec.confidence_score = (existing_rec.confidence_score + rec.confidence_score) / 2
                    existing_rec.recommendation_reason = "Combined recommendation based on similar users and your preferences"
                else:
                    rec.confidence_score *= 0.9  # Slight weight reduction for content-based
                    all_recommendations[rec.course_id] = rec
            
            # Sort by confidence score and return top recommendations
            sorted_recommendations = sorted(
                all_recommendations.values(), 
                key=lambda x: x.confidence_score, 
                reverse=True
            )
            
            return sorted_recommendations[:limit]
            
        except Exception as e:
            logger.error(f"Error in hybrid recommendations: {e}")
            return self._content_based_filtering(user_id, limit, user_profile)
    
    def _get_fallback_recommendations(self, user_id: int, limit: int) -> List[RecommendationResponse]:
        """
        Get fallback recommendations when AI is not available.
        
        Args:
            user_id: User ID
            limit: Number of recommendations
            
        Returns:
            List[RecommendationResponse]: Fallback recommendations
        """
        try:
            # Get popular courses that user hasn't interacted with
            interacted_courses = self.db.query(UserInteraction.course_id).filter(
                UserInteraction.user_id == user_id
            ).subquery()
            
            courses = self.db.query(Course).filter(
                Course.is_active == True,
                ~Course.id.in_(interacted_courses)
            ).order_by(Course.rating.desc(), Course.enrollment_count.desc()).limit(limit).all()
            
            recommendations = []
            for i, course in enumerate(courses):
                confidence = max(0.5, 0.8 - (i * 0.05))
                recommendations.append(self._create_recommendation_response(
                    course, confidence, "Popular course with high ratings"
                ))
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Error in fallback recommendations: {e}")
            return []
    
    def _create_recommendation_response(
        self, 
        course: Course, 
        confidence: float, 
        reason: str
    ) -> RecommendationResponse:
        """
        Create a RecommendationResponse from a Course object.
        
        Args:
            course: Course object
            confidence: Confidence score
            reason: Recommendation reason
            
        Returns:
            RecommendationResponse: Recommendation response
        """
        return RecommendationResponse(
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
            confidence_score=round(confidence, 2),
            recommendation_reason=reason,
            category_name=course.category.name if course.category else None
        )
    
    def get_similar_courses(self, course_id: int, limit: int = 5) -> List[RecommendationResponse]:
        """
        Get courses similar to the specified course.
        
        Args:
            course_id: Course ID
            limit: Number of similar courses to return
            
        Returns:
            List[RecommendationResponse]: List of similar courses
        """
        try:
            # Get the target course
            target_course = self.db.query(Course).filter(Course.id == course_id).first()
            if not target_course:
                return []
            
            # Find similar courses based on category, difficulty, and content type
            similar_courses = self.db.query(Course).filter(
                Course.is_active == True,
                Course.id != course_id,
                Course.category_id == target_course.category_id,
                Course.difficulty_level == target_course.difficulty_level
            ).order_by(Course.rating.desc()).limit(limit).all()
            
            recommendations = []
            for i, course in enumerate(similar_courses):
                confidence = max(0.6, 0.9 - (i * 0.1))
                recommendations.append(self._create_recommendation_response(
                    course, confidence, f"Similar to {target_course.title}"
                ))
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Error getting similar courses: {e}")
            return []
    
    def record_user_feedback(self, user_id: int, course_id: int, feedback_type: str) -> None:
        """
        Record user feedback for a recommendation.
        
        Args:
            user_id: User ID
            course_id: Course ID
            feedback_type: Type of feedback
        """
        try:
            # Create user interaction record
            interaction = UserInteraction(
                user_id=user_id,
                course_id=course_id,
                interaction_type=feedback_type,
                created_at=datetime.now()
            )
            self.db.add(interaction)
            self.db.commit()
            
            logger.info(f"Recorded feedback: user={user_id}, course={course_id}, type={feedback_type}")
            
        except Exception as e:
            logger.error(f"Error recording feedback: {e}")
            self.db.rollback()
