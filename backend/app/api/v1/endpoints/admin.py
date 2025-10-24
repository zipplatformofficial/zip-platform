"""Admin endpoints for managing all platform entities"""
from typing import List, Optional
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_

from app.api.v1.deps import get_db, require_admin
from app.models.user import User, UserRole
from app.models.maintenance import ServiceBooking, MaintenanceService, Technician
from app.models.rental import RentalBooking, RentalVehicle
from app.models.store import Order, Product, Vendor
from app.models.application import RoleApplication, ApplicationStatus
from app.models.payment import Payment, PaymentStatus
from app.models.fraud import FraudAlert, FraudStatus
from app.models.analytics import AnalyticsEvent, DailyStats, EventType
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
    """Get comprehensive platform-wide statistics (Admin only)"""

    # Calculate date ranges
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)
    last_7_days = today - timedelta(days=7)
    last_30_days = today - timedelta(days=30)

    # ==================== USERS ====================
    total_users = db.query(User).count()
    active_users = db.query(User).filter(User.is_active == True).count()
    verified_users = db.query(User).filter(User.is_verified == True).count()

    # New users today
    new_users_today = db.query(User).filter(
        func.date(User.created_at) == str(today)
    ).count()

    # Users by role
    users_by_role = {}
    for role in UserRole:
        count = db.query(User).filter(User.role == role).count()
        users_by_role[role.value] = count

    # ==================== VISITORS & ANALYTICS ====================
    total_visitors = db.query(AnalyticsEvent.session_id).distinct().count()

    # Today's visitors
    today_visitors = db.query(AnalyticsEvent.session_id).filter(
        func.date(AnalyticsEvent.created_at) == str(today)
    ).distinct().count()

    # Page views
    total_page_views = db.query(AnalyticsEvent).filter(
        AnalyticsEvent.event_type == EventType.PAGE_VIEW
    ).count()

    # Today's page views
    today_page_views = db.query(AnalyticsEvent).filter(
        and_(
            AnalyticsEvent.event_type == EventType.PAGE_VIEW,
            func.date(AnalyticsEvent.created_at) == str(today)
        )
    ).count()

    # ==================== BOOKINGS & ORDERS ====================
    total_service_bookings = db.query(ServiceBooking).count()
    total_rental_bookings = db.query(RentalBooking).count()
    total_orders = db.query(Order).count()

    # Today's bookings
    today_service_bookings = db.query(ServiceBooking).filter(
        func.date(ServiceBooking.created_at) == str(today)
    ).count()
    today_rental_bookings = db.query(RentalBooking).filter(
        func.date(RentalBooking.created_at) == str(today)
    ).count()
    today_orders = db.query(Order).filter(
        func.date(Order.created_at) == str(today)
    ).count()

    # ==================== REVENUE & PAYMENTS ====================
    # Total revenue from completed payments
    total_revenue_result = db.query(func.sum(Payment.amount)).filter(
        Payment.status == PaymentStatus.COMPLETED
    ).scalar()
    total_revenue = float(total_revenue_result) if total_revenue_result else 0.0

    # Today's revenue
    today_revenue_result = db.query(func.sum(Payment.amount)).filter(
        and_(
            Payment.status == PaymentStatus.COMPLETED,
            func.date(Payment.completed_at) == str(today)
        )
    ).scalar()
    today_revenue = float(today_revenue_result) if today_revenue_result else 0.0

    # Platform commission
    platform_commission_result = db.query(func.sum(Payment.platform_fee)).filter(
        Payment.status == PaymentStatus.COMPLETED
    ).scalar()
    platform_commission = float(platform_commission_result) if platform_commission_result else 0.0

    # Payment success rate
    total_payments = db.query(Payment).count()
    successful_payments = db.query(Payment).filter(
        Payment.status == PaymentStatus.COMPLETED
    ).count()
    payment_success_rate = (successful_payments / total_payments * 100) if total_payments > 0 else 0

    # Failed payments today
    failed_payments_today = db.query(Payment).filter(
        and_(
            Payment.status == PaymentStatus.FAILED,
            func.date(Payment.created_at) == str(today)
        )
    ).count()

    # ==================== CATALOG ====================
    total_products = db.query(Product).count()
    total_vehicles = db.query(RentalVehicle).count()
    total_services = db.query(MaintenanceService).count()

    # Active products
    active_products = db.query(Product).filter(Product.is_active == True).count()
    active_vehicles = db.query(RentalVehicle).filter(RentalVehicle.is_available == True).count()

    # ==================== PROVIDERS ====================
    total_technicians = db.query(Technician).count()
    verified_technicians = db.query(Technician).filter(Technician.is_verified == True).count()

    total_vendors = db.query(Vendor).count()
    verified_vendors = db.query(Vendor).filter(Vendor.is_verified == True).count()

    # Active providers today
    active_technicians_today = db.query(Technician).filter(
        and_(
            Technician.is_verified == True,
            Technician.is_available == True
        )
    ).count()

    # ==================== APPLICATIONS ====================
    total_applications = db.query(RoleApplication).count()
    pending_applications = db.query(RoleApplication).filter(
        RoleApplication.status == ApplicationStatus.PENDING
    ).count()
    under_review_applications = db.query(RoleApplication).filter(
        RoleApplication.status == ApplicationStatus.UNDER_REVIEW
    ).count()
    approved_applications = db.query(RoleApplication).filter(
        RoleApplication.status == ApplicationStatus.APPROVED
    ).count()
    rejected_applications = db.query(RoleApplication).filter(
        RoleApplication.status == ApplicationStatus.REJECTED
    ).count()

    # New applications today
    new_applications_today = db.query(RoleApplication).filter(
        func.date(RoleApplication.created_at) == str(today)
    ).count()

    # ==================== FRAUD DETECTION ====================
    total_fraud_alerts = db.query(FraudAlert).count()

    # Active fraud alerts (detected, under review)
    active_fraud_alerts = db.query(FraudAlert).filter(
        or_(
            FraudAlert.status == FraudStatus.DETECTED,
            FraudAlert.status == FraudStatus.UNDER_REVIEW
        )
    ).count()

    # Confirmed fraud cases
    confirmed_fraud = db.query(FraudAlert).filter(
        FraudAlert.status == FraudStatus.CONFIRMED
    ).count()

    # Fraud alerts today
    fraud_alerts_today = db.query(FraudAlert).filter(
        func.date(FraudAlert.created_at) == str(today)
    ).count()

    # Total amount involved in fraud
    fraud_amount_result = db.query(func.sum(FraudAlert.amount_involved)).filter(
        FraudAlert.status == FraudStatus.CONFIRMED
    ).scalar()
    total_fraud_amount = float(fraud_amount_result) if fraud_amount_result else 0.0

    # Fraud by type
    fraud_by_type = {}
    fraud_types = db.query(
        FraudAlert.fraud_type,
        func.count(FraudAlert.id)
    ).group_by(FraudAlert.fraud_type).all()

    for fraud_type, count in fraud_types:
        fraud_by_type[fraud_type.value] = count

    # Fraud blocked amount
    blocked_amount_result = db.query(func.sum(FraudAlert.amount_involved)).filter(
        FraudAlert.auto_blocked == True
    ).scalar()
    fraud_blocked_amount = float(blocked_amount_result) if blocked_amount_result else 0.0

    # ==================== RECENT ACTIVITY ====================
    # Last 10 recent activities (payments, bookings, applications)
    recent_payments = db.query(Payment).order_by(
        Payment.created_at.desc()
    ).limit(5).all()

    recent_applications = db.query(RoleApplication).order_by(
        RoleApplication.created_at.desc()
    ).limit(5).all()

    recent_fraud_alerts = db.query(FraudAlert).order_by(
        FraudAlert.created_at.desc()
    ).limit(5).all()

    # ==================== SYSTEM HEALTH ====================
    # Database health indicators
    system_health = {
        "status": "healthy",
        "total_records": total_users + total_products + total_vehicles + total_services,
        "database_size_mb": 0,  # Would need to query database size
        "active_sessions": total_visitors,
        "error_rate": 0.0,  # Would track from error logs
    }

    # ==================== TRENDS (Last 7 Days) ====================
    # Daily stats for last 7 days
    daily_stats = db.query(DailyStats).filter(
        DailyStats.date >= str(last_7_days)
    ).order_by(DailyStats.date.asc()).all()

    trends = {
        "dates": [stat.date for stat in daily_stats],
        "revenue": [stat.total_revenue for stat in daily_stats],
        "users": [stat.active_users for stat in daily_stats],
        "visitors": [stat.total_visitors for stat in daily_stats],
        "bookings": [stat.service_bookings + stat.rental_bookings + stat.store_orders for stat in daily_stats],
        "fraud_alerts": [stat.fraud_alerts for stat in daily_stats],
    }

    return {
        "users": {
            "total": total_users,
            "active": active_users,
            "verified": verified_users,
            "new_today": new_users_today,
            "by_role": users_by_role
        },
        "visitors": {
            "total": total_visitors,
            "today": today_visitors,
            "total_page_views": total_page_views,
            "today_page_views": today_page_views
        },
        "bookings": {
            "service_bookings": {
                "total": total_service_bookings,
                "today": today_service_bookings
            },
            "rental_bookings": {
                "total": total_rental_bookings,
                "today": today_rental_bookings
            },
            "store_orders": {
                "total": total_orders,
                "today": today_orders
            },
            "total": total_service_bookings + total_rental_bookings + total_orders,
            "today_total": today_service_bookings + today_rental_bookings + today_orders
        },
        "revenue": {
            "total": total_revenue,
            "today": today_revenue,
            "platform_commission": platform_commission,
            "currency": "GHS"
        },
        "payments": {
            "total": total_payments,
            "successful": successful_payments,
            "success_rate": round(payment_success_rate, 2),
            "failed_today": failed_payments_today
        },
        "catalog": {
            "products": {
                "total": total_products,
                "active": active_products
            },
            "rental_vehicles": {
                "total": total_vehicles,
                "available": active_vehicles
            },
            "maintenance_services": total_services
        },
        "providers": {
            "technicians": {
                "total": total_technicians,
                "verified": verified_technicians,
                "active_today": active_technicians_today
            },
            "vendors": {
                "total": total_vendors,
                "verified": verified_vendors
            }
        },
        "applications": {
            "total": total_applications,
            "pending": pending_applications,
            "under_review": under_review_applications,
            "approved": approved_applications,
            "rejected": rejected_applications,
            "new_today": new_applications_today
        },
        "fraud": {
            "total_alerts": total_fraud_alerts,
            "active_alerts": active_fraud_alerts,
            "confirmed_cases": confirmed_fraud,
            "alerts_today": fraud_alerts_today,
            "total_amount_involved": total_fraud_amount,
            "blocked_amount": fraud_blocked_amount,
            "by_type": fraud_by_type
        },
        "recent_activity": {
            "payments": [
                {
                    "id": p.id,
                    "amount": p.amount,
                    "status": p.status.value,
                    "method": p.payment_method.value,
                    "created_at": p.created_at
                } for p in recent_payments
            ],
            "applications": [
                {
                    "id": a.id,
                    "user_id": a.user_id,
                    "role": a.desired_role.value,
                    "status": a.status.value,
                    "created_at": a.created_at
                } for a in recent_applications
            ],
            "fraud_alerts": [
                {
                    "id": f.id,
                    "type": f.fraud_type.value,
                    "severity": f.severity,
                    "amount": f.amount_involved,
                    "status": f.status.value,
                    "created_at": f.created_at
                } for f in recent_fraud_alerts
            ]
        },
        "system_health": system_health,
        "trends": trends
    }
