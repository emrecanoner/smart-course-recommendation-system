"""
Dataset seeding script for Smart Course Recommendation System.
This script populates the database with course data from Hugging Face dataset.
"""

import random
import pandas as pd
import sys
import os
import re
from datetime import datetime, timedelta
from typing import List
from datasets import load_dataset

# Add backend directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'backend'))

from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.models.course import Course, Category
from app.core.config import settings


def create_categories_from_skills(db: Session, all_skills: set) -> List[Category]:
    """Create categories dynamically based on skills from dataset."""
    # Skill to category mapping
    skill_category_map = {
        # Programming
        'python': 'Programming',
        'javascript': 'Programming', 
        'java': 'Programming',
        'c++': 'Programming',
        'c#': 'Programming',
        'ruby': 'Programming',
        'go': 'Programming',
        'rust': 'Programming',
        'swift': 'Programming',
        'kotlin': 'Programming',
        'php': 'Programming',
        'r': 'Programming',
        'scala': 'Programming',
        'programming': 'Programming',
        'coding': 'Programming',
        
        # Data Science & AI
        'data science': 'Data Science',
        'machine learning': 'Data Science',
        'artificial intelligence': 'Data Science',
        'deep learning': 'Data Science',
        'data analysis': 'Data Science',
        'statistics': 'Data Science',
        'analytics': 'Data Science',
        'big data': 'Data Science',
        'data visualization': 'Data Science',
        'pandas': 'Data Science',
        'numpy': 'Data Science',
        'tensorflow': 'Data Science',
        'pytorch': 'Data Science',
        'scikit-learn': 'Data Science',
        
        # Web Development
        'web development': 'Web Development',
        'html': 'Web Development',
        'css': 'Web Development',
        'react': 'Web Development',
        'angular': 'Web Development',
        'vue': 'Web Development',
        'node.js': 'Web Development',
        'django': 'Web Development',
        'flask': 'Web Development',
        'spring': 'Web Development',
        'express': 'Web Development',
        'frontend': 'Web Development',
        'backend': 'Web Development',
        'full stack': 'Web Development',
        
        # Mobile Development
        'mobile development': 'Mobile Development',
        'ios': 'Mobile Development',
        'android': 'Mobile Development',
        'react native': 'Mobile Development',
        'flutter': 'Mobile Development',
        'xamarin': 'Mobile Development',
        'ionic': 'Mobile Development',
        
        # Business & Management
        'business': 'Business',
        'management': 'Business',
        'leadership': 'Business',
        'entrepreneurship': 'Business',
        'finance': 'Business',
        'marketing': 'Business',
        'strategy': 'Business',
        'project management': 'Business',
        'agile': 'Business',
        'scrum': 'Business',
        
        # Design
        'design': 'Design',
        'ui': 'Design',
        'ux': 'Design',
        'graphic design': 'Design',
        'web design': 'Design',
        'user experience': 'Design',
        'user interface': 'Design',
        'photoshop': 'Design',
        'illustrator': 'Design',
        'figma': 'Design',
        'sketch': 'Design',
        
        # Cloud & DevOps
        'cloud': 'Cloud Computing',
        'aws': 'Cloud Computing',
        'azure': 'Cloud Computing',
        'google cloud': 'Cloud Computing',
        'devops': 'DevOps',
        'docker': 'DevOps',
        'kubernetes': 'DevOps',
        'jenkins': 'DevOps',
        'ci/cd': 'DevOps',
        'terraform': 'DevOps',
        
        # Cybersecurity
        'cybersecurity': 'Cybersecurity',
        'security': 'Cybersecurity',
        'ethical hacking': 'Cybersecurity',
        'penetration testing': 'Cybersecurity',
        'network security': 'Cybersecurity',
        'information security': 'Cybersecurity',
    }
    
    # Create categories based on skills
    created_categories = {}
    for skill in all_skills:
        skill_lower = skill.lower().strip()
        for skill_key, category_name in skill_category_map.items():
            if skill_key in skill_lower:
                if category_name not in created_categories:
                    # Check if category already exists
                    existing_category = db.query(Category).filter(Category.name == category_name).first()
                    if existing_category:
                        created_categories[category_name] = existing_category
                    else:
                        category = Category(
                            name=category_name,
                            description=f"Courses related to {category_name.lower()}",
                            is_active=True
                        )
                        db.add(category)
                        created_categories[category_name] = category
                break
    
    # Add a default "Other" category for unmatched skills
    if "Other" not in created_categories:
        existing_other = db.query(Category).filter(Category.name == "Other").first()
        if existing_other:
            created_categories["Other"] = existing_other
        else:
            other_category = Category(
                name="Other",
                description="Courses that don't fit into specific categories",
                is_active=True
            )
            db.add(other_category)
            created_categories["Other"] = other_category
    
    db.commit()
    return list(created_categories.values())


