"""
Application constants and configuration values.
"""

# Engagement Score Weights
# These weights define the relative importance of different user interactions
# for calculating engagement scores across the application.

ENGAGEMENT_WEIGHTS = {
    'view': 1,      # Basic engagement - user viewed a course
    'like': 3,      # Positive engagement - user liked a course
    'unlike': -2,   # Negative engagement - user unliked a course
    'enroll': 5,    # Strong commitment - user enrolled in a course
    'unenroll': -3, # Negative commitment - user unenrolled from a course
    'complete': 10, # Highest engagement - user completed a course
    'rate': 4,      # Feedback engagement - user rated a course
    'share': 3      # Social engagement - user shared a course
}

# Interaction Types
INTERACTION_TYPES = [
    'view',
    'like', 
    'unlike',
    'enroll',
    'unenroll',
    'complete',
    'rate',
    'share'
]

# Positive vs Negative Action Classification
POSITIVE_ACTIONS = ['like', 'enroll', 'complete', 'rate', 'share']
NEGATIVE_ACTIONS = ['unlike', 'unenroll']

# Engagement Score Calculation Parameters
ENGAGEMENT_RATIO_BONUS_MULTIPLIER = 10  # Multiplier for engagement ratio bonus
MIN_ENGAGEMENT_SCORE = 0  # Minimum engagement score

# Pre-calculated engagement score multipliers for optimization
ENGAGEMENT_SCORE_MULTIPLIERS = {
    'view': 0.1,      # Low value for passive viewing
    'like': 1.0,      # Moderate positive engagement
    'unlike': -0.5,   # Small negative impact
    'enroll': 2.0,    # High commitment
    'unenroll': -1.0, # Negative commitment
    'complete': 3.0,  # Highest achievement
    'rate': 1.5,      # Good engagement
    'share': 2.0      # High engagement
}

# Learning velocity calculation parameters
LEARNING_VELOCITY_MIN_MONTHS = 1.0   # Minimum 1 month for realistic velocity calculation
LEARNING_VELOCITY_MAX_MONTHS = 12.0  # Maximum months for velocity calculation

def calculate_engagement_score(interactions, total_courses_liked=0, total_courses_unliked=0, 
                              total_courses_enrolled=0, total_courses_unenrolled=0, 
                              total_courses_completed=0, total_courses_rated=0):
    """
    Calculate engagement score based on user interactions.
    
    Args:
        interactions: List of interaction objects (used for base engagement calculation)
        total_courses_liked: Count of liked courses (used for engagement ratio)
        total_courses_unliked: Count of unliked courses (used for engagement ratio)
        total_courses_enrolled: Count of enrolled courses (used for engagement ratio)
        total_courses_unenrolled: Count of unenrolled courses (used for engagement ratio)
        total_courses_completed: Count of completed courses (used for engagement ratio)
        total_courses_rated: Count of rated courses (used for engagement ratio)
    
    Returns:
        float: Calculated engagement score
    """
    if not interactions:
        return 0.0
    
    # Calculate base engagement score from all interactions
    base_engagement = sum(
        ENGAGEMENT_SCORE_MULTIPLIERS.get(i.interaction_type, 1.0) for i in interactions
    )
    
    # Calculate positive vs negative engagement ratio
    # Positive actions: like, enroll, complete, rate
    # Negative actions: unlike, unenroll
    positive_actions = total_courses_liked + total_courses_enrolled + total_courses_completed + total_courses_rated
    negative_actions = total_courses_unliked + total_courses_unenrolled
    
    # Calculate engagement ratio bonus (only if there are positive actions)
    if positive_actions > 0:
        total_actions = positive_actions + negative_actions
        if total_actions > 0:
            engagement_ratio = positive_actions / total_actions
            # Bonus for high positive engagement ratio (0.5 = neutral, 1.0 = all positive)
            engagement_bonus = (engagement_ratio - 0.5) * ENGAGEMENT_RATIO_BONUS_MULTIPLIER
        else:
            engagement_bonus = 0
    else:
        engagement_bonus = 0
    
    final_score = round(max(MIN_ENGAGEMENT_SCORE, base_engagement + engagement_bonus), 2)
    return final_score

def get_engagement_level(engagement_score):
    """
    Get engagement level based on score.
    
    Args:
        engagement_score: Calculated engagement score
    
    Returns:
        str: Engagement level description
    """
    if engagement_score < 10.0:
        return "Low"
    elif engagement_score < 25.0:
        return "Medium"
    elif engagement_score < 50.0:
        return "Good"
    elif engagement_score < 100.0:
        return "High"
    else:
        return "Very High"

def get_learning_velocity_level(learning_velocity):
    """
    Get learning velocity level based on velocity.
    
    Args:
        learning_velocity: Calculated learning velocity
    
    Returns:
        str: Learning velocity level description
    """
    if learning_velocity < 0.5:
        return "Slow"
    elif learning_velocity < 1.0:
        return "Below Average"
    elif learning_velocity < 2.0:
        return "Average"
    elif learning_velocity < 4.0:
        return "Fast"
    else:
        return "Very Fast"

def calculate_learning_velocity(completed_enrollments, user_created_at=None):
    """
    Calculate learning velocity (courses completed per month).
    
    Args:
        completed_enrollments: List of completed enrollment objects
        user_created_at: User registration date (optional, for more accurate calculation)
    
    Returns:
        float: Learning velocity (courses completed per month)
    """
    if not completed_enrollments:
        return 0.0
    
    # Get completion dates
    completion_dates = [e.completion_date for e in completed_enrollments if e.completion_date]
    if not completion_dates:
        return 0.0
    
    # Use user creation date as start point if available, otherwise use first completion
    if user_created_at:
        start_date = user_created_at
    else:
        start_date = min(completion_dates)
    
    # Use current date as end point
    from datetime import datetime
    end_date = datetime.now()
    
    # Calculate months with bounds
    months = (end_date - start_date).days / 30.0
    months = max(LEARNING_VELOCITY_MIN_MONTHS, min(months, LEARNING_VELOCITY_MAX_MONTHS))
    
    return round(len(completed_enrollments) / months, 2)
