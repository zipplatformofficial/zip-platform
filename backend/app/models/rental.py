"""Car Rental models"""
import enum
from sqlalchemy import Column, String, Integer, ForeignKey, Enum, Text, JSON, Float, Boolean
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class RentalBookingStatus(str, enum.Enum):
    """Rental booking status"""
    PENDING = "pending"
    CONFIRMED = "confirmed"
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    OVERDUE = "overdue"


class RentalVehicle(BaseModel):
    """Rental fleet vehicles"""

    __tablename__ = "rental_vehicles"

    # Vehicle Details
    make = Column(String(100), nullable=False)
    model = Column(String(100), nullable=False)
    year = Column(Integer, nullable=False)
    vehicle_type = Column(String(50), nullable=False)
    license_plate = Column(String(20), unique=True, nullable=False, index=True)
    vin = Column(String(50), unique=True, nullable=True)

    # Specifications
    transmission = Column(String(50), nullable=False)  # Automatic/Manual
    fuel_type = Column(String(50), nullable=False)
    seating_capacity = Column(Integer, nullable=False)
    color = Column(String(50), nullable=True)
    features = Column(JSON, nullable=True)  # AC, GPS, etc.

    # Media
    photos = Column(JSON, nullable=False)  # Array of photo URLs
    description = Column(Text, nullable=True)

    # Pricing
    hourly_rate = Column(Float, nullable=True)
    daily_rate = Column(Float, nullable=False)
    weekly_rate = Column(Float, nullable=True)
    monthly_rate = Column(Float, nullable=True)
    driver_fee_per_day = Column(Float, nullable=True)
    delivery_fee = Column(Float, nullable=True)

    # Insurance
    insurance_details = Column(JSON, nullable=True)

    # Availability
    is_available = Column(Boolean, default=True, nullable=False)
    current_location = Column(JSON, nullable=True)  # {lat, lng, address}
    geo_fence_area = Column(JSON, nullable=True)  # Allowed operating area

    # Maintenance
    odometer_reading = Column(Integer, nullable=True)
    last_service_date = Column(String(50), nullable=True)
    next_service_due = Column(String(50), nullable=True)
    condition_notes = Column(Text, nullable=True)

    # Tracking
    gps_device_id = Column(String(100), nullable=True)
    real_time_tracking_enabled = Column(Boolean, default=True, nullable=False)

    # Performance
    total_rentals = Column(Integer, default=0, nullable=False)
    average_rating = Column(Float, default=0.0, nullable=False)

    # Relationships
    bookings = relationship("RentalBooking", back_populates="vehicle")
    inspections = relationship("VehicleInspection", back_populates="vehicle")

    def __repr__(self):
        return f"<RentalVehicle {self.make} {self.model} - {self.license_plate}>"


