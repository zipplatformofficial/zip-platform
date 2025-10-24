"""Mobile car maintenance endpoints"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.api.v1.deps import get_db, get_current_active_user, require_admin
from app.models.user import User
from app.models.maintenance import MaintenanceService, ServiceBooking, Technician, ServiceBookingStatus as BookingStatus
from app.models.vehicle import Vehicle
from app.schemas.maintenance import (
    MaintenanceServiceCreate,
    MaintenanceServiceUpdate,
    MaintenanceServiceResponse,
    ServiceBookingCreate,
    ServiceBookingUpdate,
    ServiceBookingResponse,
    BookingStatusUpdate,
    BookingRating,
    TechnicianResponse,
)


router = APIRouter()


# ==================== MAINTENANCE SERVICES ====================

@router.get("/services", response_model=List[MaintenanceServiceResponse])
async def list_maintenance_services(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    service_type: Optional[str] = None,
    search: Optional[str] = None,
    active_only: bool = True,
    db: Session = Depends(get_db)
):
    """
    List all maintenance services

    - **service_type**: Filter by service type
    - **search**: Search in name and description
    - **active_only**: Show only active services (default: true)
    """
    query = db.query(MaintenanceService)

    if active_only:
        query = query.filter(MaintenanceService.is_active == True)

    if service_type:
        query = query.filter(MaintenanceService.service_type == service_type)

    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                MaintenanceService.name.ilike(search_term),
                MaintenanceService.description.ilike(search_term)
            )
        )

    services = query.offset(skip).limit(limit).all()
    return services


@router.get("/services/{service_id}", response_model=MaintenanceServiceResponse)
async def get_maintenance_service(
    service_id: str,
    db: Session = Depends(get_db)
):
    """Get a specific maintenance service by ID"""
    service = db.query(MaintenanceService).filter(MaintenanceService.id == service_id).first()

    if not service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service not found"
        )

    return service


@router.post("/services", response_model=MaintenanceServiceResponse, status_code=status.HTTP_201_CREATED)
async def create_maintenance_service(
    service_in: MaintenanceServiceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Create a new maintenance service (Admin only)"""
    service = MaintenanceService(**service_in.model_dump())

    db.add(service)
    db.commit()
    db.refresh(service)

    return service


@router.put("/services/{service_id}", response_model=MaintenanceServiceResponse)
async def update_maintenance_service(
    service_id: str,
    service_update: MaintenanceServiceUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Update a maintenance service (Admin only)"""
    service = db.query(MaintenanceService).filter(MaintenanceService.id == service_id).first()

    if not service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service not found"
        )

    update_data = service_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(service, field, value)

    db.commit()
    db.refresh(service)

    return service


@router.delete("/services/{service_id}")
async def delete_maintenance_service(
    service_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Delete (deactivate) a maintenance service (Admin only)"""
    service = db.query(MaintenanceService).filter(MaintenanceService.id == service_id).first()

    if not service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service not found"
        )

    service.is_active = False
    db.commit()

    return {"message": "Service deactivated successfully"}


# ==================== SERVICE BOOKINGS ====================

