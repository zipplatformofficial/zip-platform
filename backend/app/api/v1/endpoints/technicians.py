"""Technician portal endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from typing import List
from datetime import datetime, timedelta
from decimal import Decimal

from app.core.database import get_db
from app.api.v1.deps import get_current_user
from app.core.security import get_password_hash
from app.models.user import User, UserRole
from app.models.maintenance import Technician, ServiceBooking, TechnicianService, MaintenanceService
from app.models.payment import Payment
from app.schemas.technician import (
    TechnicianRegister,
    TechnicianProfileUpdate,
    TechnicianResponse,
    TechnicianEarnings,
    AvailabilityUpdate
)
from app.schemas.maintenance import ServiceBookingResponse

router = APIRouter()


@router.post("/register", response_model=TechnicianResponse, status_code=status.HTTP_201_CREATED)
async def register_technician(
    registration: TechnicianRegister,
    db: Session = Depends(get_db)
):
    """
    Register as a technician

    - Creates user account with TECHNICIAN role
    - Creates technician profile
    - Requires verification before accepting jobs
    """
    # Check if email already exists
    existing_user = db.query(User).filter(User.email == registration.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Create user account
    user = User(
        email=registration.email,
        password_hash=get_password_hash(registration.password),
        full_name=registration.full_name,
        phone=registration.phone,
        role=UserRole.TECHNICIAN,
        is_active=True,
        email_verified=False
    )
    db.add(user)
    db.flush()  # Get user.id

    # Create technician profile
    technician = Technician(
        user_id=user.id,
        specializations=registration.specializations,
        years_of_experience=registration.years_of_experience,
        rating=Decimal("0.0"),
        total_jobs=0,
        is_available=False,  # Disabled until verified
        is_verified=False,
        address=registration.address,
        latitude=registration.latitude,
        longitude=registration.longitude,
        ghana_card_number=registration.ghana_card_number
    )
    db.add(technician)
    db.commit()
    db.refresh(technician)

    return technician


@router.get("/me", response_model=TechnicianResponse)
async def get_my_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get my technician profile

    - Returns technician profile data
    - Requires TECHNICIAN role
    """
    if current_user.role != UserRole.TECHNICIAN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only technicians can access this endpoint"
        )

    technician = db.query(Technician).filter(
        Technician.user_id == current_user.id
    ).first()

    if not technician:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Technician profile not found"
        )

    return technician


@router.put("/me", response_model=TechnicianResponse)
async def update_my_profile(
    profile_update: TechnicianProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update my technician profile

    - Update specializations, experience, location
    - Requires TECHNICIAN role
    """
    if current_user.role != UserRole.TECHNICIAN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only technicians can access this endpoint"
        )

    technician = db.query(Technician).filter(
        Technician.user_id == current_user.id
    ).first()

    if not technician:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Technician profile not found"
        )

    # Update only provided fields
    update_data = profile_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(technician, field, value)

    db.commit()
    db.refresh(technician)

    return technician


@router.put("/me/availability", response_model=TechnicianResponse)
async def toggle_availability(
    availability: AvailabilityUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Toggle availability status

    - Set as available/unavailable for new jobs
    - Can only be available if verified
    """
    if current_user.role != UserRole.TECHNICIAN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only technicians can access this endpoint"
        )

    technician = db.query(Technician).filter(
        Technician.user_id == current_user.id
    ).first()

    if not technician:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Technician profile not found"
        )

    # Can only set available if verified
    if availability.is_available and not technician.is_verified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Must be verified before accepting jobs"
        )

    technician.is_available = availability.is_available
    db.commit()
    db.refresh(technician)

    return technician


