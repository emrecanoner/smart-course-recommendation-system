"""
Authentication schemas for user registration and login.
"""

from typing import Optional
from pydantic import BaseModel
from pydantic import EmailStr


class UserBase(BaseModel):
    """Base user schema with common fields."""
    email: EmailStr
    username: str
    full_name: Optional[str] = None
    is_active: bool = True


class UserCreate(UserBase):
    """Schema for user creation."""
    password: str


class UserUpdate(BaseModel):
    """Schema for user updates."""
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    full_name: Optional[str] = None
    bio: Optional[str] = None
    learning_goals: Optional[str] = None
    preferred_categories: Optional[str] = None
    skill_level: Optional[str] = None
    time_commitment: Optional[str] = None


class UserResponse(UserBase):
    """Schema for user response."""
    id: int
    bio: Optional[str] = None
    learning_goals: Optional[str] = None
    preferred_categories: Optional[str] = None
    skill_level: Optional[str] = None
    time_commitment: Optional[str] = None
    created_at: str
    updated_at: str
    last_login: Optional[str] = None

    class Config:
        from_attributes = True


class Token(BaseModel):
    """Schema for authentication token."""
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    """Schema for token payload."""
    sub: Optional[int] = None
