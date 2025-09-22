"""
Real-time Learning and Feedback Loop System for continuous model improvement.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime, timedelta
import logging
import json
import pickle
import os
from collections import defaultdict, deque
from dataclasses import dataclass
import threading
import time

logger = logging.getLogger(__name__)


@dataclass
class UserFeedback:
    """User feedback data structure."""
    user_id: int
    course_id: int
    feedback_type: str  # like, dislike, view, enroll, complete, rate
    rating: Optional[float] = None
    timestamp: datetime = None
    session_id: Optional[str] = None
    context: Optional[Dict] = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow()


@dataclass
class LearningMetrics:
    """Learning performance metrics."""
    accuracy: float
    precision: float
    recall: float
    f1_score: float
    user_satisfaction: float
    engagement_rate: float
    conversion_rate: float
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow()


class RealTimeLearningEngine:
    """
    Real-time learning engine that continuously improves recommendations
    based on user feedback and behavior patterns.
    """
    
    def __init__(self, feedback_buffer_size: int = 1000, learning_interval: int = 300):
        self.feedback_buffer = deque(maxlen=feedback_buffer_size)
        self.user_preference_updates = defaultdict(list)
        self.model_performance_history = deque(maxlen=100)
        self.learning_interval = learning_interval  # seconds
        self.is_learning = False
        self.learning_thread = None
        self.lock = threading.Lock()
        
        # Performance tracking
        self.recommendation_accuracy = defaultdict(list)
        self.user_engagement_scores = defaultdict(list)
        self.conversion_rates = defaultdict(list)
        
        # Start background learning
        self.start_background_learning()
    
    def record_feedback(self, feedback: UserFeedback):
        """Record user feedback for real-time learning."""
        with self.lock:
            self.feedback_buffer.append(feedback)
            
            # Update user preferences immediately for critical feedback
            if feedback.feedback_type in ['like', 'dislike', 'rate']:
                self._update_user_preferences_immediate(feedback)
            
            logger.debug(f"Recorded feedback: user={feedback.user_id}, course={feedback.course_id}, type={feedback.feedback_type}")
    
    def _update_user_preferences_immediate(self, feedback: UserFeedback):
        """Immediately update user preferences for critical feedback."""
        user_id = feedback.user_id
        course_id = feedback.course_id
        feedback_type = feedback.feedback_type
        
        # Create preference update
        preference_update = {
            'course_id': course_id,
            'feedback_type': feedback_type,
            'rating': feedback.rating,
            'timestamp': feedback.timestamp,
            'weight': self._get_feedback_weight(feedback_type, feedback.rating)
        }
        
        self.user_preference_updates[user_id].append(preference_update)
        
        # Keep only recent updates (last 30 days)
        cutoff_date = datetime.utcnow() - timedelta(days=30)
        self.user_preference_updates[user_id] = [
            update for update in self.user_preference_updates[user_id]
            if update['timestamp'] > cutoff_date
        ]
    
    def _get_feedback_weight(self, feedback_type: str, rating: Optional[float] = None) -> float:
        """Get weight for different types of feedback."""
        weights = {
            'like': 0.8,
            'dislike': -0.8,
            'rate': rating / 5.0 if rating else 0.0,  # Normalize rating to -1 to 1
            'enroll': 0.6,
            'complete': 1.0,
            'view': 0.2,
            'unlike': -0.6
        }
        
        return weights.get(feedback_type, 0.0)
    
    def start_background_learning(self):
        """Start background learning thread."""
        if self.learning_thread is None or not self.learning_thread.is_alive():
            self.learning_thread = threading.Thread(target=self._background_learning_loop, daemon=True)
            self.learning_thread.start()
            logger.info("Background learning thread started")
    
    def _background_learning_loop(self):
        """Background learning loop."""
        while True:
            try:
                time.sleep(self.learning_interval)
                if len(self.feedback_buffer) > 0:
                    self._process_feedback_batch()
                    self._update_model_performance()
            except Exception as e:
                logger.error(f"Error in background learning loop: {e}")
    
    def _process_feedback_batch(self):
        """Process a batch of feedback for learning."""
        with self.lock:
            if len(self.feedback_buffer) == 0:
                return
            
            # Get recent feedback
            recent_feedback = list(self.feedback_buffer)
            self.feedback_buffer.clear()
            
            # Process feedback
            self._analyze_feedback_patterns(recent_feedback)
            self._update_recommendation_weights(recent_feedback)
            self._detect_user_behavior_changes(recent_feedback)
            
            logger.info(f"Processed {len(recent_feedback)} feedback items")
    
    def _analyze_feedback_patterns(self, feedback_list: List[UserFeedback]):
        """Analyze patterns in user feedback."""
        # Group feedback by user
        user_feedback = defaultdict(list)
        for feedback in feedback_list:
            user_feedback[feedback.user_id].append(feedback)
        
        # Analyze patterns for each user
        for user_id, feedbacks in user_feedback.items():
            self._analyze_user_patterns(user_id, feedbacks)
    
    def _analyze_user_patterns(self, user_id: int, feedbacks: List[UserFeedback]):
        """Analyze patterns for a specific user."""
        # Calculate engagement score
        engagement_score = self._calculate_engagement_score(feedbacks)
        self.user_engagement_scores[user_id].append(engagement_score)
        
        # Track recommendation accuracy
        accuracy = self._calculate_recommendation_accuracy(user_id, feedbacks)
        self.recommendation_accuracy[user_id].append(accuracy)
        
        # Track conversion rate
        conversion_rate = self._calculate_conversion_rate(feedbacks)
        self.conversion_rates[user_id].append(conversion_rate)
    
    def _calculate_engagement_score(self, feedbacks: List[UserFeedback]) -> float:
        """Calculate user engagement score from feedback."""
        if not feedbacks:
            return 0.0
        
        # Weight different feedback types
        engagement_weights = {
            'view': 0.1,
            'like': 0.3,
            'enroll': 0.5,
            'complete': 1.0,
            'rate': 0.4,
            'dislike': -0.2,
            'unlike': -0.3
        }
        
        total_score = 0.0
        for feedback in feedbacks:
            weight = engagement_weights.get(feedback.feedback_type, 0.0)
            if feedback.rating:
                weight *= (feedback.rating / 5.0)  # Normalize rating
            total_score += weight
        
        return total_score / len(feedbacks)
    
    def _calculate_recommendation_accuracy(self, user_id: int, feedbacks: List[UserFeedback]) -> float:
        """Calculate recommendation accuracy for a user."""
        positive_feedback = ['like', 'enroll', 'complete']
        negative_feedback = ['dislike', 'unlike']
        
        positive_count = sum(1 for f in feedbacks if f.feedback_type in positive_feedback)
        negative_count = sum(1 for f in feedbacks if f.feedback_type in negative_feedback)
        
        total_feedback = positive_count + negative_count
        if total_feedback == 0:
            return 0.5  # Neutral accuracy
        
        return positive_count / total_feedback
    
    def _calculate_conversion_rate(self, feedbacks: List[UserFeedback]) -> float:
        """Calculate conversion rate from feedback."""
        views = sum(1 for f in feedbacks if f.feedback_type == 'view')
        enrollments = sum(1 for f in feedbacks if f.feedback_type == 'enroll')
        
        if views == 0:
            return 0.0
        
        return enrollments / views
    
    def _update_recommendation_weights(self, feedback_list: List[UserFeedback]):
        """Update recommendation weights based on feedback."""
        # Group by course
        course_feedback = defaultdict(list)
        for feedback in feedback_list:
            course_feedback[feedback.course_id].append(feedback)
        
        # Update weights for each course
        for course_id, feedbacks in course_feedback.items():
            self._update_course_weights(course_id, feedbacks)
    
    def _update_course_weights(self, course_id: int, feedbacks: List[UserFeedback]):
        """Update weights for a specific course."""
        # Calculate average feedback score
        total_score = 0.0
        total_weight = 0.0
        
        for feedback in feedbacks:
            weight = self._get_feedback_weight(feedback.feedback_type, feedback.rating)
            total_score += weight
            total_weight += abs(weight)
        
        if total_weight > 0:
            average_score = total_score / total_weight
            # Update course recommendation weight (this would integrate with main recommendation engine)
            self._apply_course_weight_update(course_id, average_score)
    
    def _apply_course_weight_update(self, course_id: int, weight_delta: float):
        """Apply course weight update to the recommendation system."""
        # This would integrate with the main recommendation engine
        # For now, we'll log the update
        logger.debug(f"Updating course {course_id} weight by {weight_delta}")
    
    def _detect_user_behavior_changes(self, feedback_list: List[UserFeedback]):
        """Detect changes in user behavior patterns."""
        # Group by user
        user_feedback = defaultdict(list)
        for feedback in feedback_list:
            user_feedback[feedback.user_id].append(feedback)
        
        # Analyze behavior changes for each user
        for user_id, feedbacks in user_feedback.items():
            self._analyze_user_behavior_change(user_id, feedbacks)
    
    def _analyze_user_behavior_change(self, user_id: int, feedbacks: List[UserFeedback]):
        """Analyze behavior changes for a specific user."""
        # Get recent engagement scores
        recent_scores = self.user_engagement_scores[user_id][-10:]  # Last 10 scores
        
        if len(recent_scores) < 5:
            return
        
        # Calculate trend
        trend = self._calculate_trend(recent_scores)
        
        # Detect significant changes
        if abs(trend) > 0.2:  # Significant change threshold
            change_type = "increasing" if trend > 0 else "decreasing"
            logger.info(f"User {user_id} engagement trend: {change_type} (trend: {trend:.3f})")
            
            # Trigger adaptive recommendations
            self._trigger_adaptive_recommendations(user_id, change_type, trend)
    
    def _calculate_trend(self, scores: List[float]) -> float:
        """Calculate trend in a series of scores."""
        if len(scores) < 2:
            return 0.0
        
        # Simple linear trend calculation
        x = np.arange(len(scores))
        y = np.array(scores)
        
        # Calculate slope
        slope = np.polyfit(x, y, 1)[0]
        return slope
    
    def _trigger_adaptive_recommendations(self, user_id: int, change_type: str, trend: float):
        """Trigger adaptive recommendations based on behavior changes."""
        # This would integrate with the main recommendation engine
        # to adjust recommendation strategies for the user
        
        adaptive_strategy = {
            'user_id': user_id,
            'change_type': change_type,
            'trend': trend,
            'timestamp': datetime.utcnow(),
            'action': self._get_adaptive_action(change_type, trend)
        }
        
        logger.info(f"Adaptive strategy for user {user_id}: {adaptive_strategy['action']}")
    
    def _get_adaptive_action(self, change_type: str, trend: float) -> str:
        """Get adaptive action based on behavior change."""
        if change_type == "increasing" and trend > 0.3:
            return "increase_difficulty"
        elif change_type == "decreasing" and trend < -0.3:
            return "decrease_difficulty"
        elif change_type == "increasing":
            return "maintain_engagement"
        else:
            return "boost_engagement"
    
    def _update_model_performance(self):
        """Update overall model performance metrics."""
        # Calculate aggregate metrics
        all_accuracy_scores = []
        all_engagement_scores = []
        all_conversion_rates = []
        
        for user_scores in self.recommendation_accuracy.values():
            if user_scores:
                all_accuracy_scores.append(user_scores[-1])
        
        for user_scores in self.user_engagement_scores.values():
            if user_scores:
                all_engagement_scores.append(user_scores[-1])
        
        for user_rates in self.conversion_rates.values():
            if user_rates:
                all_conversion_rates.append(user_rates[-1])
        
        if all_accuracy_scores and all_engagement_scores and all_conversion_rates:
            metrics = LearningMetrics(
                accuracy=np.mean(all_accuracy_scores),
                precision=np.mean(all_accuracy_scores),  # Simplified
                recall=np.mean(all_accuracy_scores),     # Simplified
                f1_score=np.mean(all_accuracy_scores),   # Simplified
                user_satisfaction=np.mean(all_engagement_scores),
                engagement_rate=np.mean(all_engagement_scores),
                conversion_rate=np.mean(all_conversion_rates)
            )
            
            self.model_performance_history.append(metrics)
            
            logger.info(f"Model performance updated: accuracy={metrics.accuracy:.3f}, "
                       f"engagement={metrics.engagement_rate:.3f}, "
                       f"conversion={metrics.conversion_rate:.3f}")
    
    def get_user_insights(self, user_id: int) -> Dict[str, Any]:
        """Get insights about a user's learning patterns."""
        insights = {
            'user_id': user_id,
            'engagement_trend': self._get_engagement_trend(user_id),
            'recommendation_accuracy': self._get_recent_accuracy(user_id),
            'conversion_rate': self._get_recent_conversion_rate(user_id),
            'preference_updates': len(self.user_preference_updates.get(user_id, [])),
            'learning_velocity': self._calculate_learning_velocity(user_id),
            'recommended_actions': self._get_recommended_actions(user_id)
        }
        
        return insights
    
    def _get_engagement_trend(self, user_id: int) -> float:
        """Get engagement trend for a user."""
        scores = self.user_engagement_scores.get(user_id, [])
        if len(scores) < 2:
            return 0.0
        
        return self._calculate_trend(scores[-10:])  # Last 10 scores
    
    def _get_recent_accuracy(self, user_id: int) -> float:
        """Get recent recommendation accuracy for a user."""
        scores = self.recommendation_accuracy.get(user_id, [])
        return scores[-1] if scores else 0.5
    
    def _get_recent_conversion_rate(self, user_id: int) -> float:
        """Get recent conversion rate for a user."""
        rates = self.conversion_rates.get(user_id, [])
        return rates[-1] if rates else 0.0
    
    def _calculate_learning_velocity(self, user_id: int) -> float:
        """Calculate user's learning velocity."""
        preference_updates = self.user_preference_updates.get(user_id, [])
        if not preference_updates:
            return 0.0
        
        # Calculate updates per day over last 30 days
        recent_updates = [
            update for update in preference_updates
            if update['timestamp'] > datetime.utcnow() - timedelta(days=30)
        ]
        
        return len(recent_updates) / 30.0  # Updates per day
    
    def _get_recommended_actions(self, user_id: int) -> List[str]:
        """Get recommended actions for improving user experience."""
        actions = []
        
        engagement_trend = self._get_engagement_trend(user_id)
        accuracy = self._get_recent_accuracy(user_id)
        conversion_rate = self._get_recent_conversion_rate(user_id)
        
        if engagement_trend < -0.2:
            actions.append("Consider easier content to boost engagement")
        
        if accuracy < 0.4:
            actions.append("Improve recommendation targeting")
        
        if conversion_rate < 0.1:
            actions.append("Focus on high-quality, relevant content")
        
        if engagement_trend > 0.3:
            actions.append("User is highly engaged - consider advanced content")
        
        return actions
    
    def get_model_performance_summary(self) -> Dict[str, Any]:
        """Get summary of model performance."""
        if not self.model_performance_history:
            return {"message": "No performance data available"}
        
        latest_metrics = self.model_performance_history[-1]
        
        return {
            'latest_metrics': {
                'accuracy': latest_metrics.accuracy,
                'user_satisfaction': latest_metrics.user_satisfaction,
                'engagement_rate': latest_metrics.engagement_rate,
                'conversion_rate': latest_metrics.conversion_rate,
                'timestamp': latest_metrics.timestamp.isoformat()
            },
            'trends': self._calculate_performance_trends(),
            'total_users_tracked': len(self.user_engagement_scores),
            'total_feedback_processed': len(self.feedback_buffer) + sum(len(updates) for updates in self.user_preference_updates.values())
        }
    
    def _calculate_performance_trends(self) -> Dict[str, float]:
        """Calculate performance trends."""
        if len(self.model_performance_history) < 2:
            return {}
        
        recent_metrics = [m for m in self.model_performance_history][-10:]  # Last 10 metrics
        
        trends = {}
        for metric in ['accuracy', 'user_satisfaction', 'engagement_rate', 'conversion_rate']:
            values = [getattr(m, metric) for m in recent_metrics]
            trends[metric] = self._calculate_trend(values)
        
        return trends
    
    def save_learning_state(self, filepath: str):
        """Save learning state to file."""
        state = {
            'user_preference_updates': dict(self.user_preference_updates),
            'model_performance_history': list(self.model_performance_history),
            'recommendation_accuracy': dict(self.recommendation_accuracy),
            'user_engagement_scores': dict(self.user_engagement_scores),
            'conversion_rates': dict(self.conversion_rates)
        }
        
        with open(filepath, 'wb') as f:
            pickle.dump(state, f)
        
        logger.info(f"Learning state saved to {filepath}")
    
    def load_learning_state(self, filepath: str):
        """Load learning state from file."""
        if not os.path.exists(filepath):
            logger.warning(f"Learning state file not found: {filepath}")
            return
        
        with open(filepath, 'rb') as f:
            state = pickle.load(f)
        
        self.user_preference_updates = defaultdict(list, state.get('user_preference_updates', {}))
        self.model_performance_history = deque(state.get('model_performance_history', []), maxlen=100)
        self.recommendation_accuracy = defaultdict(list, state.get('recommendation_accuracy', {}))
        self.user_engagement_scores = defaultdict(list, state.get('user_engagement_scores', {}))
        self.conversion_rates = defaultdict(list, state.get('conversion_rates', {}))
        
        logger.info(f"Learning state loaded from {filepath}")
