"""Online Auto Store models"""
import enum
from sqlalchemy import Column, String, Integer, ForeignKey, Enum, Text, JSON, Float, Boolean
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class ProductCategory(str, enum.Enum):
    """Product categories"""
    ENGINE_PARTS = "engine_parts"
    BODY_PARTS = "body_parts"
    ELECTRICAL = "electrical"
    TIRES = "tires"
    ACCESSORIES = "accessories"
    FLUIDS = "fluids"
    BRAKES = "brakes"
    SUSPENSION = "suspension"
    EXHAUST = "exhaust"
    INTERIOR = "interior"
    LIGHTING = "lighting"
    OTHER = "other"


class OrderStatus(str, enum.Enum):
    """Order status"""
    PENDING = "pending"
    CONFIRMED = "confirmed"
    PROCESSING = "processing"
    PACKED = "packed"
    DISPATCHED = "dispatched"
    IN_TRANSIT = "in_transit"
    DELIVERED = "delivered"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    RETURNED = "returned"
    REFUNDED = "refunded"


class Vendor(BaseModel):
    """Vendor/Seller profile"""

    __tablename__ = "vendors"

    # Link to user account
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)

    # Business Information
    business_name = Column(String(255), nullable=False)
    business_registration = Column(String(100), nullable=True)
    business_address = Column(JSON, nullable=False)
    business_phone = Column(String(20), nullable=False)
    business_email = Column(String(255), nullable=False)

    # Verification
    is_verified = Column(Boolean, default=False, nullable=False)
    verification_documents = Column(JSON, nullable=True)
    verified_badge = Column(Boolean, default=False, nullable=False)

    # Store Info
    store_logo = Column(String(500), nullable=True)
    store_banner = Column(String(500), nullable=True)
    store_description = Column(Text, nullable=True)

    # Performance
    total_products = Column(Integer, default=0, nullable=False)
    total_sales = Column(Integer, default=0, nullable=False)
    total_revenue = Column(Float, default=0.0, nullable=False)
    average_rating = Column(Float, default=0.0, nullable=False)
    total_ratings = Column(Integer, default=0, nullable=False)
    response_rate = Column(Float, default=0.0, nullable=False)
    fulfillment_rate = Column(Float, default=0.0, nullable=False)

    # Financial
    commission_rate = Column(Float, nullable=False)  # Platform commission
    pending_payout = Column(Float, default=0.0, nullable=False)
    total_payouts = Column(Float, default=0.0, nullable=False)
    payout_method = Column(JSON, nullable=True)  # Mobile money, bank details

    # Settings
    is_active = Column(Boolean, default=True, nullable=False)
    auto_accept_orders = Column(Boolean, default=False, nullable=False)

    # Relationships
    user = relationship("User")
    products = relationship("Product", back_populates="vendor")
    orders = relationship("Order", back_populates="vendor")

    def __repr__(self):
        return f"<Vendor {self.business_name}>"


class Product(BaseModel):
    """Product listing"""

    __tablename__ = "products"

    # Vendor
    vendor_id = Column(Integer, ForeignKey("vendors.id", ondelete="CASCADE"), nullable=False)

    # Product Info
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    category = Column(Enum(ProductCategory), nullable=False)
    subcategory = Column(String(100), nullable=True)

    # Product Details
    brand = Column(String(100), nullable=True)
    part_number = Column(String(100), nullable=True)
    condition = Column(String(50), nullable=False)  # New/Refurbished
    specifications = Column(JSON, nullable=True)

    # Vehicle Compatibility
    compatible_makes = Column(JSON, nullable=True)  # Array of makes
    compatible_models = Column(JSON, nullable=True)  # Array of models
    compatible_years = Column(JSON, nullable=True)  # Array of years

    # Media
    images = Column(JSON, nullable=False)  # Array of image URLs
    videos = Column(JSON, nullable=True)

    # Pricing & Inventory
    price = Column(Float, nullable=False)
    compare_at_price = Column(Float, nullable=True)  # Original price for discounts
    stock_quantity = Column(Integer, nullable=False)
    low_stock_threshold = Column(Integer, default=5, nullable=False)

    # Verification & Quality
    is_verified = Column(Boolean, default=False, nullable=False)
    authenticity_certificate = Column(String(500), nullable=True)
    warranty_info = Column(JSON, nullable=True)

    # Status
    is_active = Column(Boolean, default=True, nullable=False)
    is_featured = Column(Boolean, default=False, nullable=False)

    # Performance
    total_sold = Column(Integer, default=0, nullable=False)
    total_views = Column(Integer, default=0, nullable=False)
    average_rating = Column(Float, default=0.0, nullable=False)
    total_ratings = Column(Integer, default=0, nullable=False)

    # SEO
    search_tags = Column(JSON, nullable=True)
    meta_description = Column(String(500), nullable=True)

    # Relationships
    vendor = relationship("Vendor", back_populates="products")
    reviews = relationship("ProductReview", back_populates="product")
    order_items = relationship("OrderItem", back_populates="product")

    def __repr__(self):
        return f"<Product {self.name}>"


