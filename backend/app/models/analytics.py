"""Analytics and visitor tracking models"""
import enum
from sqlalchemy import Column, String, Integer, ForeignKey, Enum, Text, JSON, Float, Boolean
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class EventType(str, enum.Enum):
    """Types of analytics events"""
    PAGE_VIEW = "page_view"
    USER_SIGNUP = "user_signup"
    USER_LOGIN = "user_login"
    USER_LOGOUT = "user_logout"
    SEARCH = "search"
    PRODUCT_VIEW = "product_view"
    VEHICLE_VIEW = "vehicle_view"
    SERVICE_VIEW = "service_view"
    ADD_TO_CART = "add_to_cart"
    REMOVE_FROM_CART = "remove_from_cart"
    CHECKOUT_START = "checkout_start"
    CHECKOUT_COMPLETE = "checkout_complete"
    BOOKING_CREATE = "booking_create"
    BOOKING_CANCEL = "booking_cancel"
    PAYMENT_INITIATE = "payment_initiate"
    PAYMENT_SUCCESS = "payment_success"
    PAYMENT_FAILED = "payment_failed"
    APPLICATION_SUBMIT = "application_submit"
    DOCUMENT_UPLOAD = "document_upload"
    REVIEW_SUBMIT = "review_submit"
    ERROR_OCCURRED = "error_occurred"


class VisitorType(str, enum.Enum):
    """Visitor classification"""
    NEW_VISITOR = "new_visitor"
    RETURNING_VISITOR = "returning_visitor"
    REGISTERED_USER = "registered_user"
    GUEST = "guest"


class AnalyticsEvent(BaseModel):
    """Analytics and user behavior tracking"""

    __tablename__ = "analytics_events"

    # User (if logged in)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    # Session
    session_id = Column(String(100), nullable=False, index=True)
    visitor_type = Column(Enum(VisitorType), nullable=False)

    # Event Details
    event_type = Column(Enum(EventType), nullable=False)
    event_name = Column(String(100), nullable=False)
    event_category = Column(String(50), nullable=True)  # maintenance, rentals, store, auth, etc.

    # Page Info
    page_url = Column(String(500), nullable=False)
    page_title = Column(String(255), nullable=True)
    referrer_url = Column(String(500), nullable=True)

    # Device & Browser
    device_type = Column(String(50), nullable=True)  # desktop, mobile, tablet
    browser = Column(String(100), nullable=True)
    operating_system = Column(String(100), nullable=True)
    screen_resolution = Column(String(50), nullable=True)

    # Location
    ip_address = Column(String(50), nullable=True)
    country = Column(String(100), nullable=True)
    city = Column(String(100), nullable=True)
    region = Column(String(100), nullable=True)

    # Search/Filter (if applicable)
    search_query = Column(String(255), nullable=True)
    filters_applied = Column(JSON, nullable=True)

    # Related Entity (if applicable)
    related_product_id = Column(Integer, nullable=True)
    related_vehicle_id = Column(Integer, nullable=True)
    related_service_id = Column(Integer, nullable=True)
    related_booking_id = Column(Integer, nullable=True)
    related_order_id = Column(Integer, nullable=True)

    # Duration & Engagement
    time_on_page = Column(Integer, nullable=True)  # seconds
    scroll_depth = Column(Float, nullable=True)  # percentage 0-100

    # Conversion Tracking
    is_conversion = Column(Boolean, default=False, nullable=False)
    conversion_value = Column(Float, nullable=True)

    # Error Tracking (if event_type is ERROR_OCCURRED)
    error_message = Column(Text, nullable=True)
    error_stack = Column(Text, nullable=True)

    # Custom Data
    custom_data = Column(JSON, nullable=True)

    # Relationships
    user = relationship("User", backref="analytics_events")

    def __repr__(self):
        return f"<AnalyticsEvent {self.event_type} - {self.event_name}>"


class DailyStats(BaseModel):
    """Daily aggregated statistics for dashboard"""

    __tablename__ = "daily_stats"

    # Date
    date = Column(String(20), nullable=False, unique=True, index=True)  # YYYY-MM-DD

    # Visitors
    total_visitors = Column(Integer, default=0, nullable=False)
    new_visitors = Column(Integer, default=0, nullable=False)
    returning_visitors = Column(Integer, default=0, nullable=False)
    unique_sessions = Column(Integer, default=0, nullable=False)

    # Users
    new_signups = Column(Integer, default=0, nullable=False)
    active_users = Column(Integer, default=0, nullable=False)

    # Revenue
    total_revenue = Column(Float, default=0.0, nullable=False)
    maintenance_revenue = Column(Float, default=0.0, nullable=False)
    rental_revenue = Column(Float, default=0.0, nullable=False)
    store_revenue = Column(Float, default=0.0, nullable=False)
    platform_commission = Column(Float, default=0.0, nullable=False)

    # Bookings & Orders
    service_bookings = Column(Integer, default=0, nullable=False)
    rental_bookings = Column(Integer, default=0, nullable=False)
    store_orders = Column(Integer, default=0, nullable=False)

    # Payments
    successful_payments = Column(Integer, default=0, nullable=False)
    failed_payments = Column(Integer, default=0, nullable=False)
    total_payment_amount = Column(Float, default=0.0, nullable=False)

    # Engagement
    avg_session_duration = Column(Integer, nullable=True)  # seconds
    pages_per_session = Column(Float, nullable=True)
    bounce_rate = Column(Float, nullable=True)  # percentage

    # Conversions
    conversion_rate = Column(Float, nullable=True)  # percentage
    total_conversions = Column(Integer, default=0, nullable=False)

    # Applications
    new_applications = Column(Integer, default=0, nullable=False)
    approved_applications = Column(Integer, default=0, nullable=False)
    rejected_applications = Column(Integer, default=0, nullable=False)

    # Fraud
    fraud_alerts = Column(Integer, default=0, nullable=False)
    fraud_blocked_amount = Column(Float, default=0.0, nullable=False)

    # Top Performers
    top_products = Column(JSON, nullable=True)  # [{"id": 1, "name": "...", "sales": 10}]
    top_services = Column(JSON, nullable=True)
    top_vehicles = Column(JSON, nullable=True)

    def __repr__(self):
        return f"<DailyStats {self.date}>"
