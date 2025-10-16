"""User management endpoints"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.v1.deps import get_db, get_current_active_user
from app.core.security import get_password_hash, verify_password
from app.models.user import User
from app.schemas.user import UserResponse, UserUpdate
from pydantic import BaseModel


router = APIRouter()


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
