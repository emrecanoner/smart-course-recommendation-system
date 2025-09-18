"""
Enrollment models for storing user course enrollments.
"""

from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, ForeignKey, Index, Boolean, Float
from sqlalchemy.orm import relationship

from app.core.database import Base


class Enrollment(Base):
    """Model for storing user course enrollments."""
    
    __tablename__ = "enrollments"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign keys
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    
    # Enrollment metadata
    is_active = Column(Boolean, default=True, nullable=False)
    deleted_date = Column(DateTime, nullable=True)
    enrollment_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    completion_percentage = Column(Float, default=0.0, nullable=False)  # 0.0 to 100.0
    last_accessed = Column(DateTime, nullable=True)
    is_completed = Column(Boolean, default=False, nullable=False)
    completion_date = Column(DateTime, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")
    
    # Indexes for performance
    __table_args__ = (
        Index('ix_enrollments_user_course', 'user_id', 'course_id', unique=True),
        Index('ix_enrollments_user_enrollment_date', 'user_id', 'enrollment_date'),
        Index('ix_enrollments_course_enrollment_date', 'course_id', 'enrollment_date'),
        Index('ix_enrollments_completion', 'is_completed', 'completion_date'),
    )
    
    def __repr__(self) -> str:
        return f"<Enrollment(id={self.id}, user_id={self.user_id}, course_id={self.course_id}, completion={self.completion_percentage}%)>"
