"""Cloudinary service for image uploads and management"""
import cloudinary
import cloudinary.uploader
import cloudinary.api
from typing import Optional, BinaryIO, Dict, Any, List
from pathlib import Path
from app.core.config import settings


class CloudinaryService:
    """Service for handling image uploads to Cloudinary"""

    def __init__(self):
        """Initialize Cloudinary configuration"""
        self.cloud_name = settings.CLOUDINARY_CLOUD_NAME
        self.api_key = settings.CLOUDINARY_API_KEY
        self.api_secret = settings.CLOUDINARY_API_SECRET
        self.folder = settings.CLOUDINARY_FOLDER

        if not all([self.cloud_name, self.api_key, self.api_secret]):
            raise ValueError("Cloudinary credentials are not fully configured")

        # Configure Cloudinary
        cloudinary.config(
            cloud_name=self.cloud_name,
            api_key=self.api_key,
            api_secret=self.api_secret,
            secure=True
        )

    def upload_image(
        self,
        file_obj: BinaryIO,
        filename: str,
        folder: Optional[str] = None,
        transformation: Optional[Dict[str, Any]] = None,
        tags: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Upload an image to Cloudinary

        Args:
            file_obj: File object to upload
            filename: Original filename
            folder: Subfolder within CLOUDINARY_FOLDER (e.g., 'vehicles', 'avatars')
            transformation: Optional transformations to apply (resize, crop, etc.)
            tags: Optional tags for organizing images

        Returns:
            Dict with image URL and metadata
        """
        try:
            # Determine full folder path
            full_folder = f"{self.folder}/{folder}" if folder else self.folder

            # Prepare upload options
            upload_options = {
                "folder": full_folder,
                "resource_type": "image",
                "use_filename": True,
                "unique_filename": True,
                "overwrite": False
            }

            # Add tags if provided
            if tags:
                upload_options["tags"] = tags

            # Add transformation if provided
            if transformation:
                upload_options["transformation"] = transformation

            # Upload to Cloudinary
            result = cloudinary.uploader.upload(file_obj, **upload_options)

            return {
                "success": True,
                "url": result.get("secure_url"),
                "public_id": result.get("public_id"),
                "width": result.get("width"),
                "height": result.get("height"),
                "format": result.get("format"),
                "size": result.get("bytes"),
                "message": "Image uploaded successfully"
            }

        except Exception as e:
            return {
                "success": False,
                "message": f"Upload failed: {str(e)}"
            }

    def upload_multiple_images(
        self,
        files: List[tuple[BinaryIO, str]],
        folder: Optional[str] = None,
        transformation: Optional[Dict[str, Any]] = None,
        tags: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Upload multiple images to Cloudinary

        Args:
            files: List of tuples (file_obj, filename)
            folder: Subfolder within CLOUDINARY_FOLDER
            transformation: Optional transformations
            tags: Optional tags

        Returns:
            Dict with list of uploaded image URLs and any errors
        """
        uploaded_urls = []
        errors = []

        for file_obj, filename in files:
            result = self.upload_image(
                file_obj=file_obj,
                filename=filename,
                folder=folder,
                transformation=transformation,
                tags=tags
            )

            if result["success"]:
                uploaded_urls.append(result["url"])
            else:
                errors.append({
                    "filename": filename,
                    "error": result["message"]
                })

        return {
            "success": len(errors) == 0,
            "uploaded_urls": uploaded_urls,
            "errors": errors,
            "total_uploaded": len(uploaded_urls),
            "total_failed": len(errors)
        }

    def delete_image(self, public_id: str) -> Dict[str, Any]:
        """
        Delete an image from Cloudinary

        Args:
            public_id: Cloudinary public ID of the image

        Returns:
            Dict with success status
        """
        try:
            result = cloudinary.uploader.destroy(public_id)

            if result.get("result") == "ok":
                return {
                    "success": True,
                    "message": "Image deleted successfully"
                }
            else:
                return {
                    "success": False,
                    "message": "Failed to delete image"
                }

        except Exception as e:
            return {
                "success": False,
                "message": f"Delete failed: {str(e)}"
            }

    def delete_multiple_images(self, public_ids: List[str]) -> Dict[str, Any]:
        """
        Delete multiple images from Cloudinary

        Args:
            public_ids: List of Cloudinary public IDs

        Returns:
            Dict with success status and details
        """
        try:
            result = cloudinary.api.delete_resources(public_ids)

            deleted = result.get("deleted", {})
            deleted_count = sum(1 for status in deleted.values() if status == "deleted")

            return {
                "success": deleted_count == len(public_ids),
                "deleted_count": deleted_count,
                "total_requested": len(public_ids),
                "message": f"Deleted {deleted_count}/{len(public_ids)} images"
            }

        except Exception as e:
            return {
                "success": False,
                "message": f"Bulk delete failed: {str(e)}"
            }

    def get_image_url(
        self,
        public_id: str,
        transformation: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Get transformed URL for an existing image

        Args:
            public_id: Cloudinary public ID
            transformation: Transformations to apply (width, height, crop, etc.)

        Returns:
            Transformed image URL
        """
        if transformation:
            return cloudinary.CloudinaryImage(public_id).build_url(**transformation)
        return cloudinary.CloudinaryImage(public_id).build_url()

    def validate_image(
        self,
        file_obj: BinaryIO,
        max_size: Optional[int] = None,
        allowed_formats: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Validate image before upload

        Args:
            file_obj: File object to validate
            max_size: Maximum file size in bytes (default: 5MB)
            allowed_formats: List of allowed formats (e.g., ['jpg', 'png', 'webp'])

        Returns:
            Dict with validation result
        """
        if max_size is None:
            max_size = settings.MAX_FILE_SIZE

        # Get file size
        file_obj.seek(0, 2)
        file_size = file_obj.tell()
        file_obj.seek(0)

        # Check max size
        if file_size > max_size:
            return {
                "valid": False,
                "message": f"Image too large. Maximum size: {max_size / 1048576:.2f}MB"
            }

        # Check file type (basic magic number detection)
        if allowed_formats:
            header = file_obj.read(512)
            file_obj.seek(0)

            detected_format = None
            if header.startswith(b'\xFF\xD8\xFF'):
                detected_format = 'jpg'
            elif header.startswith(b'\x89PNG'):
                detected_format = 'png'
            elif header.startswith(b'GIF'):
                detected_format = 'gif'
            elif header.startswith(b'RIFF') and b'WEBP' in header[:20]:
                detected_format = 'webp'

            if detected_format and detected_format not in allowed_formats:
                return {
                    "valid": False,
                    "message": f"Image format not allowed. Allowed formats: {', '.join(allowed_formats)}"
                }

        return {
            "valid": True,
            "size": file_size,
            "message": "Image is valid"
        }


# Create singleton instance (will be initialized when credentials are available)
try:
    cloudinary_service = CloudinaryService()
except ValueError:
    # If Cloudinary credentials not configured, service won't be available
    cloudinary_service = None
