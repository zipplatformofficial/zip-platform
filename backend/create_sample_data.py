"""Create sample data for the ZIP platform"""
import asyncio
from datetime import date, datetime, timedelta
from sqlalchemy.orm import Session

from app.core.database import SessionLocal, engine
from app.models.base import Base
from app.models.maintenance import MaintenanceService
from app.models.rental import RentalVehicle

def create_sample_data():
    """Create sample maintenance services and rental vehicles"""
    db: Session = SessionLocal()

    try:
        print("Creating sample maintenance services...")

        # Check if services already exist
        existing_services = db.query(MaintenanceService).count()
        if existing_services > 0:
            print(f"✓ {existing_services} maintenance services already exist")
        else:
            services = [
                {
                    "name": "Full Car Service",
                    "description": "Complete car servicing including oil change, filter replacement, and general inspection",
                    "category": "general",
                    "base_price": 350.00,
                    "estimated_duration": 120,  # 2 hours
                    "is_active": True
                },
                {
                    "name": "Oil Change Service",
                    "description": "Professional oil and oil filter change with inspection",
                    "category": "oil_change",
                    "base_price": 150.00,
                    "estimated_duration": 45,
                    "is_active": True
                },
                {
                    "name": "Brake System Service",
                    "description": "Brake pads, discs, and fluid check and replacement",
                    "category": "brakes",
                    "base_price": 400.00,
                    "estimated_duration": 90,
                    "is_active": True
                },
                {
                    "name": "Battery Check & Replacement",
                    "description": "Battery health check and replacement if needed",
                    "category": "electrical",
                    "base_price": 200.00,
                    "estimated_duration": 30,
                    "is_active": True
                },
                {
                    "name": "AC Service & Repair",
                    "description": "Air conditioning system check, repair, and gas recharge",
                    "category": "ac_service",
                    "base_price": 300.00,
                    "estimated_duration": 60,
                    "is_active": True
                },
                {
                    "name": "Tire Rotation & Alignment",
                    "description": "Professional tire rotation and wheel alignment service",
                    "category": "tires",
                    "base_price": 180.00,
                    "estimated_duration": 60,
                    "is_active": True
                },
                {
                    "name": "Engine Diagnostic",
                    "description": "Comprehensive engine diagnostic with computer scan",
                    "category": "diagnostic",
                    "base_price": 250.00,
                    "estimated_duration": 45,
                    "is_active": True
                },
                {
                    "name": "Transmission Service",
                    "description": "Transmission fluid change and system check",
                    "category": "transmission",
                    "base_price": 320.00,
                    "estimated_duration": 90,
                    "is_active": True
                },
            ]

            for service_data in services:
                service = MaintenanceService(**service_data)
                db.add(service)

            db.commit()
            print(f"✓ Created {len(services)} maintenance services")

        print("\nCreating sample rental vehicles...")

        # Check if vehicles already exist
        existing_vehicles = db.query(RentalVehicle).count()
        if existing_vehicles > 0:
            print(f"✓ {existing_vehicles} rental vehicles already exist")
        else:
            vehicles = [
                {
                    "make": "Toyota",
                    "model": "Camry",
                    "year": 2023,
                    "registration_number": "GR-1234-23",
                    "color": "Silver",
                    "fuel_type": "Petrol",
                    "transmission": "Automatic",
                    "seats": 5,
                    "daily_rate": 250.00,
                    "weekly_rate": 1500.00,
                    "monthly_rate": 5500.00,
                    "features": ["GPS", "Bluetooth", "Backup Camera", "Climate Control"],
                    "images": [],
                    "status": "active",
                    "is_available": True,
                    "current_mileage": 15000,
                    "average_rating": 4.5,
                    "total_ratings": 10,
                    "total_trips": 25
                },
                {
                    "make": "Honda",
                    "model": "Accord",
                    "year": 2023,
                    "registration_number": "GR-5678-23",
                    "color": "Black",
                    "fuel_type": "Hybrid",
                    "transmission": "Automatic",
                    "seats": 5,
                    "daily_rate": 280.00,
                    "weekly_rate": 1650.00,
                    "monthly_rate": 6000.00,
                    "features": ["GPS", "Bluetooth", "Lane Assist", "Adaptive Cruise Control"],
                    "images": [],
                    "status": "active",
                    "is_available": True,
                    "current_mileage": 12000,
                    "average_rating": 4.7,
                    "total_ratings": 15,
                    "total_trips": 30
                },
                {
                    "make": "Mercedes-Benz",
                    "model": "C-Class",
                    "year": 2024,
                    "registration_number": "GR-9012-24",
                    "color": "White",
                    "fuel_type": "Diesel",
                    "transmission": "Automatic",
                    "seats": 5,
                    "daily_rate": 450.00,
                    "weekly_rate": 2800.00,
                    "monthly_rate": 10000.00,
                    "features": ["GPS", "Premium Sound", "Leather Seats", "Sunroof", "Parking Sensors"],
                    "images": [],
                    "status": "active",
                    "is_available": True,
                    "current_mileage": 8000,
                    "average_rating": 4.9,
                    "total_ratings": 20,
                    "total_trips": 18
                },
                {
                    "make": "Toyota",
                    "model": "RAV4",
                    "year": 2023,
                    "registration_number": "GR-3456-23",
                    "color": "Blue",
                    "fuel_type": "Petrol",
                    "transmission": "Automatic",
                    "seats": 7,
                    "daily_rate": 320.00,
                    "weekly_rate": 1900.00,
                    "monthly_rate": 7000.00,
                    "features": ["GPS", "Bluetooth", "AWD", "Third Row Seating"],
                    "images": [],
                    "status": "active",
                    "is_available": True,
                    "current_mileage": 18000,
                    "average_rating": 4.6,
                    "total_ratings": 12,
                    "total_trips": 22
                },
                {
                    "make": "Nissan",
                    "model": "Altima",
                    "year": 2023,
                    "registration_number": "GR-7890-23",
                    "color": "Red",
                    "fuel_type": "Petrol",
                    "transmission": "Automatic",
                    "seats": 5,
                    "daily_rate": 230.00,
                    "weekly_rate": 1400.00,
                    "monthly_rate": 5000.00,
                    "features": ["GPS", "Bluetooth", "USB Ports"],
                    "images": [],
                    "status": "active",
                    "is_available": True,
                    "current_mileage": 20000,
                    "average_rating": 4.3,
                    "total_ratings": 8,
                    "total_trips": 20
                },
                {
                    "make": "BMW",
                    "model": "X5",
                    "year": 2024,
                    "registration_number": "GR-2345-24",
                    "color": "Gray",
                    "fuel_type": "Hybrid",
                    "transmission": "Automatic",
                    "seats": 7,
                    "daily_rate": 550.00,
                    "weekly_rate": 3300.00,
                    "monthly_rate": 12000.00,
                    "features": ["GPS", "Premium Sound", "Leather Seats", "Panoramic Roof", "360 Camera"],
                    "images": [],
                    "status": "active",
                    "is_available": True,
                    "current_mileage": 5000,
                    "average_rating": 5.0,
                    "total_ratings": 25,
                    "total_trips": 15
                },
            ]

            for vehicle_data in vehicles:
                vehicle = RentalVehicle(**vehicle_data)
                db.add(vehicle)

            db.commit()
            print(f"✓ Created {len(vehicles)} rental vehicles")

        print("\n" + "="*50)
        print("Sample data creation completed successfully!")
        print("="*50)

        # Print summary
        total_services = db.query(MaintenanceService).count()
        total_vehicles = db.query(RentalVehicle).count()

        print(f"\nDatabase Summary:")
        print(f"  - Maintenance Services: {total_services}")
        print(f"  - Rental Vehicles: {total_vehicles}")

    except Exception as e:
        print(f"❌ Error creating sample data: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    print("ZIP Platform - Sample Data Creator")
    print("="*50)
    create_sample_data()
