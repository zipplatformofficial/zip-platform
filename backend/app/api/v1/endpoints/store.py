"""Online auto store endpoints"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
import uuid

from app.api.v1.deps import get_db, get_current_active_user, require_vendor, require_admin
from app.models.user import User
from app.models.store import (
    Product,
    Vendor,
    Cart,
    CartItem,
    Order,
    OrderItem,
    ProductReview,
    OrderStatus
)
from app.schemas.store import (
    ProductCreate,
    ProductUpdate,
    ProductResponse,
    VendorCreate,
    VendorUpdate,
    VendorResponse,
    CartItemAdd,
    CartItemUpdate,
    CartResponse,
    OrderCreate,
    OrderUpdate,
    OrderResponse,
    ProductReviewCreate,
    ProductReviewResponse,
)


router = APIRouter()


# ==================== PRODUCTS ====================

@router.get("/products", response_model=List[ProductResponse])
async def list_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    category: Optional[str] = None,
    brand: Optional[str] = None,
    search: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    in_stock_only: bool = True,
    db: Session = Depends(get_db)
):
    """
    List all products with filters

    - **category**: Filter by product category
    - **brand**: Filter by brand
    - **search**: Search in name and description
    - **min_price**: Minimum price
    - **max_price**: Maximum price
    - **in_stock_only**: Show only in-stock products
    """
    query = db.query(Product).filter(Product.is_active == True)

    if in_stock_only:
        query = query.filter(Product.stock_quantity > 0)

    if category:
        query = query.filter(Product.category == category)

    if brand:
        query = query.filter(Product.brand.ilike(f"%{brand}%"))

    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                Product.name.ilike(search_term),
                Product.description.ilike(search_term)
            )
        )

    if min_price is not None:
        query = query.filter(Product.price >= min_price)

    if max_price is not None:
        query = query.filter(Product.price <= max_price)

    products = query.order_by(Product.average_rating.desc()).offset(skip).limit(limit).all()
    return products


@router.get("/products/{product_id}", response_model=ProductResponse)
async def get_product(
    product_id: str,
    db: Session = Depends(get_db)
):
    """Get a specific product by ID"""
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    return product


@router.post("/products", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(
    product_in: ProductCreate,
    current_user: User = Depends(require_vendor),
    db: Session = Depends(get_db)
):
    """Create a new product (Vendor only)"""
    # Get vendor profile
    vendor = db.query(Vendor).filter(Vendor.user_id == current_user.id).first()

    if not vendor:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Vendor profile not found"
        )

    if not vendor.is_verified or not vendor.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Vendor account must be verified and active"
        )

    # Check if SKU already exists
    existing_product = db.query(Product).filter(Product.sku == product_in.sku).first()
    if existing_product:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product with this SKU already exists"
        )

    product = Product(
        **product_in.model_dump(),
        vendor_id=vendor.id
    )

    db.add(product)
    db.commit()
    db.refresh(product)

    return product


@router.put("/products/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: str,
    product_update: ProductUpdate,
    current_user: User = Depends(require_vendor),
    db: Session = Depends(get_db)
):
    """Update a product (Vendor only, own products)"""
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    # Verify vendor owns this product
    vendor = db.query(Vendor).filter(Vendor.user_id == current_user.id).first()
    if not vendor or product.vendor_id != vendor.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this product"
        )

    update_data = product_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(product, field, value)

    db.commit()
    db.refresh(product)

    return product


@router.delete("/products/{product_id}")
async def delete_product(
    product_id: str,
    current_user: User = Depends(require_vendor),
    db: Session = Depends(get_db)
):
    """Deactivate a product (Vendor only, own products)"""
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    vendor = db.query(Vendor).filter(Vendor.user_id == current_user.id).first()
    if not vendor or product.vendor_id != vendor.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this product"
        )

    product.is_active = False
    db.commit()

    return {"message": "Product deactivated successfully"}


# ==================== SHOPPING CART ====================

@router.get("/cart", response_model=CartResponse)
async def get_cart(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get current user's shopping cart"""
    cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()

    if not cart:
        # Create cart if doesn't exist
        cart = Cart(user_id=current_user.id)
        db.add(cart)
        db.commit()
        db.refresh(cart)

    # Calculate totals
    total_items = len(cart.items)
    total_price = sum(item.subtotal for item in cart.items)

    return {
        "id": str(cart.id),
        "user_id": str(cart.user_id),
        "items": cart.items,
        "total_items": total_items,
        "total_price": total_price,
        "updated_at": cart.updated_at
    }


