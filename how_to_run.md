# 🚀 Smart Course Recommendation System - How to Run

## 📋 Prerequisites

### System Requirements
- **Python**: 3.10+ (recommended: 3.12)
- **Node.js**: 18+ (for React Native frontend)
- **PostgreSQL**: 13+ (database)
- **Docker**: 20+ (optional, for containerized setup)
- **Git**: Latest version

### Package Managers
- **Python**: `uv` (recommended) or `pip`
- **Node.js**: `npm` or `yarn`

---

## 🛠️ Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/smart-course-recommendation-system.git
cd smart-course-recommendation-system
```

### 2. Environment Setup
```bash
# Copy environment template
cp env.example .env

# Edit environment variables
nano .env  # or use your preferred editor
```

**Required Environment Variables:**
```env
# Database Configuration
POSTGRES_SERVER=localhost
POSTGRES_USER=your_username
POSTGRES_PASSWORD=your_password
POSTGRES_DB=course_recommendation
POSTGRES_PORT=5432

# API Configuration
API_V1_STR=/api/v1
PROJECT_NAME=Smart Course Recommendation System
VERSION=1.0.0

# Security
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# AI/ML Configuration
AI_MODELS_PATH=./ai-ml/models
AI_TRAINING_DATA_PATH=./ai-ml/data
```

### 3. Database Setup

#### Option A: Local PostgreSQL
```bash
# Install PostgreSQL (Ubuntu/Debian)
sudo apt update
sudo apt install postgresql postgresql-contrib

# Create database and user
sudo -u postgres psql
CREATE DATABASE course_recommendation;
CREATE USER your_username WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE course_recommendation TO your_username;
\q
```

#### Option B: Docker PostgreSQL
```bash
# Run PostgreSQL in Docker
docker run --name postgres-db \
  -e POSTGRES_DB=course_recommendation \
  -e POSTGRES_USER=your_username \
  -e POSTGRES_PASSWORD=your_password \
  -p 5432:5432 \
  -d postgres:13
```

### 4. Python Dependencies

#### Using uv (Recommended)
```bash
# Install uv if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install Python dependencies
uv sync

# Activate virtual environment
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate     # Windows
```

#### Using pip
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

### 5. AI/ML Dependencies
```bash
# Install AI/ML specific dependencies
cd ai-ml
uv sync  # or pip install -r requirements.txt

# Download spaCy English model
uv run python -m spacy download en_core_web_sm
```

### 6. Frontend Dependencies
```bash
# Install Node.js dependencies
cd frontend
npm install

# For React Native development
npm install -g expo-cli
```

---

## 🚀 Running the Application

### 1. Database Migration & Data Setup
```bash
# Run database migrations
cd backend
uv run alembic upgrade head

# Add sample courses to database (creates courses, categories, users)
cd ../database/scripts
uv run python dataset.py

# Update analytics schema (required for AI recommendations)
# This populates analytics.user_learning_profile, analytics.course_performance, etc.
cd ../../backend
uv run python scripts/update_analytics.py
```

**Important Notes:**
- **`dataset.py`**: Creates sample courses, categories, and users for testing
- **`update_analytics.py`**: Populates analytics schema tables (like a data warehouse)
  - `analytics.user_learning_profile`: User behavior analytics
  - `analytics.course_performance`: Course performance metrics
  - `analytics.recommendation_analytics`: AI recommendation analytics
  - `analytics.system_performance`: System-wide performance metrics

### 2. Train AI Models
```bash
# Train AI models (first time only)
cd ai-ml
uv run python training/train_models.py

# This will create:
# - Neural collaborative filtering models
# - Semantic understanding models
# - Context-aware recommendation models
# - Real-time learning models
```

### 3. Start Backend Server
```bash
# Start FastAPI backend
cd backend
uv run python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Backend will be available at:
# http://localhost:8000
# API Documentation: http://localhost:8000/docs
```

### 4. Start Frontend
```bash
# Start React Native frontend
cd frontend

# For web development
npm run web

# For mobile development (iOS)
npm run ios

# For mobile development (Android)
npm run android

# For Expo development
npx expo start
```

---

## 🧪 Testing the System

### 1. API Testing
```bash
# Test API endpoints
curl http://localhost:8000/health

