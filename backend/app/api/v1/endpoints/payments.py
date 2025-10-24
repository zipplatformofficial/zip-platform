"""Payment endpoints"""
from fastapi import APIRouter, Depends, HTTPException, Header, Request, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.core.database import get_db
from app.api.v1.deps import get_current_user
from app.models.user import User
from app.models.payment import Payment
from app.services.paystack_service import paystack_service
from app.schemas.payment import (
    PaymentInitializeRequest,
    PaymentInitializeResponse,
    PaymentVerifyResponse,
    RefundRequest,
    RefundResponse,
    TransferRecipientRequest,
    TransferRecipientResponse,
    TransferRequest,
    TransferResponse,
    BanksResponse,
    PaymentWebhookEvent,
    PaymentHistoryResponse
)

router = APIRouter()


@router.post("/initialize", response_model=PaymentInitializeResponse)
async def initialize_payment(
    request: PaymentInitializeRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Initialize a payment transaction

    - Creates payment record in database
    - Initializes Paystack transaction
    - Returns authorization URL for customer to complete payment
    """
    # Check if reference already exists
    existing_payment = db.query(Payment).filter(
        Payment.reference == request.reference
    ).first()

    if existing_payment:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Payment reference already exists"
        )

    # Initialize payment with Paystack
    result = paystack_service.initialize_transaction(
        email=request.email,
        amount=request.amount,
        reference=request.reference,
        callback_url=request.callback_url,
        metadata=request.metadata,
        channels=[ch.value for ch in request.channels] if request.channels else None
    )

    if not result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get("message", "Failed to initialize payment")
        )

    # Create payment record
    payment = Payment(
        user_id=current_user.id,
        amount=request.amount,
        currency="GHS",
        reference=request.reference,
        payment_method="paystack",
        status="pending",
        metadata=request.metadata
    )
    db.add(payment)
    db.commit()
    db.refresh(payment)

    return PaymentInitializeResponse(**result)


@router.get("/verify/{reference}", response_model=PaymentVerifyResponse)
async def verify_payment(
    reference: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Verify a payment transaction

    - Verifies payment with Paystack
    - Updates payment record in database
    - Returns payment details
    """
    # Get payment from database
    payment = db.query(Payment).filter(
        Payment.reference == reference,
        Payment.user_id == current_user.id
    ).first()

    if not payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found"
        )

    # Verify with Paystack
    result = paystack_service.verify_transaction(reference)

    if not result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get("message", "Verification failed")
        )

    # Update payment record
    if result.get("status") == "success":
        payment.status = "success"
        payment.payment_method = result.get("channel", "paystack")
        payment.paid_at = datetime.utcnow()
    else:
        payment.status = "failed"

    db.commit()
    db.refresh(payment)

    return PaymentVerifyResponse(**result)


@router.post("/webhook")
async def payment_webhook(
    request: Request,
    x_paystack_signature: str = Header(None),
    db: Session = Depends(get_db)
):
    """
    Handle Paystack webhook events

    - Verifies webhook signature
    - Processes payment events (charge.success, transfer.success, etc.)
    - Updates payment records automatically

    Note: This endpoint should be configured in your Paystack dashboard
    """
    if not x_paystack_signature:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing webhook signature"
        )

    # Get raw body for signature verification
    body = await request.body()

    # Verify signature
    is_valid = paystack_service.verify_webhook_signature(
        body,
        x_paystack_signature
    )

    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid webhook signature"
        )

    # Parse event
    event_data = await request.json()
    event = event_data.get("event")
    data = event_data.get("data", {})

    # Handle different event types
    if event == "charge.success":
        # Payment succeeded
        reference = data.get("reference")
        payment = db.query(Payment).filter(
            Payment.reference == reference
        ).first()

        if payment:
            payment.status = "success"
            payment.payment_method = data.get("channel", "paystack")
            payment.paid_at = datetime.utcnow()
            payment.metadata = payment.metadata or {}
            payment.metadata["paystack_data"] = data
            db.commit()

    elif event == "transfer.success":
        # Transfer succeeded (for payouts)
        reference = data.get("reference")
        payment = db.query(Payment).filter(
            Payment.reference == reference
        ).first()

        if payment:
            payment.status = "success"
            payment.paid_at = datetime.utcnow()
            db.commit()

    elif event == "transfer.failed":
        # Transfer failed
        reference = data.get("reference")
        payment = db.query(Payment).filter(
            Payment.reference == reference
        ).first()

        if payment:
            payment.status = "failed"
            db.commit()

    return {"status": "success", "message": "Webhook processed"}


