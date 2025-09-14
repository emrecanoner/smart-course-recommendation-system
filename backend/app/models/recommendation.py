"""
Recommendation models for storing and managing course recommendations.
"""

from datetime import datetime
from typing import Optional

from sqlalchemy import Column, DateTime, Float, Integer, String, Text, ForeignKey, Index, Boolean
from sqlalchemy.orm import relationship

from app.core.database import Base


class Recommendation(Base):
    """Model for storing generated course recommendations."""
    
    __tablename__ = "recommendations"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign keys
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    
    # Recommendation details
    algorithm_used = Column(String(100), nullable=False)  # collaborative, content-based, hybrid
    confidence_score = Column(Float, nullable=False)  # 0.0 to 1.0
    recommendation_reason = Column(Text, nullable=True)  # Explanation for the recommendation
    
    # Recommendation metadata
    batch_id = Column(String(255), nullable=True)  # For batch recommendations
    position = Column(Integer, nullable=True)  # Position in recommendation list
    is_active = Column(Boolean, default=True, nullable=False)
    
    # User feedback on recommendation
    user_feedback = Column(String(50), nullable=True)  # like, dislike, view, enroll, ignore
    feedback_timestamp = Column(DateTime, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    expires_at = Column(DateTime, nullable=True)  # When recommendation expires
    
    # Relationships
    user = relationship("User", back_populates="recommendations")
    course = relationship("Course", back_populates="recommendations")
    
    # Indexes for performance
    __table_args__ = (
        Index('ix_recommendations_user_created', 'user_id', 'created_at'),
        Index('ix_recommendations_algorithm_score', 'algorithm_used', 'confidence_score'),
        Index('ix_recommendations_batch', 'batch_id'),
    )
    
    def __repr__(self) -> str:
        return f"<Recommendation(id={self.id}, user_id={self.user_id}, course_id={self.course_id}, algorithm='{self.algorithm_used}')>"


class RecommendationModel(Base):
    """Model for storing trained recommendation models and their metadata."""
    
    __tablename__ = "recommendation_models"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Model identification
    model_name = Column(String(100), nullable=False, unique=True)
    model_type = Column(String(50), nullable=False)  # collaborative, content-based, hybrid
    version = Column(String(20), nullable=False)
    
    # Model metadata
    description = Column(Text, nullable=True)
    parameters = Column(Text, nullable=True)  # JSON string of model parameters
    training_data_size = Column(Integer, nullable=True)
    training_accuracy = Column(Float, nullable=True)
    validation_accuracy = Column(Float, nullable=True)
    
    # Model status
    is_active = Column(Boolean, default=False, nullable=False)
    is_training = Column(Boolean, default=False, nullable=False)
    
    # File paths and storage
    model_file_path = Column(String(500), nullable=True)
    feature_file_path = Column(String(500), nullable=True)
    metadata_file_path = Column(String(500), nullable=True)
    
    # Training information
    training_started_at = Column(DateTime, nullable=True)
    training_completed_at = Column(DateTime, nullable=True)
    last_retrained_at = Column(DateTime, nullable=True)
    
    # Performance metrics
    average_confidence = Column(Float, nullable=True)
    click_through_rate = Column(Float, nullable=True)
    conversion_rate = Column(Float, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def __repr__(self) -> str:
        return f"<RecommendationModel(id={self.id}, name='{self.model_name}', type='{self.model_type}', version='{self.version}')>"


class RecommendationLog(Base):
    """Model for logging recommendation generation and performance."""
    
    __tablename__ = "recommendation_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Request information
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # Nullable for anonymous users
    session_id = Column(String(255), nullable=True)
    request_id = Column(String(255), nullable=True, unique=True)
    
    # Recommendation details
    algorithm_used = Column(String(100), nullable=False)
    model_version = Column(String(20), nullable=True)
    number_of_recommendations = Column(Integer, nullable=False)
    processing_time_ms = Column(Integer, nullable=True)
    
    # Request context
    user_context = Column(Text, nullable=True)  # JSON string of user context
    request_parameters = Column(Text, nullable=True)  # JSON string of request parameters
    
    # Response information
    recommendations_generated = Column(Integer, nullable=False)
    average_confidence = Column(Float, nullable=True)
    
    # Performance metrics
    cache_hit = Column(Boolean, default=False, nullable=False)
    error_occurred = Column(Boolean, default=False, nullable=False)
    error_message = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    user = relationship("User")
    
    # Indexes for performance
    __table_args__ = (
        Index('ix_recommendation_logs_user_created', 'user_id', 'created_at'),
        Index('ix_recommendation_logs_algorithm_created', 'algorithm_used', 'created_at'),
        Index('ix_recommendation_logs_request_id', 'request_id'),
    )
    
    def __repr__(self) -> str:
        return f"<RecommendationLog(id={self.id}, user_id={self.user_id}, algorithm='{self.algorithm_used}')>"
