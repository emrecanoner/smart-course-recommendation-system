#!/usr/bin/env python3
"""
Analytics Schema Update Script

This script updates all analytics tables with current data from the main tables.
It can be run as a scheduled job to keep analytics data up to date.

Usage:
    python scripts/update_analytics.py
    uv run python scripts/update_analytics.py
"""

import sys
import os
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import get_db
from app.core.constants import (
    ENGAGEMENT_WEIGHTS, POSITIVE_ACTIONS, NEGATIVE_ACTIONS, 
    ENGAGEMENT_RATIO_BONUS_MULTIPLIER, MIN_ENGAGEMENT_SCORE,
    calculate_engagement_score, calculate_learning_velocity
)
from app.models.user import User
from app.models.course import Course, Category
from app.models.enrollment import Enrollment
from app.models.interaction import UserInteraction, UserPreference
from app.models.recommendation import Recommendation, RecommendationLog
from sqlalchemy import text, func, and_
from sqlalchemy.orm import Session

def update_user_learning_profiles(db: Session) -> int:
    """
    Update user learning profiles in analytics schema.
    
    Returns:
        int: Number of profiles updated
    """
    print("🔄 Updating user learning profiles...")
    
    # Get all users
    users = db.query(User).all()
    updated_count = 0
    
    for user in users:
        try:
            # Get user interactions
            interactions = db.query(UserInteraction).filter(
                UserInteraction.user_id == user.id
            ).all()
            
            # Get user enrollments
            enrollments = db.query(Enrollment).filter(
                and_(
                    Enrollment.user_id == user.id,
                    Enrollment.is_active == True,
                    Enrollment.deleted_at.is_(None)
                )
            ).all()
            
            # Calculate metrics
            total_courses_viewed = len([i for i in interactions if i.interaction_type == 'view'])
            total_courses_enrolled = len([i for i in interactions if i.interaction_type == 'enroll'])
            total_courses_completed = len([i for i in interactions if i.interaction_type == 'complete'])
            total_courses_rated = len([i for i in interactions if i.interaction_type == 'rate'])
            total_courses_liked = len([i for i in interactions if i.interaction_type == 'like'])
            total_courses_unliked = len([i for i in interactions if i.interaction_type == 'unlike'])
            total_courses_unenrolled = len([i for i in interactions if i.interaction_type == 'unenroll'])
            total_interactions = len(interactions)
            
            # Calculate average completion rate
            completed_enrollments = [e for e in enrollments if e.is_completed]
            avg_completion_rate = (sum(e.completion_percentage for e in completed_enrollments) / len(completed_enrollments)) if completed_enrollments else 0.0
            
            # Calculate average rating given
            ratings = [i.rating for i in interactions if i.rating is not None]
            avg_rating_given = sum(ratings) / len(ratings) if ratings else 0.0
            
            # Get preferred categories from interactions
            course_ids = [i.course_id for i in interactions if i.interaction_type in ['like', 'enroll', 'complete']]
            if course_ids:
                courses = db.query(Course).filter(Course.id.in_(course_ids)).all()
                categories = {}
                for course in courses:
                    if course.category_id:
                        cat_name = course.category.name if course.category else 'Unknown'
                        categories[cat_name] = categories.get(cat_name, 0) + 1
                preferred_categories = list(categories.keys())[:5]  # Top 5
            else:
                preferred_categories = []
            
            # Calculate engagement score using optimized function
            engagement_score = calculate_engagement_score(
                interactions, 
                total_courses_liked, 
                total_courses_unliked,
                total_courses_enrolled, 
                total_courses_unenrolled,
                total_courses_completed, 
                total_courses_rated
            )
            
            # Calculate enrollment and completion dates from interactions
            enrollment_dates = []
            completion_dates = []
            
            # Get enrollment dates from interactions
            for interaction in interactions:
                if interaction.interaction_type == 'enroll':
                    enrollment_dates.append(interaction.created_at)
                elif interaction.interaction_type == 'complete':
                    completion_dates.append(interaction.created_at)
            
            # Calculate first and last dates
            first_enrollment_date = min(enrollment_dates) if enrollment_dates else None
            last_enrollment_date = max(enrollment_dates) if enrollment_dates else None
            first_completion_date = min(completion_dates) if completion_dates else None
            last_completion_date = max(completion_dates) if completion_dates else None
            
            # Calculate behavioral patterns
            hour_counts = {}
            day_counts = {}
            device_counts = {}
            
            for interaction in interactions:
                # Time of day analysis
                hour = interaction.created_at.hour
                hour_counts[hour] = hour_counts.get(hour, 0) + 1
                
                # Day of week analysis
                day = interaction.created_at.strftime('%A')
                day_counts[day] = day_counts.get(day, 0) + 1
                
                # Device analysis
                if interaction.device_type:
                    device_counts[interaction.device_type] = device_counts.get(interaction.device_type, 0) + 1
            
            # Find most common patterns
            preferred_time_of_day = max(hour_counts.items(), key=lambda x: x[1])[0] if hour_counts else None
            preferred_day_of_week = max(day_counts.items(), key=lambda x: x[1])[0] if day_counts else None
            device_preference = max(device_counts.items(), key=lambda x: x[1])[0] if device_counts else None
            
            # Determine learning pattern
            if not interactions:
                learning_pattern = None
            else:
                dates = [interaction.created_at.date() for interaction in interactions]
                unique_dates = set(dates)
                
                if len(unique_dates) <= 1:
                    learning_pattern = 'sporadic'
                elif len(unique_dates) >= len(dates) * 0.8:
                    learning_pattern = 'consistent'
                else:
                    learning_pattern = 'intensive'
            
            # Calculate activity metrics
            last_activity_date = max(interaction.created_at for interaction in interactions) if interactions else None
            days_since_last_activity = (datetime.now() - last_activity_date).days if last_activity_date else 0
            
            # Calculate learning velocity using optimized function
            learning_velocity = calculate_learning_velocity(completed_enrollments)
            
            # Get user preferences
            user_pref = db.query(UserPreference).filter(UserPreference.user_id == user.id).first()
            learning_goals = []
            interests = []
            skills_developed = []
            if user_pref:
                if user_pref.learning_goals:
                    learning_goals = json.loads(user_pref.learning_goals)
                if user_pref.interests:
                    interests = json.loads(user_pref.interests)
                if user_pref.skills_to_develop:
                    skills_developed = json.loads(user_pref.skills_to_develop)
            
            # Insert or update user learning profile
            db.execute(text("""
                INSERT INTO analytics.user_learning_profile (
                    user_id, total_courses_viewed, total_courses_enrolled, 
                    total_courses_completed, total_courses_rated, 
                    total_courses_liked, total_courses_unliked, total_courses_unenrolled,
                    total_interactions,
                    avg_completion_rate, avg_rating_given, 
                    preferred_categories, engagement_score, learning_velocity,
                    learning_goals, skills_developed, 
                    first_enrollment_date, last_enrollment_date,
                    first_completion_date, last_completion_date,
                    preferred_time_of_day, preferred_day_of_week,
                    learning_pattern, device_preference,
                    last_activity_date, days_since_last_activity,
                    updated_at
                ) VALUES (
                    :user_id, :total_courses_viewed, :total_courses_enrolled,
                    :total_courses_completed, :total_courses_rated,
                    :total_courses_liked, :total_courses_unliked, :total_courses_unenrolled,
                    :total_interactions,
                    :avg_completion_rate, :avg_rating_given,
                    :preferred_categories, :engagement_score, :learning_velocity,
                    :learning_goals, :skills_developed,
                    :first_enrollment_date, :last_enrollment_date,
                    :first_completion_date, :last_completion_date,
                    :preferred_time_of_day, :preferred_day_of_week,
                    :learning_pattern, :device_preference,
                    :last_activity_date, :days_since_last_activity,
                    CURRENT_TIMESTAMP
                )
                ON CONFLICT (user_id) DO UPDATE SET
                    total_courses_viewed = EXCLUDED.total_courses_viewed,
                    total_courses_enrolled = EXCLUDED.total_courses_enrolled,
                    total_courses_completed = EXCLUDED.total_courses_completed,
                    total_courses_rated = EXCLUDED.total_courses_rated,
                    total_courses_liked = EXCLUDED.total_courses_liked,
                    total_courses_unliked = EXCLUDED.total_courses_unliked,
                    total_courses_unenrolled = EXCLUDED.total_courses_unenrolled,
                    total_interactions = EXCLUDED.total_interactions,
                    avg_completion_rate = EXCLUDED.avg_completion_rate,
                    avg_rating_given = EXCLUDED.avg_rating_given,
                    preferred_categories = EXCLUDED.preferred_categories,
                    engagement_score = EXCLUDED.engagement_score,
                    learning_velocity = EXCLUDED.learning_velocity,
                    learning_goals = EXCLUDED.learning_goals,
                    skills_developed = EXCLUDED.skills_developed,
                    first_enrollment_date = EXCLUDED.first_enrollment_date,
                    last_enrollment_date = EXCLUDED.last_enrollment_date,
                    first_completion_date = EXCLUDED.first_completion_date,
                    last_completion_date = EXCLUDED.last_completion_date,
                    preferred_time_of_day = EXCLUDED.preferred_time_of_day,
                    preferred_day_of_week = EXCLUDED.preferred_day_of_week,
                    learning_pattern = EXCLUDED.learning_pattern,
                    device_preference = EXCLUDED.device_preference,
                    last_activity_date = EXCLUDED.last_activity_date,
                    days_since_last_activity = EXCLUDED.days_since_last_activity,
                    updated_at = CURRENT_TIMESTAMP
            """), {
                'user_id': user.id,
                'total_courses_viewed': total_courses_viewed,
                'total_courses_enrolled': total_courses_enrolled,
                'total_courses_completed': total_courses_completed,
                'total_courses_rated': total_courses_rated,
                'total_courses_liked': total_courses_liked,
                'total_courses_unliked': total_courses_unliked,
                'total_courses_unenrolled': total_courses_unenrolled,
                'total_interactions': total_interactions,
                'avg_completion_rate': avg_completion_rate,
                'avg_rating_given': avg_rating_given,
                'preferred_categories': json.dumps(preferred_categories),
                'engagement_score': engagement_score,
                'learning_velocity': learning_velocity,
                'learning_goals': json.dumps(learning_goals),
                'skills_developed': json.dumps(skills_developed),
                'first_enrollment_date': first_enrollment_date,
                'last_enrollment_date': last_enrollment_date,
                'first_completion_date': first_completion_date,
                'last_completion_date': last_completion_date,
                'preferred_time_of_day': str(preferred_time_of_day) if preferred_time_of_day is not None else None,
                'preferred_day_of_week': preferred_day_of_week,
                'learning_pattern': learning_pattern,
                'device_preference': device_preference,
                'last_activity_date': last_activity_date,
                'days_since_last_activity': days_since_last_activity
            })
            
            updated_count += 1
            
        except Exception as e:
            print(f"❌ Error updating profile for user {user.id}: {e}")
            continue
    
    db.commit()
    print(f"✅ Updated {updated_count} user learning profiles")
    return updated_count