@router.post("/refund", response_model=RefundResponse)
async def request_refund(
    request: RefundRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Initiate a refund for a payment

    - Verifies payment belongs to user
    - Initiates refund with Paystack
    - Updates payment record
    - Supports partial and full refunds
    """
    # Get payment from database
    payment = db.query(Payment).filter(
        Payment.reference == request.transaction_reference,
        Payment.user_id == current_user.id
    ).first()

    if not payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found"
        )

    if payment.status != "success":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only successful payments can be refunded"
        )

    if payment.status == "refunded":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Payment already refunded"
        )

    # Initiate refund
    result = paystack_service.initiate_refund(
        transaction_reference=request.transaction_reference,
        amount=request.amount,
        merchant_note=request.merchant_note
    )

    if not result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get("message", "Refund failed")
        )

    # Update payment record
    payment.status = "refunded"
    payment.metadata = payment.metadata or {}
    payment.metadata["refund_note"] = request.merchant_note
    payment.metadata["refund_amount"] = float(request.amount) if request.amount else float(payment.amount)
    db.commit()

    return RefundResponse(**result)


@router.get("/history", response_model=List[PaymentHistoryResponse])
async def get_payment_history(
    skip: int = 0,
    limit: int = 20,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get payment history for current user

    - Returns paginated list of user's payments
    - Includes payment status, amount, and metadata
    """
    payments = db.query(Payment).filter(
        Payment.user_id == current_user.id
    ).order_by(Payment.created_at.desc()).offset(skip).limit(limit).all()

    return [
        PaymentHistoryResponse(
            id=p.id,
            reference=p.reference,
            amount=p.amount,
            currency=p.currency,
            status=p.status,
            payment_method=p.payment_method,
            created_at=p.created_at,
            metadata=p.metadata
        )
        for p in payments
    ]


@router.post("/recipient", response_model=TransferRecipientResponse)
async def create_transfer_recipient(
    request: TransferRecipientRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Create a transfer recipient for payouts

    - Used by technicians and vendors to receive payments
    - Creates recipient in Paystack
    - Returns recipient code for future transfers

    Requires admin or service provider role
    """
    # Check if user is authorized (technician or vendor)
    if current_user.role not in ["TECHNICIAN", "VENDOR", "ADMIN"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only service providers can create transfer recipients"
        )

    result = paystack_service.create_transfer_recipient(
        account_number=request.account_number,
        bank_code=request.bank_code,
        name=request.name,
        currency=request.currency
    )

    if not result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get("message", "Failed to create recipient")
        )

    return TransferRecipientResponse(**result)


@router.post("/transfer", response_model=TransferResponse)
async def initiate_transfer(
    request: TransferRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Initiate a transfer (payout) to a recipient

    - Admin only endpoint
    - Transfers funds to technicians/vendors
    - Creates payment record with negative amount

    Requires admin role
    """
    if current_user.role != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only administrators can initiate transfers"
        )

    # Check if reference already exists
    existing_payment = db.query(Payment).filter(
        Payment.reference == request.reference
    ).first()

    if existing_payment:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Transfer reference already exists"
        )

    result = paystack_service.initiate_transfer(
        recipient_code=request.recipient_code,
        amount=request.amount,
        reference=request.reference,
        reason=request.reason
    )

    if not result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get("message", "Transfer failed")
        )

    # Create payment record (negative amount for payout)
    payment = Payment(
        user_id=current_user.id,
        amount=-request.amount,  # Negative for payout
        currency="GHS",
        reference=request.reference,
        payment_method="paystack_transfer",
        status="processing",
        metadata={
            "recipient_code": request.recipient_code,
            "reason": request.reason
        }
    )
    db.add(payment)
    db.commit()

    return TransferResponse(**result)


@router.get("/banks", response_model=BanksResponse)
async def get_banks(
    country: str = "ghana",
    current_user: User = Depends(get_current_user)
):
    """
    Get list of supported banks

    - Returns banks available for transfers
    - Used when creating transfer recipients
    """
    result = paystack_service.get_banks(country)

    if not result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get("message", "Failed to fetch banks")
        )

    return BanksResponse(**result)