def determine_category_from_skills(skills: List[str], categories: List[Category]) -> Category:
    """Determine the best category for a course based on its skills."""
    # Skill to category mapping (same as in create_categories_from_skills)
    skill_category_map = {
        'python': 'Programming', 'javascript': 'Programming', 'java': 'Programming',
        'data science': 'Data Science', 'machine learning': 'Data Science', 'ai': 'Data Science',
        'web development': 'Web Development', 'html': 'Web Development', 'css': 'Web Development',
        'mobile development': 'Mobile Development', 'ios': 'Mobile Development', 'android': 'Mobile Development',
        'business': 'Business', 'management': 'Business', 'leadership': 'Business',
        'design': 'Design', 'ui': 'Design', 'ux': 'Design',
        'cloud': 'Cloud Computing', 'aws': 'Cloud Computing', 'azure': 'Cloud Computing',
        'devops': 'DevOps', 'docker': 'DevOps', 'kubernetes': 'DevOps',
        'cybersecurity': 'Cybersecurity', 'security': 'Cybersecurity',
    }
    
    # Find the best matching category
    for skill in skills:
        skill_lower = skill.lower().strip()
        for skill_key, category_name in skill_category_map.items():
            if skill_key in skill_lower:
                # Find the category in the list
                for category in categories:
                    if category.name == category_name:
                        return category
    
    # Return "Other" category if no match found
    for category in categories:
        if category.name == "Other":
            return category
    
    # Fallback to first category if "Other" not found
    return categories[0] if categories else None


def load_dataset_data() -> pd.DataFrame:
    """Load course data from Hugging Face dataset."""
    try:
        print("📚 Loading Coursera dataset from Hugging Face...")
        ds = load_dataset('azrai99/coursera-course-dataset')
        df = ds['train'].to_pandas()
        print(f"✅ Loaded {len(df)} courses from Hugging Face dataset")
        return df
    except Exception as e:
        print(f"❌ Error loading Hugging Face dataset: {e}")
        print("📁 Trying to load from local CSV file...")
        try:
            df = pd.read_csv(settings.COURSE_DATASET_PATH)
            print(f"✅ Loaded {len(df)} courses from {settings.COURSE_DATASET_PATH}")
            return df
        except FileNotFoundError:
            print(f"❌ {settings.COURSE_DATASET_PATH} file not found.")
            return None
        except Exception as e2:
            print(f"❌ Error loading {settings.COURSE_DATASET_PATH}: {e2}")
            return None