# Test recommendations (requires authentication)
curl -X GET "http://localhost:8000/api/v1/recommendations/" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### 2. AI System Testing
```bash
# Test AI recommendation engine
cd ai-ml
uv run python -c "
from inference.recommendation_engine import AIRecommendationEngine
from app.core.database import get_db

# Test basic functionality
engine = AIRecommendationEngine(next(get_db()))
print('AI Engine initialized successfully!')
"
```

### 3. Frontend Testing
```bash
# Run frontend tests
cd frontend
npm test

# Run linting
npm run lint

# Run type checking
npm run type-check
```

---

## 📊 Monitoring & Logs

### 1. Backend Logs
```bash
# View backend logs
tail -f backend/logs/app.log

# View AI engine logs
tail -f ai-ml/logs/recommendation_engine.log
```

### 2. Database Monitoring
```bash
# Connect to database
psql -h localhost -U your_username -d course_recommendation

# Check recommendation logs
SELECT * FROM recommendation_logs ORDER BY created_at DESC LIMIT 10;

# Check user interactions
SELECT COUNT(*) FROM user_interactions;

# Check analytics schema (data warehouse)
SELECT COUNT(*) FROM analytics.user_learning_profile;
SELECT COUNT(*) FROM analytics.course_performance;
SELECT COUNT(*) FROM analytics.recommendation_analytics;

# Check user learning profiles
SELECT user_id, engagement_score, learning_velocity, preferred_categories 
FROM analytics.user_learning_profile 
ORDER BY engagement_score DESC LIMIT 5;
```

### 3. Performance Monitoring
```bash
# Monitor API performance
curl -w "@curl-format.txt" -o /dev/null -s "http://localhost:8000/api/v1/recommendations/"

# Check AI model performance
cd ai-ml
uv run python -c "
import json
with open('models/training_summary.json', 'r') as f:
    summary = json.load(f)
    print('Model Performance:', summary)
"
```

---

## 🔧 Configuration Options

### 1. AI Algorithm Configuration
```python
# In ai-ml/inference/recommendation_engine.py
ALGORITHM_CONFIG = {
    'neural_cf': {
        'embedding_dim': 64,
        'hidden_layers': [128, 64, 32],
        'learning_rate': 0.001,
        'epochs': 100
    },
    'semantic': {
        'model_name': 'all-MiniLM-L6-v2',
        'similarity_threshold': 0.7,
        'max_features': 1000
    },
    'context_aware': {
        'timeout_seconds': 300,
        'context_weights': {
            'learning_session': 0.3,
            'user_mood': 0.2,
            'learning_goal': 0.3,
            'device_type': 0.2
        }
    }
}
```

### 2. Database Configuration
```python
# In backend/app/core/config.py
DATABASE_CONFIG = {
    'pool_size': 10,
    'max_overflow': 20,
    'pool_timeout': 30,
    'pool_recycle': 3600
}
```

### 3. Frontend Configuration
```typescript
// In frontend/src/config/api.ts
export const API_CONFIG = {
  baseURL: 'http://localhost:8000',
  timeout: 300000, // 5 minutes for AI recommendations
  retryAttempts: 3,
  retryDelay: 1000
};
```

---

## 🐛 Troubleshooting

### Common Issues

#### 1. Database Connection Issues
```bash
# Check PostgreSQL status
sudo systemctl status postgresql

# Check database connectivity
psql -h localhost -U your_username -d course_recommendation -c "SELECT 1;"

# Reset database (if needed)
dropdb course_recommendation
createdb course_recommendation
```

#### 2. AI Model Issues
```bash
# Reinstall AI dependencies
cd ai-ml
uv sync --reinstall

# Retrain models
uv run python training/train_models.py --force-retrain

# Check model files
ls -la models/
```

#### 2.1. Analytics Data Issues
```bash
# If AI recommendations are not working, update analytics data
cd backend
uv run python scripts/update_analytics.py

# Check analytics tables
psql -h localhost -U your_username -d course_recommendation -c "
SELECT COUNT(*) FROM analytics.user_learning_profile;
SELECT COUNT(*) FROM analytics.course_performance;
SELECT COUNT(*) FROM analytics.recommendation_analytics;
"
```

#### 3. Frontend Issues
```bash
# Clear npm cache
cd frontend
npm cache clean --force

# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install

# Clear Expo cache
npx expo r -c
```

#### 4. Port Conflicts
```bash
# Check port usage
lsof -i :8000  # Backend port
lsof -i :3000  # Frontend port
lsof -i :5432  # Database port

# Kill processes if needed
kill -9 <PID>
```

