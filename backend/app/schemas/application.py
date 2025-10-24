"""Role application schemas"""
from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field, EmailStr
from app.models.application import ApplicationStatus, ApplicationType


# Technician Application
class TechnicianApplicationCreate(BaseModel):
    """Create technician application"""
    ghana_card_number: str
    ghana_card_front: str  # Base64 or URL
    ghana_card_back: str
    selfie_with_card: str
    drivers_license_number: Optional[str] = None
    drivers_license_front: Optional[str] = None
    drivers_license_back: Optional[str] = None
    certifications: Optional[List[str]] = None
    experience_letter: Optional[str] = None
    specializations: List[str]
    years_experience: int = Field(ge=0)
    bio: str
    applicant_notes: Optional[str] = None


# Vendor Application
class VendorApplicationCreate(BaseModel):
    """Create vendor application"""
    ghana_card_number: str
    ghana_card_front: str
    ghana_card_back: str
    selfie_with_card: str
    business_registration_number: str
    business_registration_document: str
    business_name: str
    business_address: Dict[str, Any]
    business_phone: str
    business_email: EmailStr
    tax_identification_number: Optional[str] = None
    applicant_notes: Optional[str] = None


# Rental Manager Application
class RentalManagerApplicationCreate(BaseModel):
    """Create rental manager application"""
    ghana_card_number: str
    ghana_card_front: str
    ghana_card_back: str
    selfie_with_card: str
    drivers_license_number: str
    drivers_license_front: str
    drivers_license_back: str
    company_registration: str
    company_documents: List[str]
    fleet_size: int = Field(gt=0)
    vehicle_documents: List[str]
    applicant_notes: Optional[str] = None


# Application Response
class RoleApplicationResponse(BaseModel):
    """Role application response"""
    id: int
    user_id: int
    application_type: ApplicationType
    status: ApplicationStatus

    # Documents
    ghana_card_number: str
    ghana_card_verified: bool
    drivers_license_verified: bool
    business_verified: bool
    all_documents_verified: bool

    # Review
    reviewed_by: Optional[int]
    reviewed_at: Optional[str]
    admin_notes: Optional[str]
    rejection_reason: Optional[str]

    # Notification
    applicant_notified: bool
    sms_sent: bool
    push_sent: bool

    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Admin Actions
class ApplicationReview(BaseModel):
    """Admin review of application"""
    ghana_card_verified: bool
    drivers_license_verified: Optional[bool] = None
    business_verified: Optional[bool] = None
    admin_notes: Optional[str] = None


class ApplicationApproval(BaseModel):
    """Approve application"""
    admin_notes: Optional[str] = None


class ApplicationRejection(BaseModel):
    """Reject application"""
    rejection_reason: str
    admin_notes: Optional[str] = None
