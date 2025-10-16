"""Online auto store schemas"""
from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field
from app.models.store import OrderStatus


# Product Schemas
class ProductBase(BaseModel):
    """Base product schema"""
    name: str
    description: str
    category: str
    brand: str
    price: float = Field(gt=0)
    stock_quantity: int = Field(ge=0)


class ProductCreate(ProductBase):
    """Create product schema"""
    sku: str
    images: Optional[List[str]] = None
    specifications: Optional[Dict[str, Any]] = None
    compatible_makes: Optional[List[str]] = None
    compatible_models: Optional[List[str]] = None


class ProductUpdate(BaseModel):
    """Update product schema"""
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    brand: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    stock_quantity: Optional[int] = Field(None, ge=0)
    images: Optional[List[str]] = None
    specifications: Optional[Dict[str, Any]] = None
    compatible_makes: Optional[List[str]] = None
    compatible_models: Optional[List[str]] = None
    is_active: Optional[bool] = None


class ProductResponse(ProductBase):
    """Product response schema"""
    id: str
    vendor_id: str
    sku: str
    images: Optional[List[str]]
    specifications: Optional[Dict[str, Any]]
    compatible_makes: Optional[List[str]]
    compatible_models: Optional[List[str]]
    is_active: bool
    average_rating: float
    total_ratings: int
    total_sold: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Vendor Schemas
class VendorBase(BaseModel):
    """Base vendor schema"""
    business_name: str
    business_registration: str
    business_description: Optional[str] = None


class VendorCreate(VendorBase):
    """Create vendor schema"""
    user_id: str
    business_address: Dict[str, Any]
    business_phone: str


class VendorUpdate(BaseModel):
    """Update vendor schema"""
    business_name: Optional[str] = None
    business_description: Optional[str] = None
    business_address: Optional[Dict[str, Any]] = None
    business_phone: Optional[str] = None
    is_verified: Optional[bool] = None
    is_active: Optional[bool] = None


class VendorResponse(VendorBase):
    """Vendor response schema"""
    id: str
    user_id: str
    business_address: Dict[str, Any]
    business_phone: str
    is_verified: bool
    is_active: bool
    average_rating: float
    total_ratings: int
    total_sales: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Cart Schemas
class CartItemAdd(BaseModel):
    """Add item to cart schema"""
    product_id: str
    quantity: int = Field(gt=0)


class CartItemUpdate(BaseModel):
    """Update cart item schema"""
    quantity: int = Field(gt=0)


class CartItemResponse(BaseModel):
    """Cart item response schema"""
    id: str
    product_id: str
    quantity: int
    unit_price: float
    subtotal: float
    created_at: datetime

    class Config:
        from_attributes = True


class CartResponse(BaseModel):
    """Cart response schema"""
    id: str
    user_id: str
    items: List[CartItemResponse]
    total_items: int
    total_price: float
    updated_at: datetime

    class Config:
        from_attributes = True


# Order Schemas
class OrderCreate(BaseModel):
    """Create order schema"""
    delivery_address: Dict[str, Any]
    payment_method: str
    notes: Optional[str] = None


class OrderUpdate(BaseModel):
    """Update order schema"""
    status: Optional[OrderStatus] = None
    tracking_number: Optional[str] = None


class OrderItemResponse(BaseModel):
    """Order item response schema"""
    id: str
    product_id: str
    vendor_id: str
    quantity: int
    unit_price: float
    subtotal: float

    class Config:
        from_attributes = True


class OrderResponse(BaseModel):
    """Order response schema"""
    id: str
    customer_id: str
    order_number: str
    status: OrderStatus
    items: List[OrderItemResponse]
    subtotal: float
    delivery_fee: float
    total_amount: float
    delivery_address: Dict[str, Any]
    payment_method: str
    payment_status: str
    notes: Optional[str]
    tracking_number: Optional[str]
    estimated_delivery: Optional[datetime]
    delivered_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Product Review Schemas
class ProductReviewCreate(BaseModel):
    """Create product review schema"""
    product_id: str
    rating: int = Field(ge=1, le=5)
    title: str
    review_text: str
    verified_purchase: bool = False


class ProductReviewResponse(BaseModel):
    """Product review response schema"""
    id: str
    product_id: str
    customer_id: str
    rating: int
    title: str
    review_text: str
    verified_purchase: bool
    helpful_count: int
    created_at: datetime

    class Config:
        from_attributes = True
