"""User management endpoints"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session

from app.api.v1.deps import get_db, get_current_active_user
from app.core.security import get_password_hash, verify_password
from app.models.user import User
from app.models.vehicle import Vehicle
from app.schemas.user import UserResponse, UserUpdate
from app.schemas.vehicle import VehicleCreate, VehicleUpdate, VehicleResponse
from app.services.cloud_storage_service import cloud_storage_service
from app.core.config import settings
from pydantic import BaseModel


router = APIRouter()

# Allowed image types for avatar
ALLOWED_IMAGE_TYPES = ['image/jpeg', 'image/png', 'image/jpg', 'image/webp']


class PasswordChange(BaseModel):
    """Password change schema"""
    current_password: str
    new_password: str


@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(
    current_user: User = Depends(get_current_active_user)
):
    """
    Get current user profile

    Requires authentication
    """
    return current_user


@router.put("/me", response_model=UserResponse)
async def update_user_profile(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Update current user profile

    Requires authentication
    """
    # Update only provided fields
    update_data = user_update.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(current_user, field, value)

    db.commit()
    db.refresh(current_user)

    return current_user


@router.post("/me/change-password")
async def change_password(
    password_data: PasswordChange,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Change user password

    Requires authentication and current password verification
    """
    # Verify current password
    if not verify_password(password_data.current_password, current_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect current password"
        )

    # Update password
    current_user.password_hash = get_password_hash(password_data.new_password)
    db.commit()

    return {"message": "Password changed successfully"}


@router.post("/me/avatar", response_model=UserResponse)
async def upload_user_avatar(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Upload user avatar/profile picture

    - Accepts JPEG, PNG, WebP formats
    - Maximum size: 5MB
    - Updates user profile photo URL
    """
    if not cloud_storage_service:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Cloud storage service is not configured"
        )

    # Validate file
    validation = cloud_storage_service.validate_file(
        file.file,
        allowed_types=ALLOWED_IMAGE_TYPES,
        max_size=settings.MAX_FILE_SIZE
    )

    if not validation.get("valid"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=validation.get("message")
        )

    # Upload file
    result = cloud_storage_service.upload_file(
        file_obj=file.file,
        filename=file.filename,
        folder="avatars",
        content_type=file.content_type,
        metadata={
            "user_id": str(current_user.id),
            "original_filename": file.filename
        }
    )

    if not result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=result.get("message")
        )

    # Update user photo URL
    current_user.photo_url = result["url"]
    db.commit()
    db.refresh(current_user)

    return current_user


@router.delete("/me")
async def delete_user_account(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Deactivate user account (soft delete)

    Requires authentication
    """
    current_user.is_active = False
    db.commit()

    return {"message": "Account deactivated successfully"}


@router.get("/me/stats")
async def get_user_stats(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get user statistics (bookings, orders, etc.)

    Requires authentication
    """
    from app.models.maintenance import ServiceBooking
    from app.models.rental import RentalBooking
    from app.models.store import Order

    # Count user's activities
    service_bookings_count = db.query(ServiceBooking).filter(
        ServiceBooking.customer_id == current_user.id
    ).count()

    rental_bookings_count = db.query(RentalBooking).filter(
        RentalBooking.customer_id == current_user.id
    ).count()

    orders_count = db.query(Order).filter(
        Order.customer_id == current_user.id
    ).count()

    return {
        "user_id": str(current_user.id),
        "full_name": current_user.full_name,
        "email": current_user.email,
        "loyalty_points": current_user.loyalty_points,
        "average_rating": current_user.average_rating,
        "total_ratings": current_user.total_ratings,
        "referral_code": current_user.referral_code,
        "statistics": {
            "service_bookings": service_bookings_count,
            "rental_bookings": rental_bookings_count,
            "orders": orders_count,
            "total_activities": service_bookings_count + rental_bookings_count + orders_count
        }
    }


# =================
# VEHICLE ENDPOINTS
# =================

@router.post("/vehicles", response_model=VehicleResponse, status_code=status.HTTP_201_CREATED)
async def add_vehicle(
    vehicle: VehicleCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Add a new vehicle to user's garage

    - Used for maintenance bookings
    - License plate must be unique
    """
    # Check if license plate already exists
    existing = db.query(Vehicle).filter(
        Vehicle.license_plate == vehicle.license_plate
    ).first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A vehicle with this license plate already exists"
        )

    # Create vehicle
    db_vehicle = Vehicle(
        owner_id=current_user.id,
        **vehicle.model_dump()
    )

    db.add(db_vehicle)
    db.commit()
    db.refresh(db_vehicle)

    return db_vehicle


@router.get("/vehicles", response_model=List[VehicleResponse])
async def list_my_vehicles(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get all vehicles owned by current user

    - Returns list of user's vehicles
    - Used for selecting vehicle when booking service
    """
    vehicles = db.query(Vehicle).filter(
        Vehicle.owner_id == current_user.id
    ).all()

    return vehicles


@router.get("/vehicles/{vehicle_id}", response_model=VehicleResponse)
async def get_vehicle(
    vehicle_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get details of a specific vehicle

    - Must be owned by current user
    """
    vehicle = db.query(Vehicle).filter(
        Vehicle.id == vehicle_id,
        Vehicle.owner_id == current_user.id
    ).first()

    if not vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vehicle not found"
        )

    return vehicle


@router.put("/vehicles/{vehicle_id}", response_model=VehicleResponse)
async def update_vehicle(
    vehicle_id: int,
    vehicle_update: VehicleUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Update vehicle information

    - Update odometer, notes, etc.
    - Must be owned by current user
    """
    vehicle = db.query(Vehicle).filter(
        Vehicle.id == vehicle_id,
        Vehicle.owner_id == current_user.id
    ).first()

    if not vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vehicle not found"
        )

    # Update only provided fields
    update_data = vehicle_update.model_dump(exclude_unset=True)

    # Check if license plate is being changed and already exists
    if "license_plate" in update_data:
        existing = db.query(Vehicle).filter(
            Vehicle.license_plate == update_data["license_plate"],
            Vehicle.id != vehicle_id
        ).first()

        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A vehicle with this license plate already exists"
            )

    for field, value in update_data.items():
        setattr(vehicle, field, value)

    db.commit()
    db.refresh(vehicle)

    return vehicle


@router.delete("/vehicles/{vehicle_id}")
async def delete_vehicle(
    vehicle_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Remove a vehicle from user's garage

    - Soft delete
    - Must be owned by current user
    - Cannot delete if has active bookings
    """
    vehicle = db.query(Vehicle).filter(
        Vehicle.id == vehicle_id,
        Vehicle.owner_id == current_user.id
    ).first()

    if not vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vehicle not found"
        )

    # Check for active bookings
    from app.models.maintenance import ServiceBooking
    active_bookings = db.query(ServiceBooking).filter(
        ServiceBooking.vehicle_id == vehicle_id,
        ServiceBooking.status.in_(["pending", "confirmed", "in_progress"])
    ).count()

    if active_bookings > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete vehicle with active service bookings"
        )

    db.delete(vehicle)
    db.commit()

    return {"message": "Vehicle deleted successfully"}
