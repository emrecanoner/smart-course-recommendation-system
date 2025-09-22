"""
Context-Aware Recommendation Engine for intelligent course recommendations.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime, timedelta
import logging
from dataclasses import dataclass
from enum import Enum
import json

logger = logging.getLogger(__name__)


class ContextType(Enum):
    """Types of context for recommendations."""
    TIME_OF_DAY = "time_of_day"
    DAY_OF_WEEK = "day_of_week"
    LEARNING_SESSION = "learning_session"
    DEVICE_TYPE = "device_type"
    USER_MOOD = "user_mood"
    LEARNING_GOAL = "learning_goal"
    SKILL_LEVEL = "skill_level"
    AVAILABLE_TIME = "available_time"


@dataclass
class UserContext:
    """User context information for recommendations."""
    time_of_day: str  # morning, afternoon, evening, night
    day_of_week: str  # weekday, weekend
    learning_session: str  # quick, focused, deep
    device_type: str  # mobile, desktop, tablet
    user_mood: str  # motivated, tired, curious, focused
    learning_goal: str  # skill_development, career_change, hobby, certification
    skill_level: str  # beginner, intermediate, advanced
    available_time: int  # minutes available for learning
    previous_course_completion: Optional[float] = None  # completion rate of last course
    learning_streak: int = 0  # consecutive days of learning
    preferred_difficulty: Optional[str] = None
    preferred_content_type: Optional[str] = None


class ContextAwareRecommendationEngine:
    """
    Context-aware recommendation engine that considers multiple contextual factors
    to provide highly personalized course recommendations.
    """
    
    def __init__(self):
        self.context_weights = self._initialize_context_weights()
        self.time_preferences = self._initialize_time_preferences()
        self.session_preferences = self._initialize_session_preferences()
        self.mood_preferences = self._initialize_mood_preferences()
        self.goal_preferences = self._initialize_goal_preferences()
    
    def _initialize_context_weights(self) -> Dict[ContextType, float]:
        """Initialize weights for different context factors."""
        return {
            ContextType.TIME_OF_DAY: 0.15,
            ContextType.DAY_OF_WEEK: 0.10,
            ContextType.LEARNING_SESSION: 0.20,
            ContextType.DEVICE_TYPE: 0.05,
            ContextType.USER_MOOD: 0.15,
            ContextType.LEARNING_GOAL: 0.20,
            ContextType.SKILL_LEVEL: 0.10,
            ContextType.AVAILABLE_TIME: 0.05
        }
    
    def _initialize_time_preferences(self) -> Dict[str, Dict[str, float]]:
        """Initialize time-based course preferences."""
        return {
            "morning": {
                "difficulty_boost": {"beginner": 0.1, "intermediate": 0.0, "advanced": -0.1},
                "content_type_boost": {"video": 0.1, "text": 0.0, "interactive": 0.05},
                "duration_boost": {"short": 0.1, "medium": 0.0, "long": -0.1}
            },
            "afternoon": {
                "difficulty_boost": {"beginner": 0.0, "intermediate": 0.1, "advanced": 0.0},
                "content_type_boost": {"video": 0.0, "text": 0.1, "interactive": 0.1},
                "duration_boost": {"short": 0.0, "medium": 0.1, "long": 0.0}
            },
            "evening": {
                "difficulty_boost": {"beginner": 0.0, "intermediate": 0.0, "advanced": 0.1},
                "content_type_boost": {"video": 0.1, "text": -0.1, "interactive": 0.0},
                "duration_boost": {"short": 0.0, "medium": 0.0, "long": 0.1}
            },
            "night": {
                "difficulty_boost": {"beginner": 0.1, "intermediate": -0.1, "advanced": -0.2},
                "content_type_boost": {"video": 0.2, "text": -0.2, "interactive": -0.1},
                "duration_boost": {"short": 0.2, "medium": -0.1, "long": -0.2}
            }
        }
    
    def _initialize_session_preferences(self) -> Dict[str, Dict[str, float]]:
        """Initialize session-based course preferences."""
        return {
            "quick": {
                "duration_boost": {"short": 0.3, "medium": -0.2, "long": -0.5},
                "content_type_boost": {"video": 0.1, "text": 0.2, "interactive": 0.0},
                "difficulty_boost": {"beginner": 0.1, "intermediate": 0.0, "advanced": -0.1}
            },
            "focused": {
                "duration_boost": {"short": 0.0, "medium": 0.2, "long": 0.1},
                "content_type_boost": {"video": 0.0, "text": 0.1, "interactive": 0.2},
                "difficulty_boost": {"beginner": 0.0, "intermediate": 0.1, "advanced": 0.1}
            },
            "deep": {
                "duration_boost": {"short": -0.2, "medium": 0.1, "long": 0.3},
                "content_type_boost": {"video": 0.1, "text": 0.2, "interactive": 0.1},
                "difficulty_boost": {"beginner": -0.1, "intermediate": 0.1, "advanced": 0.2}
            }
        }
    
    def _initialize_mood_preferences(self) -> Dict[str, Dict[str, float]]:
        """Initialize mood-based course preferences."""
        return {
            "motivated": {
                "difficulty_boost": {"beginner": 0.0, "intermediate": 0.1, "advanced": 0.2},
                "content_type_boost": {"video": 0.0, "text": 0.1, "interactive": 0.2},
                "duration_boost": {"short": 0.0, "medium": 0.1, "long": 0.1}
            },
            "tired": {
                "difficulty_boost": {"beginner": 0.2, "intermediate": -0.1, "advanced": -0.2},
                "content_type_boost": {"video": 0.2, "text": -0.1, "interactive": -0.1},
                "duration_boost": {"short": 0.3, "medium": -0.1, "long": -0.2}
            },
            "curious": {
                "difficulty_boost": {"beginner": 0.1, "intermediate": 0.1, "advanced": 0.0},
                "content_type_boost": {"video": 0.1, "text": 0.0, "interactive": 0.2},
                "duration_boost": {"short": 0.1, "medium": 0.1, "long": 0.0}
            },
            "focused": {
                "difficulty_boost": {"beginner": 0.0, "intermediate": 0.1, "advanced": 0.1},
                "content_type_boost": {"video": 0.0, "text": 0.2, "interactive": 0.1},
                "duration_boost": {"short": 0.0, "medium": 0.2, "long": 0.1}
            }
        }
    
    def _initialize_goal_preferences(self) -> Dict[str, Dict[str, float]]:
        """Initialize goal-based course preferences."""
        return {
            "skill_development": {
                "difficulty_boost": {"beginner": 0.1, "intermediate": 0.2, "advanced": 0.1},
                "content_type_boost": {"video": 0.1, "text": 0.1, "interactive": 0.2},
                "duration_boost": {"short": 0.0, "medium": 0.1, "long": 0.1}
            },
            "career_change": {
                "difficulty_boost": {"beginner": 0.2, "intermediate": 0.1, "advanced": 0.0},
                "content_type_boost": {"video": 0.1, "text": 0.2, "interactive": 0.1},
                "duration_boost": {"short": 0.0, "medium": 0.2, "long": 0.1}
            },
            "hobby": {
                "difficulty_boost": {"beginner": 0.2, "intermediate": 0.0, "advanced": -0.1},
                "content_type_boost": {"video": 0.2, "text": 0.0, "interactive": 0.1},
                "duration_boost": {"short": 0.1, "medium": 0.0, "long": -0.1}
            },
            "certification": {
                "difficulty_boost": {"beginner": 0.0, "intermediate": 0.1, "advanced": 0.2},
                "content_type_boost": {"video": 0.0, "text": 0.2, "interactive": 0.1},
                "duration_boost": {"short": -0.1, "medium": 0.1, "long": 0.2}
            }
        }
    
    def extract_context_from_request(self, request_data: Dict) -> UserContext:
        """Extract user context from request data."""
        current_time = datetime.now()
        
        # Determine time of day
        hour = current_time.hour
        if 5 <= hour < 12:
            time_of_day = "morning"
        elif 12 <= hour < 17:
            time_of_day = "afternoon"
        elif 17 <= hour < 22:
            time_of_day = "evening"
        else:
            time_of_day = "night"
        
        # Determine day of week
        day_of_week = "weekday" if current_time.weekday() < 5 else "weekend"
        
        # Extract from request or use defaults
        learning_session = request_data.get('learning_session', 'focused')
        device_type = request_data.get('device_type', 'desktop')
        user_mood = request_data.get('user_mood', 'motivated')
        learning_goal = request_data.get('learning_goal', 'skill_development')
        skill_level = request_data.get('skill_level', 'intermediate')
        available_time = request_data.get('available_time', 60)  # minutes
        
        return UserContext(
            time_of_day=time_of_day,
            day_of_week=day_of_week,
            learning_session=learning_session,
            device_type=device_type,
            user_mood=user_mood,
            learning_goal=learning_goal,
            skill_level=skill_level,
            available_time=available_time,
            previous_course_completion=request_data.get('previous_course_completion'),
            learning_streak=request_data.get('learning_streak', 0),
            preferred_difficulty=request_data.get('preferred_difficulty'),
            preferred_content_type=request_data.get('preferred_content_type')
        )
    
    def calculate_context_score(self, course: Dict, context: UserContext) -> float:
        """Calculate context-based score for a course."""
        total_score = 0.0
        
        # Time-based scoring
        time_score = self._calculate_time_score(course, context)
        total_score += time_score * self.context_weights[ContextType.TIME_OF_DAY]
        
        # Session-based scoring
        session_score = self._calculate_session_score(course, context)
        total_score += session_score * self.context_weights[ContextType.LEARNING_SESSION]
        
        # Mood-based scoring
        mood_score = self._calculate_mood_score(course, context)
        total_score += mood_score * self.context_weights[ContextType.USER_MOOD]
        
        # Goal-based scoring
        goal_score = self._calculate_goal_score(course, context)
        total_score += goal_score * self.context_weights[ContextType.LEARNING_GOAL]
        
        # Skill level scoring
        skill_score = self._calculate_skill_score(course, context)
        total_score += skill_score * self.context_weights[ContextType.SKILL_LEVEL]
        
        # Available time scoring
        time_availability_score = self._calculate_time_availability_score(course, context)
        total_score += time_availability_score * self.context_weights[ContextType.AVAILABLE_TIME]
        
        # Learning streak bonus
        streak_bonus = self._calculate_streak_bonus(course, context)
        total_score += streak_bonus
        
        return max(0.0, min(1.0, total_score))  # Normalize to 0-1 range
    
    def _calculate_time_score(self, course: Dict, context: UserContext) -> float:
        """Calculate time-based score."""
        time_prefs = self.time_preferences.get(context.time_of_day, {})
        
        score = 0.0
        
        # Difficulty boost
        difficulty = course.get('difficulty_level', '').lower()
        difficulty_boost = time_prefs.get('difficulty_boost', {}).get(difficulty, 0.0)
        score += difficulty_boost
        
        # Content type boost
        content_type = course.get('content_type', '').lower()
        content_boost = time_prefs.get('content_type_boost', {}).get(content_type, 0.0)
        score += content_boost
        
        # Duration boost
        duration_hours = course.get('duration_hours', 0)
        duration_category = self._categorize_duration(duration_hours)
        duration_boost = time_prefs.get('duration_boost', {}).get(duration_category, 0.0)
        score += duration_boost
        
        return score
    
    def _calculate_session_score(self, course: Dict, context: UserContext) -> float:
        """Calculate session-based score."""
        session_prefs = self.session_preferences.get(context.learning_session, {})
        
        score = 0.0
        
        # Duration boost
        duration_hours = course.get('duration_hours', 0)
        duration_category = self._categorize_duration(duration_hours)
        duration_boost = session_prefs.get('duration_boost', {}).get(duration_category, 0.0)
        score += duration_boost
        
        # Content type boost
        content_type = course.get('content_type', '').lower()
        content_boost = session_prefs.get('content_type_boost', {}).get(content_type, 0.0)
        score += content_boost
        
        # Difficulty boost
        difficulty = course.get('difficulty_level', '').lower()
        difficulty_boost = session_prefs.get('difficulty_boost', {}).get(difficulty, 0.0)
        score += difficulty_boost
        
        return score
    
    def _calculate_mood_score(self, course: Dict, context: UserContext) -> float:
        """Calculate mood-based score."""
        mood_prefs = self.mood_preferences.get(context.user_mood, {})
        
        score = 0.0
        
        # Difficulty boost
        difficulty = course.get('difficulty_level', '').lower()
        difficulty_boost = mood_prefs.get('difficulty_boost', {}).get(difficulty, 0.0)
        score += difficulty_boost
        
        # Content type boost
        content_type = course.get('content_type', '').lower()
        content_boost = mood_prefs.get('content_type_boost', {}).get(content_type, 0.0)
        score += content_boost
        
        # Duration boost
        duration_hours = course.get('duration_hours', 0)
        duration_category = self._categorize_duration(duration_hours)
        duration_boost = mood_prefs.get('duration_boost', {}).get(duration_category, 0.0)
        score += duration_boost
        
        return score
    
    def _calculate_goal_score(self, course: Dict, context: UserContext) -> float:
        """Calculate goal-based score."""
        goal_prefs = self.goal_preferences.get(context.learning_goal, {})
        
        score = 0.0
        
        # Difficulty boost
        difficulty = course.get('difficulty_level', '').lower()
        difficulty_boost = goal_prefs.get('difficulty_boost', {}).get(difficulty, 0.0)
        score += difficulty_boost
        
        # Content type boost
        content_type = course.get('content_type', '').lower()
        content_boost = goal_prefs.get('content_type_boost', {}).get(content_type, 0.0)
        score += content_boost
        
        # Duration boost
        duration_hours = course.get('duration_hours', 0)
        duration_category = self._categorize_duration(duration_hours)
        duration_boost = goal_prefs.get('duration_boost', {}).get(duration_category, 0.0)
        score += duration_boost
        
        return score
    
    def _calculate_skill_score(self, course: Dict, context: UserContext) -> float:
        """Calculate skill level matching score."""
        course_difficulty = course.get('difficulty_level', '').lower()
        user_skill = context.skill_level.lower()
        
        # Perfect match
        if course_difficulty == user_skill:
            return 0.2
        
        # Adjacent levels
        skill_levels = ['beginner', 'intermediate', 'advanced']
        user_idx = skill_levels.index(user_skill) if user_skill in skill_levels else 1
        course_idx = skill_levels.index(course_difficulty) if course_difficulty in skill_levels else 1
        
        if abs(user_idx - course_idx) == 1:
            return 0.1
        
        # Too far apart
        return -0.1
    
    def _calculate_time_availability_score(self, course: Dict, context: UserContext) -> float:
        """Calculate score based on available time."""
        course_duration = course.get('duration_hours', 0) * 60  # Convert to minutes
        available_time = context.available_time
        
        if course_duration <= available_time:
            # Perfect fit or shorter
            return 0.1
        elif course_duration <= available_time * 1.5:
            # Slightly longer but manageable
            return 0.0
        else:
            # Too long
            return -0.2
    
    def _calculate_streak_bonus(self, course: Dict, context: UserContext) -> float:
        """Calculate learning streak bonus."""
        if context.learning_streak >= 7:
            # Strong streak - boost challenging content
            difficulty = course.get('difficulty_level', '').lower()
            if difficulty == 'advanced':
                return 0.1
            elif difficulty == 'intermediate':
                return 0.05
        elif context.learning_streak >= 3:
            # Moderate streak - slight boost
            return 0.02
        
        return 0.0
    
    def _categorize_duration(self, duration_hours: float) -> str:
        """Categorize course duration."""
        if duration_hours <= 2:
            return "short"
        elif duration_hours <= 8:
            return "medium"
        else:
            return "long"
    
    def enhance_recommendations_with_context(
        self, 
        recommendations: List[Dict], 
        context: UserContext
    ) -> List[Dict]:
        """Enhance recommendations with context-aware scoring."""
        enhanced_recommendations = []
        
        for rec in recommendations:
            # Calculate context score
            context_score = self.calculate_context_score(rec, context)
            
            # Combine with original confidence score
            original_confidence = rec.get('confidence_score', 0.5)
            enhanced_confidence = (original_confidence * 0.7) + (context_score * 0.3)
            
            # Create enhanced recommendation
            enhanced_rec = rec.copy()
            enhanced_rec['confidence_score'] = min(0.95, enhanced_confidence)
            enhanced_rec['context_score'] = context_score
            enhanced_rec['context_factors'] = self._get_context_factors(rec, context)
            
            enhanced_recommendations.append(enhanced_rec)
        
        # Sort by enhanced confidence score
        enhanced_recommendations.sort(key=lambda x: x['confidence_score'], reverse=True)
        
        return enhanced_recommendations
    
    def _get_context_factors(self, course: Dict, context: UserContext) -> Dict[str, Any]:
        """Get context factors that influenced the recommendation."""
        factors = {
            'time_of_day': context.time_of_day,
            'learning_session': context.learning_session,
            'user_mood': context.user_mood,
            'learning_goal': context.learning_goal,
            'skill_level_match': self._calculate_skill_score(course, context),
            'time_availability': self._calculate_time_availability_score(course, context),
            'learning_streak': context.learning_streak
        }
        
        return factors
