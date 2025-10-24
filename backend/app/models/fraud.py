"""Fraud detection and security tracking models"""
import enum
from sqlalchemy import Column, String, Integer, ForeignKey, Enum, Text, JSON, Float, Boolean
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class FraudType(str, enum.Enum):
    """Types of fraud detected"""
    PAYMENT_FRAUD = "payment_fraud"
    IDENTITY_FRAUD = "identity_fraud"
    ACCOUNT_TAKEOVER = "account_takeover"
    FAKE_REVIEW = "fake_review"
    DUPLICATE_ACCOUNT = "duplicate_account"
    SUSPICIOUS_ACTIVITY = "suspicious_activity"
    CHARGEBACK_FRAUD = "chargeback_fraud"
    STOLEN_CARD = "stolen_card"
    FAKE_DOCUMENT = "fake_document"


class FraudStatus(str, enum.Enum):
    """Fraud case status"""
    DETECTED = "detected"
    UNDER_REVIEW = "under_review"
    CONFIRMED = "confirmed"
    FALSE_POSITIVE = "false_positive"
    RESOLVED = "resolved"


class FraudAlert(BaseModel):
    """Fraud detection alerts and tracking"""

    __tablename__ = "fraud_alerts"

    # Related User (if applicable)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    # Fraud Details
    fraud_type = Column(Enum(FraudType), nullable=False)
    status = Column(Enum(FraudStatus), default=FraudStatus.DETECTED, nullable=False)
    severity = Column(String(20), nullable=False)  # low, medium, high, critical

    # Detection Info
    detection_method = Column(String(100), nullable=False)  # ML model, rule-based, manual report
    confidence_score = Column(Float, nullable=True)  # 0.0 - 1.0

    # Details
    description = Column(Text, nullable=False)
    evidence = Column(JSON, nullable=True)  # Screenshots, logs, etc.

    # Related Entity
    related_payment_id = Column(Integer, ForeignKey("payments.id", ondelete="SET NULL"), nullable=True)
    related_booking_id = Column(Integer, nullable=True)
    related_order_id = Column(Integer, nullable=True)

    # Source Information
    ip_address = Column(String(50), nullable=True)
    device_fingerprint = Column(String(255), nullable=True)
    user_agent = Column(String(500), nullable=True)
    location = Column(JSON, nullable=True)  # {lat, lng, country, city}

    # Amount (if financial fraud)
    amount_involved = Column(Float, nullable=True)
    currency = Column(String(10), default="GHS", nullable=True)

    # Review
    reviewed_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    reviewed_at = Column(String(50), nullable=True)
    review_notes = Column(Text, nullable=True)

    # Actions Taken
    actions_taken = Column(JSON, nullable=True)  # ["account_suspended", "payment_blocked", etc.]
    auto_blocked = Column(Boolean, default=False, nullable=False)

    # Resolution
    resolved_at = Column(String(50), nullable=True)
    resolution_notes = Column(Text, nullable=True)

    # Extra Data
    extra_data = Column(JSON, nullable=True)

    # Relationships
    user = relationship("User", foreign_keys=[user_id], backref="fraud_alerts")
    reviewer = relationship("User", foreign_keys=[reviewed_by])

    def __repr__(self):
        return f"<FraudAlert {self.fraud_type} - {self.status}>"