class Cart(BaseModel):
    """Shopping cart"""

    __tablename__ = "carts"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)

    # Relationships
    user = relationship("User", back_populates="cart")
    items = relationship("CartItem", back_populates="cart", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Cart user_id={self.user_id}>"


class CartItem(BaseModel):
    """Cart item"""

    __tablename__ = "cart_items"

    cart_id = Column(Integer, ForeignKey("carts.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)

    # Relationships
    cart = relationship("Cart", back_populates="items")
    product = relationship("Product")

    def __repr__(self):
        return f"<CartItem cart={self.cart_id} product={self.product_id}>"


class Order(BaseModel):
    """Customer order"""

    __tablename__ = "orders"

    # Customer & Vendor
    customer_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    vendor_id = Column(Integer, ForeignKey("vendors.id", ondelete="SET NULL"), nullable=True)

    # Order Details
    order_number = Column(String(50), unique=True, nullable=False, index=True)
    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING, nullable=False)

    # Delivery
    delivery_option = Column(String(50), nullable=False)  # standard/express/pickup
    delivery_address = Column(JSON, nullable=False)
    delivery_fee = Column(Float, default=0.0, nullable=False)
    estimated_delivery_date = Column(String(50), nullable=True)
    actual_delivery_date = Column(String(50), nullable=True)

    # Vehicle Compatibility (optional)
    customer_vehicle = Column(JSON, nullable=True)  # Vehicle details for compatibility check

    # Pricing
    subtotal = Column(Float, nullable=False)
    delivery_cost = Column(Float, default=0.0, nullable=False)
    tax = Column(Float, default=0.0, nullable=False)
    discount = Column(Float, default=0.0, nullable=False)
    total_amount = Column(Float, nullable=False)

    # Vendor Commission
    platform_commission = Column(Float, nullable=False)
    vendor_payout = Column(Float, nullable=False)

    # Tracking
    tracking_number = Column(String(100), nullable=True)
    tracking_url = Column(String(500), nullable=True)
    current_location = Column(JSON, nullable=True)

    # Vendor Actions
    vendor_confirmed_at = Column(String(50), nullable=True)
    packed_at = Column(String(50), nullable=True)
    dispatched_at = Column(String(50), nullable=True)

    # Customer Actions
    customer_received_at = Column(String(50), nullable=True)
    customer_confirmed_delivery = Column(Boolean, default=False, nullable=False)

    # Return/Refund
    return_requested = Column(Boolean, default=False, nullable=False)
    return_reason = Column(Text, nullable=True)
    return_approved = Column(Boolean, default=False, nullable=False)
    return_photos = Column(JSON, nullable=True)
    refund_amount = Column(Float, default=0.0, nullable=False)
    refund_processed = Column(Boolean, default=False, nullable=False)

    # Cancellation
    cancellation_reason = Column(Text, nullable=True)
    cancelled_by = Column(String(50), nullable=True)

    # Notes
    customer_notes = Column(Text, nullable=True)
    vendor_notes = Column(Text, nullable=True)
    internal_notes = Column(Text, nullable=True)

    # Relationships
    customer = relationship("User", back_populates="orders")
    vendor = relationship("Vendor", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    payment = relationship("Payment", back_populates="order", uselist=False)

    def __repr__(self):
        return f"<Order {self.order_number}>"


class OrderItem(BaseModel):
    """Order item"""

    __tablename__ = "order_items"

    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="SET NULL"), nullable=True)

    # Product snapshot (in case product is deleted/changed)
    product_name = Column(String(255), nullable=False)
    product_image = Column(String(500), nullable=True)
    product_price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)
    subtotal = Column(Float, nullable=False)

    # Product details at time of purchase
    product_details = Column(JSON, nullable=True)

    # Relationships
    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")

    def __repr__(self):
        return f"<OrderItem {self.product_name} x {self.quantity}>"


class ProductReview(BaseModel):
    """Product review"""

    __tablename__ = "product_reviews"

    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    customer_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="SET NULL"), nullable=True)

    # Review
    rating = Column(Integer, nullable=False)  # 1-5 stars
    title = Column(String(200), nullable=True)
    review_text = Column(Text, nullable=True)
    photos = Column(JSON, nullable=True)

    # Verification
    is_verified_purchase = Column(Boolean, default=False, nullable=False)

    # Moderation
    is_approved = Column(Boolean, default=True, nullable=False)
    is_flagged = Column(Boolean, default=False, nullable=False)

    # Helpfulness
    helpful_count = Column(Integer, default=0, nullable=False)
    not_helpful_count = Column(Integer, default=0, nullable=False)

    # Vendor Response
    vendor_response = Column(Text, nullable=True)
    vendor_responded_at = Column(String(50), nullable=True)

    # Relationships
    product = relationship("Product", back_populates="reviews")
    customer = relationship("User")

    def __repr__(self):
        return f"<ProductReview product={self.product_id} rating={self.rating}>"
