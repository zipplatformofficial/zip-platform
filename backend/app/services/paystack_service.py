"""Paystack payment integration service"""
import hashlib
import hmac
import requests
from typing import Dict, Optional, Any
from decimal import Decimal
from app.core.config import settings


class PaystackService:
    """Service for handling Paystack payment operations"""

    BASE_URL = "https://api.paystack.co"

    def __init__(self):
        self.secret_key = settings.PAYSTACK_SECRET_KEY
        self.public_key = settings.PAYSTACK_PUBLIC_KEY
        self.webhook_secret = settings.PAYSTACK_WEBHOOK_SECRET

        # Allow service to initialize without key for development
        # Key will be checked when actual payment methods are called
        if not self.secret_key:
            self.secret_key = None

    def _get_headers(self) -> Dict[str, str]:
        """Get request headers with authorization"""
        return {
            "Authorization": f"Bearer {self.secret_key}",
            "Content-Type": "application/json"
        }

    def initialize_transaction(
        self,
        email: str,
        amount: Decimal,
        reference: str,
        callback_url: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        channels: Optional[list] = None
    ) -> Dict[str, Any]:
        """
        Initialize a payment transaction

        Args:
            email: Customer's email address
            amount: Amount in major currency unit (e.g., GHS 100.00)
            reference: Unique transaction reference
            callback_url: URL to redirect after payment
            metadata: Additional data to attach to transaction
            channels: Payment channels to allow ['card', 'bank', 'mobile_money']

        Returns:
            Dict with authorization_url and access_code
        """
        # Convert amount to pesewas (Paystack uses minor currency units)
        amount_pesewas = int(amount * 100)

        payload = {
            "email": email,
            "amount": amount_pesewas,
            "reference": reference,
            "currency": "GHS",
            "metadata": metadata or {}
        }

        if callback_url:
            payload["callback_url"] = callback_url
        elif settings.PAYSTACK_CALLBACK_URL:
            payload["callback_url"] = settings.PAYSTACK_CALLBACK_URL

        if channels:
            payload["channels"] = channels

        try:
            response = requests.post(
                f"{self.BASE_URL}/transaction/initialize",
                json=payload,
                headers=self._get_headers(),
                timeout=30
            )
            response.raise_for_status()
            data = response.json()

            if data.get("status"):
                return {
                    "success": True,
                    "authorization_url": data["data"]["authorization_url"],
                    "access_code": data["data"]["access_code"],
                    "reference": data["data"]["reference"]
                }
            else:
                return {
                    "success": False,
                    "message": data.get("message", "Transaction initialization failed")
                }

        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "message": f"Payment gateway error: {str(e)}"
            }

    def verify_transaction(self, reference: str) -> Dict[str, Any]:
        """
        Verify a transaction status

        Args:
            reference: Transaction reference to verify

        Returns:
            Dict with transaction details
        """
        try:
            response = requests.get(
                f"{self.BASE_URL}/transaction/verify/{reference}",
                headers=self._get_headers(),
                timeout=30
            )
            response.raise_for_status()
            data = response.json()

            if data.get("status"):
                transaction_data = data["data"]
                # Convert amount from pesewas back to cedis
                amount = Decimal(transaction_data["amount"]) / 100

                return {
                    "success": True,
                    "status": transaction_data["status"],
                    "reference": transaction_data["reference"],
                    "amount": amount,
                    "currency": transaction_data["currency"],
                    "channel": transaction_data.get("channel"),
                    "paid_at": transaction_data.get("paid_at"),
                    "customer": transaction_data.get("customer"),
                    "metadata": transaction_data.get("metadata", {})
                }
            else:
                return {
                    "success": False,
                    "message": data.get("message", "Verification failed")
                }

        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "message": f"Verification error: {str(e)}"
            }

    def verify_webhook_signature(self, payload: bytes, signature: str) -> bool:
        """
        Verify Paystack webhook signature

        Args:
            payload: Raw request body
            signature: X-Paystack-Signature header value

        Returns:
            True if signature is valid
        """
        if not self.webhook_secret:
            raise ValueError("PAYSTACK_WEBHOOK_SECRET is not configured")

        computed_signature = hmac.new(
            self.webhook_secret.encode('utf-8'),
            payload,
            hashlib.sha512
        ).hexdigest()

        return hmac.compare_digest(computed_signature, signature)

    def initiate_refund(
        self,
        transaction_reference: str,
        amount: Optional[Decimal] = None,
        merchant_note: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Initiate a refund

        Args:
            transaction_reference: Original transaction reference
            amount: Amount to refund (partial refund). If None, full refund
            merchant_note: Reason for refund

        Returns:
            Dict with refund status
        """
        payload = {
            "transaction": transaction_reference
        }

        if amount:
            # Convert to pesewas
            payload["amount"] = int(amount * 100)

        if merchant_note:
            payload["merchant_note"] = merchant_note

        try:
            response = requests.post(
                f"{self.BASE_URL}/refund",
                json=payload,
                headers=self._get_headers(),
                timeout=30
            )
            response.raise_for_status()
            data = response.json()

            if data.get("status"):
                refund_data = data["data"]
                return {
                    "success": True,
                    "refund_id": refund_data.get("id"),
                    "status": refund_data.get("status"),
                    "message": data.get("message", "Refund initiated successfully")
                }
            else:
                return {
                    "success": False,
                    "message": data.get("message", "Refund failed")
                }

        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "message": f"Refund error: {str(e)}"
            }

    def create_transfer_recipient(
        self,
        account_number: str,
        bank_code: str,
        name: str,
        currency: str = "GHS"
    ) -> Dict[str, Any]:
        """
        Create a transfer recipient for payouts (e.g., to technicians, vendors)

        Args:
            account_number: Recipient's bank account number
            bank_code: Bank code (get from Paystack banks API)
            name: Recipient's account name
            currency: Currency code

        Returns:
            Dict with recipient code
        """
        payload = {
            "type": "nuban",
            "name": name,
            "account_number": account_number,
            "bank_code": bank_code,
            "currency": currency
        }

        try:
            response = requests.post(
                f"{self.BASE_URL}/transferrecipient",
                json=payload,
                headers=self._get_headers(),
                timeout=30
            )
            response.raise_for_status()
            data = response.json()

            if data.get("status"):
                recipient_data = data["data"]
                return {
                    "success": True,
                    "recipient_code": recipient_data["recipient_code"],
                    "details": recipient_data.get("details")
                }
            else:
                return {
                    "success": False,
                    "message": data.get("message", "Failed to create recipient")
                }

        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "message": f"Error creating recipient: {str(e)}"
            }

    def initiate_transfer(
        self,
        recipient_code: str,
        amount: Decimal,
        reference: str,
        reason: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Initiate a transfer to a recipient (for payouts)

        Args:
            recipient_code: Recipient code from create_transfer_recipient
            amount: Amount to transfer
            reference: Unique transfer reference
            reason: Transfer description

        Returns:
            Dict with transfer status
        """
        payload = {
            "source": "balance",
            "amount": int(amount * 100),  # Convert to pesewas
            "recipient": recipient_code,
            "reference": reference,
            "reason": reason or "Payout from ZIP Platform"
        }

        try:
            response = requests.post(
                f"{self.BASE_URL}/transfer",
                json=payload,
                headers=self._get_headers(),
                timeout=30
            )
            response.raise_for_status()
            data = response.json()

            if data.get("status"):
                transfer_data = data["data"]
                return {
                    "success": True,
                    "transfer_code": transfer_data.get("transfer_code"),
                    "status": transfer_data.get("status"),
                    "reference": transfer_data.get("reference")
                }
            else:
                return {
                    "success": False,
                    "message": data.get("message", "Transfer failed")
                }

        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "message": f"Transfer error: {str(e)}"
            }

    def get_banks(self, country: str = "ghana") -> Dict[str, Any]:
        """
        Get list of supported banks

        Args:
            country: Country code (ghana, nigeria, etc.)

        Returns:
            Dict with list of banks
        """
        try:
            response = requests.get(
                f"{self.BASE_URL}/bank",
                params={"country": country},
                headers=self._get_headers(),
                timeout=30
            )
            response.raise_for_status()
            data = response.json()

            if data.get("status"):
                return {
                    "success": True,
                    "banks": data["data"]
                }
            else:
                return {
                    "success": False,
                    "message": data.get("message", "Failed to fetch banks")
                }

        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "message": f"Error fetching banks: {str(e)}"
            }


# Create singleton instance
paystack_service = PaystackService()
