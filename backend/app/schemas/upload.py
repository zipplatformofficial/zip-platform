"""Upload schemas"""
from pydantic import BaseModel, Field
from typing import Optional


class UploadResponse(BaseModel):
    """Response schema for file upload"""
    success: bool
    url: Optional[str] = None
    key: Optional[str] = None
    content_type: Optional[str] = None
    message: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "url": "https://cdn.zipghana.com/avatars/abc123.jpg",
                "key": "avatars/abc123.jpg",
                "content_type": "image/jpeg",
                "message": "File uploaded successfully"
            }
        }


class DeleteResponse(BaseModel):
    """Response schema for file deletion"""
    success: bool
    message: str

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "File deleted successfully"
            }
        }
