"""Create default admin user"""
import sys
import bcrypt
from sqlalchemy.orm import Session
from app.core.database import engine, SessionLocal
from app.models.user import User, UserRole

def create_admin_user():
    """Create default admin user if not exists"""
    db = SessionLocal()

    try:
        # Check if admin already exists and delete it
        admin = db.query(User).filter(User.email == "admin@zipghana.com").first()

        if admin:
            print("Deleting old admin user...")
            db.delete(admin)
            db.commit()
            print("Old admin user deleted!")

        # Hash password directly with bcrypt
        password = "Admin@123"
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        # Create admin user
        admin = User(
            email="admin@zipghana.com",
            password_hash=password_hash,
            full_name="ZIP Platform Admin",
            phone="+233000000000",
            role=UserRole.ADMIN,
            is_active=True,
            email_verified=True  # Admin is pre-verified
        )

        db.add(admin)
        db.commit()
        db.refresh(admin)

        print("=" * 50)
        print("Admin user created successfully!")
        print("=" * 50)
        print(f"Email: admin@zipghana.com")
        print(f"Password: Admin@123")
        print(f"Role: {admin.role}")
        print("=" * 50)
        print("\nYou can now login with these credentials at:")
        print("http://localhost:5173/login")
        print("=" * 50)

    except Exception as e:
        print(f"Error creating admin user: {str(e)}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_admin_user()
