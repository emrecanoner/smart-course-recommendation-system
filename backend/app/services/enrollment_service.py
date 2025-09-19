"""
Enrollment service for enrollment management operations.
"""

from typing import Any, List, Optional
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, func

from app.models.enrollment import Enrollment
from app.schemas.enrollment import EnrollmentCreate, EnrollmentUpdate


class EnrollmentService:
    """Service class for enrollment operations."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get(self, id: Any) -> Optional[Enrollment]:
        """
        Get enrollment by ID.
        
        Args:
            id: Enrollment ID
            
        Returns:
            Optional[Enrollment]: Enrollment if found, None otherwise
        """
        return self.db.query(Enrollment).filter(Enrollment.id == id).first()
    
    def get_user_enrollments(self, user_id: int) -> List[Enrollment]:
        """
        Get all enrollments for a user.
        
        Args:
            user_id: User ID
            
        Returns:
            List[Enrollment]: List of user's enrollments
        """
        return self.db.query(Enrollment).options(
            joinedload(Enrollment.course)
        ).filter(
            and_(
                Enrollment.user_id == user_id, 
                Enrollment.is_active == True,
                Enrollment.deleted_date.is_(None)
            )
        ).order_by(Enrollment.enrollment_date.desc()).all()
    
    def get_course_enrollments(self, course_id: int) -> List[Enrollment]:
        """
        Get all enrollments for a course.
        
        Args:
            course_id: Course ID
            
        Returns:
            List[Enrollment]: List of course enrollments
        """
        return self.db.query(Enrollment).options(
            joinedload(Enrollment.course)
        ).filter(
            and_(
                Enrollment.course_id == course_id, 
                Enrollment.is_active == True,
                Enrollment.deleted_date.is_(None)
            )
        ).order_by(Enrollment.enrollment_date.desc()).all()
    
    def is_enrolled(self, user_id: int, course_id: int) -> bool:
        """
        Check if a user is enrolled in a course.
        
        Args:
            user_id: User ID
            course_id: Course ID
            
        Returns:
            bool: True if enrolled, False otherwise
        """
        enrollment = self.db.query(Enrollment).filter(
            and_(
                Enrollment.user_id == user_id,
                Enrollment.course_id == course_id,
                Enrollment.is_active == True,
                Enrollment.deleted_date.is_(None)
            )
        ).first()
        return enrollment is not None
    
    def get_enrollment(self, user_id: int, course_id: int) -> Optional[Enrollment]:
        """
        Get specific enrollment for user and course.
        
        Args:
            user_id: User ID
            course_id: Course ID
            
        Returns:
            Optional[Enrollment]: Enrollment if found, None otherwise
        """
        return self.db.query(Enrollment).filter(
            and_(
                Enrollment.user_id == user_id,
                Enrollment.course_id == course_id,
                Enrollment.is_active == True,
                Enrollment.deleted_date.is_(None)
            )
        ).first()
    
    def create(self, *, obj_in: EnrollmentCreate, user_id: int) -> Enrollment:
        """
        Create new enrollment.
        
        Args:
            obj_in: Enrollment creation data
            user_id: User ID
            
        Returns:
            Enrollment: Created enrollment
        """
        # Check if already enrolled
        existing = self.db.query(Enrollment).filter(
            and_(
                Enrollment.user_id == user_id,
                Enrollment.course_id == obj_in.course_id
            )
        ).first()
        
        if existing:
            # If exists but inactive, reactivate it
            if not existing.is_active:
                existing.is_active = True
                existing.deleted_date = None  # Clear deleted date
                existing.enrollment_date = func.now()
                existing.completion_percentage = 0.0
                existing.is_completed = False
                existing.completion_date = None
                existing.updated_at = func.now()
                self.db.commit()
                self.db.refresh(existing)
                return existing
            else:
                # Already enrolled, return existing
                return existing
        
        # Create new enrollment
        db_obj = Enrollment(
            user_id=user_id,
            course_id=obj_in.course_id,
            is_active=True,
            completion_percentage=0.0,
            is_completed=False
        )
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj
    
    def update(self, *, db_obj: Enrollment, obj_in: EnrollmentUpdate) -> Enrollment:
        """
        Update enrollment.
        
        Args:
            db_obj: Enrollment to update
            obj_in: Update data
            
        Returns:
            Enrollment: Updated enrollment
        """
        update_data = obj_in.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        
        # If completion percentage is 100%, mark as completed
        if hasattr(obj_in, 'completion_percentage') and obj_in.completion_percentage is not None:
            if obj_in.completion_percentage >= 100.0:
                db_obj.is_completed = True
                db_obj.completion_date = func.now()
        
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj
    
    def update_progress(self, user_id: int, course_id: int, completion_percentage: float) -> Optional[Enrollment]:
        """
        Update course progress for a user.
        
        Args:
            user_id: User ID
            course_id: Course ID
            completion_percentage: Completion percentage (0.0 to 100.0)
            
        Returns:
            Optional[Enrollment]: Updated enrollment if found, None otherwise
        """
        enrollment = self.get_enrollment(user_id, course_id)
        if not enrollment:
            return None
        
        enrollment.completion_percentage = min(100.0, max(0.0, completion_percentage))
        enrollment.last_accessed = func.now()
        
        # Mark as completed if 100%
        if enrollment.completion_percentage >= 100.0:
            enrollment.is_completed = True
            enrollment.completion_date = func.now()
        
        self.db.commit()
        self.db.refresh(enrollment)
        return enrollment
    
    def get_user_stats(self, user_id: int) -> dict:
        """
        Get enrollment statistics for a user.
        
        Args:
            user_id: User ID
            
        Returns:
            dict: User enrollment statistics
        """
        enrollments = self.get_user_enrollments(user_id)
        
        total_enrollments = len(enrollments)
        completed_courses = len([e for e in enrollments if e.is_completed])
        in_progress_courses = total_enrollments - completed_courses
        
        completion_rate = (completed_courses / total_enrollments * 100) if total_enrollments > 0 else 0.0
        
        return {
            "total_enrollments": total_enrollments,
            "completed_courses": completed_courses,
            "in_progress_courses": in_progress_courses,
            "completion_rate": completion_rate
        }
    
    def unenroll(self, user_id: int, course_id: int) -> Optional[Enrollment]:
        """
        Unenroll user from a course by setting is_active=False and deleted_date=now.
        
        Args:
            user_id: User ID
            course_id: Course ID
            
        Returns:
            Optional[Enrollment]: Updated enrollment if found, None otherwise
        """
        enrollment = self.db.query(Enrollment).filter(
            and_(
                Enrollment.user_id == user_id,
                Enrollment.course_id == course_id,
                Enrollment.is_active == True,
                Enrollment.deleted_date.is_(None)
            )
        ).first()
        
        if not enrollment:
            return None
        
        enrollment.is_active = False
        enrollment.deleted_date = func.now()
        enrollment.updated_at = func.now()
        
        self.db.commit()
        self.db.refresh(enrollment)
        return enrollment
