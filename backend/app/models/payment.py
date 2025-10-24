"""Payment models"""
import enum
from sqlalchemy import Column, String, Integer, ForeignKey, Enum, Text, JSON, Float, Boolean
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class PaymentStatus(str, enum.Enum):
    """Payment status"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"
    PARTIALLY_REFUNDED = "partially_refunded"


class PaymentMethod(str, enum.Enum):
    """Payment methods"""
    MTN_MOBILE_MONEY = "mtn_mobile_money"
    VODAFONE_CASH = "vodafone_cash"
    AIRTELTIGO_MONEY = "airteltigo_money"
    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"
    CASH = "cash"
    BANK_TRANSFER = "bank_transfer"


class Payment(BaseModel):
    """Payment transaction"""

    __tablename__ = "payments"

    # User
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    # Transaction Details
    transaction_id = Column(String(100), unique=True, nullable=False, index=True)
    payment_reference = Column(String(100), unique=True, nullable=False, index=True)

    # Related Entity (one of these will be set)
    service_booking_id = Column(Integer, ForeignKey("service_bookings.id", ondelete="SET NULL"), nullable=True)
    rental_booking_id = Column(Integer, ForeignKey("rental_bookings.id", ondelete="SET NULL"), nullable=True)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="SET NULL"), nullable=True)

    # Payment Info
    payment_method = Column(Enum(PaymentMethod), nullable=False)
    status = Column(Enum(PaymentStatus), default=PaymentStatus.PENDING, nullable=False)

    # Amount
    amount = Column(Float, nullable=False)
    currency = Column(String(10), default="GHS", nullable=False)  # Ghana Cedis

    # Fee breakdown
    service_fee = Column(Float, default=0.0, nullable=False)
    platform_fee = Column(Float, default=0.0, nullable=False)
    payment_gateway_fee = Column(Float, default=0.0, nullable=False)

    # Provider Details (for mobile money, cards, etc.)
    provider_transaction_id = Column(String(200), nullable=True)
    provider_response = Column(JSON, nullable=True)
    phone_number = Column(String(20), nullable=True)  # For mobile money
    card_last_four = Column(String(4), nullable=True)  # For cards

    # Timestamps
    initiated_at = Column(String(50), nullable=False)
    completed_at = Column(String(50), nullable=True)
    failed_at = Column(String(50), nullable=True)

    # Refund Info
    refund_amount = Column(Float, default=0.0, nullable=False)
    refund_reason = Column(Text, nullable=True)
    refunded_at = Column(String(50), nullable=True)

    # Error handling
    error_code = Column(String(50), nullable=True)
    error_message = Column(Text, nullable=True)
    retry_count = Column(Integer, default=0, nullable=False)

    # Receipt
    receipt_url = Column(String(500), nullable=True)
    invoice_url = Column(String(500), nullable=True)

    # Metadata
    payment_metadata = Column(JSON, nullable=True)
    ip_address = Column(String(50), nullable=True)
    user_agent = Column(String(500), nullable=True)

    # Relationships
    user = relationship("User", back_populates="payments")
    service_booking = relationship("ServiceBooking", back_populates="payment")
    rental_booking = relationship("RentalBooking", back_populates="payment")
    order = relationship("Order", back_populates="payment")

    def __repr__(self):
        return f"<Payment {self.payment_reference} - {self.status}>"
