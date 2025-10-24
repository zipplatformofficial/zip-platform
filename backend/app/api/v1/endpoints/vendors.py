"""Vendor portal endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from typing import List
from datetime import datetime
from decimal import Decimal

from app.core.database import get_db
from app.api.v1.deps import get_current_user
from app.core.security import get_password_hash
from app.models.user import User, UserRole
from app.models.store import Vendor, Product, Order, OrderItem
from app.schemas.vendor import (
    VendorRegister,
    VendorProfileUpdate,
    VendorResponse,
    VendorAnalytics,
    PayoutRequest
)
from app.schemas.store import ProductResponse, OrderResponse
from app.services.paystack_service import paystack_service

router = APIRouter()


@router.post("/register", response_model=VendorResponse, status_code=status.HTTP_201_CREATED)
async def register_vendor(
    registration: VendorRegister,
    db: Session = Depends(get_db)
):
    """
    Register as a vendor

    - Creates user account with VENDOR role
    - Creates vendor profile
    - Requires verification before selling
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
        full_name=registration.contact_person,
        phone=registration.phone,
        role=UserRole.VENDOR,
        is_active=True,
        email_verified=False
    )
    db.add(user)
    db.flush()

    # Create vendor profile
    vendor = Vendor(
        user_id=user.id,
        business_name=registration.business_name,
        business_registration_number=registration.business_registration_number,
        contact_person=registration.contact_person,
        address=registration.address,
        rating=Decimal("0.0"),
        total_sales=0,
        is_verified=False
    )
    db.add(vendor)
    db.commit()
    db.refresh(vendor)

    return vendor


@router.get("/me", response_model=VendorResponse)
async def get_my_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get my vendor profile"""
    if current_user.role != UserRole.VENDOR:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only vendors can access this endpoint"
        )

    vendor = db.query(Vendor).filter(
        Vendor.user_id == current_user.id
    ).first()

    if not vendor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vendor profile not found"
        )

    return vendor


@router.put("/me", response_model=VendorResponse)
async def update_my_profile(
    profile_update: VendorProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update my vendor profile"""
    if current_user.role != UserRole.VENDOR:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only vendors can access this endpoint"
        )

    vendor = db.query(Vendor).filter(
        Vendor.user_id == current_user.id
    ).first()

    if not vendor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vendor profile not found"
        )

    # Update only provided fields
    update_data = profile_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(vendor, field, value)

    db.commit()
    db.refresh(vendor)

    return vendor


@router.get("/me/products", response_model=List[ProductResponse])
async def get_my_products(
    skip: int = 0,
    limit: int = 50,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all my products"""
    if current_user.role != UserRole.VENDOR:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only vendors can access this endpoint"
        )

    vendor = db.query(Vendor).filter(
        Vendor.user_id == current_user.id
    ).first()

    if not vendor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vendor profile not found"
        )

    products = db.query(Product).filter(
        Product.vendor_id == vendor.id
    ).offset(skip).limit(limit).all()

    return products


@router.get("/me/orders", response_model=List[OrderResponse])
async def get_my_orders(
    status_filter: str = None,
    skip: int = 0,
    limit: int = 20,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get orders containing my products

    - View all orders with my products
    - Filter by status
    """
    if current_user.role != UserRole.VENDOR:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only vendors can access this endpoint"
        )

    vendor = db.query(Vendor).filter(
        Vendor.user_id == current_user.id
    ).first()

    if not vendor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vendor profile not found"
        )

    # Get orders that contain products from this vendor
    query = db.query(Order).join(OrderItem).join(Product).filter(
        Product.vendor_id == vendor.id
    ).distinct()

    if status_filter:
        query = query.filter(Order.status == status_filter)

    orders = query.order_by(
        Order.created_at.desc()
    ).offset(skip).limit(limit).all()

    return orders