### Performance Issues

#### 1. Slow AI Recommendations
```bash
# Check AI model performance
cd ai-ml
uv run python -c "
import time
from inference.recommendation_engine import AIRecommendationEngine
from app.core.database import get_db

start_time = time.time()
engine = AIRecommendationEngine(next(get_db()))
print(f'AI Engine initialization: {time.time() - start_time:.2f}s')
"
```

#### 2. Database Performance
```sql
-- Check slow queries
SELECT query, mean_time, calls 
FROM pg_stat_statements 
ORDER BY mean_time DESC 
LIMIT 10;

-- Check database size
SELECT pg_size_pretty(pg_database_size('course_recommendation'));
```

---

## 📈 Production Deployment

### 1. Environment Setup
```bash
# Production environment variables
export ENVIRONMENT=production
export DEBUG=false
export LOG_LEVEL=INFO
export DATABASE_URL=postgresql://user:pass@host:port/db
```

### 2. Database Optimization
```sql
-- Create indexes for performance
CREATE INDEX CONCURRENTLY idx_user_interactions_user_id ON user_interactions(user_id);
CREATE INDEX CONCURRENTLY idx_user_interactions_course_id ON user_interactions(course_id);
CREATE INDEX CONCURRENTLY idx_enrollments_user_id ON enrollments(user_id);
CREATE INDEX CONCURRENTLY idx_courses_rating ON courses(rating);
CREATE INDEX CONCURRENTLY idx_courses_enrollment_count ON courses(enrollment_count);
```

### 3. AI Model Optimization
```bash
# Optimize AI models for production
cd ai-ml
uv run python training/optimize_models.py --production

# This will:
# - Reduce model size
# - Optimize inference speed
# - Enable batch processing
```

### 4. Monitoring Setup
```bash
# Install monitoring tools
pip install prometheus-client
pip install grafana-api

# Start monitoring
uv run python monitoring/metrics_collector.py
```

---

## 🔄 Development Workflow

### 1. Making Changes
```bash
# Create feature branch
git checkout -b feature/new-algorithm

# Make changes
# ... edit files ...

# Test changes
npm test
uv run pytest

# Commit changes
git add .
git commit -m "Add new recommendation algorithm"

# Push changes
git push origin feature/new-algorithm
```

### 2. AI Model Updates
```bash
# Update AI models
cd ai-ml
uv run python training/train_models.py --incremental

# Update analytics data (if new user interactions exist)
cd ../backend
uv run python scripts/update_analytics.py

# Test new models
cd ../ai-ml
uv run python -c "
from inference.recommendation_engine import AIRecommendationEngine
# Test new model functionality
"

# Deploy models
uv run python deployment/deploy_models.py
```

### 3. Database Migrations
```bash
# Create new migration
cd backend
uv run alembic revision --autogenerate -m "Add new table"

# Apply migration
uv run alembic upgrade head

# Rollback if needed
uv run alembic downgrade -1
```

---

## 📚 Additional Resources

### Documentation
- [API Documentation](http://localhost:8000/docs) - Interactive API docs
- [Recommendation Systems Guide](docs/recommendation_systems.md) - Detailed algorithm documentation
- [Database Schema](docs/database/) - Database structure and relationships

### Support
- **Issues**: [GitHub Issues](https://github.com/emrecanoner/smart-course-recommendation-system/issues)
- **Discussions**: [GitHub Discussions](https://github.com/emrecanoner/smart-course-recommendation-system/discussions)
- **Wiki**: [Project Wiki](https://github.com/emrecanoner/smart-course-recommendation-system/wiki)

---

## 🎉 Success!

If you've followed all the steps above, you should now have a fully functional Smart Course Recommendation System running with:

- ✅ **Backend API** running on http://localhost:8000
- ✅ **Frontend** running on http://localhost:3000 (web) or Expo
- ✅ **Database** with proper schema and sample data
- ✅ **AI Models** trained and ready for recommendations
- ✅ **7 Advanced Algorithms** available for testing

**Next Steps:**
1. Test the recommendation system with different algorithms
2. Explore the API documentation at http://localhost:8000/docs
3. Check out the [Recommendation Systems Guide](docs/recommendation_systems.md) for algorithm details
4. Start developing new features or customizing the system

Happy coding! 🚀
