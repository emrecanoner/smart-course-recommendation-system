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
from sqlalchemy import text, func
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import TruncatedSVD
import re
import pickle

# Add backend path for imports
backend_path = os.path.join(os.path.dirname(__file__), '..', '..', 'backend')
if backend_path not in sys.path:
    sys.path.append(backend_path)

from app.models.course import Course
from app.models.interaction import UserInteraction
from app.models.enrollment import Enrollment
from app.schemas.recommendation import RecommendationResponse

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class AIRecommendationEngine:
    """
    AI-powered recommendation engine that uses multiple algorithms
    to provide personalized course recommendations.
    """
    
    def __init__(self, db: Session):
        self.db = db
        self.min_interactions_for_ai = 5  # Minimum interactions needed for AI recommendations
        self.min_enrollments_for_ai = 2   # Minimum enrollments needed for AI recommendations
        
        # Initialize ML components
        self.tfidf_vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words='english',
            ngram_range=(1, 2),
            min_df=2,
            max_df=0.8
        )
        self.course_tfidf_matrix = None
        self.course_ids = None
        self.svd_model = None
        self._initialize_ml_models()
    
    def _initialize_ml_models(self):
        """Initialize ML models for content-based recommendations."""
        try:
            # Load all courses for TF-IDF vectorization
            courses = self.db.query(Course).filter(Course.is_active == True).all()
            
            if not courses:
                logger.warning("No active courses found for ML model initialization")
                return
            
            # Prepare course text data
            course_texts = []
            self.course_ids = []
            
            for course in courses:
                # Combine course title, description, and skills
                text_parts = []
                if course.title:
                    text_parts.append(course.title)
                if course.description:
                    text_parts.append(course.description)
                if course.short_description:
                    text_parts.append(course.short_description)
                if course.skills:
                    text_parts.extend(course.skills)
                if course.category and course.category.name:
                    text_parts.append(course.category.name)
                if course.difficulty_level:
                    text_parts.append(course.difficulty_level)
                if course.content_type:
                    text_parts.append(course.content_type)
                
                course_text = ' '.join(text_parts)
                course_texts.append(course_text)
                self.course_ids.append(course.id)
            
            # Fit TF-IDF vectorizer
            self.course_tfidf_matrix = self.tfidf_vectorizer.fit_transform(course_texts)
            
            # Apply SVD for dimensionality reduction
            self.svd_model = TruncatedSVD(n_components=100, random_state=42)
            self.course_tfidf_matrix = self.svd_model.fit_transform(self.course_tfidf_matrix)
            
            # logger.info(f"ML models initialized with {len(courses)} courses")
            
        except Exception as e:
            logger.error(f"Error initializing ML models: {e}")
            self.course_tfidf_matrix = None
            self.course_ids = None
            self.svd_model = None
        
    def get_recommendations(
        self, 
        user_id: int, 
        limit: int = 10, 
        algorithm: str = "hybrid",
        difficulty_level: Optional[str] = None,
        categories: Optional[List[str]] = None,
        max_duration_hours: Optional[int] = None,
        content_type: Optional[str] = None
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
                recommendations = self._collaborative_filtering(user_id, limit, user_profile, difficulty_level, categories, max_duration_hours, content_type)
            elif algorithm == "content":
                recommendations = self._content_based_filtering(user_id, limit, user_profile, difficulty_level, categories, max_duration_hours, content_type)
            elif algorithm == "hybrid":
                recommendations = self._hybrid_recommendations(user_id, limit, user_profile, difficulty_level, categories, max_duration_hours, content_type)
            elif algorithm == "popularity":
                recommendations = self._popularity_based_recommendations(user_id, limit, user_profile, difficulty_level, categories, max_duration_hours, content_type)
            else:
                recommendations = self._hybrid_recommendations(user_id, limit, user_profile, difficulty_level, categories, max_duration_hours, content_type)
            
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
            Enrollment.deleted_at.is_(None)
        ).count()
        
        # Check if user has enough data
        has_sufficient_interactions = interaction_count >= self.min_interactions_for_ai
        has_sufficient_enrollments = enrollment_count >= self.min_enrollments_for_ai
        
        # logger.info(f"User {user_id} data check: interactions={interaction_count}, enrollments={enrollment_count}")
        
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
    
    def _collaborative_filtering(self, user_id: int, limit: int, user_profile: Dict, difficulty_level: Optional[str] = None, categories: Optional[List[str]] = None, max_duration_hours: Optional[int] = None, content_type: Optional[str] = None) -> List[RecommendationResponse]:
        """
        Advanced collaborative filtering with matrix factorization and temporal weighting.
        
        Args:
            user_id: User ID
            limit: Number of recommendations
            user_profile: User profile data
            
        Returns:
            List[RecommendationResponse]: Recommendations
        """
        try:
            # logger.info(f"DEBUG: Starting collaborative filtering for user {user_id} with filters: difficulty_level={difficulty_level}, categories={categories}, max_duration_hours={max_duration_hours}, content_type={content_type}")
            # Try advanced collaborative filtering first
            advanced_recs = self._advanced_collaborative_filtering(user_id, limit, user_profile, difficulty_level, categories, max_duration_hours, content_type)
            if advanced_recs:
                return advanced_recs
            
            # Fallback to traditional collaborative filtering
            traditional_recs = self._traditional_collaborative_filtering(user_id, limit, user_profile, difficulty_level, categories, max_duration_hours, content_type)
            return traditional_recs
            
        except Exception as e:
            logger.error(f"Error in collaborative filtering: {e}")
            try:
                traditional_recs = self._traditional_collaborative_filtering(user_id, limit, user_profile, difficulty_level, categories, max_duration_hours, content_type)
                return traditional_recs
            except Exception as e2:
                logger.error(f"Error in traditional collaborative filtering: {e2}")
                return []
    
    def _advanced_collaborative_filtering(self, user_id: int, limit: int, user_profile: Dict, difficulty_level: Optional[str] = None, categories: Optional[List[str]] = None, max_duration_hours: Optional[int] = None, content_type: Optional[str] = None) -> List[RecommendationResponse]:
        """Advanced collaborative filtering using user-item matrix and similarity."""
        try:
            # Rollback any failed transaction
            try:
                self.db.rollback()
            except:
                pass
            # Get all user interactions for matrix building
            all_interactions = self.db.query(UserInteraction).filter(
                UserInteraction.interaction_type.in_(['like', 'enroll', 'complete', 'rate'])
            ).all()
            
            if not all_interactions:
                return []
            
            # Build user-item matrix
            user_item_matrix = self._build_user_item_matrix(all_interactions)
            
            if user_item_matrix is None or user_id not in user_item_matrix:
                return []
            
            # Find similar users using cosine similarity
            similar_users = self._find_similar_users(user_id, user_item_matrix, top_k=20)
            
            if not similar_users:
                return []
            
            # Get recommendations from similar users
            recommendations = self._get_recommendations_from_similar_users(
                user_id, similar_users, user_item_matrix, limit, difficulty_level, categories, max_duration_hours, content_type
            )
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Error in advanced collaborative filtering: {e}")
            return []
    
    def _build_user_item_matrix(self, interactions: List) -> Optional[Dict]:
        """Build user-item interaction matrix with temporal weighting."""
        try:
            user_item_matrix = {}
            
            for interaction in interactions:
                user_id = interaction.user_id
                course_id = interaction.course_id
                
                if user_id not in user_item_matrix:
                    user_item_matrix[user_id] = {}
                
                # Calculate interaction weight with temporal decay
                weight = self._get_interaction_weight(interaction)
                
                # Accumulate weights for multiple interactions
                if course_id in user_item_matrix[user_id]:
                    user_item_matrix[user_id][course_id] += weight
                else:
                    user_item_matrix[user_id][course_id] = weight
            
            return user_item_matrix
            
        except Exception as e:
            logger.error(f"Error building user-item matrix: {e}")
            return None
    
    def _find_similar_users(self, user_id: int, user_item_matrix: Dict, top_k: int = 20) -> List[Tuple[int, float]]:
        """Find similar users using cosine similarity."""
        try:
            if user_id not in user_item_matrix:
                return []
            
            target_user_items = user_item_matrix[user_id]
            similar_users = []
            
            for other_user_id, other_user_items in user_item_matrix.items():
                if other_user_id == user_id:
                    continue
                
                # Calculate cosine similarity
                similarity = self._calculate_cosine_similarity(target_user_items, other_user_items)
                
                if similarity > 0.1:  # Minimum similarity threshold
                    similar_users.append((other_user_id, similarity))
            
            # Sort by similarity and return top k
            similar_users.sort(key=lambda x: x[1], reverse=True)
            return similar_users[:top_k]
            
        except Exception as e:
            logger.error(f"Error finding similar users: {e}")
            return []
    
    def _calculate_cosine_similarity(self, user1_items: Dict, user2_items: Dict) -> float:
        """Calculate cosine similarity between two user's item vectors."""
        try:
            # Get common items
            common_items = set(user1_items.keys()).intersection(set(user2_items.keys()))
            
            if not common_items:
                return 0.0
            
            # Calculate dot product and magnitudes
            dot_product = sum(user1_items[item] * user2_items[item] for item in common_items)
            magnitude1 = sum(user1_items[item] ** 2 for item in user1_items) ** 0.5
            magnitude2 = sum(user2_items[item] ** 2 for item in user2_items) ** 0.5
            
            if magnitude1 == 0 or magnitude2 == 0:
                return 0.0
            
            return dot_product / (magnitude1 * magnitude2)
            
        except Exception as e:
            logger.error(f"Error calculating cosine similarity: {e}")
            return 0.0
    
    def _get_recommendations_from_similar_users(
        self, 
        user_id: int, 
        similar_users: List[Tuple[int, float]], 
        user_item_matrix: Dict, 
        limit: int,
        difficulty_level: Optional[str] = None,
        categories: Optional[List[str]] = None,
        max_duration_hours: Optional[int] = None,
        content_type: Optional[str] = None
    ) -> List[RecommendationResponse]:
        """Get recommendations from similar users."""
        try:
            # Get user's interacted courses
            user_interactions = self.db.query(UserInteraction.course_id).filter(
                UserInteraction.user_id == user_id
            ).all()
            user_course_ids = {interaction.course_id for interaction in user_interactions}
            
            # Collect course scores from similar users
            course_scores = {}
            
            for similar_user_id, similarity in similar_users:
                if similar_user_id not in user_item_matrix:
                    continue
                
                similar_user_items = user_item_matrix[similar_user_id]
                
                for course_id, score in similar_user_items.items():
                    if course_id not in user_course_ids:  # Not interacted by target user
                        if course_id not in course_scores:
                            course_scores[course_id] = 0.0
                        course_scores[course_id] += score * similarity
            
            # Sort courses by score
            sorted_courses = sorted(course_scores.items(), key=lambda x: x[1], reverse=True)
            
            # Get top recommendations
            recommendations = []
            for course_id, score in sorted_courses[:limit]:
                course = self.db.query(Course).filter(Course.id == course_id).first()
                if course and course.is_active:
                    # Normalize confidence score
                    confidence = min(0.9, max(0.6, score / 10.0))  # Normalize to 0.6-0.9 range
                    recommendations.append(self._create_recommendation_response(
                        course, confidence, "Recommended by users with similar learning patterns"
                    ))
            
            # Apply additional filters
            filtered_recommendations = self._apply_filters_to_recommendations(
                recommendations, difficulty_level, categories, max_duration_hours, content_type
            )
            
            return filtered_recommendations
            
        except Exception as e:
            logger.error(f"Error getting recommendations from similar users: {e}")
            return []
    
    def _traditional_collaborative_filtering(self, user_id: int, limit: int, user_profile: Dict, difficulty_level: Optional[str] = None, categories: Optional[List[str]] = None, max_duration_hours: Optional[int] = None, content_type: Optional[str] = None) -> List[RecommendationResponse]:
        """Traditional collaborative filtering as fallback."""
        try:
            # Rollback any failed transaction
            try:
                self.db.rollback()
            except:
                pass
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
                    AND u1.preferred_categories IS NOT NULL 
                    AND u2.preferred_categories IS NOT NULL
                    AND jsonb_array_length(u1.preferred_categories) > 0
                    AND jsonb_array_length(u2.preferred_categories) > 0
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
            
            # Apply additional filters
            filtered_recommendations = self._apply_filters_to_recommendations(
                recommendations, difficulty_level, categories, max_duration_hours, content_type
            )
            
            return filtered_recommendations
            
        except Exception as e:
            logger.error(f"Error in traditional collaborative filtering: {e}")
            return []
    
    def _content_based_filtering(self, user_id: int, limit: int, user_profile: Dict, difficulty_level: Optional[str] = None, categories: Optional[List[str]] = None, max_duration_hours: Optional[int] = None, content_type: Optional[str] = None) -> List[RecommendationResponse]:
        """
        Advanced content-based filtering using TF-IDF and semantic similarity.
        
        Args:
            user_id: User ID
            limit: Number of recommendations
            user_profile: User profile data
            
        Returns:
            List[RecommendationResponse]: Recommendations
        """
        try:
            # logger.info(f"Starting content-based filtering for user {user_id} with filters: difficulty_level={difficulty_level}, categories={categories}, max_duration_hours={max_duration_hours}, content_type={content_type}")
            # Rollback any failed transaction
            try:
                self.db.rollback()
            except:
                pass
            # Get user's interacted courses for similarity calculation
            user_interactions = self.db.query(UserInteraction).filter(
                UserInteraction.user_id == user_id,
                UserInteraction.interaction_type.in_(['like', 'enroll', 'complete', 'rate'])
            ).all()
            
            if not user_interactions or not self.course_tfidf_matrix is not None:
                # Fallback to traditional content-based filtering
                return self._traditional_content_based_filtering(user_id, limit, user_profile)
            
            # Calculate user preference vector from interacted courses
            user_preference_vector = self._calculate_user_preference_vector(user_interactions)
            
            if user_preference_vector is None:
                return self._traditional_content_based_filtering(user_id, limit, user_profile)
            
            # Calculate similarity scores for all courses
            similarity_scores = cosine_similarity(
                user_preference_vector.reshape(1, -1), 
                self.course_tfidf_matrix
            )[0]
            
            # Get course recommendations with similarity scores
            course_similarities = list(zip(self.course_ids, similarity_scores))
            
            # Filter out courses user has already interacted with
            interacted_course_ids = {interaction.course_id for interaction in user_interactions}
            course_similarities = [
                (course_id, score) for course_id, score in course_similarities 
                if course_id not in interacted_course_ids
            ]
            
            # Sort by similarity score
            course_similarities.sort(key=lambda x: x[1], reverse=True)
            
            # Get top recommendations
            recommendations = []
            for course_id, similarity_score in course_similarities[:limit * 2]:  # Get more for filtering
                course = self.db.query(Course).filter(Course.id == course_id).first()
                if course and course.is_active:
                    # Apply additional filters
                    if self._matches_user_preferences(course, user_profile):
                        # Calculate skill match score
                        skill_score = self._calculate_skill_match_score(course, user_profile)
                        
                        # Combine semantic similarity with skill matching
                        base_confidence = similarity_score * 1.2
                        skill_boost = skill_score * 0.3
                        confidence = min(0.95, max(0.6, base_confidence + skill_boost))
                        
                        # Update recommendation reason based on skill matching
                        reason = "Semantically similar to your interests"
                        if skill_score > 0.3:
                            reason = "Matches your learning goals and interests"
                        
                        recommendations.append(self._create_recommendation_response(
                            course, confidence, reason
                        ))
                        
                        if len(recommendations) >= limit:
                            break
            
            # If we don't have enough recommendations, fallback to traditional method
            if len(recommendations) < limit:
                fallback_recs = self._traditional_content_based_filtering(
                    user_id, limit - len(recommendations), user_profile
                )
                recommendations.extend(fallback_recs)
            
            # Apply additional filters
            filtered_recommendations = self._apply_filters_to_recommendations(
                recommendations[:limit], difficulty_level, categories, max_duration_hours, content_type
            )
            
            return filtered_recommendations
            
        except Exception as e:
            logger.error(f"Error in advanced content-based filtering: {e}")
            try:
                traditional_recs = self._traditional_content_based_filtering(user_id, limit, user_profile)
                filtered_recs = self._apply_filters_to_recommendations(
                    traditional_recs, difficulty_level, categories, max_duration_hours, content_type
                )
                return filtered_recs
            except Exception as e2:
                logger.error(f"Error in traditional content-based filtering: {e2}")
                return []
    
    def _calculate_user_preference_vector(self, user_interactions: List) -> Optional[np.ndarray]:
        """Calculate user preference vector from interactions."""
        try:
            if not user_interactions or not self.course_tfidf_matrix is not None:
                return None
            
            # Get course indices for user's interacted courses
            course_indices = []
            weights = []
            
            for interaction in user_interactions:
                if interaction.course_id in self.course_ids:
                    course_idx = self.course_ids.index(interaction.course_id)
                    course_indices.append(course_idx)
                    
                    # Weight interactions based on type and recency
                    weight = self._get_interaction_weight(interaction)
                    weights.append(weight)
            
            if not course_indices:
                return None
            
            # Calculate weighted average of course vectors
            weights = np.array(weights)
            weights = weights / weights.sum()  # Normalize weights
            
            user_vector = np.average(
                self.course_tfidf_matrix[course_indices], 
                axis=0, 
                weights=weights
            )
            
            return user_vector
            
        except Exception as e:
            logger.error(f"Error calculating user preference vector: {e}")
            return None
    
    def _get_interaction_weight(self, interaction) -> float:
        """Get weight for interaction based on type and recency."""
        # Base weights for different interaction types
        type_weights = {
            'view': 0.1,
            'like': 0.3,
            'enroll': 0.5,
            'complete': 1.0,
            'rate': 0.4
        }
        
        base_weight = type_weights.get(interaction.interaction_type, 0.1)
        
        # Apply temporal decay (recent interactions are more important)
        days_ago = (datetime.utcnow() - interaction.created_at).days
        temporal_decay = max(0.1, 1.0 - (days_ago / 365.0))  # Decay over a year
        
        return base_weight * temporal_decay
    
    def _matches_user_preferences(self, course: Course, user_profile: Dict) -> bool:
        """Check if course matches user preferences."""
        # Check category preference
        if user_profile.get('preferred_categories'):
            if not course.category or course.category.name not in user_profile['preferred_categories']:
                return False
        
        # Check difficulty preference
        if user_profile.get('preferred_difficulty_levels'):
            if not course.difficulty_level or course.difficulty_level not in user_profile['preferred_difficulty_levels']:
                return False
        
        # Check content type preference
        if user_profile.get('preferred_content_types'):
            if not course.content_type or course.content_type not in user_profile['preferred_content_types']:
                return False
        
        return True
    
    def _calculate_skill_match_score(self, course: Course, user_profile: Dict) -> float:
        """Calculate skill matching score between course and user's learning goals."""
        try:
            if not course.skills or not user_profile.get('skills_to_develop'):
                return 0.0
            
            course_skills = set(course.skills)
            user_skills_to_develop = set(user_profile['skills_to_develop'])
            
            if not course_skills or not user_skills_to_develop:
                return 0.0
            
            # Calculate Jaccard similarity for skills
            intersection = course_skills.intersection(user_skills_to_develop)
            union = course_skills.union(user_skills_to_develop)
            
            if not union:
                return 0.0
            
            jaccard_similarity = len(intersection) / len(union)
            
            # Boost score if course teaches skills user wants to develop
            skill_boost = len(intersection) / len(user_skills_to_develop)
            
            # Combine Jaccard similarity with skill boost
            final_score = (jaccard_similarity * 0.7) + (skill_boost * 0.3)
            
            return min(1.0, final_score)
            
        except Exception as e:
            logger.error(f"Error calculating skill match score: {e}")
            return 0.0
    
    def _apply_filters_to_recommendations(
        self, 
        recommendations: List[RecommendationResponse], 
        difficulty_level: Optional[str] = None,
        categories: Optional[List[str]] = None,
        max_duration_hours: Optional[int] = None,
        content_type: Optional[str] = None
    ) -> List[RecommendationResponse]:
        """Apply additional filters to recommendations."""
        try:
            if not recommendations:
                return []
            
            # logger.info(f"DEBUG: Applying filters: difficulty_level={difficulty_level}, categories={categories}, max_duration_hours={max_duration_hours}, content_type={content_type}")
            # logger.info(f"DEBUG: Original recommendations count: {len(recommendations)}")
            
            filtered_recommendations = []
            
            for rec in recommendations:
                # Get course details to check filters
                course = self.db.query(Course).filter(Course.id == rec.course_id).first()
                if not course:
                    continue
                
                # Apply difficulty level filter (case-insensitive)
                if difficulty_level and course.difficulty_level and course.difficulty_level.lower() != difficulty_level.lower():
                    # logger.info(f"DEBUG: Filtering out course {rec.course_id}: difficulty_level {course.difficulty_level} != {difficulty_level}")
                    continue
                
                # Apply category filter (case-insensitive)
                if categories and course.category and course.category.name.lower() not in [c.lower() for c in categories]:
                    continue
                
                # Apply duration filter
                if max_duration_hours and course.duration_hours and course.duration_hours > max_duration_hours:
                    continue
                
                # Apply content type filter (case-insensitive)
                if content_type and course.content_type and course.content_type.lower() != content_type.lower():
                    continue
                
                filtered_recommendations.append(rec)
            
            # logger.info(f"DEBUG: Filtered recommendations count: {len(filtered_recommendations)}")
            return filtered_recommendations
            
        except Exception as e:
            logger.error(f"Error applying filters to recommendations: {e}")
            return recommendations
    
    def _traditional_content_based_filtering(self, user_id: int, limit: int, user_profile: Dict) -> List[RecommendationResponse]:
        """Traditional content-based filtering as fallback."""
        try:
            # Build query based on user preferences
            query = self.db.query(Course).filter(Course.is_active == True)
            
            # Exclude courses user has already interacted with
            interacted_courses = self.db.query(UserInteraction.course_id).filter(
                UserInteraction.user_id == user_id
            ).subquery()
            query = query.filter(~Course.id.in_(self.db.query(interacted_courses.c.course_id)))
            
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
            logger.error(f"Error in traditional content-based filtering: {e}")
            return []
    
    def _hybrid_recommendations(self, user_id: int, limit: int, user_profile: Dict, difficulty_level: Optional[str] = None, categories: Optional[List[str]] = None, max_duration_hours: Optional[int] = None, content_type: Optional[str] = None) -> List[RecommendationResponse]:
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
            # logger.info(f"Starting hybrid recommendations for user {user_id} with filters: difficulty_level={difficulty_level}, categories={categories}, max_duration_hours={max_duration_hours}, content_type={content_type}")
            # Get recommendations from both approaches
            collaborative_recs = self._collaborative_filtering(user_id, limit // 2, user_profile, difficulty_level, categories, max_duration_hours, content_type)
            content_recs = self._content_based_filtering(user_id, limit // 2, user_profile, difficulty_level, categories, max_duration_hours, content_type)
            
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
            try:
                content_recs = self._content_based_filtering(user_id, limit, user_profile, difficulty_level, categories, max_duration_hours, content_type)
                return content_recs
            except Exception as e2:
                logger.error(f"Error in content-based fallback: {e2}")
                return []
    
    def _popularity_based_recommendations(self, user_id: int, limit: int, user_profile: Dict, difficulty_level: Optional[str] = None, categories: Optional[List[str]] = None, max_duration_hours: Optional[int] = None, content_type: Optional[str] = None) -> List[RecommendationResponse]:
        """
        Popularity-based recommendations with intelligent filtering.
        
        Args:
            user_id: User ID
            limit: Number of recommendations
            user_profile: User profile data
            
        Returns:
            List[RecommendationResponse]: Recommendations
        """
        try:
            # logger.info(f"Starting popularity-based recommendations for user {user_id} with filters: difficulty_level={difficulty_level}, categories={categories}, max_duration_hours={max_duration_hours}, content_type={content_type}")
            # Rollback any failed transaction
            try:
                self.db.rollback()
            except:
                pass
            # Get popular courses that user hasn't interacted with
            interacted_courses = self.db.query(UserInteraction.course_id).filter(
                UserInteraction.user_id == user_id
            ).subquery()
            
            # Build query for popular courses
            query = self.db.query(Course).filter(
                Course.is_active == True,
                ~Course.id.in_(self.db.query(interacted_courses.c.course_id))
            )
            
            # Apply user preference filters if available
            category_joined = False
            if user_profile.get('preferred_categories'):
                from app.models.course import Category
                # Case-insensitive filtering for user preferences
                query = query.join(Category).filter(
                    func.lower(Category.name).in_([c.lower() for c in user_profile['preferred_categories']])
                )
                category_joined = True
            
            if user_profile.get('preferred_difficulty_levels'):
                preferred_difficulties = list(user_profile['preferred_difficulty_levels'].keys())
                # Case-insensitive filtering for user preferences
                query = query.filter(
                    func.lower(Course.difficulty_level).in_([d.lower() for d in preferred_difficulties])
                )
            
            if user_profile.get('preferred_content_types'):
                preferred_content_types = list(user_profile['preferred_content_types'].keys())
                # Case-insensitive filtering for user preferences
                query = query.filter(
                    func.lower(Course.content_type).in_([c.lower() for c in preferred_content_types])
                )
            
            # Apply additional filters from request
            if difficulty_level:
                query = query.filter(func.lower(Course.difficulty_level) == func.lower(difficulty_level))
            
            if categories:
                from app.models.course import Category
                # Case-insensitive filtering for categories
                if not category_joined:
                    # Only join if not already joined
                    query = query.join(Category).filter(
                        func.lower(Category.name).in_([c.lower() for c in categories])
                    )
                else:
                    # Already joined, just add filter
                    query = query.filter(
                        func.lower(Category.name).in_([c.lower() for c in categories])
                    )
            
            if max_duration_hours:
                query = query.filter(Course.duration_hours <= max_duration_hours)
            
            if content_type:
                query = query.filter(func.lower(Course.content_type) == func.lower(content_type))
            
            # Order by popularity metrics (rating, enrollment count, recency)
            courses = query.order_by(
                Course.rating.desc(),
                Course.enrollment_count.desc(),
                Course.created_at.desc()
            ).limit(limit * 2).all()  # Get more for skill matching
            
            recommendations = []
            for i, course in enumerate(courses):
                # Calculate confidence based on popularity and user preferences
                base_confidence = max(0.5, 0.8 - (i * 0.02))  # Decreasing confidence
                
                # Boost confidence if course matches user's skill goals
                skill_boost = 0.0
                if user_profile.get('skills_to_develop') and course.skills:
                    skill_score = self._calculate_skill_match_score(course, user_profile)
                    skill_boost = skill_score * 0.2
                
                # Boost confidence if course matches user's preferred duration
                duration_boost = 0.0
                if user_profile.get('preferred_durations') and course.duration_hours:
                    duration_category = self._categorize_duration(course.duration_hours)
                    if duration_category in user_profile['preferred_durations']:
                        duration_boost = 0.1
                
                final_confidence = min(0.9, base_confidence + skill_boost + duration_boost)
                
                # Generate recommendation reason
                reason_parts = ["Popular course with high ratings"]
                if skill_boost > 0.1:
                    reason_parts.append("matches your learning goals")
                if duration_boost > 0:
                    reason_parts.append("fits your preferred duration")
                
                reason = " and ".join(reason_parts)
                
                recommendations.append(self._create_recommendation_response(
                    course, final_confidence, reason
                ))
                
                if len(recommendations) >= limit:
                    break
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Error in popularity-based recommendations: {e}")
            return self._get_fallback_recommendations(user_id, limit)
    
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
            # Rollback any failed transaction
            try:
                self.db.rollback()
            except:
                pass
            # Get popular courses that user hasn't interacted with
            interacted_courses = self.db.query(UserInteraction.course_id).filter(
                UserInteraction.user_id == user_id
            ).subquery()
            
            courses = self.db.query(Course).filter(
                Course.is_active == True,
                ~Course.id.in_(self.db.query(interacted_courses.c.course_id))
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
