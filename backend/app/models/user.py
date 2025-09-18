"""
User model for the course recommendation system.
"""

from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text
from sqlalchemy.orm import relationship

from app.core.database import Base


class User(Base):
    """User model for storing user information and preferences."""
    
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    full_name = Column(String(255), nullable=True)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    
    # User preferences and profile information
    bio = Column(Text, nullable=True)
    learning_goals = Column(Text, nullable=True)  # JSON string of learning goals
    preferred_categories = Column(Text, nullable=True)  # JSON string of preferred categories
    skill_level = Column(String(50), nullable=True)  # beginner, intermediate, advanced
    time_commitment = Column(String(50), nullable=True)  # low, medium, high
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    last_login = Column(DateTime, nullable=True)
    
    # Relationships
    interactions = relationship("UserInteraction", back_populates="user")
    recommendations = relationship("Recommendation", back_populates="user")
    enrollments = relationship("Enrollment", back_populates="user")
    
    def __repr__(self) -> str:
        return f"<User(id={self.id}, email='{self.email}', username='{self.username}')>"
