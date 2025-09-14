"""
Course service for course management operations.
"""

from typing import Any, Dict, List, Optional, Union
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

from app.models.course import Course, Category
from app.schemas.course import CourseCreate, CourseUpdate, CategoryCreate, CategoryUpdate


class CourseService:
    """Service class for course operations."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get(self, id: Any) -> Optional[Course]:
        """
        Get course by ID.
        
        Args:
            id: Course ID
            
        Returns:
            Optional[Course]: Course if found, None otherwise
        """
        return self.db.query(Course).filter(Course.id == id).first()
    
    def get_multi(
        self, 
        *, 
        skip: int = 0, 
        limit: int = 100,
        category: Optional[str] = None,
        search: Optional[str] = None
    ) -> List[Course]:
        """
        Get multiple courses with optional filtering.
        
        Args:
            skip: Number of records to skip
            limit: Number of records to return
            category: Filter by category name
            search: Search in title and description
            
        Returns:
            List[Course]: List of courses
        """
        query = self.db.query(Course).filter(Course.is_active == True)
        
        if category:
            query = query.join(Category).filter(Category.name == category)
        
        if search:
            search_filter = or_(
                Course.title.ilike(f"%{search}%"),
                Course.description.ilike(f"%{search}%")
            )
            query = query.filter(search_filter)
        
        return query.offset(skip).limit(limit).all()
    
    def create(self, *, obj_in: CourseCreate) -> Course:
        """
        Create new course.
        
        Args:
            obj_in: Course creation data
            
        Returns:
            Course: Created course
        """
        db_obj = Course(**obj_in.dict())
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj
    
    def update(
        self, *, db_obj: Course, obj_in: Union[CourseUpdate, Dict[str, Any]]
    ) -> Course:
        """
        Update course.
        
        Args:
            db_obj: Course to update
            obj_in: Update data
            
        Returns:
            Course: Updated course
        """
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj
    
    def delete(self, *, id: int) -> Course:
        """
        Delete course (soft delete by setting is_active to False).
        
        Args:
            id: Course ID
            
        Returns:
            Course: Deleted course
        """
        obj = self.db.query(Course).get(id)
        obj.is_active = False
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj


class CategoryService:
    """Service class for category operations."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get(self, id: Any) -> Optional[Category]:
        """
        Get category by ID.
        
        Args:
            id: Category ID
            
        Returns:
            Optional[Category]: Category if found, None otherwise
        """
        return self.db.query(Category).filter(Category.id == id).first()
    
    def get_by_name(self, *, name: str) -> Optional[Category]:
        """
        Get category by name.
        
        Args:
            name: Category name
            
        Returns:
            Optional[Category]: Category if found, None otherwise
        """
        return self.db.query(Category).filter(Category.name == name).first()
    
    def get_multi(self, *, skip: int = 0, limit: int = 100) -> List[Category]:
        """
        Get multiple categories.
        
        Args:
            skip: Number of records to skip
            limit: Number of records to return
            
        Returns:
            List[Category]: List of categories
        """
        return (
            self.db.query(Category)
            .filter(Category.is_active == True)
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def create(self, *, obj_in: CategoryCreate) -> Category:
        """
        Create new category.
        
        Args:
            obj_in: Category creation data
            
        Returns:
            Category: Created category
        """
        db_obj = Category(**obj_in.dict())
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj
    
    def update(
        self, *, db_obj: Category, obj_in: Union[CategoryUpdate, Dict[str, Any]]
    ) -> Category:
        """
        Update category.
        
        Args:
            db_obj: Category to update
            obj_in: Update data
            
        Returns:
            Category: Updated category
        """
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj
