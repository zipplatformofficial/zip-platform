"""API v1 router - combines all endpoint routers"""
from fastapi import APIRouter
from app.api.v1.endpoints import auth, users, maintenance, rentals, store, admin, payments, uploads, notifications, technicians, vendors, tracking, applications

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

# Include payment routes
api_router.include_router(
    payments.router,
    prefix="/payments",
    tags=["Payments"]
)

# Include upload routes
api_router.include_router(
    uploads.router,
    prefix="/uploads",
    tags=["File Uploads"]
)

# Include notification routes
api_router.include_router(
    notifications.router,
    prefix="/notifications",
    tags=["Notifications"]
)

# Include technician routes
api_router.include_router(
    technicians.router,
    prefix="/technicians",
    tags=["Technician Portal"]
)

# Include vendor routes
api_router.include_router(
    vendors.router,
    prefix="/vendors",
    tags=["Vendor Portal"]
)

# Include tracking routes
api_router.include_router(
    tracking.router,
    prefix="/tracking",
    tags=["Real-time Tracking"]
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

# Include role application routes
api_router.include_router(
    applications.router,
    prefix="/applications",
    tags=["Role Applications"]
)
