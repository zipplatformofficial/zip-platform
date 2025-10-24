"""SMS service for sending SMS via Hubtel (Ghana SMS provider)"""
import logging
from typing import Optional
from app.core.config import settings

logger = logging.getLogger(__name__)


class SMSService:
    """Service for sending SMS"""

    def __init__(self):
        # Default to Hubtel for Ghana
        self.provider = "hubtel"

        # Hubtel configuration
        self.client_id = settings.HUBTEL_CLIENT_ID
        self.client_secret = settings.HUBTEL_CLIENT_SECRET
        self.api_key = settings.HUBTEL_API_KEY
        self.sender_id = settings.HUBTEL_SENDER_ID or "ZIP"

    def send_sms_twilio(self, to_phone: str, message: str) -> bool:
        """Send SMS using Twilio"""
        try:
            message = self.client.messages.create(
                body=message,
                from_=self.from_number,
                to=to_phone
            )
            logger.info(f"SMS sent successfully to {to_phone} via Twilio. SID: {message.sid}")
            return True
        except Exception as e:
            logger.error(f"Failed to send SMS via Twilio to {to_phone}: {str(e)}")
            return False

    def send_sms_hubtel(self, to_phone: str, message: str) -> bool:
        """Send SMS using Hubtel (Ghana)"""
        try:
            import requests
            import base64

            if not self.client_id or not self.client_secret:
                logger.error("Hubtel credentials not configured")
                return False

            # Hubtel API endpoint
            url = "https://api.hubtel.com/v1/messages/send"

            # Create basic auth with Client ID and Secret
            auth_string = f"{self.client_id}:{self.client_secret}"
            auth_bytes = auth_string.encode('ascii')
            base64_bytes = base64.b64encode(auth_bytes)
            base64_auth = base64_bytes.decode('ascii')

            headers = {
                "Authorization": f"Basic {base64_auth}",
                "Content-Type": "application/json"
            }

            payload = {
                "From": self.sender_id,
                "To": to_phone,
                "Content": message
            }

            response = requests.post(url, json=payload, headers=headers, timeout=30)

            if response.status_code == 201:
                logger.info(f"SMS sent successfully to {to_phone} via Hubtel")
                return True
            else:
                logger.error(f"Failed to send SMS via Hubtel: {response.text}")
                return False

        except Exception as e:
            logger.error(f"Failed to send SMS via Hubtel to {to_phone}: {str(e)}")
            return False

    def send_sms(self, to_phone: str, message: str) -> bool:
        """
        Send SMS using configured provider

        Args:
            to_phone: Phone number (international format: +233XXXXXXXXX)
            message: SMS message content

        Returns:
            bool: True if SMS sent successfully
        """
        # Ensure phone number is in international format
        if not to_phone.startswith("+"):
            if to_phone.startswith("233"):
                to_phone = f"+{to_phone}"
            elif to_phone.startswith("0"):
                to_phone = f"+233{to_phone[1:]}"

        # Default to Hubtel
        return self.send_sms_hubtel(to_phone, message)

    def send_verification_sms(self, to_phone: str, verification_code: str) -> bool:
        """
        Send phone verification SMS

        Args:
            to_phone: Phone number
            verification_code: 6-digit OTP code

        Returns:
            bool: True if SMS sent successfully
        """
        message = f"Your ZIP Platform verification code is: {verification_code}. Valid for 10 minutes. Do not share this code."
        return self.send_sms(to_phone, message)

    def send_password_reset_sms(self, to_phone: str, reset_code: str) -> bool:
        """
        Send password reset SMS

        Args:
            to_phone: Phone number
            reset_code: Reset code

        Returns:
            bool: True if SMS sent successfully
        """
        message = f"Your ZIP Platform password reset code is: {reset_code}. Valid for 1 hour. Do not share this code."
        return self.send_sms(to_phone, message)

    def send_booking_sms(
        self,
        to_phone: str,
        booking_ref: str,
        message_type: str = "confirmation"
    ) -> bool:
        """Send booking-related SMS"""
        if message_type == "confirmation":
            message = f"Your ZIP booking {booking_ref} has been confirmed. Check the app for details."
        elif message_type == "technician_assigned":
            message = f"A technician has been assigned to your booking {booking_ref}. They will arrive shortly."
        elif message_type == "completed":
            message = f"Your booking {booking_ref} has been completed. Rate your experience in the app!"
        else:
            message = f"Update on your booking {booking_ref}. Check the app for details."

        return self.send_sms(to_phone, message)


# Singleton instance
sms_service = SMSService()