def update_course_performance(db: Session) -> int:
    """
    Update course performance analytics.
    
    Returns:
        int: Number of courses updated
    """
    print("🔄 Updating course performance analytics...")
    
    courses = db.query(Course).all()
    updated_count = 0
    
    for course in courses:
        try:
            # Get course enrollments
            enrollments = db.query(Enrollment).filter(
                and_(
                    Enrollment.course_id == course.id,
                    Enrollment.is_active == True,
                    Enrollment.deleted_at.is_(None)
                )
            ).all()
            
            # Get course interactions
            interactions = db.query(UserInteraction).filter(
                UserInteraction.course_id == course.id
            ).all()
            
            # Calculate metrics
            total_enrollments = len(enrollments)
            total_completions = len([e for e in enrollments if e.is_completed])
            completion_rate = (total_completions / total_enrollments * 100) if total_enrollments > 0 else 0.0
            
            # Calculate average completion time
            completed_enrollments = [e for e in enrollments if e.is_completed and e.completion_date]
            avg_completion_time = 0.0
            if completed_enrollments:
                total_time = 0
                for enrollment in completed_enrollments:
                    if enrollment.enrollment_date and enrollment.completion_date:
                        time_diff = enrollment.completion_date - enrollment.enrollment_date
                        total_time += time_diff.total_seconds() / 3600  # Convert to hours
                avg_completion_time = total_time / len(completed_enrollments)
            
            # Calculate average rating
            ratings = [i.rating for i in interactions if i.rating is not None]
            avg_rating = sum(ratings) / len(ratings) if ratings else 0.0
            
            # Calculate engagement metrics
            total_views = len([i for i in interactions if i.interaction_type == 'view'])
            total_likes = len([i for i in interactions if i.interaction_type == 'like'])
            total_unlikes = len([i for i in interactions if i.interaction_type == 'unlike'])
            engagement_score = total_views + (total_likes * 2) - total_unlikes
            
            # Insert or update course performance
            db.execute(text("""
                INSERT INTO analytics.course_performance (
                    course_id, total_enrollments, total_completions, 
                    completion_rate, average_rating,
                    total_views, engagement_score,
                    updated_at
                ) VALUES (
                    :course_id, :total_enrollments, :total_completions,
                    :completion_rate, :avg_rating,
                    :total_views, :engagement_score,
                    CURRENT_TIMESTAMP
                )
                ON CONFLICT (course_id) DO UPDATE SET
                    total_enrollments = EXCLUDED.total_enrollments,
                    total_completions = EXCLUDED.total_completions,
                    completion_rate = EXCLUDED.completion_rate,
                    average_rating = EXCLUDED.average_rating,
                    total_views = EXCLUDED.total_views,
                    engagement_score = EXCLUDED.engagement_score,
                    updated_at = CURRENT_TIMESTAMP
            """), {
                'course_id': course.id,
                'total_enrollments': total_enrollments,
                'total_completions': total_completions,
                'completion_rate': completion_rate,
                'avg_completion_time_hours': avg_completion_time,
                'avg_rating': avg_rating,
                'total_views': total_views,
                'engagement_score': engagement_score
            })
            
            updated_count += 1
            
        except Exception as e:
            print(f"❌ Error updating performance for course {course.id}: {e}")
            continue
    
    db.commit()
    print(f"✅ Updated {updated_count} course performance records")
    return updated_count

