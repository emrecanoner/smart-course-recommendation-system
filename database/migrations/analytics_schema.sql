-- Analytics Schema for Data Warehouse
-- This schema will be used for analytics and reporting purposes

-- Create analytics schema
CREATE SCHEMA IF NOT EXISTS analytics;

-- Drop existing tables to recreate with new columns
DROP TABLE IF EXISTS analytics.user_learning_profile CASCADE;
DROP TABLE IF EXISTS analytics.course_performance CASCADE;
DROP TABLE IF EXISTS analytics.recommendation_analytics CASCADE;
DROP TABLE IF EXISTS analytics.user_journey CASCADE;
DROP TABLE IF EXISTS analytics.system_performance CASCADE;

-- User Learning Profile Table
-- Aggregated user data for analytics and reporting
CREATE TABLE IF NOT EXISTS analytics.user_learning_profile (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    
    -- Basic Statistics
    total_courses_viewed INTEGER DEFAULT 0,
    total_courses_enrolled INTEGER DEFAULT 0,
    total_courses_completed INTEGER DEFAULT 0,
    total_courses_rated INTEGER DEFAULT 0,
    total_courses_liked INTEGER DEFAULT 0,
    total_courses_unliked INTEGER DEFAULT 0,
    total_courses_unenrolled INTEGER DEFAULT 0,
    total_interactions INTEGER DEFAULT 0,
    
    -- Performance Metrics
    avg_completion_rate DECIMAL(5,2) DEFAULT 0.00,
    avg_rating_given DECIMAL(3,2) DEFAULT 0.00,
    avg_rating_received DECIMAL(3,2) DEFAULT 0.00,
    learning_velocity DECIMAL(5,2) DEFAULT 0.00, -- courses completed per month
    engagement_score DECIMAL(5,2) DEFAULT 0.00,
    
    -- Preferences (JSON fields for flexibility)
    preferred_categories JSONB DEFAULT '[]'::jsonb,
    preferred_difficulty_levels JSONB DEFAULT '{}'::jsonb,
    preferred_content_types JSONB DEFAULT '{}'::jsonb,
    preferred_durations JSONB DEFAULT '{}'::jsonb,
    learning_goals JSONB DEFAULT '[]'::jsonb,
    skills_developed JSONB DEFAULT '[]'::jsonb,
    
    -- Behavioral Patterns
    preferred_time_of_day VARCHAR(20) DEFAULT 'unknown',
    preferred_day_of_week VARCHAR(20) DEFAULT 'unknown',
    learning_pattern VARCHAR(50) DEFAULT 'unknown', -- consistent, sporadic, intensive
    device_preference VARCHAR(50) DEFAULT 'unknown',
    
    -- Engagement Metrics
    last_activity_date TIMESTAMP,
    days_since_last_activity INTEGER DEFAULT 0,
    streak_days INTEGER DEFAULT 0,
    longest_streak INTEGER DEFAULT 0,
    
    -- Learning Journey
    first_enrollment_date TIMESTAMP,
    last_enrollment_date TIMESTAMP,
    first_completion_date TIMESTAMP,
    last_completion_date TIMESTAMP,
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Constraints
    UNIQUE(user_id)
);

-- Course Performance Analytics Table
-- Aggregated course data for analytics
CREATE TABLE IF NOT EXISTS analytics.course_performance (
    id SERIAL PRIMARY KEY,
    course_id INTEGER NOT NULL REFERENCES courses(id) ON DELETE CASCADE,
    
    -- Basic Statistics
    total_views INTEGER DEFAULT 0,
    total_enrollments INTEGER DEFAULT 0,
    total_completions INTEGER DEFAULT 0,
    total_ratings INTEGER DEFAULT 0,
    total_shares INTEGER DEFAULT 0,
    
    -- Performance Metrics
    completion_rate DECIMAL(5,2) DEFAULT 0.00,
    average_rating DECIMAL(3,2) DEFAULT 0.00,
    engagement_score DECIMAL(5,2) DEFAULT 0.00,
    popularity_score DECIMAL(5,2) DEFAULT 0.00,
    
    -- User Demographics (JSON for flexibility)
    user_skill_levels JSONB DEFAULT '{}'::jsonb,
    user_age_groups JSONB DEFAULT '{}'::jsonb,
    user_regions JSONB DEFAULT '{}'::jsonb,
    
    -- Content Analysis
    difficulty_rating DECIMAL(3,2) DEFAULT 0.00,
    content_quality_score DECIMAL(3,2) DEFAULT 0.00,
    instructor_rating DECIMAL(3,2) DEFAULT 0.00,
    
    -- Trends
    enrollment_trend VARCHAR(20) DEFAULT 'stable', -- increasing, decreasing, stable
    completion_trend VARCHAR(20) DEFAULT 'stable',
    rating_trend VARCHAR(20) DEFAULT 'stable',
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Constraints
    UNIQUE(course_id)
);

