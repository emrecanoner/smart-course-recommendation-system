"""
Main API router that includes all endpoint routers.
"""

from fastapi import APIRouter

from app.api.api_v1.endpoints import auth, users, courses, recommendations

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(courses.router, prefix="/courses", tags=["courses"])
api_router.include_router(
    recommendations.router, 
    prefix="/recommendations", 
    tags=["recommendations"]
)
