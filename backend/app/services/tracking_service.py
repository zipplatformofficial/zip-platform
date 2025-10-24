"""Real-time tracking service for technicians and vehicles"""
from typing import Dict, Optional
from datetime import datetime
import json


class TrackingService:
    """Service for managing real-time location tracking"""

    def __init__(self):
        # In-memory storage for active tracking sessions
        # In production, use Redis for distributed systems
        self.active_sessions: Dict[str, Dict] = {}
        self.location_history: Dict[str, list] = {}

    def start_tracking(self, booking_id: int, tracker_type: str = "technician") -> Dict:
        """
        Start tracking session for a booking

        Args:
            booking_id: Booking ID
            tracker_type: 'technician' or 'vehicle'

        Returns:
            Session info
        """
        session_key = f"{tracker_type}_{booking_id}"

        self.active_sessions[session_key] = {
            "booking_id": booking_id,
            "tracker_type": tracker_type,
            "started_at": datetime.utcnow().isoformat(),
            "current_location": None,
            "eta_minutes": None
        }

        self.location_history[session_key] = []

        return {
            "session_key": session_key,
            "status": "tracking_started"
        }

    def update_location(
        self,
        booking_id: int,
        latitude: float,
        longitude: float,
        tracker_type: str = "technician",
        heading: Optional[float] = None,
        speed: Optional[float] = None
    ) -> Dict:
        """
        Update current location

        Args:
            booking_id: Booking ID
            latitude: Current latitude
            longitude: Current longitude
            tracker_type: 'technician' or 'vehicle'
            heading: Direction in degrees (0-360)
            speed: Speed in km/h

        Returns:
            Updated location info
        """
        session_key = f"{tracker_type}_{booking_id}"

        if session_key not in self.active_sessions:
            # Auto-start tracking if not exists
            self.start_tracking(booking_id, tracker_type)

        location_data = {
            "latitude": latitude,
            "longitude": longitude,
            "timestamp": datetime.utcnow().isoformat(),
            "heading": heading,
            "speed": speed
        }

        # Update current location
        self.active_sessions[session_key]["current_location"] = location_data

        # Add to history
        if session_key not in self.location_history:
            self.location_history[session_key] = []

        self.location_history[session_key].append(location_data)

        # Keep only last 100 locations
        if len(self.location_history[session_key]) > 100:
            self.location_history[session_key] = self.location_history[session_key][-100:]

        return location_data

    def get_current_location(self, booking_id: int, tracker_type: str = "technician") -> Optional[Dict]:
        """Get current location for a booking"""
        session_key = f"{tracker_type}_{booking_id}"

        if session_key in self.active_sessions:
            return self.active_sessions[session_key].get("current_location")

        return None

    def get_location_history(
        self,
        booking_id: int,
        tracker_type: str = "technician",
        limit: int = 50
    ) -> list:
        """Get location history for a booking"""
        session_key = f"{tracker_type}_{booking_id}"

        if session_key in self.location_history:
            return self.location_history[session_key][-limit:]

        return []

    def calculate_eta(
        self,
        current_lat: float,
        current_lng: float,
        destination_lat: float,
        destination_lng: float,
        average_speed_kmh: float = 40.0
    ) -> Dict:
        """
        Calculate ETA (simple haversine distance calculation)

        For production, integrate with Google Maps Distance Matrix API
        """
        from math import radians, sin, cos, sqrt, atan2

        # Haversine formula
        R = 6371  # Earth radius in km

        lat1, lon1 = radians(current_lat), radians(current_lng)
        lat2, lon2 = radians(destination_lat), radians(destination_lng)

        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))

        distance_km = R * c

        # Calculate ETA
        if average_speed_kmh > 0:
            eta_hours = distance_km / average_speed_kmh
            eta_minutes = int(eta_hours * 60)
        else:
            eta_minutes = None

        return {
            "distance_km": round(distance_km, 2),
            "eta_minutes": eta_minutes,
            "calculated_at": datetime.utcnow().isoformat()
        }

    def update_eta(self, booking_id: int, eta_minutes: int, tracker_type: str = "technician"):
        """Update ETA for a booking"""
        session_key = f"{tracker_type}_{booking_id}"

        if session_key in self.active_sessions:
            self.active_sessions[session_key]["eta_minutes"] = eta_minutes
            self.active_sessions[session_key]["eta_updated_at"] = datetime.utcnow().isoformat()

    def stop_tracking(self, booking_id: int, tracker_type: str = "technician"):
        """Stop tracking session"""
        session_key = f"{tracker_type}_{booking_id}"

        if session_key in self.active_sessions:
            del self.active_sessions[session_key]

        # Keep history for analytics (could move to database)

    def get_active_sessions(self) -> Dict:
        """Get all active tracking sessions (for monitoring)"""
        return self.active_sessions

    def is_tracking_active(self, booking_id: int, tracker_type: str = "technician") -> bool:
        """Check if tracking is active for a booking"""
        session_key = f"{tracker_type}_{booking_id}"
        return session_key in self.active_sessions


# Singleton instance
tracking_service = TrackingService()
