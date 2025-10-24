"""Car rental endpoints"""
from typing import List, Optional
from datetime import date, datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
import uuid

from app.api.v1.deps import get_db, get_current_active_user, require_admin, require_rental_manager
from app.models.user import User
from app.models.rental import (
    RentalVehicle,
    RentalBooking,
    VehicleInspection,
    RentalBookingStatus as RentalStatus
)
from app.schemas.rental import (
    RentalVehicleCreate,
    RentalVehicleUpdate,
    RentalVehicleResponse,
    RentalBookingCreate,
    RentalBookingUpdate,
    RentalBookingResponse,
    RentalBookingStatusUpdate,
    RentalBookingRating,
    VehicleInspectionCreate,
    VehicleInspectionResponse,
)


router = APIRouter()


# ==================== RENTAL VEHICLES ====================

@router.get("/vehicles", response_model=List[RentalVehicleResponse])
async def list_rental_vehicles(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    make: Optional[str] = None,
    fuel_type: Optional[str] = None,
    transmission: Optional[str] = None,
    min_seats: Optional[int] = None,
    max_daily_rate: Optional[float] = None,
    available_only: bool = True,
    db: Session = Depends(get_db)
):
    """
    List all rental vehicles with filters

    - **make**: Filter by vehicle make
    - **fuel_type**: Filter by fuel type (petrol, diesel, electric, hybrid)
    - **transmission**: Filter by transmission (manual, automatic)
    - **min_seats**: Minimum number of seats
    - **max_daily_rate**: Maximum daily rental rate
    - **available_only**: Show only available vehicles
    """
    query = db.query(RentalVehicle)

    if available_only:
        query = query.filter(RentalVehicle.is_available == True)

    if make:
        query = query.filter(RentalVehicle.make.ilike(f"%{make}%"))

    if fuel_type:
        query = query.filter(RentalVehicle.fuel_type == fuel_type)

    if transmission:
        query = query.filter(RentalVehicle.transmission == transmission)

    if min_seats:
        query = query.filter(RentalVehicle.seating_capacity >= min_seats)

    if max_daily_rate:
        query = query.filter(RentalVehicle.daily_rate <= max_daily_rate)

    vehicles = query.order_by(RentalVehicle.average_rating.desc()).offset(skip).limit(limit).all()
    return vehicles


@router.get("/vehicles/{vehicle_id}", response_model=RentalVehicleResponse)
async def get_rental_vehicle(
    vehicle_id: str,
    db: Session = Depends(get_db)
):
    """Get a specific rental vehicle by ID"""
    vehicle = db.query(RentalVehicle).filter(RentalVehicle.id == vehicle_id).first()

    if not vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vehicle not found"
        )

    return vehicle


@router.get("/vehicles/{vehicle_id}/availability")
async def check_vehicle_availability(
    vehicle_id: str,
    start_date: date,
    end_date: date,
    db: Session = Depends(get_db)
):
    """Check if a vehicle is available for specific dates"""
    vehicle = db.query(RentalVehicle).filter(RentalVehicle.id == vehicle_id).first()

    if not vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vehicle not found"
        )

    # Check for overlapping bookings
    overlapping_bookings = db.query(RentalBooking).filter(
        and_(
            RentalBooking.vehicle_id == vehicle_id,
            RentalBooking.status.in_([RentalStatus.CONFIRMED, RentalStatus.ACTIVE]),
            or_(
                and_(RentalBooking.start_date <= start_date, RentalBooking.end_date >= start_date),
                and_(RentalBooking.start_date <= end_date, RentalBooking.end_date >= end_date),
                and_(RentalBooking.start_date >= start_date, RentalBooking.end_date <= end_date)
            )
        )
    ).count()

    is_available = overlapping_bookings == 0 and vehicle.is_available

    return {
        "vehicle_id": str(vehicle_id),
        "start_date": start_date,
        "end_date": end_date,
        "is_available": is_available,
        "daily_rate": vehicle.daily_rate,
        "total_days": (end_date - start_date).days + 1,
        "estimated_total": vehicle.daily_rate * ((end_date - start_date).days + 1)
    }


