# Database Scripts

This directory contains scripts for database management and data seeding.

## Scripts

### `dataset.py`
Populates the database with course data from Hugging Face dataset.

**Features:**
- Loads real course data from Hugging Face dataset
- Creates categories and courses
- Configurable via environment variables
- Uses real Coursera course data from Hugging Face

**Usage:**
```bash
# From project root
python database/scripts/dataset.py

# Or from database/scripts directory
cd database/scripts
python dataset.py
```

**Environment Variables:**
- `SEED_DATA_ENABLED`: Enable/disable seeding (True/False)
- `USE_COURSE_DATASET`: Use Hugging Face dataset (True/False)
- `SEED_COURSES_COUNT`: Number of courses to create (0 = all courses)
- `COURSE_DATASET_PATH`: Path to local CSV file as fallback

## Data Sources

### Hugging Face Dataset
Real course data from Coursera platform via Hugging Face containing:
- Course names and descriptions
- University information
- Difficulty levels
- Course ratings
- Skills and topics
- Enrollment counts
- Review counts

## Requirements

- Python 3.11+
- pandas
- datasets (Hugging Face)
- sqlalchemy
- All backend dependencies

## Notes

- Script automatically adds backend directory to Python path
- Dataset path is configured via environment variables
- Creates categories and courses only
- All course data comes from real Coursera courses via Hugging Face
- Falls back to local CSV if Hugging Face dataset fails
