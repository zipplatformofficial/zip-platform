"""API v1 router - combines all endpoint routers"""
from fastapi import APIRouter
from app.api.v1.endpoints import auth, users, maintenance, rentals, store, admin

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

# Include mobile car maintenance routes
api_router.include_router(
    maintenance.router,
    prefix="/maintenance",
    tags=["Mobile Maintenance"]
)

# Include car rentals routes
api_router.include_router(
    rentals.router,
    prefix="/rentals",
    tags=["Car Rentals"]
)

# Include online store routes
api_router.include_router(
    store.router,
    prefix="/store",
    tags=["Online Auto Store"]
)

# Include admin routes
api_router.include_router(
    admin.router,
    prefix="/admin",
    tags=["Admin Panel"]
)
