"""Authentication endpoints"""
import uuid
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.v1.deps import get_db
from app.core.config import settings
from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    create_refresh_token,
    decode_token,
)
from app.models.user import User, UserRole
from app.schemas.user import UserCreate, UserResponse, UserLogin
from app.schemas.auth import Token, RefreshToken


router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_in: UserCreate,
    db: Session = Depends(get_db)
):
    """
    Register a new user

    - **email**: Valid email address (unique)
    - **phone**: Ghana phone number (unique)
    - **password**: Minimum 8 characters with at least 1 digit and 1 uppercase letter
    - **full_name**: User's full name
    - **user_type**: individual, corporate, or ride_hailing_driver
    """
    # Check if user with email already exists
    existing_user = db.query(User).filter(User.email == user_in.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Check if user with phone already exists
    existing_phone = db.query(User).filter(User.phone == user_in.phone).first()
    if existing_phone:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Phone number already registered"
        )

    # Generate unique referral code
    referral_code = f"ZIP{str(uuid.uuid4())[:8].upper()}"
    while db.query(User).filter(User.referral_code == referral_code).first():
        referral_code = f"ZIP{str(uuid.uuid4())[:8].upper()}"

    # Create new user
    db_user = User(
        email=user_in.email,
        phone=user_in.phone,
        password_hash=get_password_hash(user_in.password),
        full_name=user_in.full_name,
        user_type=user_in.user_type,
        role=UserRole.CUSTOMER,  # Default role
        referral_code=referral_code,
        company_name=user_in.company_name,
        company_registration=user_in.company_registration,
        location=user_in.location,
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


@router.post("/login", response_model=Token)
async def login(
    credentials: UserLogin,
    db: Session = Depends(get_db)
):
    """
    Login with email and password

    Returns JWT access token and refresh token
    """
    # Find user by email
    user = db.query(User).filter(User.email == credentials.email).first()

    if not user or not verify_password(credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is inactive. Please contact support."
        )

    # Create access and refresh tokens
    access_token = create_access_token(subject=str(user.id))
    refresh_token = create_refresh_token(subject=str(user.id))

    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer"
    )


@router.post("/refresh", response_model=Token)
async def refresh_access_token(
    refresh_data: RefreshToken,
    db: Session = Depends(get_db)
):
    """
    Refresh access token using refresh token

    Returns new access token and refresh token
    """
    # Decode refresh token
    payload = decode_token(refresh_data.refresh_token)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Check if it's a refresh token
    if payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Get user
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is inactive"
        )

    # Create new tokens
    access_token = create_access_token(subject=str(user.id))
    new_refresh_token = create_refresh_token(subject=str(user.id))

    return Token(
        access_token=access_token,
        refresh_token=new_refresh_token,
        token_type="bearer"
    )


@router.post("/logout")
async def logout():
    """
    Logout user

    Note: With JWT tokens, logout is handled client-side by deleting the tokens.
    This endpoint is provided for consistency and can be extended with token blacklisting.
    """
    return {"message": "Successfully logged out"}
