"""
User interaction models for tracking user behavior and preferences.
"""

from datetime import datetime
from typing import Optional

from sqlalchemy import Column, DateTime, Float, Integer, String, Text, ForeignKey, Index
from sqlalchemy.orm import relationship

from app.core.database import Base


class UserInteraction(Base):
    """Model for tracking user interactions with courses."""
    
    __tablename__ = "user_interactions"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign keys
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    
    # Interaction details
    interaction_type = Column(String(50), nullable=False)  # view, like, dislike, enroll, complete, rate
    rating = Column(Float, nullable=True)  # 1.0 to 5.0 scale
    time_spent_minutes = Column(Integer, nullable=True)
    progress_percentage = Column(Float, nullable=True)  # 0.0 to 100.0
    
    # Additional metadata
    session_id = Column(String(255), nullable=True)
    device_type = Column(String(50), nullable=True)  # mobile, desktop, tablet
    referrer = Column(String(255), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="interactions")
    course = relationship("Course", back_populates="interactions")
    
    # Indexes for performance
    __table_args__ = (
        Index('ix_user_interactions_user_course', 'user_id', 'course_id'),
        Index('ix_user_interactions_type_created', 'interaction_type', 'created_at'),
    )
    
    def __repr__(self) -> str:
        return f"<UserInteraction(id={self.id}, user_id={self.user_id}, course_id={self.course_id}, type='{self.interaction_type}')>"


class UserPreference(Base):
    """Model for storing user learning preferences and settings."""
    
    __tablename__ = "user_preferences"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    
    # Learning preferences
    preferred_difficulty = Column(String(50), nullable=True)  # beginner, intermediate, advanced
    preferred_duration = Column(String(50), nullable=True)  # short, medium, long
    preferred_content_type = Column(String(50), nullable=True)  # video, text, interactive
    preferred_language = Column(String(10), default="en", nullable=False)
    
    # Notification preferences
    email_notifications = Column(String(50), default="weekly", nullable=False)  # daily, weekly, monthly, never
    push_notifications = Column(String(50), default="enabled", nullable=False)  # enabled, disabled
    
    # Privacy settings
    profile_visibility = Column(String(50), default="private", nullable=False)  # public, private, friends
    data_sharing = Column(String(50), default="limited", nullable=False)  # full, limited, none
    
    # Learning goals and interests (JSON strings)
    learning_goals = Column(Text, nullable=True)
    interests = Column(Text, nullable=True)
    skills_to_develop = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    user = relationship("User")
    
    def __repr__(self) -> str:
        return f"<UserPreference(id={self.id}, user_id={self.user_id})>"
