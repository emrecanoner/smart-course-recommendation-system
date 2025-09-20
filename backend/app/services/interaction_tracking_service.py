"""
Interaction tracking service for comprehensive user behavior monitoring.
"""

import logging
from typing import Optional, Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import and_, desc

from app.core.constants import (
    ENGAGEMENT_WEIGHTS, POSITIVE_ACTIONS, NEGATIVE_ACTIONS, 
    ENGAGEMENT_RATIO_BONUS_MULTIPLIER, MIN_ENGAGEMENT_SCORE,
    calculate_engagement_score
)
from app.models.interaction import UserInteraction
from app.models.user import User
from app.models.course import Course
from app.models.enrollment import Enrollment

logger = logging.getLogger(__name__)


class InteractionTrackingService:
    """
    Service for tracking user interactions with courses and learning content.
    """
    
    def __init__(self, db: Session):
        self.db = db
    
    def track_course_view(
        self,
        user_id: int,
        course_id: int,
        session_id: Optional[str] = None,
        device_type: Optional[str] = None,
        referrer: Optional[str] = None
    ) -> bool:
        """
        Track when a user views a course.
        
        Args:
            user_id: User ID
            course_id: Course ID
            session_id: Session ID
            device_type: Device type (mobile, desktop, tablet)
            referrer: Referrer URL
            
        Returns:
            bool: Success status
        """
        success = self._create_interaction(
            user_id=user_id,
            course_id=course_id,
            interaction_type='view',
            session_id=session_id,
            device_type=device_type,
            referrer=referrer
        )
        
        if success:
            # Also update last access in enrollment table
            from app.services.enrollment_service import EnrollmentService
            enrollment_service = EnrollmentService(self.db)
            enrollment_service.update_last_access(user_id, course_id)
            
            # Analytics will be updated by scheduled script
        
        return success
    
    def track_course_like(
        self,
        user_id: int,
        course_id: int,
        session_id: Optional[str] = None,
        device_type: Optional[str] = None,
        referrer: Optional[str] = None
    ) -> bool:
        """
        Track when a user likes a course.
        
        Args:
            user_id: User ID
            course_id: Course ID
            session_id: Session ID
            device_type: Device type (web, mobile, tablet)
            referrer: Referrer page
            
        Returns:
            bool: Success status
        """
        success = self._create_interaction(
            user_id=user_id,
            course_id=course_id,
            interaction_type='like',
            session_id=session_id,
            device_type=device_type,
            referrer=referrer
        )
        
        if success:
            # Also trigger preference learning
            from app.services.user_preference_service import UserPreferenceService
            pref_service = UserPreferenceService(self.db)
            pref_service.learn_from_interactions(user_id)
            
            # Analytics will be updated by scheduled script
        
        return success
    
    def track_course_unlike(
        self,
        user_id: int,
        course_id: int,
        session_id: Optional[str] = None,
        device_type: Optional[str] = None,
        referrer: Optional[str] = None
    ) -> bool:
        """
        Track when a user unlikes/unfavorites a course.
        
        Args:
            user_id: User ID
            course_id: Course ID
            session_id: Session ID
            device_type: Device type (web, mobile, tablet)
            referrer: Referrer page
            
        Returns:
            bool: Success status
        """
        success = self._create_interaction(
            user_id=user_id,
            course_id=course_id,
            interaction_type='unlike',
            session_id=session_id,
            device_type=device_type,
            referrer=referrer
        )
        
        if success:
            # Also trigger preference learning
            from app.services.user_preference_service import UserPreferenceService
            pref_service = UserPreferenceService(self.db)
            pref_service.learn_from_interactions(user_id)
            
            # Analytics will be updated by scheduled script
        
        return success
    
    def track_course_enroll(
        self,
        user_id: int,
        course_id: int,
        session_id: Optional[str] = None,
        device_type: Optional[str] = None,
        referrer: Optional[str] = None
    ) -> bool:
        """
        Track when a user enrolls in a course.
        
        Args:
            user_id: User ID
            course_id: Course ID
            session_id: Session ID
            device_type: Device type (web, mobile, tablet)
            referrer: Referrer page
            
        Returns:
            bool: Success status
        """
        success = self._create_interaction(
            user_id=user_id,
            course_id=course_id,
            interaction_type='enroll',
            session_id=session_id,
            device_type=device_type,
            referrer=referrer
        )
        
        if success:
            # Also trigger preference learning
            from app.services.user_preference_service import UserPreferenceService
            pref_service = UserPreferenceService(self.db)
            pref_service.learn_from_interactions(user_id)
            
            # Analytics will be updated by scheduled script
        
        return success
    
    def track_course_unenroll(
        self,
        user_id: int,
        course_id: int,
        session_id: Optional[str] = None,
        device_type: Optional[str] = None,
        referrer: Optional[str] = None
    ) -> bool:
        """
        Track when a user unenrolls from a course.
        
        Args:
            user_id: User ID
            course_id: Course ID
            session_id: Session ID
            device_type: Device type (web, mobile, tablet)
            referrer: Referrer page
            
        Returns:
            bool: Success status
        """
        success = self._create_interaction(
            user_id=user_id,
            course_id=course_id,
            interaction_type='unenroll',
            session_id=session_id,
            device_type=device_type,
            referrer=referrer
        )
        
        if success:
            # Also trigger preference learning for negative feedback
            from app.services.user_preference_service import UserPreferenceService
            pref_service = UserPreferenceService(self.db)
            pref_service.learn_from_interactions(user_id)
        
        return success
    
    def track_course_complete(
        self,
        user_id: int,
        course_id: int,
        completion_percentage: float,
        session_id: Optional[str] = None,
        device_type: Optional[str] = None,
        referrer: Optional[str] = None
    ) -> bool:
        """
        Track when a user completes a course.
        
        Args:
            user_id: User ID
            course_id: Course ID
            completion_percentage: Completion percentage (0-100)
            session_id: Session ID
            device_type: Device type (web, mobile, tablet)
            referrer: Referrer page
            
        Returns:
            bool: Success status
        """
        # Calculate time spent from enroll to complete
        time_spent_minutes = self._calculate_time_spent_from_enroll_to_complete(user_id, course_id)
        
        # Create interaction record
        success = self._create_interaction(
            user_id=user_id,
            course_id=course_id,
            interaction_type='complete',
            progress_percentage=completion_percentage,
            time_spent_minutes=time_spent_minutes,
            session_id=session_id,
            device_type=device_type,
            referrer=referrer
        )
        
        if success:
            # Also update enrollment table
            from app.services.enrollment_service import EnrollmentService
            enrollment_service = EnrollmentService(self.db)
            enrollment_service.complete_course(user_id, course_id, completion_percentage)
            
            # Note: time_spent_minutes is already set from frontend in the interaction
            # No need to recalculate it as it would cause incorrect values
            
            # Also trigger preference learning
            from app.services.user_preference_service import UserPreferenceService
            pref_service = UserPreferenceService(self.db)
            pref_service.learn_from_interactions(user_id)
            
            # Analytics will be updated by scheduled script
        
        return success
    
    def track_course_rate(
        self,
        user_id: int,
        course_id: int,
        rating: float,
        session_id: Optional[str] = None,
        device_type: Optional[str] = None,
        referrer: Optional[str] = None
    ) -> bool:
        """
        Track when a user rates a course.
        
        Args:
            user_id: User ID
            course_id: Course ID
            rating: Rating (1.0-5.0)
            session_id: Session ID
            device_type: Device type
            referrer: Referrer URL
            
        Returns:
            bool: Success status
        """
        return self._create_interaction(
            user_id=user_id,
            course_id=course_id,
            interaction_type='rate',
            rating=rating,
            session_id=session_id,
            device_type=device_type,
            referrer=referrer
        )
    
    def track_course_share(
        self,
        user_id: int,
        course_id: int,
        share_platform: Optional[str] = None,
        session_id: Optional[str] = None
    ) -> bool:
        """
        Track when a user shares a course.
        
        Args:
            user_id: User ID
            course_id: Course ID
            share_platform: Platform where shared (facebook, twitter, etc.)
            session_id: Session ID
            
        Returns:
            bool: Success status
        """
        return self._create_interaction(
            user_id=user_id,
            course_id=course_id,
            interaction_type='share',
            session_id=session_id,
            referrer=share_platform
        )
    
    def _create_interaction(
        self,
        user_id: int,
        course_id: int,
        interaction_type: str,
        rating: Optional[float] = None,
        time_spent_minutes: Optional[int] = None,
        progress_percentage: Optional[float] = None,
        session_id: Optional[str] = None,
        device_type: Optional[str] = None,
        referrer: Optional[str] = None
    ) -> bool:
        """
        Create a user interaction record.
        
        Args:
            user_id: User ID
            course_id: Course ID
            interaction_type: Type of interaction
            rating: Rating if applicable
            time_spent_minutes: Time spent if applicable
            progress_percentage: Progress percentage if applicable
            session_id: Session ID
            device_type: Device type
            referrer: Referrer
            
        Returns:
            bool: Success status
        """
        try:
            # Validate user and course exist
            user = self.db.query(User).filter(User.id == user_id).first()
            course = self.db.query(Course).filter(Course.id == course_id).first()
            
            if not user:
                logger.error(f"User {user_id} not found")
                return False
            
            if not course:
                logger.error(f"Course {course_id} not found")
                return False
            
            # Create interaction record
            interaction = UserInteraction(
                user_id=user_id,
                course_id=course_id,
                interaction_type=interaction_type,
                rating=rating,
                time_spent_minutes=time_spent_minutes,
                progress_percentage=progress_percentage,
                session_id=session_id,
                device_type=device_type,
                referrer=referrer
            )
            
            self.db.add(interaction)
            self.db.commit()
            
            logger.info(f"Tracked {interaction_type} interaction for user {user_id}, course {course_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error tracking interaction: {e}")
            self.db.rollback()
            return False
    
    def get_user_interaction_summary(self, user_id: int) -> Dict[str, Any]:
        """
        Get summary of user interactions.
        
        Args:
            user_id: User ID
            
        Returns:
            Dict: Interaction summary
        """
        interactions = self.db.query(UserInteraction).filter(
            UserInteraction.user_id == user_id
        ).all()
        
        summary = {
            'total_interactions': len(interactions),
            'interaction_types': {},
            'recent_interactions': [],
            'most_viewed_courses': [],
            'completion_rate': 0.0,
            'average_rating_given': 0.0
        }
        
        if not interactions:
            return summary
        
        # Count interaction types
        for interaction in interactions:
            interaction_type = interaction.interaction_type
            summary['interaction_types'][interaction_type] = \
                summary['interaction_types'].get(interaction_type, 0) + 1
        
        # Get recent interactions
        recent_interactions = self.db.query(UserInteraction).filter(
            UserInteraction.user_id == user_id
        ).order_by(desc(UserInteraction.created_at)).limit(10).all()
        
        for interaction in recent_interactions:
            course = self.db.query(Course).filter(Course.id == interaction.course_id).first()
            summary['recent_interactions'].append({
                'course_id': interaction.course_id,
                'course_title': course.title if course else 'Unknown',
                'interaction_type': interaction.interaction_type,
                'timestamp': interaction.created_at.isoformat(),
                'rating': interaction.rating
            })
        
        # Calculate completion rate
        enrollments = self.db.query(Enrollment).filter(
            and_(
                Enrollment.user_id == user_id,
                Enrollment.is_active == True
            )
        ).all()
        
        if enrollments:
            completed = sum(1 for e in enrollments if e.is_completed)
            summary['completion_rate'] = (completed / len(enrollments)) * 100
        
        # Calculate average rating given
        ratings = [inter.rating for inter in interactions if inter.rating is not None]
        if ratings:
            summary['average_rating_given'] = sum(ratings) / len(ratings)
        
        return summary
    
    def get_course_interaction_stats(self, course_id: int) -> Dict[str, Any]:
        """
        Get interaction statistics for a course.
        
        Args:
            course_id: Course ID
            
        Returns:
            Dict: Course interaction statistics
        """
        interactions = self.db.query(UserInteraction).filter(
            UserInteraction.course_id == course_id
        ).all()
        
        stats = {
            'total_interactions': len(interactions),
            'unique_users': len(set(inter.user_id for inter in interactions)),
            'interaction_types': {},
            'average_rating': 0.0,
            'completion_rate': 0.0,
            'engagement_score': 0.0
        }
        
        if not interactions:
            return stats
        
        # Count interaction types
        for interaction in interactions:
            interaction_type = interaction.interaction_type
            stats['interaction_types'][interaction_type] = \
                stats['interaction_types'].get(interaction_type, 0) + 1
        
        # Calculate average rating
        ratings = [inter.rating for inter in interactions if inter.rating is not None]
        if ratings:
            stats['average_rating'] = sum(ratings) / len(ratings)
        
        # Calculate completion rate
        enrollments = self.db.query(Enrollment).filter(
            and_(
                Enrollment.course_id == course_id,
                Enrollment.is_active == True
            )
        ).all()
        
        if enrollments:
            completed = sum(1 for e in enrollments if e.is_completed)
            stats['completion_rate'] = (completed / len(enrollments)) * 100
        
        # Calculate engagement score using optimized function
        # For interaction tracking service, we don't have pre-calculated counts, so use basic calculation
        stats['engagement_score'] = calculate_engagement_score(interactions)
        
        return stats
    
    def _calculate_time_spent_from_enroll_to_complete(self, user_id: int, course_id: int) -> Optional[int]:
        """
        Calculate time spent from enroll to complete by finding the time difference
        between the last enroll interaction and the current complete interaction.
        
        Args:
            user_id: User ID
            course_id: Course ID
            
        Returns:
            Optional[int]: Time spent in minutes, or None if no enroll found
        """
        try:
            # Find the most recent enroll interaction for this user and course
            enroll_interaction = self.db.query(UserInteraction).filter(
                and_(
                    UserInteraction.user_id == user_id,
                    UserInteraction.course_id == course_id,
                    UserInteraction.interaction_type == 'enroll'
                )
            ).order_by(UserInteraction.created_at.desc()).first()
            
            if not enroll_interaction:
                # If no enroll found, return None
                return None
            
            # Calculate time difference between enroll and now (complete time)
            from datetime import datetime
            current_time = datetime.utcnow()
            enroll_time = enroll_interaction.created_at
            
            # Calculate difference in minutes
            time_diff = current_time - enroll_time
            time_spent_minutes = int(time_diff.total_seconds() / 60)
            
            # Ensure minimum 1 minute
            return max(1, time_spent_minutes)
            
        except Exception as e:
            print(f"Error calculating time spent: {e}")
            return None