@router.post("/bookings", response_model=ServiceBookingResponse, status_code=status.HTTP_201_CREATED)
async def create_service_booking(
    booking_in: ServiceBookingCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create a new service booking"""
    # Verify service exists
    service = db.query(MaintenanceService).filter(
        MaintenanceService.id == booking_in.service_id,
        MaintenanceService.is_active == True
    ).first()

    if not service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service not found or inactive"
        )

    # Verify vehicle belongs to user
    vehicle = db.query(Vehicle).filter(
        Vehicle.id == booking_in.vehicle_id,
        Vehicle.owner_id == current_user.id
    ).first()

    if not vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vehicle not found or does not belong to you"
        )

    # Create booking
    booking = ServiceBooking(
        **booking_in.model_dump(),
        customer_id=current_user.id,
        status=BookingStatus.PENDING
    )

    db.add(booking)
    db.commit()
    db.refresh(booking)

    return booking


@router.get("/bookings", response_model=List[ServiceBookingResponse])
async def list_my_bookings(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    status: Optional[BookingStatus] = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """List current user's service bookings"""
    query = db.query(ServiceBooking).filter(ServiceBooking.customer_id == current_user.id)

    if status:
        query = query.filter(ServiceBooking.status == status)

    bookings = query.order_by(ServiceBooking.created_at.desc()).offset(skip).limit(limit).all()
    return bookings


@router.get("/bookings/{booking_id}", response_model=ServiceBookingResponse)
async def get_service_booking(
    booking_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get a specific service booking"""
    booking = db.query(ServiceBooking).filter(ServiceBooking.id == booking_id).first()

    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )

    # Check if user owns the booking or is the assigned technician
    if booking.customer_id != current_user.id and booking.technician_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this booking"
        )

    return booking


@router.put("/bookings/{booking_id}", response_model=ServiceBookingResponse)
async def update_service_booking(
    booking_id: str,
    booking_update: ServiceBookingUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update a service booking (customer can update before assignment)"""
    booking = db.query(ServiceBooking).filter(ServiceBooking.id == booking_id).first()

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

    if booking.status not in [BookingStatus.PENDING, BookingStatus.CONFIRMED]:
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


@router.post("/bookings/{booking_id}/status", response_model=ServiceBookingResponse)
async def update_booking_status(
    booking_id: str,
    status_update: BookingStatusUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update booking status (for technicians and admins)"""
    booking = db.query(ServiceBooking).filter(ServiceBooking.id == booking_id).first()

    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )

    # Only technician assigned to booking or admin can update status
    from app.models.user import UserRole
    if current_user.role not in [UserRole.ADMIN, UserRole.TECHNICIAN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only technicians and admins can update booking status"
        )

    if current_user.role == UserRole.TECHNICIAN and booking.technician_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this booking"
        )

    booking.status = status_update.status
    db.commit()
    db.refresh(booking)

    return booking


@router.post("/bookings/{booking_id}/rate", response_model=ServiceBookingResponse)
async def rate_service_booking(
    booking_id: str,
    rating: BookingRating,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Rate a completed service booking"""
    booking = db.query(ServiceBooking).filter(ServiceBooking.id == booking_id).first()

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

    if booking.status != BookingStatus.COMPLETED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Can only rate completed bookings"
        )

    booking.customer_rating = rating.rating
    booking.customer_feedback = rating.feedback

    # Update technician rating if assigned
    if booking.technician_id:
        technician = db.query(Technician).filter(Technician.user_id == booking.technician_id).first()
        if technician:
            total_ratings = technician.total_ratings
            avg_rating = technician.average_rating
            new_total = total_ratings + 1
            new_avg = ((avg_rating * total_ratings) + rating.rating) / new_total

            technician.average_rating = new_avg
            technician.total_ratings = new_total

    db.commit()
    db.refresh(booking)

    return booking


@router.delete("/bookings/{booking_id}")
async def cancel_service_booking(
    booking_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Cancel a service booking"""
    booking = db.query(ServiceBooking).filter(ServiceBooking.id == booking_id).first()

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

    if booking.status not in [BookingStatus.PENDING, BookingStatus.CONFIRMED]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot cancel booking in current status"
        )

    booking.status = BookingStatus.CANCELLED
    db.commit()

    return {"message": "Booking cancelled successfully"}


# ==================== TECHNICIANS ====================

@router.get("/technicians", response_model=List[TechnicianResponse])
async def list_technicians(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    available_only: bool = False,
    verified_only: bool = True,
    db: Session = Depends(get_db)
):
    """List all technicians"""
    query = db.query(Technician)

    if available_only:
        query = query.filter(Technician.is_available == True)

    if verified_only:
        query = query.filter(Technician.is_verified == True)

    technicians = query.order_by(Technician.average_rating.desc()).offset(skip).limit(limit).all()
    return technicians


@router.get("/technicians/{technician_id}", response_model=TechnicianResponse)
async def get_technician(
    technician_id: str,
    db: Session = Depends(get_db)
):
    """Get a specific technician by ID"""
    technician = db.query(Technician).filter(Technician.id == technician_id).first()

    if not technician:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Technician not found"
        )

    return technician