@router.get("/me/bookings", response_model=List[ServiceBookingResponse])
async def get_my_bookings(
    status_filter: str = None,
    skip: int = 0,
    limit: int = 20,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get my assigned bookings

    - View all jobs assigned to me
    - Filter by status (pending, confirmed, in_progress, completed, cancelled)
    """
    if current_user.role != UserRole.TECHNICIAN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only technicians can access this endpoint"
        )

    technician = db.query(Technician).filter(
        Technician.user_id == current_user.id
    ).first()

    if not technician:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Technician profile not found"
        )

    query = db.query(ServiceBooking).filter(
        ServiceBooking.technician_id == technician.id
    )

    if status_filter:
        query = query.filter(ServiceBooking.status == status_filter)

    bookings = query.order_by(
        ServiceBooking.created_at.desc()
    ).offset(skip).limit(limit).all()

    return bookings


@router.put("/me/bookings/{booking_id}/status")
async def update_booking_status(
    booking_id: int,
    new_status: str,
    notes: str = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update booking status

    - Update status: confirmed, in_progress, completed
    - Add notes about the service
    """
    if current_user.role != UserRole.TECHNICIAN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only technicians can access this endpoint"
        )

    technician = db.query(Technician).filter(
        Technician.user_id == current_user.id
    ).first()

    if not technician:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Technician profile not found"
        )

    booking = db.query(ServiceBooking).filter(
        ServiceBooking.id == booking_id,
        ServiceBooking.technician_id == technician.id
    ).first()

    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found or not assigned to you"
        )

    # Validate status transition
    valid_statuses = ["confirmed", "in_progress", "completed"]
    if new_status not in valid_statuses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
        )

    booking.status = new_status

    if new_status == "completed":
        booking.completed_at = datetime.utcnow()
        # Update technician stats
        technician.total_jobs += 1

    if notes:
        booking.technician_notes = notes

    db.commit()

    return {"message": f"Booking status updated to {new_status}"}


@router.get("/me/earnings", response_model=TechnicianEarnings)
async def get_my_earnings(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get earnings dashboard

    - Total earnings
    - Pending payout
    - Monthly statistics
    - Average rating
    """
    if current_user.role != UserRole.TECHNICIAN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only technicians can access this endpoint"
        )

    technician = db.query(Technician).filter(
        Technician.user_id == current_user.id
    ).first()

    if not technician:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Technician profile not found"
        )

    # Calculate total earnings from completed bookings
    total_earnings_result = db.query(
        func.sum(ServiceBooking.total_price)
    ).filter(
        ServiceBooking.technician_id == technician.id,
        ServiceBooking.status == "completed",
        ServiceBooking.payment_status == "paid"
    ).scalar()

    total_earnings = total_earnings_result or Decimal("0.0")

    # Calculate pending payout (completed but not paid out)
    pending_result = db.query(
        func.sum(ServiceBooking.total_price)
    ).filter(
        ServiceBooking.technician_id == technician.id,
        ServiceBooking.status == "completed",
        ServiceBooking.payment_status == "paid",
        # Add condition for payout_status if you have it
    ).scalar()

    pending_payout = pending_result or Decimal("0.0")

    # This month earnings
    current_month = datetime.utcnow().month
    current_year = datetime.utcnow().year

    month_earnings_result = db.query(
        func.sum(ServiceBooking.total_price)
    ).filter(
        ServiceBooking.technician_id == technician.id,
        ServiceBooking.status == "completed",
        ServiceBooking.payment_status == "paid",
        extract('month', ServiceBooking.completed_at) == current_month,
        extract('year', ServiceBooking.completed_at) == current_year
    ).scalar()

    this_month_earnings = month_earnings_result or Decimal("0.0")

    # This month jobs count
    month_jobs = db.query(ServiceBooking).filter(
        ServiceBooking.technician_id == technician.id,
        ServiceBooking.status == "completed",
        extract('month', ServiceBooking.completed_at) == current_month,
        extract('year', ServiceBooking.completed_at) == current_year
    ).count()

    return TechnicianEarnings(
        total_earnings=total_earnings,
        pending_payout=pending_payout,
        completed_jobs=technician.total_jobs,
        this_month_earnings=this_month_earnings,
        this_month_jobs=month_jobs,
        average_rating=technician.rating
    )


@router.post("/me/documents")
async def upload_document(
    document_type: str,
    document_url: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Upload certification document

    - Upload Ghana Card, certifications, licenses
    - Use /uploads/verification endpoint first to get URL
    - Then submit URL here
    """
    if current_user.role != UserRole.TECHNICIAN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only technicians can access this endpoint"
        )

    technician = db.query(Technician).filter(
        Technician.user_id == current_user.id
    ).first()

    if not technician:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Technician profile not found"
        )

    # Add document to certifications list
    if technician.certifications is None:
        technician.certifications = []

    technician.certifications.append({
        "type": document_type,
        "url": document_url,
        "uploaded_at": datetime.utcnow().isoformat()
    })

    # Mark as modified for JSON field
    from sqlalchemy import orm
    orm.attributes.flag_modified(technician, "certifications")

    db.commit()

    return {"message": "Document uploaded successfully"}
