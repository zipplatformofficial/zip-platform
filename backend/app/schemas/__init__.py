"""Pydantic schemas for request/response validation"""
from app.schemas.user import (
    UserCreate,
    UserUpdate,
    UserResponse,
    UserLogin,
    UserInDB,
)
from app.schemas.auth import (
    Token,
    TokenData,
    RefreshToken,
    PasswordReset,
    PasswordResetConfirm,
)
from app.schemas.maintenance import (
    MaintenanceServiceCreate,
    MaintenanceServiceUpdate,
    MaintenanceServiceResponse,
    ServiceBookingCreate,
    ServiceBookingUpdate,
    ServiceBookingResponse,
    TechnicianResponse,
)
from app.schemas.rental import (
    RentalVehicleCreate,
    RentalVehicleUpdate,
    RentalVehicleResponse,
    RentalBookingCreate,
    RentalBookingUpdate,
    RentalBookingResponse,
)
from app.schemas.store import (
    ProductCreate,
    ProductUpdate,
    ProductResponse,
    VendorCreate,
    VendorUpdate,
    VendorResponse,
    CartResponse,
    OrderCreate,
    OrderResponse,
    ProductReviewCreate,
    ProductReviewResponse,
)

__all__ = [
    # User & Auth
    "UserCreate",
    "UserUpdate",
    "UserResponse",
    "UserLogin",
    "UserInDB",
    "Token",
    "TokenData",
    "RefreshToken",
    "PasswordReset",
    "PasswordResetConfirm",
    # Maintenance
    "MaintenanceServiceCreate",
    "MaintenanceServiceUpdate",
    "MaintenanceServiceResponse",
    "ServiceBookingCreate",
    "ServiceBookingUpdate",
    "ServiceBookingResponse",
    "TechnicianResponse",
    # Rentals
    "RentalVehicleCreate",
    "RentalVehicleUpdate",
    "RentalVehicleResponse",
    "RentalBookingCreate",
    "RentalBookingUpdate",
    "RentalBookingResponse",
    # Store
    "ProductCreate",
    "ProductUpdate",
    "ProductResponse",
    "VendorCreate",
    "VendorUpdate",
    "VendorResponse",
    "CartResponse",
    "OrderCreate",
    "OrderResponse",
    "ProductReviewCreate",
    "ProductReviewResponse",
]