def update_recommendation_analytics(db: Session) -> int:
    """
    Update recommendation analytics.
    
    Returns:
        int: Number of recommendation records updated
    """
    print("🔄 Updating recommendation analytics...")
    
    # Get recommendation logs
    logs = db.query(RecommendationLog).all()
    updated_count = 0
    
    for log in logs:
        try:
            # Get recommendations for this log
            recommendations = db.query(Recommendation).filter(
                Recommendation.user_id == log.user_id
            ).filter(
                Recommendation.created_at >= log.started_at
            ).filter(
                Recommendation.created_at <= (log.completed_at or datetime.utcnow())
            ).all()
            
            # Calculate metrics
            total_recommendations = len(recommendations)
            avg_confidence = sum(r.confidence_score for r in recommendations) / total_recommendations if total_recommendations > 0 else 0.0
            
            # Count positive feedback
            positive_feedback = len([r for r in recommendations if r.user_feedback == 'positive'])
            negative_feedback = len([r for r in recommendations if r.user_feedback == 'negative'])
            
            # Insert or update recommendation analytics
            db.execute(text("""
                INSERT INTO analytics.recommendation_analytics (
                    user_id, algorithm_used, total_recommendations,
                    avg_confidence_score, positive_feedback_count, negative_feedback_count,
                    processing_time_ms, success_rate, last_updated
                ) VALUES (
                    :user_id, :algorithm_used, :total_recommendations,
                    :avg_confidence_score, :positive_feedback_count, :negative_feedback_count,
                    :processing_time_ms, :success_rate, CURRENT_TIMESTAMP
                )
                ON CONFLICT (user_id, algorithm_used) DO UPDATE SET
                    total_recommendations = EXCLUDED.total_recommendations,
                    avg_confidence_score = EXCLUDED.avg_confidence_score,
                    positive_feedback_count = EXCLUDED.positive_feedback_count,
                    negative_feedback_count = EXCLUDED.negative_feedback_count,
                    processing_time_ms = EXCLUDED.processing_time_ms,
                    success_rate = EXCLUDED.success_rate,
                    last_updated = CURRENT_TIMESTAMP
            """), {
                'user_id': log.user_id,
                'algorithm_used': log.algorithm_used or 'unknown',
                'total_recommendations': total_recommendations,
                'avg_confidence_score': avg_confidence,
                'positive_feedback_count': positive_feedback,
                'negative_feedback_count': negative_feedback,
                'processing_time_ms': log.processing_time_ms or 0,
                'success_rate': 1.0 if log.status == 'completed' else 0.0
            })
            
            updated_count += 1
            
        except Exception as e:
            print(f"❌ Error updating recommendation analytics for log {log.id}: {e}")
            continue
    
    db.commit()
    print(f"✅ Updated {updated_count} recommendation analytics records")
    return updated_count