def create_courses_from_dataset(db: Session, categories: List[Category], df: pd.DataFrame) -> List[Course]:
    """Create courses from Hugging Face dataset data."""
    if not settings.USE_COURSE_DATASET:
        print("📚 Dataset usage disabled.")
        return []
    
    if df is None:
        return []
    
    courses = []
    # If SEED_COURSES_COUNT is 0 or not set, load all courses
    if settings.SEED_COURSES_COUNT == 0:
        max_courses = len(df)
        print(f"📚 Creating ALL {max_courses} courses from dataset...")
    else:
        max_courses = min(settings.SEED_COURSES_COUNT, len(df))
        print(f"📚 Creating {max_courses} courses from dataset...")
    
    for idx, row in df.head(max_courses).iterrows():
        # Map difficulty levels from new dataset
        difficulty_mapping = {
            'Beginner level': 'beginner',
            'Intermediate level': 'intermediate', 
            'Advanced level': 'advanced'
        }
        difficulty = difficulty_mapping.get(row['Level'], 'beginner')
        
        # Extract skills and create skills string
        skills = row['Skills'] if isinstance(row['Skills'], list) else []
        if not skills and pd.notna(row['Skills']):
            skills = str(row['Skills']).split(',')[:5]
        skills_string = ', '.join([skill.strip() for skill in skills[:5]]) if skills else None
        
        # Handle rating conversion
        try:
            rating = float(row['rating'])
        except (ValueError, TypeError):
            rating = random.uniform(3.5, 4.8)  # Default rating for invalid values
        
        # Handle enrollment count
        try:
            enrolled_str = str(row['enrolled']).replace(',', '').replace('K', '000').replace('M', '000000')
            enrollment_count = int(float(enrolled_str))
        except (ValueError, TypeError):
            enrollment_count = random.randint(500, 10000)
        
        # Handle review count
        try:
            rating_count = int(row['num_reviews']) if pd.notna(row['num_reviews']) else random.randint(100, 2000)
        except (ValueError, TypeError):
            rating_count = random.randint(100, 2000)
        
        # Handle satisfaction rate (completion rate)
        try:
            satisfaction_str = str(row['Satisfaction Rate']).replace('%', '')
            completion_rate = float(satisfaction_str) if pd.notna(row['Satisfaction Rate']) and satisfaction_str != 'None' else random.uniform(60.0, 85.0)
        except (ValueError, TypeError):
            completion_rate = random.uniform(60.0, 85.0)
        
        # Handle duration from Schedule
        duration_hours = random.randint(20, 80)  # Default
        if pd.notna(row['Schedule']):
            schedule_str = str(row['Schedule']).lower()
            if 'hours' in schedule_str:
                try:
                    # Extract hours from schedule like "10 hours to complete"
                    hours_match = re.search(r'(\d+)\s*hours?', schedule_str)
                    if hours_match:
                        duration_hours = int(hours_match.group(1))
                except:
                    duration_hours = random.randint(20, 80)
        
        # Determine category based on skills
        category = determine_category_from_skills(skills, categories)
        
        # Create course with dataset data only
        course = Course(
            title=str(row['title']),
            description=str(row['Description']),
            short_description=f"Learn {skills_string}" if skills_string else "Comprehensive course",
            skills=skills_string,
            instructor=str(row['Instructor']),
            organization=str(row['Organization']),
            duration_hours=duration_hours,
            difficulty_level=difficulty,
            course_url=str(row['URL']),
            modules_count=str(row['Modules/Courses']),
            rating=rating,
            rating_count=rating_count,
            enrollment_count=enrollment_count,
            completion_rate=completion_rate,
            is_active=True,
            category_id=category.id,
            published_at=datetime.utcnow() - timedelta(days=random.randint(1, 365))
        )
        db.add(course)
        courses.append(course)
    
    db.commit()
    return courses


def main():
    """Main function to seed courses."""
    print("🌱 Starting dataset seeding...")
    
    # Check if seeding is enabled
    if not settings.SEED_DATA_ENABLED:
        print("❌ Seed data is disabled. Set SEED_DATA_ENABLED=True in .env file.")
        return
    
    # Create database session
    db = SessionLocal()
    
    try:
        # Load dataset first to collect all skills
        print("📚 Loading dataset to collect skills...")
        df = load_dataset_data()
        if df is None:
            print("❌ Failed to load dataset")
            return
        
        # Collect all unique skills
        all_skills = set()
        for idx, row in df.iterrows():
            skills = row['Skills'] if isinstance(row['Skills'], list) else []
            if not skills and pd.notna(row['Skills']):
                skills = str(row['Skills']).split(',')
            for skill in skills:
                if skill and skill.strip():
                    all_skills.add(skill.strip())
        
        print(f"📊 Found {len(all_skills)} unique skills")
        
        # Create categories based on skills
        print("📁 Creating categories from skills...")
        categories = create_categories_from_skills(db, all_skills)
        print(f"✅ Created {len(categories)} categories")
        
        # Create courses
        print("📚 Creating courses...")
        courses = create_courses_from_dataset(db, categories, df)
        print(f"✅ Created {len(courses)} courses from dataset")
        
        print("🎉 Dataset seeding completed successfully!")
        
    except Exception as e:
        print(f"❌ Error during seeding: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    main()
