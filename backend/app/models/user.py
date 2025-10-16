"""User models"""
import enum
from sqlalchemy import Column, String, Boolean, Enum, Text, JSON, Float, Integer
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class UserRole(str, enum.Enum):
    """User roles"""
    ADMIN = "admin"
    CUSTOMER = "customer"
    TECHNICIAN = "technician"
    VENDOR = "vendor"
    RENTAL_MANAGER = "rental_manager"
    OPERATIONS_MANAGER = "operations_manager"
    CUSTOMER_SUPPORT = "customer_support"


class UserType(str, enum.Enum):
    """User types"""
    INDIVIDUAL = "individual"
    CORPORATE = "corporate"
    RIDE_HAILING_DRIVER = "ride_hailing_driver"


class User(BaseModel):
    """User model"""

    __tablename__ = "users"

    # Basic Information
    email = Column(String(255), unique=True, index=True, nullable=False)
    phone = Column(String(20), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    profile_photo = Column(String(500), nullable=True)

    # User Classification
    role = Column(Enum(UserRole), default=UserRole.CUSTOMER, nullable=False)
    user_type = Column(Enum(UserType), default=UserType.INDIVIDUAL, nullable=True)

    # Verification
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    email_verified = Column(Boolean, default=False, nullable=False)
    phone_verified = Column(Boolean, default=False, nullable=False)

    # KYC/Verification Documents
    ghana_card_number = Column(String(50), nullable=True)
    ghana_card_verified = Column(Boolean, default=False, nullable=False)
    drivers_license_number = Column(String(50), nullable=True)
    drivers_license_verified = Column(Boolean, default=False, nullable=False)

    # Location
    location = Column(JSON, nullable=True)  # {lat, lng, address}
    saved_addresses = Column(JSON, nullable=True)  # Array of addresses

    # Corporate Fields (if user_type is CORPORATE)
    company_name = Column(String(255), nullable=True)
    company_registration = Column(String(100), nullable=True)
    company_documents = Column(JSON, nullable=True)

    # Ratings & Reviews
    average_rating = Column(Float, default=0.0, nullable=False)
    total_ratings = Column(Integer, default=0, nullable=False)

    # Preferences
    notification_preferences = Column(JSON, nullable=True)
    language_preference = Column(String(10), default="en", nullable=False)

    # Loyalty & Referral
    loyalty_points = Column(Integer, default=0, nullable=False)
    referral_code = Column(String(20), unique=True, nullable=True)
    referred_by = Column(String(20), nullable=True)

    # Relationships
    vehicles = relationship("Vehicle", back_populates="owner", cascade="all, delete-orphan")
    service_bookings = relationship("ServiceBooking", back_populates="customer", foreign_keys="ServiceBooking.customer_id")
    rental_bookings = relationship("RentalBooking", back_populates="customer", cascade="all, delete-orphan")
    orders = relationship("Order", back_populates="customer", cascade="all, delete-orphan")
    payments = relationship("Payment", back_populates="user", cascade="all, delete-orphan")
    notifications = relationship("Notification", back_populates="user", cascade="all, delete-orphan")
    cart = relationship("Cart", back_populates="user", uselist=False, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User {self.email}>"
