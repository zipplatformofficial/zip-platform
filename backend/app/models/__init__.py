"""Database models"""
from app.models.user import User, UserRole, UserType
from app.models.vehicle import Vehicle, VehicleType
from app.models.maintenance import (
    MaintenanceService,
    MaintenanceServiceType,
    ServiceBooking,
    ServiceBookingStatus,
    Technician,
    TechnicianService
)
from app.models.rental import (
    RentalVehicle,
    RentalBooking,
    RentalBookingStatus,
    VehicleInspection,
    FleetSubscription
)
from app.models.store import (
    Product,
    ProductCategory,
    Vendor,
    Order,
    OrderItem,
    OrderStatus,
    ProductReview,
    Cart,
    CartItem
)
from app.models.payment import Payment, PaymentStatus, PaymentMethod
from app.models.notification import Notification, NotificationType
from app.models.application import RoleApplication, ApplicationStatus, ApplicationType
from app.models.fraud import FraudAlert, FraudType, FraudStatus
from app.models.analytics import AnalyticsEvent, DailyStats, EventType, VisitorType

__all__ = [
    "User",
    "UserRole",
    "UserType",
    "Vehicle",
    "VehicleType",
    "MaintenanceService",
    "MaintenanceServiceType",
    "ServiceBooking",
    "ServiceBookingStatus",
    "Technician",
    "TechnicianService",
    "RentalVehicle",
    "RentalBooking",
    "RentalBookingStatus",
    "VehicleInspection",
    "FleetSubscription",
    "Product",
    "ProductCategory",
    "Vendor",
    "Order",
    "OrderItem",
    "OrderStatus",
    "ProductReview",
    "Cart",
    "CartItem",
    "Payment",
    "PaymentStatus",
    "PaymentMethod",
    "Notification",
    "NotificationType",
    "RoleApplication",
    "ApplicationStatus",
    "ApplicationType",
    "FraudAlert",
    "FraudType",
    "FraudStatus",
    "AnalyticsEvent",
    "DailyStats",
    "EventType",
    "VisitorType",
]
