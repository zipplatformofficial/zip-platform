"""Vehicle models"""
import enum
from sqlalchemy import Column, String, Integer, ForeignKey, Enum, JSON
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class VehicleType(str, enum.Enum):
    """Vehicle types"""
    SEDAN = "sedan"
    SUV = "suv"
    TRUCK = "truck"
    VAN = "van"
    COUPE = "coupe"
    HATCHBACK = "hatchback"
    WAGON = "wagon"
    CONVERTIBLE = "convertible"
    MINIVAN = "minivan"
    PICKUP = "pickup"


class Vehicle(BaseModel):
    """Vehicle model - for customer vehicles"""

    __tablename__ = "vehicles"

    # Owner
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    # Vehicle Details
    make = Column(String(100), nullable=False)  # e.g., Toyota
    model = Column(String(100), nullable=False)  # e.g., Camry
    year = Column(Integer, nullable=False)
    vehicle_type = Column(Enum(VehicleType), nullable=False)

    # Identification
    license_plate = Column(String(20), unique=True, nullable=False, index=True)
    vin = Column(String(50), unique=True, nullable=True)  # Vehicle Identification Number
    color = Column(String(50), nullable=True)

    # Technical Specs
    transmission = Column(String(50), nullable=True)  # Automatic/Manual
    fuel_type = Column(String(50), nullable=True)  # Petrol/Diesel/Electric/Hybrid
    engine_size = Column(String(50), nullable=True)

    # Current Status
    odometer_reading = Column(Integer, nullable=True)  # Current mileage
    last_service_date = Column(String(50), nullable=True)

    # Additional Info
    photos = Column(JSON, nullable=True)  # Array of photo URLs
    notes = Column(String(500), nullable=True)

    # Relationships
    owner = relationship("User", back_populates="vehicles")
    service_bookings = relationship("ServiceBooking", back_populates="vehicle")

    def __repr__(self):
        return f"<Vehicle {self.make} {self.model} - {self.license_plate}>"
