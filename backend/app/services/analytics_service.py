"""
Analytics service for data warehouse operations and reporting.
"""

import json
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import text, and_, desc, func

from app.core.constants import (
    ENGAGEMENT_WEIGHTS, POSITIVE_ACTIONS, NEGATIVE_ACTIONS, 
    ENGAGEMENT_RATIO_BONUS_MULTIPLIER, MIN_ENGAGEMENT_SCORE,
    calculate_engagement_score, calculate_learning_velocity
)
from app.models.user import User
from app.models.course import Course, Category
from app.models.interaction import UserInteraction
from app.models.enrollment import Enrollment
from app.models.recommendation import Recommendation, RecommendationLog

logger = logging.getLogger(__name__)


class AnalyticsService:
    """
    Service for analytics and data warehouse operations.
    """
    
    def __init__(self, db: Session):
        self.db = db
    
    def update_user_learning_profile(self, user_id: int) -> Dict[str, Any]:
        """
        Update user learning profile in analytics schema.
        
        Args:
            user_id: User ID
            
        Returns:
            Dict: Updated profile data
        """
        logger.info(f"Updating learning profile for user {user_id}")
        
        try:
            # Get user data
            user = self.db.query(User).filter(User.id == user_id).first()
            if not user:
                logger.warning(f"User {user_id} not found")
                return {}
            
            # Calculate statistics
            stats = self._calculate_user_statistics(user_id)
            
            # Get preferences
            preferences = self._extract_user_preferences(user_id)
            
            # Get behavioral patterns
            patterns = self._analyze_user_patterns(user_id)
            
            # Update or create profile
            profile_data = {
                'user_id': user_id,
                **stats,
                **preferences,
                **patterns,
                'updated_at': datetime.now()
            }
            
            # Insert or update in analytics schema
            self._upsert_user_profile(profile_data)
            
            logger.info(f"Updated learning profile for user {user_id}")
            return profile_data
            
        except Exception as e:
            logger.error(f"Error updating user learning profile: {e}")
            return {}
    
    def _calculate_user_statistics(self, user_id: int) -> Dict[str, Any]:
        """Calculate user statistics."""
        # Get interaction counts
        interactions = self.db.query(UserInteraction).filter(
            UserInteraction.user_id == user_id
        ).all()
        
        # Get enrollment data
        enrollments = self.db.query(Enrollment).filter(
            and_(
                Enrollment.user_id == user_id,
                Enrollment.is_active == True
            )
        ).all()
        
        # Calculate metrics
        total_courses_viewed = len([i for i in interactions if i.interaction_type == 'view'])
        total_courses_enrolled = len(enrollments)
        total_courses_completed = len([e for e in enrollments if e.is_completed])
        total_courses_rated = len([i for i in interactions if i.interaction_type == 'rate'])
        total_courses_liked = len([i for i in interactions if i.interaction_type == 'like'])
        total_courses_unliked = len([i for i in interactions if i.interaction_type == 'unlike'])
        total_courses_unenrolled = len([i for i in interactions if i.interaction_type == 'unenroll'])
        total_interactions = len(interactions)
        
        # Calculate rates
        avg_completion_rate = (total_courses_completed / total_courses_enrolled * 100) if total_courses_enrolled > 0 else 0
        
        # Calculate average rating given
        ratings = [i.rating for i in interactions if i.rating is not None]
        avg_rating_given = sum(ratings) / len(ratings) if ratings else 0
        
        # Calculate learning velocity using optimized function
        completed_enrollments = [e for e in enrollments if e.is_completed]
        learning_velocity = calculate_learning_velocity(completed_enrollments)
        
        # Calculate engagement score using optimized function
        engagement_score = calculate_engagement_score(
            interactions, 
            total_courses_liked, 
            total_courses_unliked,
            total_courses_enrolled, 
            total_courses_unenrolled,
            total_courses_completed, 
            total_courses_rated
        )
        
        return {
            'total_courses_viewed': total_courses_viewed,
            'total_courses_enrolled': total_courses_enrolled,
            'total_courses_completed': total_courses_completed,
            'total_courses_rated': total_courses_rated,
            'total_courses_liked': total_courses_liked,
            'total_courses_unliked': total_courses_unliked,
            'total_courses_unenrolled': total_courses_unenrolled,
            'total_interactions': total_interactions,
            'avg_completion_rate': round(avg_completion_rate, 2),
            'avg_rating_given': round(avg_rating_given, 2),
            'learning_velocity': round(learning_velocity, 2),
            'engagement_score': round(engagement_score, 2)
        }
    
    def _extract_user_preferences(self, user_id: int) -> Dict[str, Any]:
        """Extract user preferences from interactions."""
        # Get user interactions with course details
        interactions = self.db.query(UserInteraction, Course, Category).join(
            Course, UserInteraction.course_id == Course.id
        ).outerjoin(
            Category, Course.category_id == Category.id
        ).filter(
            UserInteraction.user_id == user_id
        ).all()
        
        preferences = {
            'preferred_categories': {},
            'preferred_difficulty_levels': {},
            'preferred_content_types': {},
            'preferred_durations': {},
            'learning_goals': [],
            'skills_developed': set()
        }
        
        for interaction, course, category in interactions:
            # Count category preferences
            if category:
                cat_name = category.name
                preferences['preferred_categories'][cat_name] = \
                    preferences['preferred_categories'].get(cat_name, 0) + 1
            
            # Count difficulty preferences
            if course.difficulty_level:
                diff_level = course.difficulty_level
                preferences['preferred_difficulty_levels'][diff_level] = \
                    preferences['preferred_difficulty_levels'].get(diff_level, 0) + 1
            
            # Count content type preferences
            if course.content_type:
                content_type = course.content_type
                preferences['preferred_content_types'][content_type] = \
                    preferences['preferred_content_types'].get(content_type, 0) + 1
            
            # Count duration preferences
            if course.duration_hours:
                duration_cat = self._categorize_duration(course.duration_hours)
                preferences['preferred_durations'][duration_cat] = \
                    preferences['preferred_durations'].get(duration_cat, 0) + 1
            
            # Extract skills
            if course.skills:
                skills = [skill.strip() for skill in course.skills.split(',')]
                preferences['skills_developed'].update(skills)
        
        # Convert sets to lists and format for JSON
        preferences['skills_developed'] = list(preferences['skills_developed'])
        
        return {
            'preferred_categories': json.dumps(preferences['preferred_categories']),
            'preferred_difficulty_levels': json.dumps(preferences['preferred_difficulty_levels']),
            'preferred_content_types': json.dumps(preferences['preferred_content_types']),
            'preferred_durations': json.dumps(preferences['preferred_durations']),
            'skills_developed': json.dumps(preferences['skills_developed'])
        }
    
    def _analyze_user_patterns(self, user_id: int) -> Dict[str, Any]:
        """Analyze user behavioral patterns."""
        interactions = self.db.query(UserInteraction).filter(
            UserInteraction.user_id == user_id
        ).order_by(UserInteraction.created_at).all()
        
        if not interactions:
            return {
                'preferred_time_of_day': None,
                'preferred_day_of_week': None,
                'learning_pattern': None,
                'device_preference': None,
                'last_activity_date': None,
                'days_since_last_activity': 0,
                'streak_days': 0,
                'longest_streak': 0,
                'first_enrollment_date': None,
                'last_enrollment_date': None,
                'first_completion_date': None,
                'last_completion_date': None
            }
        
        # Analyze time patterns
        hour_counts = {}
        day_counts = {}
        device_counts = {}
        enrollment_dates = []
        completion_dates = []
        
        for interaction in interactions:
            # Time of day analysis
            hour = interaction.created_at.hour
            hour_counts[hour] = hour_counts.get(hour, 0) + 1
            
            # Day of week analysis
            day = interaction.created_at.strftime('%A')
            day_counts[day] = day_counts.get(day, 0) + 1
            
            # Device analysis
            if interaction.device_type:
                device_counts[interaction.device_type] = device_counts.get(interaction.device_type, 0) + 1
            
            # Enrollment and completion date analysis
            if interaction.interaction_type == 'enroll':
                enrollment_dates.append(interaction.created_at)
            elif interaction.interaction_type == 'complete':
                completion_dates.append(interaction.created_at)
        
        # Find most common patterns
        preferred_time = max(hour_counts.items(), key=lambda x: x[1])[0] if hour_counts else None
        preferred_day = max(day_counts.items(), key=lambda x: x[1])[0] if day_counts else None
        device_preference = max(device_counts.items(), key=lambda x: x[1])[0] if device_counts else None
        
        # Determine learning pattern
        learning_pattern = self._determine_learning_pattern(interactions)
        
        # Calculate activity metrics
        last_activity = max(interaction.created_at for interaction in interactions) if interactions else None
        days_since_last = (datetime.now() - last_activity).days if last_activity else 0
        
        # Calculate streak
        streak_days, longest_streak = self._calculate_streak(interactions)
        
        # Calculate first and last dates
        first_enrollment_date = min(enrollment_dates) if enrollment_dates else None
        last_enrollment_date = max(enrollment_dates) if enrollment_dates else None
        first_completion_date = min(completion_dates) if completion_dates else None
        last_completion_date = max(completion_dates) if completion_dates else None
        
        return {
            'preferred_time_of_day': str(preferred_time) if preferred_time is not None else None,
            'preferred_day_of_week': preferred_day,
            'learning_pattern': learning_pattern,
            'device_preference': device_preference,
            'last_activity_date': last_activity,
            'days_since_last_activity': days_since_last,
            'streak_days': streak_days,
            'longest_streak': longest_streak,
            'first_enrollment_date': first_enrollment_date,
            'last_enrollment_date': last_enrollment_date,
            'first_completion_date': first_completion_date,
            'last_completion_date': last_completion_date
        }
    
    def _categorize_duration(self, duration_hours: int) -> str:
        """Categorize course duration."""
        if duration_hours <= 5:
            return 'short'
        elif duration_hours <= 20:
            return 'medium'
        else:
            return 'long'
    
    def _determine_learning_pattern(self, interactions: List[UserInteraction]) -> str:
        """Determine user's learning pattern."""
        if not interactions:
            return None
        
        # Analyze interaction frequency
        dates = [interaction.created_at.date() for interaction in interactions]
        unique_dates = set(dates)
        
        if len(unique_dates) <= 1:
            return 'sporadic'
        elif len(unique_dates) >= len(dates) * 0.8:
            return 'consistent'
        else:
            return 'intensive'
    
    def _calculate_streak(self, interactions: List[UserInteraction]) -> tuple:
        """Calculate current and longest streak."""
        if not interactions:
            return 0, 0
        
        # Get unique dates
        dates = sorted(set(interaction.created_at.date() for interaction in interactions))
        
        if not dates:
            return 0, 0
        
        # Calculate streaks
        current_streak = 0
        longest_streak = 0
        temp_streak = 1
        
        for i in range(1, len(dates)):
            if (dates[i] - dates[i-1]).days == 1:
                temp_streak += 1
            else:
                longest_streak = max(longest_streak, temp_streak)
                temp_streak = 1
        
        longest_streak = max(longest_streak, temp_streak)
        
        # Calculate current streak
        today = datetime.now().date()
        if dates[-1] == today or dates[-1] == today - timedelta(days=1):
            current_streak = temp_streak
        
        return current_streak, longest_streak
    
    def _upsert_user_profile(self, profile_data: Dict[str, Any]) -> None:
        """Insert or update user profile in analytics schema."""
        try:
            # Use raw SQL for analytics schema operations
            sql = """
            INSERT INTO analytics.user_learning_profile (
                user_id, total_courses_viewed, total_courses_enrolled, total_courses_completed,
                total_courses_rated, total_courses_liked, total_courses_unliked, total_courses_unenrolled,
                total_interactions, avg_completion_rate, avg_rating_given,
                learning_velocity, engagement_score, preferred_categories, preferred_difficulty_levels,
                preferred_content_types, preferred_durations, skills_developed, preferred_time_of_day,
                preferred_day_of_week, learning_pattern, device_preference, last_activity_date,
                days_since_last_activity, streak_days, longest_streak, 
                first_enrollment_date, last_enrollment_date, first_completion_date, last_completion_date,
                updated_at
            ) VALUES (
                :user_id, :total_courses_viewed, :total_courses_enrolled, :total_courses_completed,
                :total_courses_rated, :total_courses_liked, :total_courses_unliked, :total_courses_unenrolled,
                :total_interactions, :avg_completion_rate, :avg_rating_given,
                :learning_velocity, :engagement_score, :preferred_categories, :preferred_difficulty_levels,
                :preferred_content_types, :preferred_durations, :skills_developed, :preferred_time_of_day,
                :preferred_day_of_week, :learning_pattern, :device_preference, :last_activity_date,
                :days_since_last_activity, :streak_days, :longest_streak,
                :first_enrollment_date, :last_enrollment_date, :first_completion_date, :last_completion_date,
                :updated_at
            )
            ON CONFLICT (user_id) DO UPDATE SET
                total_courses_viewed = EXCLUDED.total_courses_viewed,
                total_courses_enrolled = EXCLUDED.total_courses_enrolled,
                total_courses_completed = EXCLUDED.total_courses_completed,
                total_courses_rated = EXCLUDED.total_courses_rated,
                total_courses_liked = EXCLUDED.total_courses_liked,
                total_courses_unliked = EXCLUDED.total_courses_unliked,
                total_courses_unenrolled = EXCLUDED.total_courses_unenrolled,
                total_interactions = EXCLUDED.total_interactions,
                avg_completion_rate = EXCLUDED.avg_completion_rate,
                avg_rating_given = EXCLUDED.avg_rating_given,
                learning_velocity = EXCLUDED.learning_velocity,
                engagement_score = EXCLUDED.engagement_score,
                preferred_categories = EXCLUDED.preferred_categories,
                preferred_difficulty_levels = EXCLUDED.preferred_difficulty_levels,
                preferred_content_types = EXCLUDED.preferred_content_types,
                preferred_durations = EXCLUDED.preferred_durations,
                skills_developed = EXCLUDED.skills_developed,
                preferred_time_of_day = EXCLUDED.preferred_time_of_day,
                preferred_day_of_week = EXCLUDED.preferred_day_of_week,
                learning_pattern = EXCLUDED.learning_pattern,
                device_preference = EXCLUDED.device_preference,
                last_activity_date = EXCLUDED.last_activity_date,
                days_since_last_activity = EXCLUDED.days_since_last_activity,
                streak_days = EXCLUDED.streak_days,
                longest_streak = EXCLUDED.longest_streak,
                first_enrollment_date = EXCLUDED.first_enrollment_date,
                last_enrollment_date = EXCLUDED.last_enrollment_date,
                first_completion_date = EXCLUDED.first_completion_date,
                last_completion_date = EXCLUDED.last_completion_date,
                updated_at = EXCLUDED.updated_at
            """
            
            self.db.execute(text(sql), profile_data)
            self.db.commit()
            
        except Exception as e:
            logger.error(f"Error upserting user profile: {e}")
            self.db.rollback()
    
    def generate_user_report(self, user_id: int) -> Dict[str, Any]:
        """
        Generate comprehensive user report from analytics data.
        
        Args:
            user_id: User ID
            
        Returns:
            Dict: User report
        """
        try:
            # Get user profile from analytics
            sql = """
            SELECT * FROM analytics.user_learning_profile 
            WHERE user_id = :user_id
            """
            result = self.db.execute(text(sql), {'user_id': user_id}).fetchone()
            
            if not result:
                logger.warning(f"No analytics data found for user {user_id}")
                return {}
            
            # Convert to dictionary
            profile = dict(result._mapping)
            
            # Parse JSON fields
            json_fields = [
                'preferred_categories', 'preferred_difficulty_levels',
                'preferred_content_types', 'preferred_durations', 'skills_developed'
            ]
            
            for field in json_fields:
                if profile.get(field):
                    try:
                        profile[field] = json.loads(profile[field])
                    except:
                        profile[field] = {}
            
            return profile
            
        except Exception as e:
            logger.error(f"Error generating user report: {e}")
            return {}
    
    def get_system_analytics(self, days: int = 30) -> Dict[str, Any]:
        """
        Get system-wide analytics.
        
        Args:
            days: Number of days to analyze
            
        Returns:
            Dict: System analytics
        """
        try:
            cutoff_date = datetime.now() - timedelta(days=days)
            
            # Get basic counts
            total_users = self.db.query(User).count()
            total_courses = self.db.query(Course).count()
            total_interactions = self.db.query(UserInteraction).filter(
                UserInteraction.created_at >= cutoff_date
            ).count()
            total_enrollments = self.db.query(Enrollment).filter(
                Enrollment.created_at >= cutoff_date
            ).count()
            
            # Get recommendation stats
            total_recommendations = self.db.query(Recommendation).filter(
                Recommendation.created_at >= cutoff_date
            ).count()
            
            # Get top categories
            top_categories = self.db.query(
                Category.name, func.count(Enrollment.id).label('enrollment_count')
            ).join(
                Course, Category.id == Course.category_id
            ).join(
                Enrollment, Course.id == Enrollment.course_id
            ).filter(
                Enrollment.created_at >= cutoff_date
            ).group_by(Category.name).order_by(desc('enrollment_count')).limit(5).all()
            
            return {
                'period_days': days,
                'total_users': total_users,
                'total_courses': total_courses,
                'total_interactions': total_interactions,
                'total_enrollments': total_enrollments,
                'total_recommendations': total_recommendations,
                'top_categories': [{'name': cat[0], 'enrollments': cat[1]} for cat in top_categories],
                'generated_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error getting system analytics: {e}")
            return {}
    
    def update_user_learning_profile(self, user_id: int) -> bool:
        """
        Update user learning profile in analytics schema.
        
        Args:
            user_id: User ID
            
        Returns:
            bool: Success status
        """
        try:
            # Get user interactions
            interactions = self.db.query(UserInteraction).filter(
                UserInteraction.user_id == user_id
            ).all()
            
            # Get user enrollments
            enrollments = self.db.query(Enrollment).filter(
                and_(
                    Enrollment.user_id == user_id,
                    Enrollment.is_active == True,
                    Enrollment.deleted_at.is_(None)
                )
            ).all()
            
            # Calculate metrics
            total_courses_viewed = len([i for i in interactions if i.interaction_type == 'view'])
            total_courses_enrolled = len([i for i in interactions if i.interaction_type == 'enroll'])
            total_courses_completed = len([i for i in interactions if i.interaction_type == 'complete'])
            
            # Calculate average completion rate
            completed_enrollments = [e for e in enrollments if e.is_completed]
            avg_completion_rate = (sum(e.completion_percentage for e in completed_enrollments) / len(completed_enrollments)) if completed_enrollments else 0.0
            
            # Get preferred categories from interactions
            course_ids = [i.course_id for i in interactions if i.interaction_type in ['like', 'enroll', 'complete']]
            if course_ids:
                courses = self.db.query(Course).filter(Course.id.in_(course_ids)).all()
                categories = {}
                for course in courses:
                    if course.category_id:
                        cat_name = course.category.name if course.category else 'Unknown'
                        categories[cat_name] = categories.get(cat_name, 0) + 1
                preferred_categories = list(categories.keys())[:5]  # Top 5
            else:
                preferred_categories = []
            
            # Calculate engagement score
            engagement_weights = {
                'view': 1, 'like': 2, 'unlike': -1, 'enroll': 3, 
                'unenroll': -2, 'complete': 5, 'rate': 2
            }
            engagement_score = sum(
                engagement_weights.get(i.interaction_type, 1) for i in interactions
            )
            
            # Calculate learning velocity (courses completed per month)
            if completed_enrollments:
                first_completion = min(e.completion_date for e in completed_enrollments if e.completion_date)
                last_completion = max(e.completion_date for e in completed_enrollments if e.completion_date)
                if first_completion and last_completion:
                    months = (last_completion - first_completion).days / 30.0
                    learning_velocity = round(len(completed_enrollments) / max(months, 1), 2)
                else:
                    learning_velocity = 0.0
            else:
                learning_velocity = 0.0
            
            # Insert or update user learning profile
            self.db.execute(text("""
                INSERT INTO analytics.user_learning_profile (
                    user_id, total_courses_viewed, total_courses_enrolled, 
                    total_courses_completed, avg_completion_rate, 
                    preferred_categories, engagement_score, learning_velocity,
                    last_updated
                ) VALUES (
                    :user_id, :total_courses_viewed, :total_courses_enrolled,
                    :total_courses_completed, :avg_completion_rate,
                    :preferred_categories, :engagement_score, :learning_velocity,
                    CURRENT_TIMESTAMP
                )
                ON CONFLICT (user_id) DO UPDATE SET
                    total_courses_viewed = EXCLUDED.total_courses_viewed,
                    total_courses_enrolled = EXCLUDED.total_courses_enrolled,
                    total_courses_completed = EXCLUDED.total_courses_completed,
                    avg_completion_rate = EXCLUDED.avg_completion_rate,
                    preferred_categories = EXCLUDED.preferred_categories,
                    engagement_score = EXCLUDED.engagement_score,
                    learning_velocity = EXCLUDED.learning_velocity,
                    last_updated = CURRENT_TIMESTAMP
            """), {
                'user_id': user_id,
                'total_courses_viewed': total_courses_viewed,
                'total_courses_enrolled': total_courses_enrolled,
                'total_courses_completed': total_courses_completed,
                'avg_completion_rate': avg_completion_rate,
                'preferred_categories': json.dumps(preferred_categories),
                'engagement_score': engagement_score,
                'learning_velocity': learning_velocity
            })
            
            self.db.commit()
            logger.info(f"Updated learning profile for user {user_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error updating user learning profile: {e}")
            self.db.rollback()
            return False
