"""Firebase Cloud Messaging service for push notifications"""
import logging
from typing import List, Dict, Any, Optional
import requests
import json
from pathlib import Path
from app.core.config import settings

logger = logging.getLogger(__name__)


class FirebaseService:
    """Service for sending push notifications via Firebase Cloud Messaging"""

    def __init__(self):
        self.server_key = settings.FIREBASE_SERVER_KEY
        self.credentials_path = settings.FIREBASE_CREDENTIALS_PATH
        self.fcm_url = "https://fcm.googleapis.com/fcm/send"

    def send_push_notification(
        self,
        device_token: str,
        title: str,
        body: str,
        data: Optional[Dict[str, Any]] = None,
        priority: str = "high"
    ) -> Dict[str, Any]:
        """
        Send push notification to a single device

        Args:
            device_token: FCM device token
            title: Notification title
            body: Notification body
            data: Additional data payload
            priority: Notification priority (high or normal)

        Returns:
            Dict with success status and message
        """
        if not self.server_key:
            logger.error("Firebase server key not configured")
            return {
                "success": False,
                "message": "Firebase not configured"
            }

        headers = {
            "Authorization": f"Bearer {self.server_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "to": device_token,
            "priority": priority,
            "notification": {
                "title": title,
                "body": body,
                "sound": "default",
                "badge": "1"
            }
        }

        if data:
            payload["data"] = data

        try:
            response = requests.post(
                self.fcm_url,
                headers=headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            result = response.json()

            if result.get("success") == 1:
                logger.info(f"Push notification sent successfully to {device_token[:10]}...")
                return {
                    "success": True,
                    "message_id": result.get("results", [{}])[0].get("message_id")
                }
            else:
                error = result.get("results", [{}])[0].get("error", "Unknown error")
                logger.error(f"Failed to send push notification: {error}")
                return {
                    "success": False,
                    "message": error
                }

        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to send push notification: {str(e)}")
            return {
                "success": False,
                "message": f"Network error: {str(e)}"
            }

    def send_multicast_notification(
        self,
        device_tokens: List[str],
        title: str,
        body: str,
        data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Send push notification to multiple devices

        Args:
            device_tokens: List of FCM device tokens
            title: Notification title
            body: Notification body
            data: Additional data payload

        Returns:
            Dict with success count and failure count
        """
        if not self.server_key:
            logger.error("Firebase server key not configured")
            return {
                "success": False,
                "message": "Firebase not configured"
            }

        if not device_tokens:
            return {
                "success": False,
                "message": "No device tokens provided"
            }

        headers = {
            "Authorization": f"Bearer {self.server_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "registration_ids": device_tokens,
            "priority": "high",
            "notification": {
                "title": title,
                "body": body,
                "sound": "default"
            }
        }

        if data:
            payload["data"] = data

        try:
            response = requests.post(
                self.fcm_url,
                headers=headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            result = response.json()

            success_count = result.get("success", 0)
            failure_count = result.get("failure", 0)

            logger.info(f"Multicast notification sent. Success: {success_count}, Failed: {failure_count}")

            return {
                "success": True,
                "success_count": success_count,
                "failure_count": failure_count,
                "total": len(device_tokens)
            }

        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to send multicast notification: {str(e)}")
            return {
                "success": False,
                "message": f"Network error: {str(e)}"
            }

    def send_topic_notification(
        self,
        topic: str,
        title: str,
        body: str,
        data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Send push notification to a topic (all subscribed devices)

        Args:
            topic: FCM topic name (e.g., "all_users", "technicians", "vendors")
            title: Notification title
            body: Notification body
            data: Additional data payload

        Returns:
            Dict with success status
        """
        if not self.server_key:
            logger.error("Firebase server key not configured")
            return {
                "success": False,
                "message": "Firebase not configured"
            }

        headers = {
            "Authorization": f"Bearer {self.server_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "to": f"/topics/{topic}",
            "priority": "high",
            "notification": {
                "title": title,
                "body": body,
                "sound": "default"
            }
        }

        if data:
            payload["data"] = data

        try:
            response = requests.post(
                self.fcm_url,
                headers=headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            result = response.json()

            if result.get("message_id"):
                logger.info(f"Topic notification sent to {topic}")
                return {
                    "success": True,
                    "message_id": result.get("message_id")
                }
            else:
                logger.error(f"Failed to send topic notification: {result}")
                return {
                    "success": False,
                    "message": "Failed to send notification"
                }

        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to send topic notification: {str(e)}")
            return {
                "success": False,
                "message": f"Network error: {str(e)}"
            }

    # Convenience methods for common notifications

    def send_booking_confirmation(
        self,
        device_token: str,
        booking_ref: str,
        service_type: str
    ) -> Dict[str, Any]:
        """Send booking confirmation notification"""
        return self.send_push_notification(
            device_token=device_token,
            title="Booking Confirmed",
            body=f"Your {service_type} booking {booking_ref} has been confirmed!",
            data={
                "type": "booking_confirmation",
                "booking_ref": booking_ref,
                "action": "view_booking"
            }
        )

    def send_technician_assigned(
        self,
        device_token: str,
        booking_ref: str,
        technician_name: str
    ) -> Dict[str, Any]:
        """Send technician assignment notification"""
        return self.send_push_notification(
            device_token=device_token,
            title="Technician Assigned",
            body=f"{technician_name} has been assigned to your booking {booking_ref}",
            data={
                "type": "technician_assigned",
                "booking_ref": booking_ref,
                "action": "track_technician"
            }
        )

    def send_payment_success(
        self,
        device_token: str,
        amount: float,
        reference: str
    ) -> Dict[str, Any]:
        """Send payment success notification"""
        return self.send_push_notification(
            device_token=device_token,
            title="Payment Successful",
            body=f"Your payment of GHS {amount:.2f} has been received. Ref: {reference}",
            data={
                "type": "payment_success",
                "amount": str(amount),
                "reference": reference,
                "action": "view_receipt"
            }
        )

    def send_order_shipped(
        self,
        device_token: str,
        order_ref: str,
        tracking_number: Optional[str] = None
    ) -> Dict[str, Any]:
        """Send order shipment notification"""
        body = f"Your order {order_ref} has been shipped!"
        if tracking_number:
            body += f" Tracking: {tracking_number}"

        return self.send_push_notification(
            device_token=device_token,
            title="Order Shipped",
            body=body,
            data={
                "type": "order_shipped",
                "order_ref": order_ref,
                "tracking_number": tracking_number or "",
                "action": "track_order"
            }
        )

    def send_promo_notification(
        self,
        topic: str,
        promo_title: str,
        promo_description: str
    ) -> Dict[str, Any]:
        """Send promotional notification to topic subscribers"""
        return self.send_topic_notification(
            topic=topic,
            title=promo_title,
            body=promo_description,
            data={
                "type": "promotion",
                "action": "view_promo"
            }
        )


# Create singleton instance
try:
    firebase_service = FirebaseService()
except Exception as e:
    logger.warning(f"Firebase service initialization warning: {e}")
    firebase_service = None
