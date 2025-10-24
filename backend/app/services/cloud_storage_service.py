"""Cloud storage service for file uploads (AWS S3)"""
import boto3
from botocore.exceptions import ClientError
import uuid
import mimetypes
from typing import Optional, BinaryIO, Dict, Any
from pathlib import Path
from app.core.config import settings


class CloudStorageService:
    """Service for handling file uploads to AWS S3"""

    def __init__(self):
        self.bucket_name = settings.AWS_S3_BUCKET_NAME
        self.region = settings.AWS_S3_REGION
        self.cdn_url = settings.AWS_S3_CDN_URL

        if not settings.AWS_ACCESS_KEY_ID or not settings.AWS_SECRET_ACCESS_KEY:
            raise ValueError("AWS credentials are not configured")

        if not self.bucket_name:
            raise ValueError("AWS_S3_BUCKET_NAME is not configured")

        # Initialize S3 client
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=self.region
        )

    def _generate_unique_filename(self, original_filename: str, folder: str = "") -> str:
        """
        Generate a unique filename to avoid conflicts

        Args:
            original_filename: Original file name
            folder: Folder path in S3 bucket (e.g., 'avatars', 'products')

        Returns:
            Unique S3 key
        """
        # Get file extension
        file_ext = Path(original_filename).suffix.lower()

        # Generate unique ID
        unique_id = str(uuid.uuid4())

        # Create filename: folder/uuid.ext
        if folder:
            return f"{folder}/{unique_id}{file_ext}"
        return f"{unique_id}{file_ext}"

    def upload_file(
        self,
        file_obj: BinaryIO,
        filename: str,
        folder: str = "",
        content_type: Optional[str] = None,
        metadata: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Upload a file to S3

        Args:
            file_obj: File object to upload
            filename: Original filename
            folder: Folder path in S3 (e.g., 'avatars', 'products', 'documents')
            content_type: MIME type (auto-detected if not provided)
            metadata: Additional metadata to attach to file

        Returns:
            Dict with file URL and metadata
        """
        try:
            # Generate unique filename
            s3_key = self._generate_unique_filename(filename, folder)

            # Auto-detect content type if not provided
            if not content_type:
                content_type, _ = mimetypes.guess_type(filename)
                if not content_type:
                    content_type = 'application/octet-stream'

            # Prepare upload parameters
            extra_args = {
                'ContentType': content_type,
                'ACL': 'public-read'  # Make file publicly accessible
            }

            if metadata:
                extra_args['Metadata'] = metadata

            # Upload file
            self.s3_client.upload_fileobj(
                file_obj,
                self.bucket_name,
                s3_key,
                ExtraArgs=extra_args
            )

            # Generate file URL
            if self.cdn_url:
                file_url = f"{self.cdn_url}/{s3_key}"
            else:
                file_url = f"https://{self.bucket_name}.s3.{self.region}.amazonaws.com/{s3_key}"

            return {
                "success": True,
                "url": file_url,
                "key": s3_key,
                "content_type": content_type,
                "message": "File uploaded successfully"
            }

        except ClientError as e:
            return {
                "success": False,
                "message": f"Upload failed: {str(e)}"
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Unexpected error: {str(e)}"
            }

    def delete_file(self, s3_key: str) -> Dict[str, Any]:
        """
        Delete a file from S3

        Args:
            s3_key: S3 key (path) of file to delete

        Returns:
            Dict with success status
        """
        try:
            self.s3_client.delete_object(
                Bucket=self.bucket_name,
                Key=s3_key
            )

            return {
                "success": True,
                "message": "File deleted successfully"
            }

        except ClientError as e:
            return {
                "success": False,
                "message": f"Delete failed: {str(e)}"
            }

    def get_presigned_url(
        self,
        s3_key: str,
        expiration: int = 3600
    ) -> Dict[str, Any]:
        """
        Generate a presigned URL for temporary access to a private file

        Args:
            s3_key: S3 key of the file
            expiration: URL expiration time in seconds (default: 1 hour)

        Returns:
            Dict with presigned URL
        """
        try:
            url = self.s3_client.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': self.bucket_name,
                    'Key': s3_key
                },
                ExpiresIn=expiration
            )

            return {
                "success": True,
                "url": url,
                "expires_in": expiration
            }

        except ClientError as e:
            return {
                "success": False,
                "message": f"Failed to generate URL: {str(e)}"
            }

    def validate_file(
        self,
        file_obj: BinaryIO,
        allowed_types: Optional[list] = None,
        max_size: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Validate file before upload

        Args:
            file_obj: File object to validate
            allowed_types: List of allowed MIME types (e.g., ['image/jpeg', 'image/png'])
            max_size: Maximum file size in bytes

        Returns:
            Dict with validation result
        """
        # Get file size
        file_obj.seek(0, 2)  # Seek to end
        file_size = file_obj.tell()
        file_obj.seek(0)  # Reset to beginning

        # Check max size
        if max_size and file_size > max_size:
            return {
                "valid": False,
                "message": f"File too large. Maximum size: {max_size / 1048576:.2f}MB"
            }

        # Check file type (if specified)
        if allowed_types:
            # Read first few bytes to detect file type
            header = file_obj.read(512)
            file_obj.seek(0)

            # Basic file type detection by magic numbers
            detected_type = None
            if header.startswith(b'\xFF\xD8\xFF'):
                detected_type = 'image/jpeg'
            elif header.startswith(b'\x89PNG'):
                detected_type = 'image/png'
            elif header.startswith(b'GIF'):
                detected_type = 'image/gif'
            elif header.startswith(b'%PDF'):
                detected_type = 'application/pdf'

            if detected_type and detected_type not in allowed_types:
                return {
                    "valid": False,
                    "message": f"File type not allowed. Allowed types: {', '.join(allowed_types)}"
                }

        return {
            "valid": True,
            "size": file_size,
            "message": "File is valid"
        }


# Create singleton instance (will be initialized when credentials are available)
try:
    cloud_storage_service = CloudStorageService()
except ValueError:
    # If AWS credentials not configured, service won't be available
    cloud_storage_service = None
