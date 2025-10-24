"""Main FastAPI application"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import engine, Base

# Import all models to ensure they are registered with SQLAlchemy
from app.models import (
    User, Vehicle, MaintenanceService, ServiceBooking, Technician,
    RentalVehicle, RentalBooking, VehicleInspection, FleetSubscription,
    Product, Vendor, Order, OrderItem, ProductReview, Cart, CartItem,
    Payment, Notification, RoleApplication
)

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="ZIP Automobile Service Platform API",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_cors_origins(),
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600,
)


@app.on_event("startup")
async def startup_event():
    """Run on application startup"""
    # Create database tables (commented out - use Alembic migrations in production)
    try:
        Base.metadata.create_all(bind=engine)
        print("[OK] Database tables created")
    except Exception as e:
        print(f"[WARNING] Database tables may already exist: {str(e)}")
    print(f"[OK] {settings.APP_NAME} API started")


@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown"""
    print(f"[BYE] {settings.APP_NAME} API shutting down")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "docs": "/docs",
        "environment": settings.ENVIRONMENT
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION
    }


# Import and include API routers
from app.api.v1.router import api_router
app.include_router(api_router, prefix=settings.API_V1_PREFIX)
