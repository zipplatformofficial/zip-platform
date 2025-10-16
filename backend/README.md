# ZIP Automobile Service Platform - Backend

## Overview
Backend API for ZIP Platform built with FastAPI, PostgreSQL, and deployed as Netlify serverless functions.

## Tech Stack
- **Framework**: FastAPI
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: JWT
- **Deployment**: Netlify Serverless Functions
- **Python Version**: 3.11+

## Project Structure
```
backend/
├── app/
│   ├── api/                    # API endpoints
│   │   ├── v1/
│   │   │   ├── endpoints/      # Route handlers
│   │   │   └── deps.py         # Dependencies
│   │   └── router.py
│   ├── core/                   # Core functionality
│   │   ├── config.py           # Configuration
│   │   ├── security.py         # Auth & security
│   │   └── database.py         # Database connection
│   ├── models/                 # SQLAlchemy models
│   ├── schemas/                # Pydantic schemas
│   ├── services/               # Business logic
│   ├── utils/                  # Utilities
│   └── main.py                 # Application entry point
├── alembic/                    # Database migrations
├── netlify/
│   └── functions/
│       └── api.py              # Serverless function handler
├── tests/                      # Unit and integration tests
├── requirements.txt
├── netlify.toml
└── .env.example
```

## Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Up Environment Variables
```bash
cp .env.example .env
# Edit .env with your configurations
```

### 3. Initialize Database
```bash
# Create database
createdb zip_platform

# Run migrations
alembic upgrade head
```

### 4. Run Development Server
```bash
uvicorn app.main:app --reload --port 8000
```

### 5. Run with Netlify Dev
```bash
netlify dev
```

## API Documentation
Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Database Migrations
```bash
# Create new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

## Testing
```bash
pytest
```

## Deployment
Deploys automatically to Netlify when pushing to main branch.

## Modules
1. **Mobile Car Maintenance** - Service booking and technician management
2. **Car Rentals** - Vehicle rental and fleet management
3. **Online Auto Store** - Parts marketplace and vendor management
4. **Admin Panel** - Full CRUD for all entities

## License
Proprietary - ZIP Ghana
