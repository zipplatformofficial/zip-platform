"""Role application endpoints"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from datetime import datetime

from app.api.v1.deps import get_db, get_current_active_user, require_admin
from app.models.user import User, UserRole
from app.models.application import RoleApplication, ApplicationStatus, ApplicationType
from app.models.maintenance import Technician
from app.models.store import Vendor
from app.schemas.application import (
    TechnicianApplicationCreate,
    VendorApplicationCreate,
    RentalManagerApplicationCreate,
    RoleApplicationResponse,
    ApplicationReview,
    ApplicationApproval,
    ApplicationRejection
)
from app.services.notification_service import notification_service


router = APIRouter()


# ==================== USER ENDPOINTS ====================

@router.post("/apply/technician", response_model=RoleApplicationResponse, status_code=status.HTTP_201_CREATED)
async def apply_as_technician(
    application_in: TechnicianApplicationCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Apply to become a technician"""

    # Check if user already has pending application
    existing = db.query(RoleApplication).filter(
        RoleApplication.user_id == current_user.id,
        RoleApplication.application_type == ApplicationType.TECHNICIAN,
        RoleApplication.status.in_([ApplicationStatus.PENDING, ApplicationStatus.UNDER_REVIEW])
    ).first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You already have a pending technician application"
        )

    # Check if user is already a technician
    if current_user.role == UserRole.TECHNICIAN:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You are already a technician"
        )

    application = RoleApplication(
        **application_in.model_dump(),
        user_id=current_user.id,
        application_type=ApplicationType.TECHNICIAN,
        status=ApplicationStatus.PENDING
    )

    db.add(application)
    db.commit()
    db.refresh(application)

    return application


@router.post("/apply/vendor", response_model=RoleApplicationResponse, status_code=status.HTTP_201_CREATED)
async def apply_as_vendor(
    application_in: VendorApplicationCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Apply to become a vendor"""

    existing = db.query(RoleApplication).filter(
        RoleApplication.user_id == current_user.id,
        RoleApplication.application_type == ApplicationType.VENDOR,
        RoleApplication.status.in_([ApplicationStatus.PENDING, ApplicationStatus.UNDER_REVIEW])
    ).first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You already have a pending vendor application"
        )

    if current_user.role == UserRole.VENDOR:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You are already a vendor"
        )

    application = RoleApplication(
        **application_in.model_dump(),
        user_id=current_user.id,
        application_type=ApplicationType.VENDOR,
        status=ApplicationStatus.PENDING
    )

    db.add(application)
    db.commit()
    db.refresh(application)

    return application


@router.post("/apply/rental-manager", response_model=RoleApplicationResponse, status_code=status.HTTP_201_CREATED)
async def apply_as_rental_manager(
    application_in: RentalManagerApplicationCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Apply to become a rental manager"""

    existing = db.query(RoleApplication).filter(
        RoleApplication.user_id == current_user.id,
        RoleApplication.application_type == ApplicationType.RENTAL_MANAGER,
        RoleApplication.status.in_([ApplicationStatus.PENDING, ApplicationStatus.UNDER_REVIEW])
    ).first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You already have a pending rental manager application"
        )

    if current_user.role == UserRole.RENTAL_MANAGER:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You are already a rental manager"
        )

    application = RoleApplication(
        **application_in.model_dump(),
        user_id=current_user.id,
        application_type=ApplicationType.RENTAL_MANAGER,
        status=ApplicationStatus.PENDING
    )

    db.add(application)
    db.commit()
    db.refresh(application)

    return application