def update_system_performance(db: Session) -> int:
    """
    Update system performance analytics.
    
    Returns:
        int: Number of system performance records updated
    """
    print("🔄 Updating system performance analytics...")
    
    # Calculate system-wide metrics
    total_users = db.query(User).count()
    total_courses = db.query(Course).count()
    total_enrollments = db.query(Enrollment).filter(
        and_(
            Enrollment.is_active == True,
            Enrollment.deleted_at.is_(None)
        )
    ).count()
    total_interactions = db.query(UserInteraction).count()
    total_recommendations = db.query(Recommendation).count()
    
    # Calculate daily metrics
    today = datetime.utcnow().date()
    yesterday = today - timedelta(days=1)
    
    daily_enrollments = db.query(Enrollment).filter(
        and_(
            Enrollment.is_active == True,
            Enrollment.deleted_at.is_(None),
            func.date(Enrollment.enrollment_date) == today
        )
    ).count()
    
    daily_interactions = db.query(UserInteraction).filter(
        func.date(UserInteraction.created_at) == today
    ).count()
    
    daily_recommendations = db.query(Recommendation).filter(
        func.date(Recommendation.created_at) == today
    ).count()
    
    # Insert or update system performance
    db.execute(text("""
        INSERT INTO analytics.system_performance (
            date, hour, total_users_active, total_sessions,
            total_page_views, total_api_calls, total_recommendations_requested,
            total_recommendations_generated, created_at
        ) VALUES (
            :date, :hour, :total_users_active, :total_sessions,
            :total_page_views, :total_api_calls, :total_recommendations_requested,
            :total_recommendations_generated, CURRENT_TIMESTAMP
        )
        ON CONFLICT (date, hour) DO UPDATE SET
            total_users_active = EXCLUDED.total_users_active,
            total_sessions = EXCLUDED.total_sessions,
            total_page_views = EXCLUDED.total_page_views,
            total_api_calls = EXCLUDED.total_api_calls,
            total_recommendations_requested = EXCLUDED.total_recommendations_requested,
            total_recommendations_generated = EXCLUDED.total_recommendations_generated
    """), {
        'date': today,
        'hour': 0,  # Default to hour 0 for daily summary
        'total_users_active': total_users,
        'total_sessions': total_enrollments,  # Using enrollments as proxy for sessions
        'total_page_views': total_interactions,  # Using interactions as proxy for page views
        'total_api_calls': total_interactions,  # Using interactions as proxy for API calls
        'total_recommendations_requested': total_recommendations,
        'total_recommendations_generated': total_recommendations
    })
    
    db.commit()
    print(f"✅ Updated system performance for {today}")
    return 1

def main():
    """Main function to update all analytics tables."""
    print("🚀 Starting Analytics Update Script")
    print("=" * 50)
    
    # Get database session
    db = next(get_db())
    
    try:
        # Update all analytics tables
        user_profiles_count = update_user_learning_profiles(db)
        course_performance_count = update_course_performance(db)
        recommendation_analytics_count = update_recommendation_analytics(db)
        system_performance_count = update_system_performance(db)
        
        print("=" * 50)
        print("✅ Analytics Update Complete!")
        print(f"📊 Updated {user_profiles_count} user learning profiles")
        print(f"📊 Updated {course_performance_count} course performance records")
        print(f"📊 Updated {recommendation_analytics_count} recommendation analytics records")
        print(f"📊 Updated {system_performance_count} system performance records")
        
    except Exception as e:
        print(f"❌ Error during analytics update: {e}")
        db.rollback()
        return 1
    
    finally:
        db.close()
    
    return 0

if __name__ == "__main__":
    exit(main())
