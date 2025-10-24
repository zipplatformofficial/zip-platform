"""Notification endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.api.v1.deps import get_current_user
from app.models.user import User
from app.services.notification_service import notification_service
from app.schemas.notification import (
    NotificationResponse,
    NotificationCreate,
    NotificationPreferences,
    FCMTokenUpdate,
    UnreadCountResponse
)

router = APIRouter()


@router.get("/", response_model=List[NotificationResponse])
async def get_notifications(
    unread_only: bool = False,
    skip: int = 0,
    limit: int = 20,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get user notifications

    - Returns paginated list of notifications
    - Filter by unread status
    - Sorted by most recent first
    """
    notifications = notification_service.get_user_notifications(
        db=db,
        user_id=current_user.id,
        unread_only=unread_only,
        skip=skip,
        limit=limit
    )

    return notifications


@router.get("/unread-count", response_model=UnreadCountResponse)
async def get_unread_count(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get count of unread notifications

    - Returns number of unread notifications
    - Used for badge counts in UI
    """
    count = notification_service.get_unread_count(
        db=db,
        user_id=current_user.id
    )

    return UnreadCountResponse(count=count)


@router.put("/{notification_id}/read")
async def mark_notification_as_read(
    notification_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Mark a notification as read

    - Marks single notification as read
    - Updates read_at timestamp
    """
    success = notification_service.mark_as_read(
        db=db,
        notification_id=notification_id,
        user_id=current_user.id
    )

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found"
        )

    return {"message": "Notification marked as read"}


@router.put("/read-all")
async def mark_all_as_read(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Mark all notifications as read

    - Marks all unread notifications as read
    - Returns count of notifications marked
    """
    count = notification_service.mark_all_as_read(
        db=db,
        user_id=current_user.id
    )

    return {
        "message": f"{count} notifications marked as read",
        "count": count
    }


@router.delete("/{notification_id}")
async def delete_notification(
    notification_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete a notification

    - Permanently deletes notification
    - Cannot be undone
    """
    success = notification_service.delete_notification(
        db=db,
        notification_id=notification_id,
        user_id=current_user.id
    )

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found"
        )

    return {"message": "Notification deleted"}


@router.post("/test", response_model=NotificationResponse)
async def send_test_notification(
    notification: NotificationCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Send a test notification to yourself

    - For testing notification delivery
    - Sends to all specified channels
    - Admin only for bulk testing
    """
    result = notification_service.send_notification(
        db=db,
        user=current_user,
        title=notification.title,
        message=notification.message,
        notification_type=notification.type,
        channels=notification.channels,
        metadata=notification.metadata
    )

    # Get the created notification
    notification_obj = notification_service.get_user_notifications(
        db=db,
        user_id=current_user.id,
        skip=0,
        limit=1
    )[0]

    return notification_obj


@router.put("/fcm-token")
async def update_fcm_token(
    token_data: FCMTokenUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update Firebase Cloud Messaging device token

    - Required for push notifications
    - Called when app is installed or token refreshes
    - Tokens expire and need to be updated
    """
    current_user.fcm_token = token_data.fcm_token
    db.commit()

    return {"message": "FCM token updated successfully"}


@router.get("/preferences", response_model=NotificationPreferences)
async def get_notification_preferences(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get user notification preferences

    - Returns current notification settings
    - Controls which notifications user receives
    """
    # Get preferences from user metadata or use defaults
    preferences = current_user.metadata.get("notification_preferences", {}) if current_user.metadata else {}

    return NotificationPreferences(
        email_enabled=preferences.get("email_enabled", True),
        sms_enabled=preferences.get("sms_enabled", True),
        push_enabled=preferences.get("push_enabled", True),
        booking_notifications=preferences.get("booking_notifications", True),
        payment_notifications=preferences.get("payment_notifications", True),
        order_notifications=preferences.get("order_notifications", True),
        promotional_notifications=preferences.get("promotional_notifications", True)
    )


@router.put("/preferences")
async def update_notification_preferences(
    preferences: NotificationPreferences,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update notification preferences

    - Set which types of notifications to receive
    - Choose delivery channels (email, SMS, push)
    - Preferences stored in user metadata
    """
    # Initialize metadata if None
    if current_user.metadata is None:
        current_user.metadata = {}

    # Update preferences
    current_user.metadata["notification_preferences"] = preferences.model_dump()

    # Mark metadata as modified (for SQLAlchemy to detect change)
    from sqlalchemy import orm
    orm.attributes.flag_modified(current_user, "metadata")

    db.commit()

    return {"message": "Notification preferences updated successfully"}
