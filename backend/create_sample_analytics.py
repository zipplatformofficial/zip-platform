"""
Create sample analytics and fraud data for testing dashboard
"""
import sys
import os
from datetime import datetime, timedelta
import random

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import SessionLocal
from app.models.analytics import AnalyticsEvent, DailyStats, EventType, VisitorType
from app.models.fraud import FraudAlert, FraudType, FraudStatus
from app.models.user import User


def create_analytics_events(db):
    """Create sample analytics events"""
    print("Creating analytics events...")

    users = db.query(User).all()
    event_types = list(EventType)
    visitor_types = list(VisitorType)

    # Create events for last 7 days
    for days_ago in range(7):
        date = datetime.now() - timedelta(days=days_ago)

        # Create 50-100 events per day
        for _ in range(random.randint(50, 100)):
            event = AnalyticsEvent(
                user_id=random.choice(users).id if users and random.random() > 0.3 else None,
                session_id=f"session_{random.randint(1000, 9999)}_{days_ago}",
                visitor_type=random.choice(visitor_types),
                event_type=random.choice(event_types),
                event_name=f"Event {random.randint(1, 100)}",
                event_category=random.choice(['maintenance', 'rentals', 'store', 'auth', 'profile']),
                page_url=f"/page/{random.randint(1, 20)}",
                page_title=f"Page {random.randint(1, 20)}",
                device_type=random.choice(['desktop', 'mobile', 'tablet']),
                browser=random.choice(['Chrome', 'Firefox', 'Safari', 'Edge']),
                operating_system=random.choice(['Windows', 'MacOS', 'Linux', 'iOS', 'Android']),
                ip_address=f"192.168.{random.randint(1, 255)}.{random.randint(1, 255)}",
                country="Ghana",
                city=random.choice(['Accra', 'Kumasi', 'Takoradi', 'Tamale']),
                time_on_page=random.randint(10, 600),
                scroll_depth=random.uniform(20, 100),
                is_conversion=random.random() > 0.9,
                conversion_value=random.uniform(50, 500) if random.random() > 0.9 else None,
                created_at=date.isoformat()
            )
            db.add(event)

    db.commit()
    print("[+] Analytics events created")


def create_daily_stats(db):
    """Create sample daily statistics"""
    print("Creating daily statistics...")

    # Create stats for last 7 days
    for days_ago in range(7):
        date = (datetime.now() - timedelta(days=days_ago)).date()

        stat = DailyStats(
            date=str(date),
            total_visitors=random.randint(200, 500),
            new_visitors=random.randint(50, 150),
            returning_visitors=random.randint(100, 300),
            unique_sessions=random.randint(150, 400),
            new_signups=random.randint(5, 25),
            active_users=random.randint(50, 150),
            total_revenue=random.uniform(5000, 15000),
            maintenance_revenue=random.uniform(1000, 4000),
            rental_revenue=random.uniform(2000, 6000),
            store_revenue=random.uniform(1500, 5000),
            platform_commission=random.uniform(500, 1500),
            service_bookings=random.randint(10, 30),
            rental_bookings=random.randint(5, 20),
            store_orders=random.randint(15, 40),
            successful_payments=random.randint(40, 80),
            failed_payments=random.randint(2, 10),
            total_payment_amount=random.uniform(6000, 18000),
            avg_session_duration=random.randint(180, 600),
            pages_per_session=random.uniform(3.0, 8.0),
            bounce_rate=random.uniform(30.0, 60.0),
            conversion_rate=random.uniform(2.0, 8.0),
            total_conversions=random.randint(15, 45),
            new_applications=random.randint(2, 10),
            approved_applications=random.randint(1, 5),
            rejected_applications=random.randint(0, 3),
            fraud_alerts=random.randint(0, 5),
            fraud_blocked_amount=random.uniform(0, 2000),
            top_products=[
                {"id": 1, "name": "Brake Pads", "sales": random.randint(10, 30)},
                {"id": 2, "name": "Engine Oil", "sales": random.randint(15, 35)},
                {"id": 3, "name": "Air Filter", "sales": random.randint(8, 25)}
            ],
            top_services=[
                {"id": 1, "name": "Oil Change", "bookings": random.randint(15, 40)},
                {"id": 2, "name": "Brake Service", "bookings": random.randint(10, 30)},
                {"id": 3, "name": "Tire Rotation", "bookings": random.randint(8, 25)}
            ],
            top_vehicles=[
                {"id": 1, "name": "Toyota Camry 2022", "rentals": random.randint(5, 15)},
                {"id": 2, "name": "Honda Civic 2023", "rentals": random.randint(4, 12)},
                {"id": 3, "name": "Hyundai Elantra 2022", "rentals": random.randint(3, 10)}
            ]
        )
        db.add(stat)

    db.commit()
    print("[+] Daily statistics created")


