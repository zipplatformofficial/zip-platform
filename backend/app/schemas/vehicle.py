"""Vehicle schemas"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class VehicleCreate(BaseModel):
    """Create vehicle request"""
    make: str = Field(..., min_length=1, max_length=100, description="Vehicle make (e.g., Toyota)")
    model: str = Field(..., min_length=1, max_length=100, description="Vehicle model (e.g., Camry)")
    year: int = Field(..., ge=1900, le=2030, description="Manufacturing year")
    vehicle_type: str = Field(..., description="Vehicle type (sedan, suv, truck, etc.)")
    license_plate: str = Field(..., min_length=1, max_length=20, description="License plate number")
    vin: Optional[str] = Field(None, max_length=50, description="Vehicle Identification Number")
    color: Optional[str] = Field(None, max_length=50)
    transmission: Optional[str] = Field(None, max_length=50, description="Automatic or Manual")
    fuel_type: Optional[str] = Field(None, max_length=50, description="Petrol, Diesel, Electric, Hybrid")
    engine_size: Optional[str] = Field(None, max_length=50)
    odometer_reading: Optional[int] = Field(None, ge=0, description="Current mileage in km")
    notes: Optional[str] = Field(None, max_length=500)

    class Config:
        json_schema_extra = {
            "example": {
                "make": "Toyota",
                "model": "Camry",
                "year": 2020,
                "vehicle_type": "sedan",
                "license_plate": "GH-123-AB",
                "vin": "1HGBH41JXMN109186",
                "color": "Silver",
                "transmission": "Automatic",
                "fuel_type": "Petrol",
                "engine_size": "2.5L",
                "odometer_reading": 45000,
                "notes": "Regular maintenance scheduled"
            }
        }


class VehicleUpdate(BaseModel):
    """Update vehicle request"""
    make: Optional[str] = Field(None, min_length=1, max_length=100)
    model: Optional[str] = Field(None, min_length=1, max_length=100)
    year: Optional[int] = Field(None, ge=1900, le=2030)
    vehicle_type: Optional[str] = None
    license_plate: Optional[str] = Field(None, min_length=1, max_length=20)
    vin: Optional[str] = Field(None, max_length=50)
    color: Optional[str] = Field(None, max_length=50)
    transmission: Optional[str] = Field(None, max_length=50)
    fuel_type: Optional[str] = Field(None, max_length=50)
    engine_size: Optional[str] = Field(None, max_length=50)
    odometer_reading: Optional[int] = Field(None, ge=0)
    notes: Optional[str] = Field(None, max_length=500)

    class Config:
        json_schema_extra = {
            "example": {
                "odometer_reading": 50000,
                "notes": "Oil changed on 2025-01-10"
            }
        }


class VehicleResponse(BaseModel):
    """Vehicle response schema"""
    id: int
    owner_id: int
    make: str
    model: str
    year: int
    vehicle_type: str
    license_plate: str
    vin: Optional[str] = None
    color: Optional[str] = None
    transmission: Optional[str] = None
    fuel_type: Optional[str] = None
    engine_size: Optional[str] = None
    odometer_reading: Optional[int] = None
    last_service_date: Optional[str] = None
    photos: Optional[List[str]] = None
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "owner_id": 123,
                "make": "Toyota",
                "model": "Camry",
                "year": 2020,
                "vehicle_type": "sedan",
                "license_plate": "GH-123-AB",
                "vin": "1HGBH41JXMN109186",
                "color": "Silver",
                "transmission": "Automatic",
                "fuel_type": "Petrol",
                "engine_size": "2.5L",
                "odometer_reading": 45000,
                "last_service_date": "2024-12-15",
                "photos": ["https://cdn.zipghana.com/vehicles/abc123.jpg"],
                "notes": "Regular maintenance scheduled",
                "created_at": "2025-01-01T10:00:00Z",
                "updated_at": "2025-01-15T14:30:00Z"
            }
        }