class RentalBooking(BaseModel):
    """Rental bookings"""

    __tablename__ = "rental_bookings"

    # Customer
    customer_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    # Vehicle
    vehicle_id = Column(Integer, ForeignKey("rental_vehicles.id", ondelete="SET NULL"), nullable=True)

    # Booking Details
    booking_reference = Column(String(50), unique=True, nullable=False, index=True)
    status = Column(Enum(RentalBookingStatus), default=RentalBookingStatus.PENDING, nullable=False)

    # Rental Period
    pickup_datetime = Column(String(50), nullable=False)
    return_datetime = Column(String(50), nullable=False)
    actual_pickup_datetime = Column(String(50), nullable=True)
    actual_return_datetime = Column(String(50), nullable=True)

    # Rental Duration (calculated)
    duration_hours = Column(Integer, nullable=False)
    duration_days = Column(Integer, nullable=False)

    # Pickup/Return
    pickup_location = Column(JSON, nullable=False)  # {type: "office/delivery", address, lat, lng}
    return_location = Column(JSON, nullable=False)
    delivery_requested = Column(Boolean, default=False, nullable=False)

    # Driver Option
    with_driver = Column(Boolean, default=False, nullable=False)
    driver_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    # Customer Documents
    drivers_license = Column(JSON, nullable=False)  # Document upload info
    ghana_card = Column(JSON, nullable=False)
    proof_of_address = Column(JSON, nullable=False)
    company_documents = Column(JSON, nullable=True)  # For corporate
    documents_verified = Column(Boolean, default=False, nullable=False)

    # Pricing
    base_cost = Column(Float, nullable=False)
    driver_cost = Column(Float, default=0.0, nullable=False)
    delivery_cost = Column(Float, default=0.0, nullable=False)
    extension_cost = Column(Float, default=0.0, nullable=False)
    damage_charges = Column(Float, default=0.0, nullable=False)
    late_return_penalty = Column(Float, default=0.0, nullable=False)
    total_cost = Column(Float, nullable=False)

    # Damage & Inspection
    pickup_inspection_id = Column(Integer, ForeignKey("vehicle_inspections.id"), nullable=True)
    return_inspection_id = Column(Integer, ForeignKey("vehicle_inspections.id"), nullable=True)
    damages_reported = Column(JSON, nullable=True)

    # Extension
    extension_requested = Column(Boolean, default=False, nullable=False)
    extension_approved = Column(Boolean, default=False, nullable=False)
    original_return_datetime = Column(String(50), nullable=True)

    # Real-time Tracking
    current_vehicle_location = Column(JSON, nullable=True)
    geo_fence_violations = Column(Integer, default=0, nullable=False)
    geo_fence_alerts = Column(JSON, nullable=True)

    # Customer Feedback
    customer_rating = Column(Integer, nullable=True)
    customer_review = Column(Text, nullable=True)

    # Cancellation
    cancellation_reason = Column(Text, nullable=True)
    cancelled_by = Column(String(50), nullable=True)

    # Relationships
    customer = relationship("User", back_populates="rental_bookings", foreign_keys=[customer_id])
    vehicle = relationship("RentalVehicle", back_populates="bookings")
    pickup_inspection = relationship("VehicleInspection", foreign_keys=[pickup_inspection_id])
    return_inspection = relationship("VehicleInspection", foreign_keys=[return_inspection_id])
    payment = relationship("Payment", back_populates="rental_booking", uselist=False)

    def __repr__(self):
        return f"<RentalBooking {self.booking_reference}>"


class VehicleInspection(BaseModel):
    """Vehicle inspection records"""

    __tablename__ = "vehicle_inspections"

    vehicle_id = Column(Integer, ForeignKey("rental_vehicles.id", ondelete="CASCADE"), nullable=False)
    inspector_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    booking_id = Column(Integer, nullable=True)  # Link to rental booking

    inspection_type = Column(String(50), nullable=False)  # pickup/return
    inspection_datetime = Column(String(50), nullable=False)

    # Inspection Data
    odometer_reading = Column(Integer, nullable=False)
    fuel_level = Column(String(20), nullable=True)  # Full, 3/4, 1/2, etc.
    condition_photos = Column(JSON, nullable=False)  # Array of photo URLs
    condition_videos = Column(JSON, nullable=True)
    damages = Column(JSON, nullable=True)  # Array of damage descriptions
    cleanliness_rating = Column(Integer, nullable=True)  # 1-5

    # Digital Signature
    customer_signature = Column(String(500), nullable=True)
    inspector_signature = Column(String(500), nullable=True)
    signed_at = Column(String(50), nullable=True)

    notes = Column(Text, nullable=True)

    # Relationships
    vehicle = relationship("RentalVehicle", back_populates="inspections")

    def __repr__(self):
        return f"<VehicleInspection {self.inspection_type} - {self.vehicle_id}>"


class FleetSubscription(BaseModel):
    """Corporate fleet management subscriptions"""

    __tablename__ = "fleet_subscriptions"

    # Corporate Customer
    company_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    # Subscription Details
    subscription_name = Column(String(200), nullable=False)
    start_date = Column(String(50), nullable=False)
    end_date = Column(String(50), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    # Vehicle Allocation
    vehicle_count = Column(Integer, nullable=False)
    assigned_vehicles = Column(JSON, nullable=True)  # Array of vehicle IDs

    # Employee Management
    authorized_employees = Column(JSON, nullable=True)  # Array of employee user IDs
    employee_vehicle_assignments = Column(JSON, nullable=True)

    # Pricing
    monthly_fee = Column(Float, nullable=False)
    per_vehicle_fee = Column(Float, nullable=True)

    # Usage Tracking
    total_distance_km = Column(Float, default=0.0, nullable=False)
    total_incidents = Column(Integer, default=0, nullable=False)

    # Relationships
    company = relationship("User")

    def __repr__(self):
        return f"<FleetSubscription {self.subscription_name}>"
