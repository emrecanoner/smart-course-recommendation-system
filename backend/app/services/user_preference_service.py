"""
User preference service for intelligent preference learning and management.
"""

import json
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import and_, func, desc

from app.core.constants import (
    ENGAGEMENT_WEIGHTS, POSITIVE_ACTIONS, NEGATIVE_ACTIONS, 
    ENGAGEMENT_RATIO_BONUS_MULTIPLIER, MIN_ENGAGEMENT_SCORE,
    calculate_engagement_score
)
from app.models.user import User
from app.models.interaction import UserInteraction, UserPreference
from app.models.course import Course, Category
from app.models.enrollment import Enrollment

logger = logging.getLogger(__name__)


class UserPreferenceService:
    """
    Service for managing user preferences through intelligent learning
    from user behavior and explicit preferences.
    """
    
    def __init__(self, db: Session):
        self.db = db
    
    def learn_from_interactions(self, user_id: int) -> Dict[str, Any]:
        """
        Learn user preferences from their interactions.
        
        Args:
            user_id: User ID
            
        Returns:
            Dict: Learned preferences
        """
        logger.info(f"Learning preferences for user {user_id} from interactions...")
        
        # Get user interactions
        interactions = self.db.query(UserInteraction).filter(
            UserInteraction.user_id == user_id
        ).all()
        
        if not interactions:
            logger.info(f"No interactions found for user {user_id}")
            return {}
        
        # Analyze interactions to learn preferences
        learned_prefs = self._analyze_interactions(interactions)
        
        # Update user preferences
        self._update_user_preferences(user_id, learned_prefs)
        
        return learned_prefs
    
    def _analyze_interactions(self, interactions: List[UserInteraction]) -> Dict[str, Any]:
        """
        Analyze user interactions to extract preferences.
        
        Args:
            interactions: List of user interactions
            
        Returns:
            Dict: Extracted preferences
        """
        preferences = {
            'preferred_categories': set(),
            'preferred_difficulty': {},
            'preferred_duration': {},
            'preferred_content_type': {},
            'learning_goals': set(),
            'interests': set()
        }
        
        # Get course details for interactions
        course_ids = [inter.course_id for inter in interactions]
        courses = self.db.query(Course).filter(Course.id.in_(course_ids)).all()
        course_dict = {course.id: course for course in courses}
        
        for interaction in interactions:
            course = course_dict.get(interaction.course_id)
            if not course:
                continue
            
            # Learn from different interaction types
            if interaction.interaction_type == 'view':
                # User is interested in this category
                if course.category:
                    preferences['preferred_categories'].add(course.category.name)
                
                # Learn content type preference
                if course.content_type:
                    preferences['preferred_content_type'][course.content_type] = \
                        preferences['preferred_content_type'].get(course.content_type, 0) + 1
                
                # Learn difficulty preference
                if course.difficulty_level:
                    preferences['preferred_difficulty'][course.difficulty_level] = \
                        preferences['preferred_difficulty'].get(course.difficulty_level, 0) + 1
                
                # Learn duration preference
                if course.duration_hours:
                    duration_category = self._categorize_duration(course.duration_hours)
                    preferences['preferred_duration'][duration_category] = \
                        preferences['preferred_duration'].get(duration_category, 0) + 1
            
            elif interaction.interaction_type == 'enroll':
                # Stronger signal for preferences
                if course.category:
                    preferences['preferred_categories'].add(course.category.name)
                
                # Extract skills as interests
                if course.skills:
                    skills = [skill.strip() for skill in course.skills.split(',')]
                    preferences['interests'].update(skills)
            
            elif interaction.interaction_type == 'complete':
                # Very strong signal - user liked this type of content
                if course.category:
                    preferences['preferred_categories'].add(course.category.name)
                
                # Learn from completion time
                if interaction.time_spent_minutes and course.duration_hours:
                    completion_rate = interaction.time_spent_minutes / (course.duration_hours * 60)
                    if completion_rate > 0.8:  # Completed quickly
                        preferences['learning_goals'].add('efficient_learning')
                    elif completion_rate < 0.5:  # Took time
                        preferences['learning_goals'].add('thorough_learning')
            
            elif interaction.interaction_type == 'rate' and interaction.rating:
                # Learn from ratings
                if interaction.rating >= 4.0:  # High rating
                    if course.category:
                        preferences['preferred_categories'].add(course.category.name)
        
        # Convert sets to lists for JSON serialization
        preferences['preferred_categories'] = list(preferences['preferred_categories'])
        preferences['learning_goals'] = list(preferences['learning_goals'])
        preferences['interests'] = list(preferences['interests'])
        
        return preferences
    
    def _categorize_duration(self, duration_hours: int) -> str:
        """Categorize course duration."""
        if duration_hours <= 5:
            return 'short'
        elif duration_hours <= 20:
            return 'medium'
        else:
            return 'long'
    
    def _update_user_preferences(self, user_id: int, learned_prefs: Dict[str, Any]) -> None:
        """
        Update user preferences with learned data.
        
        Args:
            user_id: User ID
            learned_prefs: Learned preferences
        """
        # Get or create user preference record
        user_pref = self.db.query(UserPreference).filter(
            UserPreference.user_id == user_id
        ).first()
        
        if not user_pref:
            user_pref = UserPreference(user_id=user_id)
            self.db.add(user_pref)
        
        # Update preferences based on learned data
        if learned_prefs.get('preferred_categories'):
            # Merge with existing categories
            existing_categories = json.loads(user_pref.interests or '[]')
            all_categories = list(set(existing_categories + learned_prefs['preferred_categories']))
            user_pref.interests = json.dumps(all_categories)
        
        if learned_prefs.get('preferred_difficulty'):
            # Find most preferred difficulty
            most_preferred = max(learned_prefs['preferred_difficulty'].items(), key=lambda x: x[1])
            user_pref.preferred_difficulty = most_preferred[0]
        
        if learned_prefs.get('preferred_duration'):
            # Find most preferred duration
            most_preferred = max(learned_prefs['preferred_duration'].items(), key=lambda x: x[1])
            user_pref.preferred_duration = most_preferred[0]
        
        if learned_prefs.get('preferred_content_type'):
            # Find most preferred content type
            most_preferred = max(learned_prefs['preferred_content_type'].items(), key=lambda x: x[1])
            user_pref.preferred_content_type = most_preferred[0]
        
        if learned_prefs.get('learning_goals'):
            # Update learning goals
            user_pref.learning_goals = json.dumps(learned_prefs['learning_goals'])
        
        if learned_prefs.get('interests'):
            # Update skills to develop
            user_pref.skills_to_develop = json.dumps(learned_prefs['interests'])
        
        user_pref.updated_at = datetime.utcnow()
        
        try:
            self.db.commit()
            logger.info(f"Updated preferences for user {user_id}")
        except Exception as e:
            logger.error(f"Error updating preferences for user {user_id}: {e}")
            self.db.rollback()
    
    def get_user_preferences(self, user_id: int) -> Dict[str, Any]:
        """
        Get comprehensive user preferences.
        
        Args:
            user_id: User ID
            
        Returns:
            Dict: User preferences
        """
        # Get user from main table
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            return {}
        
        # Get detailed preferences
        user_pref = self.db.query(UserPreference).filter(
            UserPreference.user_id == user_id
        ).first()
        
        preferences = {
            'user_id': user_id,
            'skill_level': user.skill_level,
            'time_commitment': user.time_commitment,
            'learning_goals': json.loads(user.learning_goals or '[]'),
            'preferred_categories': json.loads(user.preferred_categories or '[]'),
        }
        
        if user_pref:
            preferences.update({
                'preferred_difficulty': user_pref.preferred_difficulty,
                'preferred_duration': user_pref.preferred_duration,
                'preferred_content_type': user_pref.preferred_content_type,
                'preferred_language': user_pref.preferred_language,
                'interests': json.loads(user_pref.interests or '[]'),
                'skills_to_develop': json.loads(user_pref.skills_to_develop or '[]'),
                'detailed_learning_goals': json.loads(user_pref.learning_goals or '[]'),
            })
        
        return preferences
    
    def update_explicit_preferences(
        self, 
        user_id: int, 
        preferences: Dict[str, Any]
    ) -> bool:
        """
        Update user preferences from explicit user input.
        
        Args:
            user_id: User ID
            preferences: User preferences
            
        Returns:
            bool: Success status
        """
        try:
            # Update main user table
            user = self.db.query(User).filter(User.id == user_id).first()
            if user:
                if 'skill_level' in preferences:
                    user.skill_level = preferences['skill_level']
                if 'time_commitment' in preferences:
                    user.time_commitment = preferences['time_commitment']
                if 'learning_goals' in preferences:
                    user.learning_goals = json.dumps(preferences['learning_goals'])
                if 'preferred_categories' in preferences:
                    user.preferred_categories = json.dumps(preferences['preferred_categories'])
                
                user.updated_at = datetime.utcnow()
            
            # Update detailed preferences
            user_pref = self.db.query(UserPreference).filter(
                UserPreference.user_id == user_id
            ).first()
            
            if not user_pref:
                user_pref = UserPreference(user_id=user_id)
                self.db.add(user_pref)
            
            if 'preferred_difficulty' in preferences:
                user_pref.preferred_difficulty = preferences['preferred_difficulty']
            if 'preferred_duration' in preferences:
                user_pref.preferred_duration = preferences['preferred_duration']
            if 'preferred_content_type' in preferences:
                user_pref.preferred_content_type = preferences['preferred_content_type']
            if 'preferred_language' in preferences:
                user_pref.preferred_language = preferences['preferred_language']
            if 'interests' in preferences:
                user_pref.interests = json.dumps(preferences['interests'])
            if 'skills_to_develop' in preferences:
                user_pref.skills_to_develop = json.dumps(preferences['skills_to_develop'])
            
            user_pref.updated_at = datetime.utcnow()
            
            self.db.commit()
            logger.info(f"Updated explicit preferences for user {user_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error updating explicit preferences for user {user_id}: {e}")
            self.db.rollback()
            return False
    
    def get_preference_insights(self, user_id: int) -> Dict[str, Any]:
        """
        Get AI-driven insights about user preferences.
        
        Args:
            user_id: User ID
            
        Returns:
            Dict: Preference insights
        """
        # Get user's interaction statistics
        interactions = self.db.query(UserInteraction).filter(
            UserInteraction.user_id == user_id
        ).all()
        
        enrollments = self.db.query(Enrollment).filter(
            and_(
                Enrollment.user_id == user_id,
                Enrollment.is_active == True
            )
        ).all()
        
        # Calculate insights
        insights = {
            'total_interactions': len(interactions),
            'total_enrollments': len(enrollments),
            'completion_rate': 0.0,
            'engagement_score': 0.0,
            'learning_velocity': 0.0,
            'preferred_time_of_day': 'unknown',
            'learning_pattern': 'unknown'
        }
        
        if enrollments:
            completed = sum(1 for e in enrollments if e.is_completed)
            insights['completion_rate'] = (completed / len(enrollments)) * 100
        
        if interactions:
            # Calculate engagement score using optimized function
            # For user preference service, we don't have pre-calculated counts, so use basic calculation
            insights['engagement_score'] = calculate_engagement_score(interactions)
        
        return insights
