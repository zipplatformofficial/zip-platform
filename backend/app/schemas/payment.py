"""Payment schemas"""
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, Dict, Any, List
from decimal import Decimal
from datetime import datetime
from enum import Enum


class PaymentMethodEnum(str, Enum):
    """Payment method types"""
    CARD = "card"
    MOBILE_MONEY = "mobile_money"
    BANK_TRANSFER = "bank_transfer"
    BANK = "bank"


class PaymentStatusEnum(str, Enum):
    """Payment status types"""
    PENDING = "pending"
    SUCCESS = "success"
    FAILED = "failed"
    PROCESSING = "processing"
    REFUNDED = "refunded"


class PaymentInitializeRequest(BaseModel):
    """Request schema for initializing payment"""
    email: EmailStr = Field(..., description="Customer email address")
    amount: Decimal = Field(..., gt=0, description="Amount to charge in cedis")
    reference: str = Field(..., min_length=8, description="Unique payment reference")
    callback_url: Optional[str] = Field(None, description="URL to redirect after payment")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional data")
    channels: Optional[List[PaymentMethodEnum]] = Field(
        None,
        description="Allowed payment channels"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "email": "customer@example.com",
                "amount": 150.00,
                "reference": "PAY_12345678",
                "callback_url": "https://app.zipghana.com/payment/callback",
                "metadata": {
                    "booking_id": 123,
                    "service_type": "maintenance"
                },
                "channels": ["card", "mobile_money"]
            }
        }


class PaymentInitializeResponse(BaseModel):
    """Response schema for payment initialization"""
    success: bool
    authorization_url: Optional[str] = None
    access_code: Optional[str] = None
    reference: Optional[str] = None
    message: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "authorization_url": "https://checkout.paystack.com/abc123",
                "access_code": "abc123xyz",
                "reference": "PAY_12345678"
            }
        }


class PaymentVerifyResponse(BaseModel):
    """Response schema for payment verification"""
    success: bool
    status: Optional[str] = None
    reference: Optional[str] = None
    amount: Optional[Decimal] = None
    currency: Optional[str] = None
    channel: Optional[str] = None
    paid_at: Optional[str] = None
    customer: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None
    message: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "status": "success",
                "reference": "PAY_12345678",
                "amount": 150.00,
                "currency": "GHS",
                "channel": "card",
                "paid_at": "2025-01-15T10:30:00Z",
                "customer": {
                    "email": "customer@example.com"
                },
                "metadata": {
                    "booking_id": 123
                }
            }
        }


class RefundRequest(BaseModel):
    """Request schema for refund"""
    transaction_reference: str = Field(..., description="Original transaction reference")
    amount: Optional[Decimal] = Field(None, gt=0, description="Amount to refund (partial). If not provided, full refund")
    merchant_note: Optional[str] = Field(None, max_length=500, description="Reason for refund")

    class Config:
        json_schema_extra = {
            "example": {
                "transaction_reference": "PAY_12345678",
                "amount": 50.00,
                "merchant_note": "Customer requested partial refund due to service delay"
            }
        }


class RefundResponse(BaseModel):
    """Response schema for refund"""
    success: bool
    refund_id: Optional[int] = None
    status: Optional[str] = None
    message: Optional[str] = None


class TransferRecipientRequest(BaseModel):
    """Request schema for creating transfer recipient"""
    account_number: str = Field(..., min_length=10, max_length=10, description="Bank account number")
    bank_code: str = Field(..., description="Bank code from Paystack banks list")
    name: str = Field(..., min_length=2, max_length=100, description="Account holder name")
    currency: str = Field(default="GHS", description="Currency code")

    class Config:
        json_schema_extra = {
            "example": {
                "account_number": "0123456789",
                "bank_code": "GH180101",
                "name": "John Doe",
                "currency": "GHS"
            }
        }


class TransferRecipientResponse(BaseModel):
    """Response schema for transfer recipient"""
    success: bool
    recipient_code: Optional[str] = None
    details: Optional[Dict[str, Any]] = None
    message: Optional[str] = None


class TransferRequest(BaseModel):
    """Request schema for initiating transfer"""
    recipient_code: str = Field(..., description="Recipient code from create recipient")
    amount: Decimal = Field(..., gt=0, description="Amount to transfer")
    reference: str = Field(..., min_length=8, description="Unique transfer reference")
    reason: Optional[str] = Field(None, max_length=200, description="Transfer description")

    class Config:
        json_schema_extra = {
            "example": {
                "recipient_code": "RCP_abc123xyz",
                "amount": 500.00,
                "reference": "TRF_12345678",
                "reason": "Service payment for booking #123"
            }
        }


class TransferResponse(BaseModel):
    """Response schema for transfer"""
    success: bool
    transfer_code: Optional[str] = None
    status: Optional[str] = None
    reference: Optional[str] = None
    message: Optional[str] = None


class BankInfo(BaseModel):
    """Bank information schema"""
    id: int
    name: str
    slug: str
    code: str
    country: str
    currency: str
    type: str
    active: bool


class BanksResponse(BaseModel):
    """Response schema for banks list"""
    success: bool
    banks: Optional[List[BankInfo]] = None
    message: Optional[str] = None


class PaymentWebhookEvent(BaseModel):
    """Paystack webhook event schema"""
    event: str = Field(..., description="Event type (charge.success, transfer.success, etc.)")
    data: Dict[str, Any] = Field(..., description="Event data")

    class Config:
        json_schema_extra = {
            "example": {
                "event": "charge.success",
                "data": {
                    "reference": "PAY_12345678",
                    "amount": 15000,
                    "status": "success",
                    "customer": {
                        "email": "customer@example.com"
                    }
                }
            }
        }


class PaymentHistoryResponse(BaseModel):
    """Payment history item"""
    id: int
    reference: str
    amount: Decimal
    currency: str
    status: str
    payment_method: str
    created_at: datetime
    metadata: Optional[Dict[str, Any]] = None

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "reference": "PAY_12345678",
                "amount": 150.00,
                "currency": "GHS",
                "status": "success",
                "payment_method": "card",
                "created_at": "2025-01-15T10:30:00Z",
                "metadata": {
                    "booking_id": 123
                }
            }
        }
