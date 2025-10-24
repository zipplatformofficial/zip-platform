"""
Script to create sample maintenance services in the database
Run this with: python create_sample_services.py
"""
import sys
import os

# Add the parent directory to sys.path to allow imports
sys.path.insert(0, os.path.dirname(__file__))

from sqlalchemy.orm import Session
from app.core.database import engine, SessionLocal
from app.models.maintenance import MaintenanceService, MaintenanceServiceType

def create_sample_services():
    """Create sample maintenance services"""
    db: Session = SessionLocal()

    try:
        # Check if services already exist
        existing = db.query(MaintenanceService).count()
        if existing > 0:
            print(f"⚠️  Found {existing} existing services. Clearing them first...")
            db.query(MaintenanceService).delete()
            db.commit()

        services = [
            {
                "name": "Premium Car Wash",
                "description": "Complete exterior and interior car wash with waxing and polishing. Includes vacuum cleaning, dashboard polish, and tire shine.",
                "service_type": MaintenanceServiceType.CAR_WASH,
                "base_price": 80.00,
                "estimated_duration": 60,
                "is_active": True
            },
            {
                "name": "Oil Change Service",
                "description": "Complete oil and filter change using premium synthetic oil. Includes 21-point inspection and fluid top-ups.",
                "service_type": MaintenanceServiceType.OIL_CHANGE,
                "base_price": 150.00,
                "estimated_duration": 45,
                "is_active": True
            },
            {
                "name": "Tire Repair & Rotation",
                "description": "Professional tire repair, rotation, and balancing. Includes pressure check and alignment inspection.",
                "service_type": MaintenanceServiceType.TIRE_REPAIR,
                "base_price": 120.00,
                "estimated_duration": 90,
                "is_active": True
            },
            {
                "name": "Computer Diagnostics",
                "description": "Comprehensive electronic system scan and diagnostics. Identifies engine, transmission, and sensor issues.",
                "service_type": MaintenanceServiceType.DIAGNOSTICS,
                "base_price": 100.00,
                "estimated_duration": 30,
                "is_active": True
            },
            {
                "name": "Battery Check & Replacement",
                "description": "Battery health check, terminal cleaning, and replacement if needed. Includes electrical system test.",
                "service_type": MaintenanceServiceType.BATTERY_CHECK,
                "base_price": 90.00,
                "estimated_duration": 30,
                "is_active": True
            },
            {
                "name": "Brake Service",
                "description": "Complete brake inspection and service. Includes pad replacement, rotor resurfacing, and fluid change.",
                "service_type": MaintenanceServiceType.BRAKE_SERVICE,
                "base_price": 250.00,
                "estimated_duration": 120,
                "is_active": True
            },
            {
                "name": "AC Service & Recharge",
                "description": "Air conditioning system service including refrigerant recharge, leak check, and filter replacement.",
                "service_type": MaintenanceServiceType.AC_SERVICE,
                "base_price": 180.00,
                "estimated_duration": 75,
                "is_active": True
            },
            {
                "name": "Engine Tune-Up",
                "description": "Complete engine tune-up including spark plug replacement, fuel system cleaning, and performance optimization.",
                "service_type": MaintenanceServiceType.ENGINE_TUNE_UP,
                "base_price": 300.00,
                "estimated_duration": 150,
                "is_active": True
            },
            {
                "name": "Transmission Service",
                "description": "Transmission fluid change, filter replacement, and system inspection. Helps prevent costly repairs.",
                "service_type": MaintenanceServiceType.TRANSMISSION_SERVICE,
                "base_price": 280.00,
                "estimated_duration": 120,
                "is_active": True
            },
            {
                "name": "Electrical System Repair",
                "description": "Diagnosis and repair of electrical issues including lights, sensors, and wiring problems.",
                "service_type": MaintenanceServiceType.ELECTRICAL_REPAIR,
                "base_price": 200.00,
                "estimated_duration": 90,
                "is_active": True
            },
            {
                "name": "Express Car Wash",
                "description": "Quick exterior wash and dry. Perfect for a fast refresh between full details.",
                "service_type": MaintenanceServiceType.CAR_WASH,
                "base_price": 40.00,
                "estimated_duration": 20,
                "is_active": True
            },
            {
                "name": "Full Service Oil Change",
                "description": "Oil change with filter, plus comprehensive 50-point vehicle inspection and report.",
                "service_type": MaintenanceServiceType.OIL_CHANGE,
                "base_price": 220.00,
                "estimated_duration": 60,
                "is_active": True
            }
        ]

        print("\n[*] Creating sample maintenance services...")
        print("=" * 50)

        created_services = []
        for service_data in services:
            service = MaintenanceService(**service_data)
            db.add(service)
            created_services.append(service_data['name'])

        db.commit()

        print("\n[SUCCESS] Successfully created the following services:")
        for idx, name in enumerate(created_services, 1):
            print(f"   {idx}. {name}")

        print(f"\n[INFO] Total services created: {len(created_services)}")
        print("=" * 50)
        print("\n[*] Sample services added successfully!")
        print("[*] You can now view them at: http://localhost:5173/maintenance")
        print("[*] Use admin credentials to manage services: admin@zipghana.com / Admin@123\n")

    except Exception as e:
        print(f"\n[ERROR] Error creating services: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("  ZIP PLATFORM - Sample Services Creator")
    print("=" * 50)
    create_sample_services()
