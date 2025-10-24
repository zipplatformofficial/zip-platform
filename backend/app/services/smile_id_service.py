"""Smile ID Ghana Card Verification Service"""
import logging
import requests
import base64
import hashlib
import hmac
from typing import Dict, Any, Optional
from datetime import datetime
from app.core.config import settings

logger = logging.getLogger(__name__)


class SmileIDService:
    """Service for Ghana Card verification using Smile ID"""

    def __init__(self):
        self.partner_id = settings.SMILE_ID_PARTNER_ID
        self.api_key = settings.SMILE_ID_API_KEY
        self.environment = settings.SMILE_ID_ENVIRONMENT

        # API endpoints based on environment
        if self.environment == "production":
            self.base_url = "https://api.smileidentity.com/v1"
        else:
            self.base_url = "https://testapi.smileidentity.com/v1"

    def generate_signature(self, timestamp: str) -> str:
        """Generate HMAC signature for API request"""
        message = f"{self.partner_id}|{timestamp}"
        signature = hmac.new(
            self.api_key.encode(),
            message.encode(),
            hashlib.sha256
        ).hexdigest()
        return signature

    async def verify_ghana_card(
        self,
        ghana_card_number: str,
        selfie_image: str,
        user_id: str,
        job_type: int = 5  # 5 = Enhanced KYC
    ) -> Dict[str, Any]:
        """
        Verify Ghana Card using Smile ID

        Args:
            ghana_card_number: Ghana Card number (e.g., GHA-123456789-0)
            selfie_image: Base64 encoded selfie image
            user_id: User identifier
            job_type: Type of verification job

        Returns:
            Verification result dictionary
        """
        try:
            timestamp = datetime.utcnow().isoformat()
            signature = self.generate_signature(timestamp)

            # Prepare request payload
            payload = {
                "partner_id": self.partner_id,
                "partner_params": {
                    "user_id": str(user_id),
                    "job_id": f"job_{user_id}_{int(datetime.utcnow().timestamp())}",
                    "job_type": job_type
                },
                "timestamp": timestamp,
                "signature": signature,
                "source_sdk": "rest_api",
                "source_sdk_version": "1.0.0",
                "id_info": {
                    "country": "GH",
                    "id_type": "NATIONAL_ID",  # Ghana Card
                    "id_number": ghana_card_number,
                    "entered": True
                },
                "images": [
                    {
                        "image_type_id": 2,  # 2 = Selfie
                        "image": selfie_image
                    }
                ],
                "callback_url": settings.SMILE_ID_CALLBACK_URL
            }

            # Make API request
            response = requests.post(
                f"{self.base_url}/id_verification",
                json=payload,
                headers={
                    "Content-Type": "application/json"
                },
                timeout=30
            )

            response.raise_for_status()
            result = response.json()

            # Parse verification result
            return self._parse_verification_result(result)

        except requests.exceptions.RequestException as e:
            logger.error(f"Smile ID API error: {e}")
            return {
                "success": False,
                "verified": False,
                "error": str(e),
                "message": "Failed to connect to verification service"
            }
        except Exception as e:
            logger.error(f"Smile ID verification error: {e}")
            return {
                "success": False,
                "verified": False,
                "error": str(e),
                "message": "Verification failed"
            }

    def _parse_verification_result(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Parse Smile ID verification result"""
        try:
            # Extract verification status
            smile_job_complete = result.get("smile_job_complete", False)
            result_code = result.get("ResultCode", "")
            result_text = result.get("ResultText", "")

            # Check if verification was successful
            verified = False
            confidence_score = 0.0

            if smile_job_complete and result_code == "0800":
                # Verification successful
                actions = result.get("Actions", {})

                # Check document verification
                doc_verification = actions.get("Document_Check", "")
                if doc_verification == "Passed":
                    verified = True

                # Get confidence score if available
                confidence = result.get("ConfidenceValue", 0)
                confidence_score = float(confidence)

            # Extract user information
            id_info = result.get("IDResult", {})
            user_data = {
                "full_name": id_info.get("FullName", ""),
                "date_of_birth": id_info.get("DOB", ""),
                "gender": id_info.get("Gender", ""),
                "photo": id_info.get("Photo", ""),
            }

            return {
                "success": True,
                "verified": verified,
                "confidence_score": confidence_score,
                "result_code": result_code,
                "result_text": result_text,
                "user_data": user_data,
                "raw_result": result
            }

        except Exception as e:
            logger.error(f"Failed to parse verification result: {e}")
            return {
                "success": False,
                "verified": False,
                "error": str(e),
                "message": "Failed to parse verification result"
            }

    async def verify_document_authenticity(
        self,
        document_front: str,
        document_back: str,
        user_id: str
    ) -> Dict[str, Any]:
        """
        Verify document authenticity (check if document is real/not fake)

        Args:
            document_front: Base64 encoded front of document
            document_back: Base64 encoded back of document
            user_id: User identifier

        Returns:
            Authenticity verification result
        """
        try:
            timestamp = datetime.utcnow().isoformat()
            signature = self.generate_signature(timestamp)

            payload = {
                "partner_id": self.partner_id,
                "partner_params": {
                    "user_id": str(user_id),
                    "job_id": f"doc_{user_id}_{int(datetime.utcnow().timestamp())}",
                    "job_type": 6  # 6 = Document Verification
                },
                "timestamp": timestamp,
                "signature": signature,
                "images": [
                    {
                        "image_type_id": 3,  # 3 = ID Card Front
                        "image": document_front
                    },
                    {
                        "image_type_id": 7,  # 7 = ID Card Back
                        "image": document_back
                    }
                ]
            }

            response = requests.post(
                f"{self.base_url}/document_verification",
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=30
            )

            response.raise_for_status()
            result = response.json()

            # Parse document verification result
            is_authentic = result.get("Actions", {}).get("Document_Check") == "Passed"

            return {
                "success": True,
                "authentic": is_authentic,
                "result": result
            }

        except Exception as e:
            logger.error(f"Document authenticity check failed: {e}")
            return {
                "success": False,
                "authentic": False,
                "error": str(e)
            }

    def check_service_status(self) -> Dict[str, Any]:
        """Check if Smile ID service is available"""
        try:
            response = requests.get(
                f"{self.base_url}/services",
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            return {
                "available": response.status_code == 200,
                "status_code": response.status_code
            }
        except Exception as e:
            logger.error(f"Smile ID service check failed: {e}")
            return {
                "available": False,
                "error": str(e)
            }


# Create singleton instance
smile_id_service = SmileIDService()