-- Recommendation Analytics Table
-- Track recommendation performance and effectiveness
CREATE TABLE IF NOT EXISTS analytics.recommendation_analytics (
    id SERIAL PRIMARY KEY,
    
    -- Recommendation Details
    algorithm_used VARCHAR(100) NOT NULL,
    model_version VARCHAR(50),
    batch_id VARCHAR(255),
    
    -- Performance Metrics
    total_recommendations_generated INTEGER DEFAULT 0,
    total_recommendations_viewed INTEGER DEFAULT 0,
    total_recommendations_clicked INTEGER DEFAULT 0,
    total_recommendations_enrolled INTEGER DEFAULT 0,
    total_recommendations_completed INTEGER DEFAULT 0,
    
    -- Conversion Rates
    view_rate DECIMAL(5,2) DEFAULT 0.00,
    click_through_rate DECIMAL(5,2) DEFAULT 0.00,
    enrollment_rate DECIMAL(5,2) DEFAULT 0.00,
    completion_rate DECIMAL(5,2) DEFAULT 0.00,
    
    -- Quality Metrics
    average_confidence_score DECIMAL(3,2) DEFAULT 0.00,
    average_user_rating DECIMAL(3,2) DEFAULT 0.00,
    diversity_score DECIMAL(3,2) DEFAULT 0.00,
    
    -- Time Period
    period_start TIMESTAMP NOT NULL,
    period_end TIMESTAMP NOT NULL,
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- User Journey Analytics Table
-- Track user learning journey and progression
CREATE TABLE IF NOT EXISTS analytics.user_journey (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    
    -- Journey Stages
    stage VARCHAR(50) NOT NULL, -- discovery, exploration, commitment, mastery
    stage_entry_date TIMESTAMP NOT NULL,
    stage_exit_date TIMESTAMP,
    days_in_stage INTEGER DEFAULT 0,
    
    -- Stage Metrics
    courses_viewed_in_stage INTEGER DEFAULT 0,
    courses_enrolled_in_stage INTEGER DEFAULT 0,
    courses_completed_in_stage INTEGER DEFAULT 0,
    skills_acquired_in_stage JSONB DEFAULT '[]'::jsonb,
    
    -- Progression Indicators
    skill_level_progression VARCHAR(50), -- beginner -> intermediate -> advanced
    category_exploration JSONB DEFAULT '[]'::jsonb,
    learning_intensity DECIMAL(3,2) DEFAULT 0.00,
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- System Performance Analytics Table
-- Track system performance and usage patterns
CREATE TABLE IF NOT EXISTS analytics.system_performance (
    id SERIAL PRIMARY KEY,
    
    -- Date and Time
    date DATE NOT NULL,
    hour INTEGER NOT NULL, -- 0-23
    
    -- Usage Metrics
    total_users_active INTEGER DEFAULT 0,
    total_sessions INTEGER DEFAULT 0,
    total_page_views INTEGER DEFAULT 0,
    total_api_calls INTEGER DEFAULT 0,
    
    -- Recommendation Metrics
    total_recommendations_requested INTEGER DEFAULT 0,
    total_recommendations_generated INTEGER DEFAULT 0,
    avg_recommendation_time_ms DECIMAL(8,2) DEFAULT 0.00,
    
    -- Performance Metrics
    avg_response_time_ms DECIMAL(8,2) DEFAULT 0.00,
    error_rate DECIMAL(5,2) DEFAULT 0.00,
    cache_hit_rate DECIMAL(5,2) DEFAULT 0.00,
    
    -- Resource Usage
    cpu_usage_percent DECIMAL(5,2) DEFAULT 0.00,
    memory_usage_percent DECIMAL(5,2) DEFAULT 0.00,
    disk_usage_percent DECIMAL(5,2) DEFAULT 0.00,
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Constraints
    UNIQUE(date, hour)
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_user_learning_profile_user_id ON analytics.user_learning_profile(user_id);
CREATE INDEX IF NOT EXISTS idx_user_learning_profile_updated_at ON analytics.user_learning_profile(updated_at);
CREATE INDEX IF NOT EXISTS idx_user_learning_profile_engagement_score ON analytics.user_learning_profile(engagement_score);

CREATE INDEX IF NOT EXISTS idx_course_performance_course_id ON analytics.course_performance(course_id);
CREATE INDEX IF NOT EXISTS idx_course_performance_updated_at ON analytics.course_performance(updated_at);
CREATE INDEX IF NOT EXISTS idx_course_performance_popularity_score ON analytics.course_performance(popularity_score);

CREATE INDEX IF NOT EXISTS idx_recommendation_analytics_algorithm ON analytics.recommendation_analytics(algorithm_used);
CREATE INDEX IF NOT EXISTS idx_recommendation_analytics_period ON analytics.recommendation_analytics(period_start, period_end);

CREATE INDEX IF NOT EXISTS idx_user_journey_user_id ON analytics.user_journey(user_id);
CREATE INDEX IF NOT EXISTS idx_user_journey_stage ON analytics.user_journey(stage);
CREATE INDEX IF NOT EXISTS idx_user_journey_entry_date ON analytics.user_journey(stage_entry_date);

CREATE INDEX IF NOT EXISTS idx_system_performance_date_hour ON analytics.system_performance(date, hour);

-- Create triggers for automatic timestamp updates
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_user_learning_profile_updated_at 
    BEFORE UPDATE ON analytics.user_learning_profile 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_course_performance_updated_at 
    BEFORE UPDATE ON analytics.course_performance 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_recommendation_analytics_updated_at 
    BEFORE UPDATE ON analytics.recommendation_analytics 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_user_journey_updated_at 
    BEFORE UPDATE ON analytics.user_journey 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