@router.get("/my-applications", response_model=List[RoleApplicationResponse])
async def get_my_applications(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get current user's applications"""
    applications = db.query(RoleApplication).filter(
        RoleApplication.user_id == current_user.id
    ).order_by(RoleApplication.created_at.desc()).all()

    return applications


# ==================== ADMIN ENDPOINTS ====================

@router.get("/admin/applications", response_model=List[RoleApplicationResponse])
async def list_all_applications(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    status_filter: Optional[ApplicationStatus] = None,
    type_filter: Optional[ApplicationType] = None,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """List all applications (Admin only)"""
    query = db.query(RoleApplication)

    if status_filter:
        query = query.filter(RoleApplication.status == status_filter)

    if type_filter:
        query = query.filter(RoleApplication.application_type == type_filter)

    applications = query.order_by(RoleApplication.created_at.desc()).offset(skip).limit(limit).all()
    return applications


@router.get("/admin/applications/{application_id}", response_model=RoleApplicationResponse)
async def get_application(
    application_id: int,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Get specific application details (Admin only)"""
    application = db.query(RoleApplication).filter(RoleApplication.id == application_id).first()

    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found"
        )

    return application


@router.put("/admin/applications/{application_id}/review", response_model=RoleApplicationResponse)
async def review_application(
    application_id: int,
    review: ApplicationReview,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Review application documents (Admin only)"""
    application = db.query(RoleApplication).filter(RoleApplication.id == application_id).first()

    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found"
        )

    # Update verification flags
    application.ghana_card_verified = review.ghana_card_verified
    if review.drivers_license_verified is not None:
        application.drivers_license_verified = review.drivers_license_verified
    if review.business_verified is not None:
        application.business_verified = review.business_verified

    # Check if all required documents are verified
    if application.application_type == ApplicationType.TECHNICIAN:
        application.all_documents_verified = application.ghana_card_verified
    elif application.application_type == ApplicationType.VENDOR:
        application.all_documents_verified = (
            application.ghana_card_verified and application.business_verified
        )
    elif application.application_type == ApplicationType.RENTAL_MANAGER:
        application.all_documents_verified = (
            application.ghana_card_verified and
            application.drivers_license_verified and
            application.business_verified
        )

    application.status = ApplicationStatus.UNDER_REVIEW
    application.admin_notes = review.admin_notes
    application.reviewed_by = current_user.id
    application.reviewed_at = datetime.utcnow().isoformat()

    db.commit()
    db.refresh(application)

    return application


@router.post("/admin/applications/{application_id}/approve", response_model=RoleApplicationResponse)
async def approve_application(
    application_id: int,
    approval: ApplicationApproval,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Approve application and upgrade user role (Admin only)"""
    application = db.query(RoleApplication).filter(RoleApplication.id == application_id).first()

    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found"
        )

    if not application.all_documents_verified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot approve application with unverified documents"
        )

    # Get the user
    user = db.query(User).filter(User.id == application.user_id).first()

    # Update application
    application.status = ApplicationStatus.APPROVED
    application.admin_notes = approval.admin_notes
    application.reviewed_by = current_user.id
    application.reviewed_at = datetime.utcnow().isoformat()

    # Upgrade user role
    if application.application_type == ApplicationType.TECHNICIAN:
        user.role = UserRole.TECHNICIAN
        user.is_verified = True
        user.ghana_card_number = application.ghana_card_number
        user.ghana_card_verified = True
        if application.drivers_license_number:
            user.drivers_license_number = application.drivers_license_number
            user.drivers_license_verified = True

        # Create technician profile
        technician = Technician(
            user_id=user.id,
            bio=application.bio,
            specializations=application.specializations,
            experience_years=application.years_experience,
            is_available=True,
            is_verified=True
        )
        db.add(technician)

    elif application.application_type == ApplicationType.VENDOR:
        user.role = UserRole.VENDOR
        user.is_verified = True
        user.ghana_card_number = application.ghana_card_number
        user.ghana_card_verified = True
        user.company_name = application.business_name
        user.company_registration = application.business_registration_number

        # Create vendor profile
        vendor = Vendor(
            user_id=user.id,
            business_name=application.business_name,
            business_registration=application.business_registration_number,
            business_address=application.business_address,
            business_phone=application.business_phone,
            business_email=application.business_email,
            is_verified=True,
            is_active=True,
            commission_rate=0.15  # 15% platform commission
        )
        db.add(vendor)

    elif application.application_type == ApplicationType.RENTAL_MANAGER:
        user.role = UserRole.RENTAL_MANAGER
        user.is_verified = True
        user.ghana_card_number = application.ghana_card_number
        user.ghana_card_verified = True
        user.drivers_license_number = application.drivers_license_number
        user.drivers_license_verified = True
        user.company_name = f"Fleet Company"
        user.company_registration = application.company_registration

    db.commit()
    db.refresh(application)

    # Send notification (SMS + Push)
    try:
        notification_service.send_application_notification(
            db=db,
            user=user,
            application_type=application.application_type.value,
            approved=True,
            new_role=user.role.value
        )
        application.applicant_notified = True
        application.notification_sent_at = datetime.utcnow().isoformat()
        application.sms_sent = True
        application.push_sent = True
        db.commit()
    except Exception as e:
        print(f"Failed to send notification: {e}")

    return application


@router.post("/admin/applications/{application_id}/reject", response_model=RoleApplicationResponse)
async def reject_application(
    application_id: int,
    rejection: ApplicationRejection,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Reject application (Admin only)"""
    application = db.query(RoleApplication).filter(RoleApplication.id == application_id).first()

    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found"
        )

    application.status = ApplicationStatus.REJECTED
    application.rejection_reason = rejection.rejection_reason
    application.admin_notes = rejection.admin_notes
    application.reviewed_by = current_user.id
    application.reviewed_at = datetime.utcnow().isoformat()

    db.commit()
    db.refresh(application)

    # Send rejection notification
    user = db.query(User).filter(User.id == application.user_id).first()
    try:
        notification_service.send_application_notification(
            db=db,
            user=user,
            application_type=application.application_type.value,
            approved=False,
            rejection_reason=rejection.rejection_reason
        )
        application.applicant_notified = True
        application.notification_sent_at = datetime.utcnow().isoformat()
        application.sms_sent = True
        application.push_sent = True
        db.commit()
    except Exception as e:
        print(f"Failed to send notification: {e}")

    return application