@router.post("/cart/items")
async def add_to_cart(
    item_in: CartItemAdd,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Add an item to cart"""
    # Verify product exists and has stock
    product = db.query(Product).filter(
        Product.id == item_in.product_id,
        Product.is_active == True
    ).first()

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    if product.stock_quantity < item_in.quantity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Insufficient stock. Only {product.stock_quantity} available"
        )

    # Get or create cart
    cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()
    if not cart:
        cart = Cart(user_id=current_user.id)
        db.add(cart)
        db.flush()

    # Check if item already in cart
    existing_item = db.query(CartItem).filter(
        CartItem.cart_id == cart.id,
        CartItem.product_id == item_in.product_id
    ).first()

    if existing_item:
        # Update quantity
        new_quantity = existing_item.quantity + item_in.quantity
        if product.stock_quantity < new_quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Insufficient stock. Only {product.stock_quantity} available"
            )
        existing_item.quantity = new_quantity
        existing_item.subtotal = existing_item.unit_price * new_quantity
    else:
        # Add new item
        cart_item = CartItem(
            cart_id=cart.id,
            product_id=item_in.product_id,
            quantity=item_in.quantity,
            unit_price=product.price,
            subtotal=product.price * item_in.quantity
        )
        db.add(cart_item)

    db.commit()

    return {"message": "Item added to cart successfully"}


@router.put("/cart/items/{item_id}")
async def update_cart_item(
    item_id: str,
    item_update: CartItemUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update cart item quantity"""
    cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()

    if not cart:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart not found"
        )

    item = db.query(CartItem).filter(
        CartItem.id == item_id,
        CartItem.cart_id == cart.id
    ).first()

    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart item not found"
        )

    # Check stock
    product = db.query(Product).filter(Product.id == item.product_id).first()
    if product.stock_quantity < item_update.quantity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Insufficient stock. Only {product.stock_quantity} available"
        )

    item.quantity = item_update.quantity
    item.subtotal = item.unit_price * item_update.quantity

    db.commit()

    return {"message": "Cart item updated successfully"}


@router.delete("/cart/items/{item_id}")
async def remove_from_cart(
    item_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Remove an item from cart"""
    cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()

    if not cart:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart not found"
        )

    item = db.query(CartItem).filter(
        CartItem.id == item_id,
        CartItem.cart_id == cart.id
    ).first()

    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart item not found"
        )

    db.delete(item)
    db.commit()

    return {"message": "Item removed from cart"}


@router.delete("/cart")
async def clear_cart(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Clear all items from cart"""
    cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()

    if cart:
        db.query(CartItem).filter(CartItem.cart_id == cart.id).delete()
        db.commit()

    return {"message": "Cart cleared successfully"}


# ==================== ORDERS ====================

@router.post("/orders", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(
    order_in: OrderCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create an order from cart"""
    # Get cart with items
    cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()

    if not cart or not cart.items:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cart is empty"
        )

    # Calculate totals
    subtotal = sum(item.subtotal for item in cart.items)
    delivery_fee = 20.0  # Fixed delivery fee (can be made dynamic)
    total_amount = subtotal + delivery_fee

    # Generate order number
    order_number = f"ORD{uuid.uuid4().hex[:8].upper()}"

    # Create order
    order = Order(
        customer_id=current_user.id,
        order_number=order_number,
        status=OrderStatus.PENDING,
        subtotal=subtotal,
        delivery_fee=delivery_fee,
        total_amount=total_amount,
        delivery_address=order_in.delivery_address,
        payment_method=order_in.payment_method,
        payment_status="pending",
        notes=order_in.notes
    )

    db.add(order)
    db.flush()

    # Create order items from cart items
    for cart_item in cart.items:
        order_item = OrderItem(
            order_id=order.id,
            product_id=cart_item.product_id,
            vendor_id=db.query(Product).filter(Product.id == cart_item.product_id).first().vendor_id,
            quantity=cart_item.quantity,
            unit_price=cart_item.unit_price,
            subtotal=cart_item.subtotal
        )
        db.add(order_item)

        # Update product stock
        product = db.query(Product).filter(Product.id == cart_item.product_id).first()
        product.stock_quantity -= cart_item.quantity
        product.total_sold += cart_item.quantity

    # Clear cart
    db.query(CartItem).filter(CartItem.cart_id == cart.id).delete()

    db.commit()
    db.refresh(order)

    return order


@router.get("/orders", response_model=List[OrderResponse])
async def list_my_orders(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    status: Optional[OrderStatus] = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """List current user's orders"""
    query = db.query(Order).filter(Order.customer_id == current_user.id)

    if status:
        query = query.filter(Order.status == status)

    orders = query.order_by(Order.created_at.desc()).offset(skip).limit(limit).all()
    return orders


@router.get("/orders/{order_id}", response_model=OrderResponse)
async def get_order(
    order_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get a specific order"""
    order = db.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )

    # Check authorization
    from app.models.user import UserRole
    if order.customer_id != current_user.id and current_user.role not in [UserRole.ADMIN, UserRole.VENDOR]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this order"
        )

    return order


# ==================== PRODUCT REVIEWS ====================

@router.post("/products/{product_id}/reviews", response_model=ProductReviewResponse, status_code=status.HTTP_201_CREATED)
async def create_product_review(
    product_id: str,
    review_in: ProductReviewCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create a product review"""
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    # Check if user already reviewed this product
    existing_review = db.query(ProductReview).filter(
        ProductReview.product_id == product_id,
        ProductReview.customer_id == current_user.id
    ).first()

    if existing_review:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have already reviewed this product"
        )

    review = ProductReview(
        **review_in.model_dump(),
        customer_id=current_user.id
    )

    db.add(review)

    # Update product rating
    total_ratings = product.total_ratings
    avg_rating = product.average_rating
    new_total = total_ratings + 1
    new_avg = ((avg_rating * total_ratings) + review_in.rating) / new_total

    product.average_rating = new_avg
    product.total_ratings = new_total

    db.commit()
    db.refresh(review)

    return review


@router.get("/products/{product_id}/reviews", response_model=List[ProductReviewResponse])
async def list_product_reviews(
    product_id: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """List all reviews for a product"""
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    reviews = db.query(ProductReview).filter(
        ProductReview.product_id == product_id
    ).order_by(ProductReview.created_at.desc()).offset(skip).limit(limit).all()

    return reviews