@router.put("/me/orders/{order_id}/status")
async def update_order_status(
    order_id: int,
    new_status: str,
    tracking_number: str = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update order status

    - Mark as processing, shipped, delivered
    - Add tracking number for shipment
    """
    if current_user.role != UserRole.VENDOR:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only vendors can access this endpoint"
        )

    vendor = db.query(Vendor).filter(
        Vendor.user_id == current_user.id
    ).first()

    if not vendor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vendor profile not found"
        )

    # Check if order contains vendor's products
    order = db.query(Order).join(OrderItem).join(Product).filter(
        Order.id == order_id,
        Product.vendor_id == vendor.id
    ).first()

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found or doesn't contain your products"
        )

    # Validate status
    valid_statuses = ["processing", "shipped", "delivered"]
    if new_status not in valid_statuses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
        )

    order.status = new_status

    if new_status == "shipped" and tracking_number:
        order.tracking_number = tracking_number

    if new_status == "delivered":
        order.delivered_at = datetime.utcnow()
        # Update vendor stats
        vendor.total_sales += 1

    db.commit()

    return {"message": f"Order status updated to {new_status}"}


@router.get("/me/analytics", response_model=VendorAnalytics)
async def get_analytics(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get vendor analytics dashboard

    - Total revenue
    - Order statistics
    - Product counts
    - Monthly performance
    """
    if current_user.role != UserRole.VENDOR:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only vendors can access this endpoint"
        )

    vendor = db.query(Vendor).filter(
        Vendor.user_id == current_user.id
    ).first()

    if not vendor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vendor profile not found"
        )

    # Total revenue from completed orders
    total_revenue_result = db.query(
        func.sum(OrderItem.subtotal)
    ).join(Product).join(Order).filter(
        Product.vendor_id == vendor.id,
        Order.status == "delivered",
        Order.payment_status == "paid"
    ).scalar()

    total_revenue = total_revenue_result or Decimal("0.0")

    # Pending payout (delivered but not paid out to vendor)
    pending_payout = total_revenue * Decimal("0.88")  # After 12% commission

    # Order statistics
    total_orders = db.query(Order).join(OrderItem).join(Product).filter(
        Product.vendor_id == vendor.id
    ).distinct().count()

    pending_orders = db.query(Order).join(OrderItem).join(Product).filter(
        Product.vendor_id == vendor.id,
        Order.status.in_(["pending", "confirmed", "processing"])
    ).distinct().count()

    completed_orders = db.query(Order).join(OrderItem).join(Product).filter(
        Product.vendor_id == vendor.id,
        Order.status == "delivered"
    ).distinct().count()

    # This month stats
    current_month = datetime.utcnow().month
    current_year = datetime.utcnow().year

    month_revenue_result = db.query(
        func.sum(OrderItem.subtotal)
    ).join(Product).join(Order).filter(
        Product.vendor_id == vendor.id,
        Order.status == "delivered",
        extract('month', Order.delivered_at) == current_month,
        extract('year', Order.delivered_at) == current_year
    ).scalar()

    this_month_revenue = month_revenue_result or Decimal("0.0")

    month_orders = db.query(Order).join(OrderItem).join(Product).filter(
        Product.vendor_id == vendor.id,
        extract('month', Order.created_at) == current_month,
        extract('year', Order.created_at) == current_year
    ).distinct().count()

    # Product counts
    total_products = db.query(Product).filter(
        Product.vendor_id == vendor.id
    ).count()

    active_products = db.query(Product).filter(
        Product.vendor_id == vendor.id,
        Product.stock_quantity > 0,
        Product.is_active == True
    ).count()

    return VendorAnalytics(
        total_revenue=total_revenue,
        pending_payout=pending_payout,
        total_orders=total_orders,
        pending_orders=pending_orders,
        completed_orders=completed_orders,
        this_month_revenue=this_month_revenue,
        this_month_orders=month_orders,
        total_products=total_products,
        active_products=active_products,
        average_rating=vendor.rating
    )


@router.post("/me/payout")
async def request_payout(
    payout_request: PayoutRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Request payout to bank account

    - Withdraw earnings to bank account
    - Uses Paystack transfer API
    - Minimum payout: GHS 100
    """
    if current_user.role != UserRole.VENDOR:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only vendors can access this endpoint"
        )

    vendor = db.query(Vendor).filter(
        Vendor.user_id == current_user.id
    ).first()

    if not vendor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vendor profile not found"
        )

    # Minimum payout check
    if payout_request.amount < Decimal("100.0"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Minimum payout amount is GHS 100"
        )

    # Create transfer recipient in Paystack
    recipient_result = paystack_service.create_transfer_recipient(
        account_number=payout_request.bank_account_number,
        bank_code=payout_request.bank_code,
        name=payout_request.account_name
    )

    if not recipient_result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=recipient_result.get("message", "Failed to create recipient")
        )

    recipient_code = recipient_result["recipient_code"]

    # Initiate transfer
    import uuid
    transfer_reference = f"PAYOUT_{vendor.id}_{uuid.uuid4().hex[:8].upper()}"

    transfer_result = paystack_service.initiate_transfer(
        recipient_code=recipient_code,
        amount=payout_request.amount,
        reference=transfer_reference,
        reason=f"Vendor payout for {vendor.business_name}"
    )

    if not transfer_result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=transfer_result.get("message", "Transfer failed")
        )

    return {
        "message": "Payout initiated successfully",
        "reference": transfer_reference,
        "amount": float(payout_request.amount),
        "status": "processing"
    }


@router.get("/me/payout-history")
async def get_payout_history(
    skip: int = 0,
    limit: int = 20,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get payout history"""
    if current_user.role != UserRole.VENDOR:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only vendors can access this endpoint"
        )

    vendor = db.query(Vendor).filter(
        Vendor.user_id == current_user.id
    ).first()

    if not vendor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vendor profile not found"
        )

    # Get payout transactions (payments with negative amounts)
    from app.models.payment import Payment
    payouts = db.query(Payment).filter(
        Payment.user_id == current_user.id,
        Payment.payment_method == "paystack_transfer"
    ).order_by(Payment.created_at.desc()).offset(skip).limit(limit).all()

    return payouts
