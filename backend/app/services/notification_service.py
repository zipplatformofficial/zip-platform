"""Unified notification service - coordinates email, SMS, and push notifications"""
import logging
from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from datetime import datetime

from app.models.notification import Notification
from app.models.user import User
from app.services.email_service import email_service
from app.services.sms_service import sms_service
from app.services.firebase_service import firebase_service

logger = logging.getLogger(__name__)


class NotificationService:
    """Service for managing and sending notifications across multiple channels"""

    def create_notification(
        self,
        db: Session,
        user_id: int,
        title: str,
        message: str,
        notification_type: str = "INFO",
        channels: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Notification:
        """
        Create a notification record in database

        Args:
            db: Database session
            user_id: User ID to receive notification
            title: Notification title
            message: Notification message
            notification_type: Type (INFO, SUCCESS, WARNING, ERROR, BOOKING, PAYMENT, etc.)
            channels: Delivery channels (email, sms, push, in_app)
            metadata: Additional data

        Returns:
            Created notification object
        """
        notification = Notification(
            user_id=user_id,
            title=title,
            message=message,
            type=notification_type,
            channels=channels or ["in_app"],
            metadata=metadata or {},
            is_read=False
        )

        db.add(notification)
        db.commit()
        db.refresh(notification)

        return notification

    def send_notification(
        self,
        db: Session,
        user: User,
        title: str,
        message: str,
        notification_type: str = "INFO",
        channels: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Send notification via specified channels and create database record

        Args:
            db: Database session
            user: User object
            title: Notification title
            message: Notification message
            notification_type: Notification type
            channels: List of channels (email, sms, push, in_app)
            metadata: Additional data

        Returns:
            Dict with delivery status per channel
        """
        if channels is None:
            channels = ["in_app"]  # Default to in-app only

        results = {}

        # Create in-app notification record
        notification = self.create_notification(
            db=db,
            user_id=user.id,
            title=title,
            message=message,
            notification_type=notification_type,
            channels=channels,
            metadata=metadata
        )
        results["in_app"] = {"success": True, "notification_id": notification.id}

        # Send email if requested
        if "email" in channels and user.email:
            try:
                email_sent = email_service.send_email(
                    to_email=user.email,
                    subject=title,
                    html_content=f"<h2>{title}</h2><p>{message}</p>",
                    text_content=message
                )
                results["email"] = {"success": email_sent}
            except Exception as e:
                logger.error(f"Failed to send email notification: {e}")
                results["email"] = {"success": False, "error": str(e)}

        # Send SMS if requested
        if "sms" in channels and user.phone:
            try:
                sms_text = f"{title}: {message}"
                sms_sent = sms_service.send_sms(user.phone, sms_text)
                results["sms"] = {"success": sms_sent}
            except Exception as e:
                logger.error(f"Failed to send SMS notification: {e}")
                results["sms"] = {"success": False, "error": str(e)}

        # Send push notification if requested
        if "push" in channels and user.fcm_token and firebase_service:
            try:
                push_result = firebase_service.send_push_notification(
                    device_token=user.fcm_token,
                    title=title,
                    body=message,
                    data=metadata or {}
                )
                results["push"] = push_result
            except Exception as e:
                logger.error(f"Failed to send push notification: {e}")
                results["push"] = {"success": False, "error": str(e)}

        return results

    def send_booking_notification(
        self,
        db: Session,
        user: User,
        booking_ref: str,
        service_type: str,
        status: str,
        channels: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Send booking-related notification"""

        status_messages = {
            "confirmed": f"Your {service_type} booking {booking_ref} has been confirmed!",
            "assigned": f"A service provider has been assigned to booking {booking_ref}",
            "in_progress": f"Your booking {booking_ref} is now in progress",
            "completed": f"Your booking {booking_ref} has been completed",
            "cancelled": f"Your booking {booking_ref} has been cancelled",
        }

        message = status_messages.get(status, f"Update on booking {booking_ref}")

        return self.send_notification(
            db=db,
            user=user,
            title=f"Booking {status.title()}",
            message=message,
            notification_type="BOOKING",
            channels=channels or ["in_app", "push", "email"],
            metadata={
                "booking_ref": booking_ref,
                "service_type": service_type,
                "status": status
            }
        )

    def send_payment_notification(
        self,
        db: Session,
        user: User,
        amount: float,
        reference: str,
        status: str,
        channels: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Send payment-related notification"""

        if status == "success":
            title = "Payment Successful"
            message = f"Your payment of GHS {amount:.2f} has been received. Reference: {reference}"
        elif status == "failed":
            title = "Payment Failed"
            message = f"Your payment of GHS {amount:.2f} could not be processed. Reference: {reference}"
        elif status == "refunded":
            title = "Payment Refunded"
            message = f"GHS {amount:.2f} has been refunded to your account. Reference: {reference}"
        else:
            title = "Payment Update"
            message = f"Update on your payment of GHS {amount:.2f}. Reference: {reference}"

        return self.send_notification(
            db=db,
            user=user,
            title=title,
            message=message,
            notification_type="PAYMENT",
            channels=channels or ["in_app", "push", "email"],
            metadata={
                "amount": amount,
                "reference": reference,
                "status": status
            }
        )

    def send_order_notification(
        self,
        db: Session,
        user: User,
        order_ref: str,
        status: str,
        channels: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Send order-related notification"""

        status_messages = {
            "confirmed": f"Your order {order_ref} has been confirmed",
            "processing": f"Your order {order_ref} is being processed",
            "shipped": f"Your order {order_ref} has been shipped",
            "delivered": f"Your order {order_ref} has been delivered",
            "cancelled": f"Your order {order_ref} has been cancelled",
        }

        message = status_messages.get(status, f"Update on order {order_ref}")

        return self.send_notification(
            db=db,
            user=user,
            title=f"Order {status.title()}",
            message=message,
            notification_type="ORDER",
            channels=channels or ["in_app", "push", "email"],
            metadata={
                "order_ref": order_ref,
                "status": status
            }
        )

    def mark_as_read(self, db: Session, notification_id: int, user_id: int) -> bool:
        """Mark a notification as read"""
        notification = db.query(Notification).filter(
            Notification.id == notification_id,
            Notification.user_id == user_id
        ).first()

        if notification:
            notification.is_read = True
            notification.read_at = datetime.utcnow()
            db.commit()
            return True

        return False

    def mark_all_as_read(self, db: Session, user_id: int) -> int:
        """Mark all notifications as read for a user"""
        count = db.query(Notification).filter(
            Notification.user_id == user_id,
            Notification.is_read == False
        ).update({
            "is_read": True,
            "read_at": datetime.utcnow()
        })
        db.commit()
        return count

    def delete_notification(self, db: Session, notification_id: int, user_id: int) -> bool:
        """Delete a notification"""
        notification = db.query(Notification).filter(
            Notification.id == notification_id,
            Notification.user_id == user_id
        ).first()

        if notification:
            db.delete(notification)
            db.commit()
            return True

        return False

    def get_user_notifications(
        self,
        db: Session,
        user_id: int,
        unread_only: bool = False,
        skip: int = 0,
        limit: int = 20
    ) -> List[Notification]:
        """Get user notifications"""
        query = db.query(Notification).filter(Notification.user_id == user_id)

        if unread_only:
            query = query.filter(Notification.is_read == False)

        notifications = query.order_by(
            Notification.created_at.desc()
        ).offset(skip).limit(limit).all()

        return notifications

    def get_unread_count(self, db: Session, user_id: int) -> int:
        """Get count of unread notifications"""
        count = db.query(Notification).filter(
            Notification.user_id == user_id,
            Notification.is_read == False
        ).count()

        return count

    def send_application_notification(
        self,
        db: Session,
        user: User,
        application_type: str,
        approved: bool,
        rejection_reason: Optional[str] = None,
        new_role: Optional[str] = None
    ) -> Dict[str, Any]:
        """Send notification for role application approval/rejection"""

        role_name = application_type.replace("_", " ").title()

        if approved:
            title = "Application Approved!"
            message = f"Congratulations! Your application to become a {role_name} has been approved. You can now access your {role_name} dashboard."
            notification_type = "APPLICATION_APPROVED"
        else:
            title = "Application Update"
            message = f"Your {role_name} application has been reviewed. "
            if rejection_reason:
                message += f"Reason: {rejection_reason}. You can reapply after addressing the issues."
            notification_type = "APPLICATION_REJECTED"

        return self.send_notification(
            db=db,
            user=user,
            title=title,
            message=message,
            notification_type=notification_type,
            channels=["in_app", "push", "sms"],  # Use all channels for important notifications
            metadata={
                "application_type": application_type,
                "approved": approved,
                "rejection_reason": rejection_reason,
                "new_role": new_role
            }
        )


# Create singleton instance
notification_service = NotificationService()
