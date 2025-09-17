"""
Course model for the course recommendation system.
"""

from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, Column, DateTime, Float, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base


class Category(Base):
    """Category model for course categorization."""
    
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)
    parent_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    courses = relationship("Course", back_populates="category")
    parent = relationship("Category", remote_side=[id], back_populates="children")
    children = relationship("Category", back_populates="parent")
    
    def __repr__(self) -> str:
        return f"<Category(id={self.id}, name='{self.name}')>"


class Course(Base):
    """Course model for storing course information."""
    
    __tablename__ = "courses"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    short_description = Column(String(500), nullable=True)
    skills = Column(String(500), nullable=True)  # Comma-separated skills
    
    # Course metadata
    instructor = Column(String(255), nullable=True)
    organization = Column(String(255), nullable=True)  # University/Organization
    duration_hours = Column(Integer, nullable=True)
    difficulty_level = Column(String(50), nullable=True)  # beginner, intermediate, advanced
    language = Column(String(10), default="en", nullable=False)
    course_url = Column(String(500), nullable=True)  # Course URL
    modules_count = Column(String(100), nullable=True)  # Modules/Courses info
    
    # Course content and features
    content_type = Column(String(50), nullable=True)  # video, text, interactive, mixed
    has_certificate = Column(Boolean, default=False, nullable=False)
    is_free = Column(Boolean, default=True, nullable=False)
    price = Column(Float, nullable=True)
    
    # Course statistics
    rating = Column(Float, default=0.0, nullable=False)
    rating_count = Column(Integer, default=0, nullable=False)
    enrollment_count = Column(Integer, default=0, nullable=False)
    completion_rate = Column(Float, default=0.0, nullable=False)
    
    # Course status
    is_active = Column(Boolean, default=True, nullable=False)
    is_featured = Column(Boolean, default=False, nullable=False)
    
    # Foreign keys
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    published_at = Column(DateTime, nullable=True)
    
    # Relationships
    category = relationship("Category", back_populates="courses")
    recommendations = relationship("Recommendation", back_populates="course")
    interactions = relationship("UserInteraction", back_populates="course")
    
    def __repr__(self) -> str:
        return f"<Course(id={self.id}, title='{self.title}')>"
