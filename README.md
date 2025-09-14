# Smart Course Recommendation System

An AI-powered course recommendation system that helps users discover relevant courses based on their preferences, learning history, and behavior patterns.

## 🚀 Features

- **AI-Powered Recommendations**: Advanced machine learning algorithms for personalized course suggestions
- **User Management**: Complete user registration, authentication, and profile management
- **Course Catalog**: Comprehensive course management with categories and search functionality
- **Real-time Analytics**: Track user behavior and improve recommendations over time
- **Modern Tech Stack**: Built with FastAPI, React Native, and PostgreSQL

## 🏗️ Architecture

- **Frontend**: React Native (mobile-first web application)
- **Backend**: Python FastAPI with high-performance async support
- **Database**: PostgreSQL with Docker containerization
- **AI/ML**: Python-based recommendation algorithms
- **Caching**: Redis for session management and performance optimization

## 📋 Prerequisites

- Docker and Docker Compose
- Python 3.11+
- Node.js 18+ (for frontend development)
- Git

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone <repository-url>
cd smart-course-recommendation-system
```

### 2. Start the Development Environment

```bash
# Start all services (database, backend, frontend)
docker-compose up -d

# Or start specific services
docker-compose up -d postgres redis
```

### 3. Set Up Backend

```bash
cd backend

# Install dependencies with uv
uv pip install -e .

# Run database migrations
alembic upgrade head

# Start the backend server
uvicorn app.main:app --reload
```

### 4. Set Up Frontend

```bash
cd frontend

# Install dependencies
npm install

# Start the development server
npm start
```

## 📁 Project Structure

```
smart-course-recommendation-system/
├── backend/                 # Python FastAPI backend
│   ├── app/
│   │   ├── api/            # API endpoints
│   │   ├── core/           # Core configuration
│   │   ├── models/         # Database models
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── services/       # Business logic
│   │   └── utils/          # Utility functions
│   ├── pyproject.toml      # Python dependencies
│   └── Dockerfile          # Backend container
├── frontend/               # React Native frontend
│   ├── src/
│   │   ├── components/     # Reusable components
│   │   ├── screens/        # Screen components
│   │   ├── navigation/     # Navigation setup
│   │   ├── services/       # API services
│   │   └── store/          # State management
│   └── package.json        # Node dependencies
├── database/               # Database scripts
│   ├── migrations/         # Database migrations
│   └── seeds/              # Sample data
├── ai-ml/                  # AI/ML components
│   ├── models/             # Trained models
│   ├── training/           # Model training scripts
│   └── inference/          # Recommendation inference
└── docs/                   # Documentation
```

## 🔧 Development

### Backend Development

```bash
cd backend

# Install development dependencies
uv pip install -e ".[dev]"

# Run tests
pytest

# Format code
black .
isort .

# Lint code
flake8 .
```

### Frontend Development

```bash
cd frontend

# Install dependencies
npm install

# Run tests
npm test

# Lint code
npm run lint

# Format code
npm run format
```

## 🗄️ Database

The system uses PostgreSQL with the following core tables:

- **users**: User information and preferences
- **courses**: Course catalog and metadata
- **categories**: Course categories and tags
- **user_interactions**: Track user behavior
- **recommendations**: Store generated recommendations

## 🤖 AI/ML Features

- **Collaborative Filtering**: User-based and item-based recommendations
- **Content-Based Filtering**: Course similarity based on features
- **Hybrid Approach**: Combines multiple recommendation strategies
- **Real-time Updates**: Dynamic recommendation generation
- **A/B Testing**: Framework for testing recommendation algorithms

## 📊 API Documentation

Once the backend is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test

# Integration tests
docker-compose -f docker-compose.test.yml up --abort-on-container-exit
```

## 🚀 Deployment

### Production Build

```bash
# Build production images
docker-compose -f docker-compose.prod.yml build

# Deploy to production
docker-compose -f docker-compose.prod.yml up -d
```

### Environment Variables

Create a `.env` file with the following variables:

```env
# Database
POSTGRES_SERVER=localhost
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password
POSTGRES_DB=course_recommendation
POSTGRES_PORT=5432

# Security
SECRET_KEY=your_secret_key

# Redis
REDIS_URL=redis://localhost:6379

# API
API_V1_STR=/api/v1
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

If you encounter any issues or have questions:

1. Check the [documentation](docs/)
2. Search existing [issues](https://github.com/your-repo/issues)
3. Create a new issue with detailed information

## 🗺️ Roadmap

- [ ] Advanced ML models (deep learning)
- [ ] Real-time recommendation updates
- [ ] Mobile app deployment
- [ ] Analytics dashboard
- [ ] Multi-language support
- [ ] Social features (reviews, ratings)
- [ ] Integration with external course platforms
