"""Notification models"""
import enum
from sqlalchemy import Column, String, Integer, ForeignKey, Enum, Text, JSON, Boolean
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class NotificationType(str, enum.Enum):
    """Notification types"""
    BOOKING_CONFIRMATION = "booking_confirmation"
    BOOKING_UPDATE = "booking_update"
    PAYMENT_SUCCESS = "payment_success"
    PAYMENT_FAILED = "payment_failed"
    SERVICE_ASSIGNED = "service_assigned"
    TECHNICIAN_EN_ROUTE = "technician_en_route"
    SERVICE_STARTED = "service_started"
    SERVICE_COMPLETED = "service_completed"
    RENTAL_CONFIRMED = "rental_confirmed"
    RENTAL_REMINDER = "rental_reminder"
    RENTAL_OVERDUE = "rental_overdue"
    ORDER_CONFIRMED = "order_confirmed"
    ORDER_SHIPPED = "order_shipped"
    ORDER_DELIVERED = "order_delivered"
    PROMOTION = "promotion"
    SYSTEM_ALERT = "system_alert"
    ACCOUNT_UPDATE = "account_update"


class Notification(BaseModel):
    """User notification"""

    __tablename__ = "notifications"

    # Recipient
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    # Notification Content
    type = Column(Enum(NotificationType), nullable=False)
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)

    # Additional data (JSON for flexibility)
    data = Column(JSON, nullable=True)  # Related IDs, URLs, etc.

    # Status
    is_read = Column(Boolean, default=False, nullable=False)
    read_at = Column(String(50), nullable=True)

    # Delivery Channels
    sent_via_push = Column(Boolean, default=False, nullable=False)
    sent_via_sms = Column(Boolean, default=False, nullable=False)
    sent_via_email = Column(Boolean, default=False, nullable=False)

    # Action
    action_url = Column(String(500), nullable=True)
    action_label = Column(String(100), nullable=True)

    # Priority
    priority = Column(String(20), default="normal", nullable=False)  # low/normal/high/urgent

    # Expiry
    expires_at = Column(String(50), nullable=True)

    # Relationships
    user = relationship("User", back_populates="notifications")

    def __repr__(self):
        return f"<Notification {self.type} for user {self.user_id}>"
