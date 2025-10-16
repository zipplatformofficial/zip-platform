# ZIP Platform Backend - Setup Guide

## What We've Built So Far

### ✅ Phase 1: Foundation (COMPLETED)

#### 1. Project Structure
```
backend/
├── app/
│   ├── core/               # Core configurations
│   │   ├── config.py       # Settings & environment variables
│   │   ├── database.py     # Database connection
│   │   └── security.py     # Password hashing & JWT tokens
│   ├── models/             # Database models (SQLAlchemy)
│   │   ├── user.py         # User, roles, authentication
│   │   ├── vehicle.py      # Customer vehicles
│   │   ├── maintenance.py  # Mobile car maintenance module
│   │   ├── rental.py       # Car rental module
│   │   ├── store.py        # Online auto store module
│   │   ├── payment.py      # Payment transactions
│   │   └── notification.py # User notifications
│   ├── main.py             # FastAPI application
│   └── __init__.py
├── alembic/                # Database migrations
├── netlify/functions/      # Serverless function handlers
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variables template
└── netlify.toml            # Netlify configuration
```

#### 2. Database Models Created

**User Management:**
- Users (with roles: admin, customer, technician, vendor, etc.)
- User types (individual, corporate, ride-hailing driver)
- KYC verification fields
- Loyalty points and referral system

**Module 1: Mobile Car Maintenance**
- MaintenanceService (service catalog)
- Technician (profiles, availability, performance metrics)
- ServiceBooking (booking lifecycle, tracking)
- TechnicianService (technician-specific services)

**Module 2: Car Rentals**
- RentalVehicle (fleet vehicles with tracking)
- RentalBooking (rental lifecycle, pricing)
- VehicleInspection (pickup/return inspections)
- FleetSubscription (corporate fleet management)

**Module 3: Online Auto Store**
- Vendor (seller profiles and verification)
- Product (parts catalog with compatibility)
- Cart & CartItem (shopping cart)
- Order & OrderItem (order management)
- ProductReview (ratings and reviews)

**Supporting Models:**
- Payment (multi-method payment processing)
- Notification (push, SMS, email notifications)
- Vehicle (customer vehicles)

#### 3. Core Features Implemented

- **Security**: Password hashing with bcrypt, JWT token generation
- **Configuration**: Environment-based settings with Pydantic
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Migrations**: Alembic for database schema management
- **Serverless**: Netlify Functions integration with Mangum

## Next Steps: Building the APIs

### Phase 2: Authentication & User Management
- [ ] User registration and login endpoints
- [ ] JWT authentication middleware
- [ ] Role-based access control (RBAC)
- [ ] User profile management
- [ ] Password reset functionality

### Phase 3: CRUD APIs for Each Module
- [ ] Mobile Maintenance API endpoints
- [ ] Car Rentals API endpoints
- [ ] Online Store API endpoints
- [ ] Admin Panel comprehensive CRUD

### Phase 4: Business Logic & Integrations
- [ ] Payment gateway integrations (MTN, Vodafone, AirtelTigo)
- [ ] SMS & Email notifications
- [ ] Real-time tracking
- [ ] File upload handling

## Quick Start

### 1. Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 2. Set Up Environment
```bash
cp .env.example .env
# Edit .env with your database and API keys
```

### 3. Create Database
```bash
# Using PostgreSQL
createdb zip_platform

# Or using psql
psql -U postgres
CREATE DATABASE zip_platform;
\q
```

### 4. Run Migrations
```bash
# Initialize Alembic (first time only)
alembic revision --autogenerate -m "Initial migration"

# Apply migrations
alembic upgrade head
```

### 5. Run Development Server
```bash
uvicorn app.main:app --reload --port 8000
```

Visit http://localhost:8000/docs for API documentation

### 6. Test with Netlify Dev (Optional)
```bash
netlify dev
```

## Database Schema Overview

### Key Relationships
- User → Vehicles (one-to-many)
- User → ServiceBookings (one-to-many)
- User → RentalBookings (one-to-many)
- User → Orders (one-to-many)
- User → Payments (one-to-many)
- Technician → ServiceBookings (one-to-many)
- RentalVehicle → RentalBookings (one-to-many)
- Vendor → Products (one-to-many)
- Vendor → Orders (one-to-many)
- Product → OrderItems (one-to-many)
- Product → ProductReviews (one-to-many)

## Environment Variables Required

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/zip_platform

# Security
SECRET_KEY=your-super-secret-key-here

# Payment Gateways
MTN_MOMO_API_KEY=your-key
VODAFONE_CASH_API_KEY=your-key
AIRTELTIGO_MONEY_API_KEY=your-key

# SMS & Email
SMS_API_KEY=your-key
SMTP_USER=your-email
SMTP_PASSWORD=your-password

# Maps
GOOGLE_MAPS_API_KEY=your-key
```

## API Endpoints Structure (Coming Next)

```
/api/v1/
├── auth/
│   ├── POST /register
│   ├── POST /login
│   ├── POST /refresh
│   └── POST /logout
├── users/
│   ├── GET /me
│   ├── PUT /me
│   └── POST /vehicles
├── maintenance/
│   ├── GET /services
│   ├── POST /bookings
│   ├── GET /bookings/{id}
│   └── PUT /bookings/{id}/status
├── rentals/
│   ├── GET /vehicles
│   ├── POST /bookings
│   ├── GET /bookings/{id}
│   └── POST /inspections
├── store/
│   ├── GET /products
│   ├── POST /cart
│   ├── POST /orders
│   └── POST /reviews
└── admin/
    ├── /users (full CRUD)
    ├── /services (full CRUD)
    ├── /vehicles (full CRUD)
    ├── /products (full CRUD)
    └── /bookings (full CRUD)
```

## Testing

```bash
# Run tests (once we create them)
pytest

# Run with coverage
pytest --cov=app
```

## Deployment to Netlify

1. Connect repository to Netlify
2. Set environment variables in Netlify dashboard
3. Deploy automatically on push to main

## Support

For issues or questions, refer to the functional requirements document or technical design document in the `docs/` folder.