@router.post("/vehicles", response_model=RentalVehicleResponse, status_code=status.HTTP_201_CREATED)
async def create_rental_vehicle(
    vehicle_in: RentalVehicleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_rental_manager)
):
    """Create a new rental vehicle (Rental Manager or Admin)"""
    vehicle = RentalVehicle(**vehicle_in.model_dump())

    db.add(vehicle)
    db.commit()
    db.refresh(vehicle)

    return vehicle


@router.put("/vehicles/{vehicle_id}", response_model=RentalVehicleResponse)
async def update_rental_vehicle(
    vehicle_id: str,
    vehicle_update: RentalVehicleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_rental_manager)
):
    """Update a rental vehicle (Admin only)"""
    vehicle = db.query(RentalVehicle).filter(RentalVehicle.id == vehicle_id).first()

    if not vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vehicle not found"
        )

    update_data = vehicle_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(vehicle, field, value)

    db.commit()
    db.refresh(vehicle)

    return vehicle


# ==================== RENTAL BOOKINGS ====================

@router.post("/bookings", response_model=RentalBookingResponse, status_code=status.HTTP_201_CREATED)
async def create_rental_booking(
    booking_in: RentalBookingCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create a new rental booking"""
    # Verify vehicle exists and is available
    vehicle = db.query(RentalVehicle).filter(
        RentalVehicle.id == booking_in.vehicle_id,
        RentalVehicle.is_available == True,
        RentalVehicle.status == "active"
    ).first()

    if not vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vehicle not found or not available"
        )

    # Validate dates
    if booking_in.end_date <= booking_in.start_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="End date must be after start date"
        )

    # Check for overlapping bookings
    overlapping = db.query(RentalBooking).filter(
        and_(
            RentalBooking.vehicle_id == booking_in.vehicle_id,
            RentalBooking.status.in_([RentalStatus.CONFIRMED, RentalStatus.ACTIVE]),
            or_(
                and_(RentalBooking.start_date <= booking_in.start_date, RentalBooking.end_date >= booking_in.start_date),
                and_(RentalBooking.start_date <= booking_in.end_date, RentalBooking.end_date >= booking_in.end_date),
                and_(RentalBooking.start_date >= booking_in.start_date, RentalBooking.end_date <= booking_in.end_date)
            )
        )
    ).first()

    if overlapping:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Vehicle is not available for these dates"
        )

    # Calculate pricing
    total_days = (booking_in.end_date - booking_in.start_date).days + 1
    daily_rate = vehicle.daily_rate
    total_price = daily_rate * total_days
    security_deposit = daily_rate * 2  # 2 days worth as deposit

    # Generate booking number
    booking_number = f"RNT{uuid.uuid4().hex[:8].upper()}"

    # Create booking
    booking = RentalBooking(
        **booking_in.model_dump(),
        customer_id=current_user.id,
        booking_number=booking_number,
        status=RentalStatus.PENDING,
        total_days=total_days,
        daily_rate=daily_rate,
        total_price=total_price,
        security_deposit=security_deposit,
    )

    db.add(booking)
    db.commit()
    db.refresh(booking)

    return booking


@router.get("/bookings", response_model=List[RentalBookingResponse])
async def list_my_rental_bookings(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    status: Optional[RentalStatus] = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """List current user's rental bookings"""
    query = db.query(RentalBooking).filter(RentalBooking.customer_id == current_user.id)

    if status:
        query = query.filter(RentalBooking.status == status)

    bookings = query.order_by(RentalBooking.created_at.desc()).offset(skip).limit(limit).all()
    return bookings


@router.get("/bookings/{booking_id}", response_model=RentalBookingResponse)
async def get_rental_booking(
    booking_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get a specific rental booking"""
    booking = db.query(RentalBooking).filter(RentalBooking.id == booking_id).first()

    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )

    # Check if user owns the booking
    if booking.customer_id != current_user.id:
        from app.models.user import UserRole
        if current_user.role not in [UserRole.ADMIN, UserRole.RENTAL_MANAGER]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to view this booking"
            )

    return booking


@router.put("/bookings/{booking_id}", response_model=RentalBookingResponse)
async def update_rental_booking(
    booking_id: str,
    booking_update: RentalBookingUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update a rental booking"""
    booking = db.query(RentalBooking).filter(RentalBooking.id == booking_id).first()

    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )

    if booking.customer_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this booking"
        )

    if booking.status not in [RentalStatus.PENDING, RentalStatus.CONFIRMED]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot update booking in current status"
        )

    update_data = booking_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(booking, field, value)

    db.commit()
    db.refresh(booking)

    return booking


