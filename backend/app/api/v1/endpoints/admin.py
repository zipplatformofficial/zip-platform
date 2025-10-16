"""Admin endpoints for managing all platform entities"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.api.v1.deps import get_db, require_admin
from app.models.user import User, UserRole
from app.models.maintenance import ServiceBooking, MaintenanceService, Technician
from app.models.rental import RentalBooking, RentalVehicle
from app.models.store import Order, Product, Vendor
from app.schemas.user import UserResponse, UserUpdate
from app.schemas.maintenance import ServiceBookingResponse, TechnicianResponse
from app.schemas.rental import RentalBookingResponse
from app.schemas.store import OrderResponse


router = APIRouter()


# ==================== USER MANAGEMENT ====================

@router.get("/users", response_model=List[UserResponse])
async def list_all_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    role: Optional[UserRole] = None,
    is_active: Optional[bool] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """List all users (Admin only)"""
    query = db.query(User)

    if role:
        query = query.filter(User.role == role)

    if is_active is not None:
        query = query.filter(User.is_active == is_active)

    users = query.order_by(User.created_at.desc()).offset(skip).limit(limit).all()
    return users


@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user_by_id(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Get a specific user by ID (Admin only)"""
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return user


@router.put("/users/{user_id}", response_model=UserResponse)
async def update_user_by_admin(
    user_id: str,
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Update any user (Admin only)"""
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    update_data = user_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)

    return user


@router.post("/users/{user_id}/activate")
async def activate_user(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Activate a user account (Admin only)"""
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    user.is_active = True
    db.commit()

    return {"message": f"User {user.email} activated successfully"}


@router.post("/users/{user_id}/deactivate")
async def deactivate_user(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Deactivate a user account (Admin only)"""
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    user.is_active = False
    db.commit()

    return {"message": f"User {user.email} deactivated successfully"}


# ==================== BOOKINGS MANAGEMENT ====================

@router.get("/maintenance/bookings", response_model=List[ServiceBookingResponse])
async def list_all_service_bookings(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """List all service bookings (Admin only)"""
    bookings = db.query(ServiceBooking).order_by(
        ServiceBooking.created_at.desc()
    ).offset(skip).limit(limit).all()

    return bookings


@router.get("/rentals/bookings", response_model=List[RentalBookingResponse])
async def list_all_rental_bookings(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """List all rental bookings (Admin only)"""
    bookings = db.query(RentalBooking).order_by(
        RentalBooking.created_at.desc()
    ).offset(skip).limit(limit).all()

    return bookings


@router.get("/store/orders", response_model=List[OrderResponse])
async def list_all_orders(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """List all store orders (Admin only)"""
    orders = db.query(Order).order_by(
        Order.created_at.desc()
    ).offset(skip).limit(limit).all()

    return orders


# ==================== TECHNICIANS MANAGEMENT ====================

@router.get("/technicians", response_model=List[TechnicianResponse])
async def list_all_technicians(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """List all technicians (Admin only)"""
    technicians = db.query(Technician).offset(skip).limit(limit).all()
    return technicians


@router.post("/technicians/{technician_id}/verify")
async def verify_technician(
    technician_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Verify a technician (Admin only)"""
    technician = db.query(Technician).filter(Technician.id == technician_id).first()

    if not technician:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Technician not found"
        )

    technician.is_verified = True
    db.commit()

    return {"message": "Technician verified successfully"}


# ==================== VENDORS MANAGEMENT ====================

@router.post("/vendors/{vendor_id}/verify")
async def verify_vendor(
    vendor_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Verify a vendor (Admin only)"""
    vendor = db.query(Vendor).filter(Vendor.id == vendor_id).first()

    if not vendor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vendor not found"
        )

    vendor.is_verified = True
    db.commit()

    return {"message": "Vendor verified successfully"}


@router.post("/vendors/{vendor_id}/deactivate")
async def deactivate_vendor(
    vendor_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Deactivate a vendor (Admin only)"""
    vendor = db.query(Vendor).filter(Vendor.id == vendor_id).first()

    if not vendor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vendor not found"
        )

    vendor.is_active = False
    db.commit()

    return {"message": "Vendor deactivated successfully"}


# ==================== ANALYTICS & STATISTICS ====================

@router.get("/stats/overview")
async def get_platform_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Get platform-wide statistics (Admin only)"""
    total_users = db.query(User).count()
    active_users = db.query(User).filter(User.is_active == True).count()

    total_service_bookings = db.query(ServiceBooking).count()
    total_rental_bookings = db.query(RentalBooking).count()
    total_orders = db.query(Order).count()

    total_products = db.query(Product).count()
    total_vehicles = db.query(RentalVehicle).count()
    total_services = db.query(MaintenanceService).count()

    total_technicians = db.query(Technician).count()
    verified_technicians = db.query(Technician).filter(Technician.is_verified == True).count()

    total_vendors = db.query(Vendor).count()
    verified_vendors = db.query(Vendor).filter(Vendor.is_verified == True).count()

    return {
        "users": {
            "total": total_users,
            "active": active_users
        },
        "bookings": {
            "service_bookings": total_service_bookings,
            "rental_bookings": total_rental_bookings,
            "store_orders": total_orders,
            "total": total_service_bookings + total_rental_bookings + total_orders
        },
        "catalog": {
            "products": total_products,
            "rental_vehicles": total_vehicles,
            "maintenance_services": total_services
        },
        "providers": {
            "technicians": {
                "total": total_technicians,
                "verified": verified_technicians
            },
            "vendors": {
                "total": total_vendors,
                "verified": verified_vendors
            }
        }
    }
