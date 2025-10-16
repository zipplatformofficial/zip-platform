# ZIP Platform API Documentation

## Overview
This document covers the authentication and user management APIs that have been implemented.

## Base URL
- Development: `http://localhost:8000`
- API Version 1: `http://localhost:8000/api/v1`

## Authentication Flow

### 1. Register a New User
**Endpoint:** `POST /api/v1/auth/register`

**Request Body:**
```json
{
  "email": "user@example.com",
  "phone": "0241234567",
  "password": "SecurePass123",
  "full_name": "John Doe",
  "user_type": "individual",
  "location": {
    "lat": 5.6037,
    "lng": -0.1870,
    "address": "Accra, Ghana"
  }
}
```

**Password Requirements:**
- Minimum 8 characters
- At least 1 uppercase letter
- At least 1 digit

**Phone Number Format:**
- Ghana phone numbers only
- Accepts formats: `0241234567` or `233241234567`
- Automatically normalized to international format

**Response (201 Created):**
```json
{
  "id": "uuid",
  "email": "user@example.com",
  "phone": "233241234567",
  "full_name": "John Doe",
  "role": "customer",
  "user_type": "individual",
  "is_active": true,
  "is_verified": false,
  "email_verified": false,
  "phone_verified": false,
  "referral_code": "ZIPABCD1234",
  "loyalty_points": 0,
  "average_rating": 0.0,
  "total_ratings": 0,
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00"
}
```

### 2. Login
**Endpoint:** `POST /api/v1/auth/login`

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePass123"
}
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Token Expiration:**
- Access Token: 30 minutes
- Refresh Token: 7 days

### 3. Refresh Access Token
**Endpoint:** `POST /api/v1/auth/refresh`

**Request Body:**
```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 4. Logout
**Endpoint:** `POST /api/v1/auth/logout`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "message": "Successfully logged out"
}
```

## User Management APIs (Protected)

All user management endpoints require authentication via Bearer token in the Authorization header.

### 1. Get Current User Profile
**Endpoint:** `GET /api/v1/users/me`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "id": "uuid",
  "email": "user@example.com",
  "phone": "233241234567",
  "full_name": "John Doe",
  "role": "customer",
  "user_type": "individual",
  "is_active": true,
  "profile_photo": null,
  "location": {
    "lat": 5.6037,
    "lng": -0.1870,
    "address": "Accra, Ghana"
  },
  "loyalty_points": 0,
  "referral_code": "ZIPABCD1234"
}
```

### 2. Update User Profile
**Endpoint:** `PUT /api/v1/users/me`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body (all fields optional):**
```json
{
  "full_name": "John Doe Updated",
  "phone": "0241234568",
  "profile_photo": "https://example.com/photo.jpg",
  "location": {
    "lat": 5.6037,
    "lng": -0.1870,
    "address": "New Address, Accra"
  },
  "notification_preferences": {
    "email": true,
    "sms": true,
    "push": true
  },
  "language_preference": "en"
}
```

**Response (200 OK):** Updated user object

### 3. Change Password
**Endpoint:** `POST /api/v1/users/me/change-password`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "current_password": "OldPassword123",
  "new_password": "NewPassword123"
}
```

**Response (200 OK):**
```json
{
  "message": "Password changed successfully"
}
```

### 4. Get User Statistics
**Endpoint:** `GET /api/v1/users/me/stats`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "user_id": "uuid",
  "full_name": "John Doe",
  "email": "user@example.com",
  "loyalty_points": 150,
  "average_rating": 4.5,
  "total_ratings": 10,
  "referral_code": "ZIPABCD1234",
  "statistics": {
    "service_bookings": 5,
    "rental_bookings": 3,
    "orders": 7,
    "total_activities": 15
  }
}
```

### 5. Deactivate Account
**Endpoint:** `DELETE /api/v1/users/me`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "message": "Account deactivated successfully"
}
```

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Email already registered"
}
```

### 401 Unauthorized
```json
{
  "detail": "Could not validate credentials"
}
```

### 403 Forbidden
```json
{
  "detail": "Account is inactive"
}
```

### 422 Validation Error
```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "value is not a valid email address",
      "type": "value_error.email"
    }
  ]
}
```

## User Roles
- `customer` - Default role for regular users
- `technician` - Mobile car service technicians
- `vendor` - Auto parts store vendors
- `rental_manager` - Car rental fleet managers
- `operations_manager` - Platform operations staff
- `customer_support` - Customer support staff
- `admin` - Full platform access

## User Types
- `individual` - Individual users
- `corporate` - Corporate/business accounts
- `ride_hailing_driver` - Ride-hailing drivers

## Interactive API Documentation

FastAPI provides automatic interactive documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

These interfaces allow you to test all endpoints directly from your browser.

## Testing the API

### Using the Test Script
```bash
cd backend
python test_api.py
```

### Using cURL

**Register:**
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "phone": "0241234567",
    "password": "SecurePass123",
    "full_name": "Test User"
  }'
```

**Login:**
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "SecurePass123"
  }'
```

**Get Profile:**
```bash
curl -X GET http://localhost:8000/api/v1/users/me \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Next Steps

The following API modules will be implemented next:
1. Mobile Car Maintenance APIs
2. Car Rentals APIs
3. Online Auto Store APIs
4. Admin Panel APIs
5. Payment Integration APIs
6. Notification APIs