@router.post("/bookings/{booking_id}/status", response_model=RentalBookingResponse)
async def update_rental_booking_status(
    booking_id: str,
    status_update: RentalBookingStatusUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update rental booking status (Admin/Rental Manager only)"""
    from app.models.user import UserRole

    if current_user.role not in [UserRole.ADMIN, UserRole.RENTAL_MANAGER]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update booking status"
        )

    booking = db.query(RentalBooking).filter(RentalBooking.id == booking_id).first()

    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )

    booking.status = status_update.status

    # Update timestamps based on status
    if status_update.status == RentalStatus.ACTIVE and not booking.picked_up_at:
        booking.picked_up_at = datetime.utcnow()

    if status_update.status == RentalStatus.COMPLETED and not booking.returned_at:
        booking.returned_at = datetime.utcnow()
        booking.actual_return_date = date.today()

    db.commit()
    db.refresh(booking)

    return booking


@router.post("/bookings/{booking_id}/rate", response_model=RentalBookingResponse)
async def rate_rental_booking(
    booking_id: str,
    rating: RentalBookingRating,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Rate a completed rental booking"""
    booking = db.query(RentalBooking).filter(RentalBooking.id == booking_id).first()

    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )

    if booking.customer_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to rate this booking"
        )

    if booking.status != RentalStatus.COMPLETED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Can only rate completed bookings"
        )

    booking.customer_rating = rating.rating
    booking.customer_feedback = rating.feedback

    # Update vehicle rating
    vehicle = db.query(RentalVehicle).filter(RentalVehicle.id == booking.vehicle_id).first()
    if vehicle:
        total_ratings = vehicle.total_ratings
        avg_rating = vehicle.average_rating
        new_total = total_ratings + 1
        new_avg = ((avg_rating * total_ratings) + rating.rating) / new_total

        vehicle.average_rating = new_avg
        vehicle.total_ratings = new_total

    db.commit()
    db.refresh(booking)

    return booking


@router.delete("/bookings/{booking_id}")
async def cancel_rental_booking(
    booking_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Cancel a rental booking"""
    booking = db.query(RentalBooking).filter(RentalBooking.id == booking_id).first()

    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )

    if booking.customer_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to cancel this booking"
        )

    if booking.status not in [RentalStatus.PENDING, RentalStatus.CONFIRMED]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot cancel booking in current status"
        )

    booking.status = RentalStatus.CANCELLED
    db.commit()

    return {"message": "Booking cancelled successfully"}


# ==================== VEHICLE INSPECTIONS ====================

@router.post("/inspections", response_model=VehicleInspectionResponse, status_code=status.HTTP_201_CREATED)
async def create_vehicle_inspection(
    inspection_in: VehicleInspectionCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create a vehicle inspection (Admin/Rental Manager only)"""
    from app.models.user import UserRole

    if current_user.role not in [UserRole.ADMIN, UserRole.RENTAL_MANAGER]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to create inspections"
        )

    inspection = VehicleInspection(
        **inspection_in.model_dump(),
        inspector_id=current_user.id
    )

    db.add(inspection)
    db.commit()
    db.refresh(inspection)

    return inspection


@router.get("/bookings/{booking_id}/inspections", response_model=List[VehicleInspectionResponse])
async def get_booking_inspections(
    booking_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get all inspections for a booking"""
    booking = db.query(RentalBooking).filter(RentalBooking.id == booking_id).first()

    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )

    # Check authorization
    from app.models.user import UserRole
    if booking.customer_id != current_user.id and current_user.role not in [UserRole.ADMIN, UserRole.RENTAL_MANAGER]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view these inspections"
        )

    inspections = db.query(VehicleInspection).filter(
        VehicleInspection.booking_id == booking_id
    ).order_by(VehicleInspection.created_at).all()

    return inspections
