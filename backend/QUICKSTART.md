# ZIP Platform Backend - Quick Start Guide

## What We've Just Built

**Phase 2: Authentication & User Management (✅ COMPLETED)**

We've successfully implemented:
- ✅ User registration with email/phone validation
- ✅ Login with JWT token authentication
- ✅ Token refresh mechanism
- ✅ Protected user profile endpoints
- ✅ Password change functionality
- ✅ User statistics endpoint
- ✅ Role-based access control (RBAC) infrastructure

## Prerequisites

- Python 3.11+
- PostgreSQL database
- pip (Python package manager)

## Setup Instructions

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Set Up Database

**Option A: Using PostgreSQL CLI**
```bash
# Create database
createdb zip_platform

# Or using psql
psql -U postgres
CREATE DATABASE zip_platform;
\q
```

**Option B: Update .env file**
The `.env` file already exists. Update the DATABASE_URL if needed:
```env
DATABASE_URL=postgresql://your_username:your_password@localhost:5432/zip_platform
```

### 3. Run Database Migrations

```bash
# Initialize Alembic (first time only)
alembic revision --autogenerate -m "Initial migration with auth"

# Apply migrations
alembic upgrade head
```

### 4. Start the Development Server

```bash
# Start with uvicorn
uvicorn app.main:app --reload --port 8000

# Or with Netlify Dev (for serverless testing)
netlify dev
```

### 5. Verify Installation

Open your browser and visit:
- API Root: http://localhost:8000/
- Health Check: http://localhost:8000/health
- Interactive API Docs: http://localhost:8000/docs
- Alternative Docs: http://localhost:8000/redoc

You should see the API documentation with all authentication and user endpoints.

## Testing the API

### Method 1: Using the Test Script

```bash
python test_api.py
```

This script will:
1. Test health check
2. Register a new user
3. Login and get JWT tokens
4. Access protected endpoints
5. Update user profile
6. Get user statistics
7. Refresh access token

### Method 2: Using the Interactive Docs

1. Go to http://localhost:8000/docs
2. Try the `/api/v1/auth/register` endpoint to create a user
3. Use `/api/v1/auth/login` to get your tokens
4. Click "Authorize" button at the top and paste your access token
5. Test all the protected endpoints

### Method 3: Using cURL or Postman

See `API_DOCUMENTATION.md` for detailed cURL examples.

## Quick Test Example

### 1. Register a User
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@zipghana.com",
    "phone": "0241234567",
    "password": "TestPass123",
    "full_name": "Test User",
    "user_type": "individual"
  }'
```

### 2. Login
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@zipghana.com",
    "password": "TestPass123"
  }'
```

Copy the `access_token` from the response.

### 3. Get Your Profile
```bash
curl -X GET http://localhost:8000/api/v1/users/me \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN_HERE"
```

## Project Structure (Updated)

```
backend/
├── app/
│   ├── api/                    # ✅ NEW: API endpoints
│   │   └── v1/
│   │       ├── endpoints/
│   │       │   ├── auth.py     # ✅ Authentication endpoints
│   │       │   └── users.py    # ✅ User management endpoints
│   │       ├── deps.py         # ✅ JWT dependencies & RBAC
│   │       └── router.py       # ✅ Main API router
│   ├── core/                   # Core functionality
│   │   ├── config.py
│   │   ├── database.py
│   │   └── security.py
│   ├── models/                 # Database models
│   │   ├── user.py
│   │   ├── vehicle.py
│   │   ├── maintenance.py
│   │   ├── rental.py
│   │   ├── store.py
│   │   ├── payment.py
│   │   └── notification.py
│   ├── schemas/                # ✅ NEW: Pydantic schemas
│   │   ├── auth.py             # ✅ Auth request/response schemas
│   │   └── user.py             # ✅ User request/response schemas
│   └── main.py                 # ✅ Updated with API router
├── alembic/                    # Database migrations
├── netlify/functions/          # Serverless deployment
├── test_api.py                 # ✅ NEW: API test script
├── API_DOCUMENTATION.md        # ✅ NEW: Complete API docs
├── requirements.txt            # ✅ Updated dependencies
└── .env                        # Environment variables
```

## Available API Endpoints

### Public Endpoints (No Authentication Required)
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login user
- `POST /api/v1/auth/refresh` - Refresh access token
- `POST /api/v1/auth/logout` - Logout user

### Protected Endpoints (Requires Authentication)
- `GET /api/v1/users/me` - Get current user profile
- `PUT /api/v1/users/me` - Update user profile
- `POST /api/v1/users/me/change-password` - Change password
- `GET /api/v1/users/me/stats` - Get user statistics
- `DELETE /api/v1/users/me` - Deactivate account

## Environment Variables

Key variables in your `.env` file:

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/zip_platform

# Security (IMPORTANT: Change SECRET_KEY in production!)
SECRET_KEY=your-secret-key-here-change-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Application
DEBUG=True
ENVIRONMENT=development
```

## Common Issues & Solutions

### Issue: "Database does not exist"
**Solution:** Create the database first:
```bash
createdb zip_platform
```

### Issue: "Module not found" errors
**Solution:** Install dependencies:
```bash
pip install -r requirements.txt
```

### Issue: "Alembic can't find models"
**Solution:** Make sure all models are imported in `app/main.py`

### Issue: "Token validation failed"
**Solution:** Make sure you're using the Bearer token format:
```
Authorization: Bearer YOUR_TOKEN_HERE
```

## Next Development Steps

With authentication complete, we can now build:

1. **Mobile Car Maintenance Module**
   - Service listing endpoints
   - Booking creation and management
   - Technician assignment
   - Real-time tracking

2. **Car Rentals Module**
   - Vehicle fleet management
   - Rental booking system
   - Vehicle inspection endpoints
   - Corporate subscriptions

3. **Online Auto Store Module**
   - Product catalog
   - Shopping cart
   - Order processing
   - Vendor management

4. **Admin Panel**
   - Full CRUD for all entities
   - Analytics and reporting
   - User management

5. **Integrations**
   - Mobile Money payments (MTN, Vodafone, AirtelTigo)
   - SMS notifications
   - Email notifications
   - Google Maps integration

## Need Help?

- Read the full API documentation: `API_DOCUMENTATION.md`
- Check the setup guide: `SETUP.md`
- View interactive docs: http://localhost:8000/docs

## Production Deployment

When ready to deploy to Netlify:

1. Push code to GitHub
2. Connect repository to Netlify
3. Set environment variables in Netlify dashboard
4. Deploy automatically on push to main branch

The app is already configured for serverless deployment with the `netlify/functions/api.py` handler.
