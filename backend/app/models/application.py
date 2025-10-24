"""User role application models"""
import enum
from sqlalchemy import Column, String, Integer, ForeignKey, Enum, Text, JSON, Boolean
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class ApplicationStatus(str, enum.Enum):
    """Application status"""
    PENDING = "pending"
    UNDER_REVIEW = "under_review"
    APPROVED = "approved"
    REJECTED = "rejected"
    CANCELLED = "cancelled"


class ApplicationType(str, enum.Enum):
    """Types of role applications"""
    TECHNICIAN = "technician"
    VENDOR = "vendor"
    RENTAL_MANAGER = "rental_manager"


class RoleApplication(BaseModel):
    """User application to become technician, vendor, or rental manager"""

    __tablename__ = "role_applications"

    # Applicant
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    # Application Details
    application_type = Column(Enum(ApplicationType), nullable=False)
    status = Column(Enum(ApplicationStatus), default=ApplicationStatus.PENDING, nullable=False)

    # Required Documents (Ghana Card is mandatory for all)
    ghana_card_number = Column(String(50), nullable=False)
    ghana_card_front = Column(String(500), nullable=False)  # Image URL
    ghana_card_back = Column(String(500), nullable=False)   # Image URL
    selfie_with_card = Column(String(500), nullable=False)  # Image URL for verification

    # Additional Documents based on type
    drivers_license_number = Column(String(50), nullable=True)
    drivers_license_front = Column(String(500), nullable=True)
    drivers_license_back = Column(String(500), nullable=True)

    # For Technician
    certifications = Column(JSON, nullable=True)  # Array of certification images
    experience_letter = Column(String(500), nullable=True)
    specializations = Column(JSON, nullable=True)  # Array of specialization areas
    years_experience = Column(Integer, nullable=True)
    bio = Column(Text, nullable=True)

    # For Vendor
    business_registration_number = Column(String(100), nullable=True)
    business_registration_document = Column(String(500), nullable=True)
    business_name = Column(String(255), nullable=True)
    business_address = Column(JSON, nullable=True)
    business_phone = Column(String(20), nullable=True)
    business_email = Column(String(255), nullable=True)
    tax_identification_number = Column(String(50), nullable=True)

    # For Rental Manager
    company_registration = Column(String(100), nullable=True)
    company_documents = Column(JSON, nullable=True)
    fleet_size = Column(Integer, nullable=True)
    vehicle_documents = Column(JSON, nullable=True)

    # Application Notes
    applicant_notes = Column(Text, nullable=True)

    # Admin Review
    reviewed_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    reviewed_at = Column(String(50), nullable=True)  # ISO datetime
    admin_notes = Column(Text, nullable=True)
    rejection_reason = Column(Text, nullable=True)

    # Verification Flags
    ghana_card_verified = Column(Boolean, default=False, nullable=False)
    drivers_license_verified = Column(Boolean, default=False, nullable=False)
    business_verified = Column(Boolean, default=False, nullable=False)
    all_documents_verified = Column(Boolean, default=False, nullable=False)

    # Notification Status
    applicant_notified = Column(Boolean, default=False, nullable=False)
    notification_sent_at = Column(String(50), nullable=True)
    sms_sent = Column(Boolean, default=False, nullable=False)
    push_sent = Column(Boolean, default=False, nullable=False)

    # Relationships
    applicant = relationship("User", foreign_keys=[user_id])
    reviewer = relationship("User", foreign_keys=[reviewed_by])

    def __repr__(self):
        return f"<RoleApplication {self.application_type} by user {self.user_id}>"
