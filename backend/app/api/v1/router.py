"""API v1 router - combines all endpoint routers"""
from fastapi import APIRouter
from app.api.v1.endpoints import auth, users

# Create main API router
api_router = APIRouter()

# Include authentication routes
api_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["Authentication"]
)

# Include user routes
api_router.include_router(
    users.router,
    prefix="/users",
    tags=["Users"]
)

# Add more routers as we build them
# api_router.include_router(maintenance.router, prefix="/maintenance", tags=["Maintenance"])
# api_router.include_router(rentals.router, prefix="/rentals", tags=["Rentals"])
# api_router.include_router(store.router, prefix="/store", tags=["Store"])
