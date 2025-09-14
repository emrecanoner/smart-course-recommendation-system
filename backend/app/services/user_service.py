"""
User service for user management operations.
"""

from typing import Any, Dict, Optional, Union
from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


class UserService:
    """Service class for user operations."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get(self, id: Any) -> Optional[User]:
        """
        Get user by ID.
        
        Args:
            id: User ID
            
        Returns:
            Optional[User]: User if found, None otherwise
        """
        return self.db.query(User).filter(User.id == id).first()
    
    def get_by_email(self, *, email: str) -> Optional[User]:
        """
        Get user by email.
        
        Args:
            email: User email
            
        Returns:
            Optional[User]: User if found, None otherwise
        """
        return self.db.query(User).filter(User.email == email).first()
    
    def get_by_username(self, *, username: str) -> Optional[User]:
        """
        Get user by username.
        
        Args:
            username: Username
            
        Returns:
            Optional[User]: User if found, None otherwise
        """
        return self.db.query(User).filter(User.username == username).first()
    
    def create(self, *, obj_in: UserCreate) -> User:
        """
        Create new user.
        
        Args:
            obj_in: User creation data
            
        Returns:
            User: Created user
        """
        db_obj = User(
            email=obj_in.email,
            username=obj_in.username,
            full_name=obj_in.full_name,
            hashed_password=get_password_hash(obj_in.password),
            is_active=obj_in.is_active,
        )
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj
    
    def update(
        self, *, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> User:
        """
        Update user.
        
        Args:
            db_obj: User to update
            obj_in: Update data
            
        Returns:
            User: Updated user
        """
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        
        # Hash password if provided
        if "password" in update_data:
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj
    
    def authenticate(self, *, email: str, password: str) -> Optional[User]:
        """
        Authenticate user with email and password.
        
        Args:
            email: User email
            password: User password
            
        Returns:
            Optional[User]: User if authentication successful, None otherwise
        """
        user = self.get_by_email(email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user
    
    def is_active(self, user: User) -> bool:
        """
        Check if user is active.
        
        Args:
            user: User to check
            
        Returns:
            bool: True if user is active, False otherwise
        """
        return user.is_active
    
    def is_superuser(self, user: User) -> bool:
        """
        Check if user is superuser.
        
        Args:
            user: User to check
            
        Returns:
            bool: True if user is superuser, False otherwise
        """
        return user.is_superuser
