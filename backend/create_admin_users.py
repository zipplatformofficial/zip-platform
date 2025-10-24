"""Create administrative and sample users for ZIP platform"""
from sqlalchemy.orm import Session
import uuid

from app.core.database import SessionLocal
from app.core.security import get_password_hash
from app.models.user import User, UserRole, UserType
from app.models.maintenance import Technician
from app.models.store import Vendor


def generate_referral_code():
    """Generate a unique referral code"""
    return f"ZIP{uuid.uuid4().hex[:8].upper()}"


def create_users():
    """Create all user types for the platform"""
    db: Session = SessionLocal()

    try:
        print("="*60)
        print("ZIP Platform - User Creation Script")
        print("="*60)

        # ==================== ADMINISTRATIVE USERS ====================
        print("\n[1] Creating Administrative Users...")
        print("-"*60)

        admin_users = [
            {
                "email": "admin@zip.com",
                "phone": "233200000001",
                "password": "Admin123!@#",
                "full_name": "System Administrator",
                "role": UserRole.ADMIN,
                "user_type": UserType.INDIVIDUAL,
            },
            {
                "email": "manager@zip.com",
                "phone": "233200000002",
                "password": "Manager123!@#",
                "full_name": "Operations Manager",
                "role": UserRole.OPERATIONS_MANAGER,
                "user_type": UserType.INDIVIDUAL,
            },
            {
                "email": "support@zip.com",
                "phone": "233200000003",
                "password": "Support123!@#",
                "full_name": "Customer Support Agent",
                "role": UserRole.CUSTOMER_SUPPORT,
                "user_type": UserType.INDIVIDUAL,
            },
        ]

        for user_data in admin_users:
            existing = db.query(User).filter(User.email == user_data["email"]).first()
            if existing:
                print(f"  * {user_data['role'].value.upper()}: {user_data['email']} (already exists)")
            else:
                password = user_data.pop("password")
                user = User(
                    **user_data,
                    password_hash=get_password_hash(password),
                    is_active=True,
                    is_verified=True,
                    email_verified=True,
                    phone_verified=True,
                    referral_code=generate_referral_code(),
                )
                db.add(user)
                db.commit()
                db.refresh(user)
                print(f"  + {user_data['role'].value.upper()}: {user_data['email']}")
                print(f"    Password: {password}")

        # ==================== RENTAL MANAGERS ====================
        print("\n[2] Creating Rental Manager...")
        print("-"*60)

        rental_managers = [
            {
                "email": "rentals@zip.com",
                "phone": "233200000010",
                "password": "Rentals123!@#",
                "full_name": "Rental Fleet Manager",
                "role": UserRole.RENTAL_MANAGER,
                "user_type": UserType.INDIVIDUAL,
            },
        ]

        for user_data in rental_managers:
            existing = db.query(User).filter(User.email == user_data["email"]).first()
            if existing:
                print(f"  * {user_data['email']} (already exists)")
            else:
                password = user_data.pop("password")
                user = User(
                    **user_data,
                    password_hash=get_password_hash(password),
                    is_active=True,
                    is_verified=True,
                    email_verified=True,
                    phone_verified=True,
                    referral_code=generate_referral_code(),
                )
                db.add(user)
                db.commit()
                db.refresh(user)
                print(f"  + {user_data['email']}")
                print(f"    Password: {password}")

        # ==================== SERVICE PROVIDERS (TECHNICIANS) ====================
        print("\n[3] Creating Service Provider Technicians...")
        print("-"*60)

        technician_users = [
            {
                "email": "tech1@zip.com",
                "phone": "233200000020",
                "password": "Tech123!@#",
                "full_name": "John Mensah",
                "role": UserRole.TECHNICIAN,
                "user_type": UserType.INDIVIDUAL,
                "bio": "Certified mechanic with 10+ years experience in general car servicing",
                "specializations": ["general", "oil_change", "brakes"],
                "experience_years": 10
            },
            {
                "email": "tech2@zip.com",
                "phone": "233200000021",
                "password": "Tech123!@#",
                "full_name": "Kwame Osei",
                "role": UserRole.TECHNICIAN,
                "user_type": UserType.INDIVIDUAL,
                "bio": "Electrical systems specialist and AC expert",
                "specializations": ["electrical", "ac_service", "diagnostic"],
                "experience_years": 8
            },
            {
                "email": "tech3@zip.com",
                "phone": "233200000022",
                "password": "Tech123!@#",
                "full_name": "Ama Boateng",
                "role": UserRole.TECHNICIAN,
                "user_type": UserType.INDIVIDUAL,
                "bio": "Transmission and tire specialist",
                "specializations": ["transmission", "tires", "general"],
                "experience_years": 7
            },
        ]

        for user_data in technician_users:
            existing = db.query(User).filter(User.email == user_data["email"]).first()
            if existing:
                print(f"  * {user_data['full_name']}: {user_data['email']} (already exists)")
            else:
                password = user_data.pop("password")
                bio = user_data.pop("bio")
                specializations = user_data.pop("specializations")
                experience_years = user_data.pop("experience_years")

                user = User(
                    **user_data,
                    password_hash=get_password_hash(password),
                    is_active=True,
                    is_verified=True,
                    email_verified=True,
                    phone_verified=True,
                    referral_code=generate_referral_code(),
                )
                db.add(user)
                db.flush()

                # Create technician profile
                technician = Technician(
                    user_id=user.id,
                    bio=bio,
                    specializations=specializations,
                    experience_years=experience_years,
                    is_available=True,
                    is_verified=True,
                    average_rating=4.5,
                    total_ratings=10,
                    total_jobs_completed=50
                )
                db.add(technician)

                db.commit()
                db.refresh(user)
                print(f"  + {user_data['full_name']}: {user_data['email']}")
                print(f"    Password: {password}")
                print(f"    Specializations: {', '.join(specializations)}")

        # ==================== VENDORS (AUTO PARTS SELLERS) ====================
        print("\n[4] Creating Auto Parts Vendors...")
        print("-"*60)

        vendor_users = [
            {
                "email": "vendor1@zip.com",
                "phone": "233200000030",
                "password": "Vendor123!@#",
                "full_name": "AutoParts Ghana Owner",
                "role": UserRole.VENDOR,
                "user_type": UserType.CORPORATE,
                "company_name": "AutoParts Ghana Ltd",
                "business_name": "AutoParts Ghana",
                "business_registration": "CS123456789",
                "business_description": "Premium auto parts supplier for all car makes and models",
                "business_address": {"street": "123 Main St", "city": "Accra", "region": "Greater Accra"},
                "business_phone": "233302000001",
            },
            {
                "email": "vendor2@zip.com",
                "phone": "233200000031",
                "password": "Vendor123!@#",
                "full_name": "Car Zone Owner",
                "role": UserRole.VENDOR,
                "user_type": UserType.CORPORATE,
                "company_name": "Car Zone Limited",
                "business_name": "Car Zone Auto Store",
                "business_registration": "CS987654321",
                "business_description": "Affordable genuine and aftermarket auto parts",
                "business_address": {"street": "456 Ring Road", "city": "Kumasi", "region": "Ashanti"},
                "business_phone": "233322000001",
            },
        ]

        for user_data in vendor_users:
            existing = db.query(User).filter(User.email == user_data["email"]).first()
            if existing:
                print(f"  * {user_data['business_name']}: {user_data['email']} (already exists)")
            else:
                password = user_data.pop("password")
                business_name = user_data.pop("business_name")
                business_registration = user_data.pop("business_registration")
                business_description = user_data.pop("business_description")
                business_address = user_data.pop("business_address")
                business_phone = user_data.pop("business_phone")

                user = User(
                    **user_data,
                    password_hash=get_password_hash(password),
                    is_active=True,
                    is_verified=True,
                    email_verified=True,
                    phone_verified=True,
                    referral_code=generate_referral_code(),
                )
                db.add(user)
                db.flush()

                # Create vendor profile
                vendor = Vendor(
                    user_id=user.id,
                    business_name=business_name,
                    business_registration=business_registration,
                    business_description=business_description,
                    business_address=business_address,
                    business_phone=business_phone,
                    is_verified=True,
                    is_active=True,
                    average_rating=4.6,
                    total_ratings=25,
                    total_sales=100
                )
                db.add(vendor)

                db.commit()
                db.refresh(user)
                print(f"  + {business_name}: {user_data['email']}")
                print(f"    Password: {password}")

        # ==================== CUSTOMERS ====================
        print("\n[5] Creating Sample Customers...")
        print("-"*60)

        customer_users = [
            {
                "email": "customer1@example.com",
                "phone": "233240000001",
                "password": "Customer123!",
                "full_name": "Kofi Asante",
                "role": UserRole.CUSTOMER,
                "user_type": UserType.INDIVIDUAL,
            },
            {
                "email": "customer2@example.com",
                "phone": "233240000002",
                "password": "Customer123!",
                "full_name": "Akua Mensah",
                "role": UserRole.CUSTOMER,
                "user_type": UserType.INDIVIDUAL,
            },
            {
                "email": "corporate1@example.com",
                "phone": "233240000010",
                "password": "Corporate123!",
                "full_name": "Fleet Manager",
                "role": UserRole.CUSTOMER,
                "user_type": UserType.CORPORATE,
                "company_name": "Uber Ghana",
                "company_registration": "CS456789123",
            },
        ]

        for user_data in customer_users:
            existing = db.query(User).filter(User.email == user_data["email"]).first()
            if existing:
                print(f"  * {user_data['full_name']}: {user_data['email']} (already exists)")
            else:
                password = user_data.pop("password")
                user = User(
                    **user_data,
                    password_hash=get_password_hash(password),
                    is_active=True,
                    is_verified=True if user_data.get("user_type") == UserType.INDIVIDUAL else False,
                    email_verified=True,
                    phone_verified=True,
                    referral_code=generate_referral_code(),
                    loyalty_points=100,
                )
                db.add(user)
                db.commit()
                db.refresh(user)
                print(f"  + {user_data['full_name']}: {user_data['email']}")
                print(f"    Password: {password}")

        # ==================== SUMMARY ====================
        print("\n" + "="*60)
        print("USER CREATION SUMMARY")
        print("="*60)

        admin_count = db.query(User).filter(User.role == UserRole.ADMIN).count()
        ops_manager_count = db.query(User).filter(User.role == UserRole.OPERATIONS_MANAGER).count()
        support_count = db.query(User).filter(User.role == UserRole.CUSTOMER_SUPPORT).count()
        rental_manager_count = db.query(User).filter(User.role == UserRole.RENTAL_MANAGER).count()
        technician_count = db.query(User).filter(User.role == UserRole.TECHNICIAN).count()
        vendor_count = db.query(User).filter(User.role == UserRole.VENDOR).count()
        customer_count = db.query(User).filter(User.role == UserRole.CUSTOMER).count()
        total_users = db.query(User).count()

        print(f"\nAdministrative Users:")
        print(f"  - Admins:              {admin_count}")
        print(f"  - Operations Managers: {ops_manager_count}")
        print(f"  - Customer Support:    {support_count}")
        print(f"  - Rental Managers:     {rental_manager_count}")
        print(f"\nService Providers:")
        print(f"  - Technicians:         {technician_count}")
        print(f"  - Vendors:             {vendor_count}")
        print(f"\nCustomers:              {customer_count}")
        print(f"\n{'='*60}")
        print(f"Total Users:            {total_users}")
        print(f"{'='*60}")

        print("\n[SUCCESS] All users created successfully!")

    except Exception as e:
        print(f"\nERROR: Error creating users: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    create_users()
