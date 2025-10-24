"""Mobile Car Maintenance models"""
import enum
from sqlalchemy import Column, String, Integer, ForeignKey, Enum, Text, JSON, Float, Boolean
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class MaintenanceServiceType(str, enum.Enum):
    """Types of maintenance services"""
    CAR_WASH = "car_wash"
    OIL_CHANGE = "oil_change"
    TIRE_REPAIR = "tire_repair"
    DIAGNOSTICS = "diagnostics"
    BATTERY_CHECK = "battery_check"
    BRAKE_SERVICE = "brake_service"
    AC_SERVICE = "ac_service"
    ENGINE_TUNE_UP = "engine_tune_up"
    TRANSMISSION_SERVICE = "transmission_service"
    ELECTRICAL_REPAIR = "electrical_repair"
    OTHER = "other"


class ServiceBookingStatus(str, enum.Enum):
    """Service booking status"""
    PENDING = "pending"
    CONFIRMED = "confirmed"
    ASSIGNED = "assigned"
    EN_ROUTE = "en_route"
    ARRIVED = "arrived"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    FAILED = "failed"


class MaintenanceService(BaseModel):
    """Maintenance service catalog"""

    __tablename__ = "maintenance_services"

    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    service_type = Column(Enum(MaintenanceServiceType), nullable=False)
    base_price = Column(Float, nullable=False)
    estimated_duration = Column(Integer, nullable=True)  # in minutes
    is_active = Column(Boolean, default=True, nullable=False)
    icon = Column(String(500), nullable=True)

    def __repr__(self):
        return f"<MaintenanceService {self.name}>"


class Technician(BaseModel):
    """Technician profile"""

    __tablename__ = "technicians"

    # Link to user account
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)

    # Professional Info
    experience_years = Column(Integer, nullable=True)
    specializations = Column(JSON, nullable=True)  # Array of service types
    certification = Column(JSON, nullable=True)  # Certification details
    bio = Column(Text, nullable=True)

    # Availability
    is_available = Column(Boolean, default=True, nullable=False)
    working_hours = Column(JSON, nullable=True)  # {start: "08:00", end: "18:00"}
    service_area = Column(JSON, nullable=True)  # Geographic boundaries

    # Current Location (for job assignment)
    current_location = Column(JSON, nullable=True)  # {lat, lng}
    last_location_update = Column(String(50), nullable=True)

    # Performance Metrics
    total_jobs_completed = Column(Integer, default=0, nullable=False)
    average_rating = Column(Float, default=0.0, nullable=False)
    total_ratings = Column(Integer, default=0, nullable=False)
    completion_rate = Column(Float, default=0.0, nullable=False)
    response_time_avg = Column(Integer, default=0, nullable=False)  # in minutes

    # Verification
    is_verified = Column(Boolean, default=False, nullable=False)
    verification_documents = Column(JSON, nullable=True)

    # Earnings
    total_earnings = Column(Float, default=0.0, nullable=False)

    # Relationships
    user = relationship("User")
    services = relationship("TechnicianService", back_populates="technician")
    bookings = relationship("ServiceBooking", back_populates="technician")

    def __repr__(self):
        return f"<Technician {self.user_id}>"


class TechnicianService(BaseModel):
    """Services offered by a technician"""

    __tablename__ = "technician_services"

    technician_id = Column(Integer, ForeignKey("technicians.id", ondelete="CASCADE"), nullable=False)
    service_type = Column(Enum(MaintenanceServiceType), nullable=False)
    price = Column(Float, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    # Relationships
    technician = relationship("Technician", back_populates="services")

    def __repr__(self):
        return f"<TechnicianService {self.technician_id} - {self.service_type}>"


class ServiceBooking(BaseModel):
    """Service booking"""

    __tablename__ = "service_bookings"

    # Customer & Vehicle
    customer_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id", ondelete="SET NULL"), nullable=True)

    # Technician Assignment
    technician_id = Column(Integer, ForeignKey("technicians.id", ondelete="SET NULL"), nullable=True)

    # Booking Details
    booking_reference = Column(String(50), unique=True, nullable=False, index=True)
    status = Column(Enum(ServiceBookingStatus), default=ServiceBookingStatus.PENDING, nullable=False)

    # Location & Timing
    service_location = Column(JSON, nullable=False)  # {lat, lng, address}
    scheduled_date = Column(String(50), nullable=True)  # ISO datetime or "immediate"
    actual_start_time = Column(String(50), nullable=True)
    actual_end_time = Column(String(50), nullable=True)

    # Services (many-to-many through association table)
    selected_services = Column(JSON, nullable=False)  # Array of service IDs

    # Service Execution
    pre_service_inspection = Column(JSON, nullable=True)  # Photos, odometer, notes
    service_documentation = Column(JSON, nullable=True)  # Parts used, work done, photos
    post_service_summary = Column(Text, nullable=True)
    additional_services_offered = Column(JSON, nullable=True)

    # Pricing
    estimated_cost = Column(Float, nullable=False)
    additional_charges = Column(Float, default=0.0, nullable=False)
    final_cost = Column(Float, nullable=True)

    # Customer Feedback
    customer_rating = Column(Integer, nullable=True)  # 1-5
    customer_review = Column(Text, nullable=True)

    # Assignment metadata
    assignment_attempts = Column(Integer, default=0, nullable=False)
    technician_response_time = Column(Integer, nullable=True)  # seconds
    eta_minutes = Column(Integer, nullable=True)

    # Cancellation
    cancellation_reason = Column(Text, nullable=True)
    cancelled_by = Column(String(50), nullable=True)  # customer/technician/system

    # Relationships
    customer = relationship("User", back_populates="service_bookings", foreign_keys=[customer_id])
    vehicle = relationship("Vehicle", back_populates="service_bookings")
    technician = relationship("Technician", back_populates="bookings")
    payment = relationship("Payment", back_populates="service_booking", uselist=False)

    def __repr__(self):
        return f"<ServiceBooking {self.booking_reference}>"