def create_fraud_alerts(db):
    """Create sample fraud alerts"""
    print("Creating fraud alerts...")

    users = db.query(User).all()
    fraud_types = list(FraudType)
    fraud_statuses = list(FraudStatus)
    severities = ['low', 'medium', 'high', 'critical']

    # Create 10-20 fraud alerts
    for i in range(random.randint(10, 20)):
        days_ago = random.randint(0, 30)
        date = datetime.now() - timedelta(days=days_ago)

        fraud_type = random.choice(fraud_types)
        status = random.choice(fraud_statuses)

        alert = FraudAlert(
            user_id=random.choice(users).id if users and random.random() > 0.2 else None,
            fraud_type=fraud_type,
            status=status,
            severity=random.choice(severities),
            detection_method=random.choice(['ML Model', 'Rule-based', 'Manual Report', 'Pattern Analysis']),
            confidence_score=random.uniform(0.6, 0.99),
            description=f"Suspicious {fraud_type.value.replace('_', ' ')} detected",
            evidence={
                "ip_address": f"192.168.{random.randint(1, 255)}.{random.randint(1, 255)}",
                "attempts": random.randint(3, 15),
                "time_span": f"{random.randint(5, 60)} minutes"
            },
            ip_address=f"192.168.{random.randint(1, 255)}.{random.randint(1, 255)}",
            device_fingerprint=f"device_{random.randint(10000, 99999)}",
            user_agent=f"Mozilla/5.0 ({random.choice(['Windows', 'Mac', 'Linux'])})",
            location={
                "country": "Ghana",
                "city": random.choice(['Accra', 'Kumasi', 'Takoradi', 'Tamale'])
            },
            amount_involved=random.uniform(100, 5000) if random.random() > 0.3 else None,
            currency="GHS",
            actions_taken=["account_flagged", "payment_blocked"] if status == FraudStatus.CONFIRMED else [],
            auto_blocked=random.random() > 0.5,
            created_at=date.isoformat(),
            reviewed_at=date.isoformat() if status in [FraudStatus.CONFIRMED, FraudStatus.FALSE_POSITIVE, FraudStatus.RESOLVED] else None,
            resolved_at=date.isoformat() if status == FraudStatus.RESOLVED else None
        )
        db.add(alert)

    db.commit()
    print("[+] Fraud alerts created")


def main():
    """Main function"""
    db = SessionLocal()

    try:
        print("\n[*] Creating sample analytics and fraud data...\n")

        # Check if data already exists
        existing_events = db.query(AnalyticsEvent).count()
        existing_stats = db.query(DailyStats).count()
        existing_fraud = db.query(FraudAlert).count()

        if existing_events > 0 or existing_stats > 0 or existing_fraud > 0:
            print(f"[!] Found existing data:")
            print(f"   - Analytics events: {existing_events}")
            print(f"   - Daily stats: {existing_stats}")
            print(f"   - Fraud alerts: {existing_fraud}")

            response = input("\nDelete existing data and recreate? (yes/no): ")
            if response.lower() == 'yes':
                print("\nDeleting existing data...")
                db.query(AnalyticsEvent).delete()
                db.query(DailyStats).delete()
                db.query(FraudAlert).delete()
                db.commit()
                print("[+] Existing data deleted")
            else:
                print("Keeping existing data and adding more...")

        # Create sample data
        create_analytics_events(db)
        create_daily_stats(db)
        create_fraud_alerts(db)

        print("\n[+] Sample data created successfully!")
        print("\nYou can now:")
        print("1. Login as admin: admin@zip.com / Admin@123")
        print("2. Visit: http://localhost:5173/admin")
        print("3. View comprehensive dashboard with all analytics\n")

    except Exception as e:
        print(f"\n[-] Error: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
