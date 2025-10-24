"""File upload endpoints"""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from typing import List
from app.api.v1.deps import get_current_user
from app.models.user import User
from app.services.cloud_storage_service import cloud_storage_service
from app.services.cloudinary_service import cloudinary_service
from app.schemas.upload import UploadResponse, DeleteResponse
from app.core.config import settings

router = APIRouter()

# Allowed file types for different upload categories
ALLOWED_IMAGE_TYPES = ['image/jpeg', 'image/png', 'image/jpg', 'image/webp']
ALLOWED_DOCUMENT_TYPES = ['application/pdf', 'image/jpeg', 'image/png']


@router.post("/image", response_model=UploadResponse)
async def upload_image(
    file: UploadFile = File(...),
    folder: str = "images",
    current_user: User = Depends(get_current_user)
):
    """
    Upload an image file

    - Accepts JPEG, PNG, WebP formats
    - Maximum file size: 5MB
    - Returns public URL
    - Used for avatars, product photos, vehicle images, etc.
    - Uses Cloudinary if configured, fallback to AWS S3
    """
    # Prefer Cloudinary for images, fallback to S3
    storage_service = cloudinary_service if cloudinary_service else cloud_storage_service

    if not storage_service:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Cloud storage service is not configured"
        )

    # Validate file
    if cloudinary_service:
        validation = cloudinary_service.validate_image(
            file.file,
            max_size=settings.MAX_FILE_SIZE,
            allowed_formats=['jpg', 'jpeg', 'png', 'webp']
        )
    else:
        validation = cloud_storage_service.validate_file(
            file.file,
            allowed_types=ALLOWED_IMAGE_TYPES,
            max_size=settings.MAX_FILE_SIZE
        )

    if not validation.get("valid"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=validation.get("message")
        )

    # Upload file
    if cloudinary_service:
        result = cloudinary_service.upload_image(
            file_obj=file.file,
            filename=file.filename,
            folder=folder,
            tags=[f"user_{current_user.id}", folder]
        )
    else:
        result = cloud_storage_service.upload_file(
            file_obj=file.file,
            filename=file.filename,
            folder=folder,
            content_type=file.content_type,
            metadata={
                "uploaded_by": str(current_user.id),
                "original_filename": file.filename
            }
        )

    if not result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=result.get("message")
        )

    return UploadResponse(**result)


@router.post("/avatar", response_model=UploadResponse)
async def upload_avatar(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    """
    Upload user avatar/profile picture

    - Uploads to 'avatars' folder
    - Accepts JPEG, PNG formats
    - Maximum size: 5MB
    """
    return await upload_image(file, folder="avatars", current_user=current_user)


@router.post("/product", response_model=UploadResponse)
async def upload_product_image(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    """
    Upload product image

    - Uploads to 'products' folder
    - For vendors uploading product photos
    - Accepts JPEG, PNG formats
    """
    # Check if user is vendor or admin
    if current_user.role not in ["VENDOR", "ADMIN"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only vendors can upload product images"
        )

    return await upload_image(file, folder="products", current_user=current_user)


@router.post("/vehicle", response_model=UploadResponse)
async def upload_vehicle_image(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    """
    Upload vehicle image

    - Uploads to 'vehicles' folder
    - For rental vehicle photos or customer vehicle photos
    - Accepts JPEG, PNG formats
    """
    return await upload_image(file, folder="vehicles", current_user=current_user)


@router.post("/document", response_model=UploadResponse)
async def upload_document(
    file: UploadFile = File(...),
    folder: str = "documents",
    current_user: User = Depends(get_current_user)
):
    """
    Upload a document file

    - Accepts PDF, JPEG, PNG formats
    - Maximum file size: 5MB
    - Used for Ghana Card, Driver's License, certificates, etc.
    """
    if not cloud_storage_service:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Cloud storage service is not configured"
        )

    # Validate file
    validation = cloud_storage_service.validate_file(
        file.file,
        allowed_types=ALLOWED_DOCUMENT_TYPES,
        max_size=settings.MAX_FILE_SIZE
    )

    if not validation.get("valid"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=validation.get("message")
        )

    # Upload file
    result = cloud_storage_service.upload_file(
        file_obj=file.file,
        filename=file.filename,
        folder=folder,
        content_type=file.content_type,
        metadata={
            "uploaded_by": str(current_user.id),
            "original_filename": file.filename,
            "document_type": folder
        }
    )

    if not result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=result.get("message")
        )

    return UploadResponse(**result)


@router.post("/verification", response_model=UploadResponse)
async def upload_verification_document(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    """
    Upload verification document

    - Uploads to 'verification' folder
    - For Ghana Card, Driver's License, etc.
    - Used for technician/vendor verification
    """
    return await upload_document(file, folder="verification", current_user=current_user)


@router.post("/multiple", response_model=List[UploadResponse])
async def upload_multiple_images(
    files: List[UploadFile] = File(...),
    folder: str = "images",
    current_user: User = Depends(get_current_user)
):
    """
    Upload multiple image files at once

    - Maximum 10 files per request
    - Each file follows same validation as single image upload
    - Used for product galleries, inspection photos, etc.
    """
    if len(files) > 10:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Maximum 10 files allowed per request"
        )

    results = []
    for file in files:
        try:
            result = await upload_image(file, folder=folder, current_user=current_user)
            results.append(result)
        except HTTPException as e:
            # If one file fails, include error in response
            results.append(UploadResponse(
                success=False,
                message=f"{file.filename}: {e.detail}"
            ))

    return results


@router.delete("/delete", response_model=DeleteResponse)
async def delete_file(
    s3_key: str,
    current_user: User = Depends(get_current_user)
):
    """
    Delete a file from cloud storage

    - Requires S3 key (path) of the file
    - Only admins or file owner can delete
    - Permanent deletion

    Args:
        s3_key: S3 key of file to delete (e.g., 'avatars/abc123.jpg')
    """
    if not cloud_storage_service:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Cloud storage service is not configured"
        )

    # TODO: Add ownership check - verify user owns this file
    # For now, only allow admins to delete
    if current_user.role != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only administrators can delete files"
        )

    result = cloud_storage_service.delete_file(s3_key)

    if not result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=result.get("message")
        )

    return DeleteResponse(**result)
