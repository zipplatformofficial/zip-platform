"""Real-time tracking endpoints"""
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Dict
import json
import asyncio

from app.core.database import get_db
from app.api.v1.deps import get_current_user
from app.models.user import User, UserRole
from app.models.maintenance import ServiceBooking, Technician
from app.models.rental import RentalBooking
from app.services.tracking_service import tracking_service
from pydantic import BaseModel

router = APIRouter()


class LocationUpdate(BaseModel):
    """Location update request"""
    latitude: float
    longitude: float
    heading: float = None
    speed: float = None


class ConnectionManager:
    """Manages WebSocket connections for tracking"""

    def __init__(self):
        self.active_connections: Dict[int, list] = {}

    async def connect(self, booking_id: int, websocket: WebSocket):
        """Connect a client to a booking's tracking session"""
        await websocket.accept()

        if booking_id not in self.active_connections:
            self.active_connections[booking_id] = []

        self.active_connections[booking_id].append(websocket)

    def disconnect(self, booking_id: int, websocket: WebSocket):
        """Disconnect a client"""
        if booking_id in self.active_connections:
            if websocket in self.active_connections[booking_id]:
                self.active_connections[booking_id].remove(websocket)

            if not self.active_connections[booking_id]:
                del self.active_connections[booking_id]

    async def broadcast_to_booking(self, booking_id: int, message: dict):
        """Broadcast message to all clients tracking a booking"""
        if booking_id in self.active_connections:
            for connection in self.active_connections[booking_id]:
                try:
                    await connection.send_json(message)
                except:
                    pass  # Client disconnected


manager = ConnectionManager()


@router.websocket("/ws/{booking_id}")
async def tracking_websocket(
    websocket: WebSocket,
    booking_id: int,
    db: Session = Depends(get_db)
):
    """
    WebSocket endpoint for real-time tracking

    - Customers connect to track their booking
    - Receives real-time location updates from technician/vehicle
    - Sends ETA updates

    Connect with: ws://localhost:8000/api/v1/tracking/ws/{booking_id}
    """
    await manager.connect(booking_id, websocket)

    try:
        # Send initial status
        current_location = tracking_service.get_current_location(booking_id)

        await websocket.send_json({
            "type": "connected",
            "booking_id": booking_id,
            "message": "Tracking session started",
            "current_location": current_location
        })

        # Keep connection alive and send updates
        while True:
            try:
                # Wait for messages (ping/pong or client requests)
                data = await websocket.receive_text()

                # Handle client requests
                if data == "get_location":
                    location = tracking_service.get_current_location(booking_id)
                    await websocket.send_json({
                        "type": "location_update",
                        "location": location
                    })

            except WebSocketDisconnect:
                break

    finally:
        manager.disconnect(booking_id, websocket)


@router.post("/technicians/location")
async def update_technician_location(
    booking_id: int,
    location: LocationUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update technician's current location

    - Called by technician app every few seconds
    - Updates real-time tracking
    - Calculates and broadcasts ETA
    """
    if current_user.role != UserRole.TECHNICIAN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only technicians can update location"
        )

    # Verify booking belongs to this technician
    technician = db.query(Technician).filter(
        Technician.user_id == current_user.id
    ).first()

    if not technician:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Technician profile not found"
        )

    booking = db.query(ServiceBooking).filter(
        ServiceBooking.id == booking_id,
        ServiceBooking.technician_id == technician.id
    ).first()

    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found or not assigned to you"
        )

    # Update location in tracking service
    location_data = tracking_service.update_location(
        booking_id=booking_id,
        latitude=location.latitude,
        longitude=location.longitude,
        tracker_type="technician",
        heading=location.heading,
        speed=location.speed
    )

    # Calculate ETA if service location is available
    if booking.service_latitude and booking.service_longitude:
        eta_info = tracking_service.calculate_eta(
            current_lat=location.latitude,
            current_lng=location.longitude,
            destination_lat=booking.service_latitude,
            destination_lng=booking.service_longitude,
            average_speed_kmh=location.speed if location.speed else 40.0
        )

        tracking_service.update_eta(booking_id, eta_info["eta_minutes"])

        # Broadcast to all connected clients
        await manager.broadcast_to_booking(booking_id, {
            "type": "location_update",
            "location": location_data,
            "eta": eta_info
        })

    return {
        "message": "Location updated successfully",
        "location": location_data
    }


@router.post("/vehicles/location")
async def update_vehicle_location(
    booking_id: int,
    location: LocationUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update rental vehicle's current location

    - Called by vehicle's GPS tracker
    - Updates real-time tracking for rentals
    - Admin or system service can update
    """
    # For vehicles, typically updated by GPS device or admin
    if current_user.role not in [UserRole.ADMIN, UserRole.VENDOR]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update vehicle location"
        )

    # Verify rental booking exists
    rental = db.query(RentalBooking).filter(
        RentalBooking.id == booking_id
    ).first()

    if not rental:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rental booking not found"
        )

    # Update location
    location_data = tracking_service.update_location(
        booking_id=booking_id,
        latitude=location.latitude,
        longitude=location.longitude,
        tracker_type="vehicle",
        heading=location.heading,
        speed=location.speed
    )

    # Broadcast to connected clients
    await manager.broadcast_to_booking(booking_id, {
        "type": "location_update",
        "location": location_data
    })

    return {
        "message": "Vehicle location updated successfully",
        "location": location_data
    }


@router.get("/{booking_id}")
async def get_tracking_info(
    booking_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get current tracking information

    - Returns current location and ETA
    - Non-WebSocket alternative for simple polling
    """
    # Verify user has access to this booking
    booking = db.query(ServiceBooking).filter(
        ServiceBooking.id == booking_id,
        ServiceBooking.customer_id == current_user.id
    ).first()

    rental = None
    if not booking:
        rental = db.query(RentalBooking).filter(
            RentalBooking.id == booking_id,
            RentalBooking.customer_id == current_user.id
        ).first()

    if not booking and not rental:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found or not authorized"
        )

    tracker_type = "technician" if booking else "vehicle"

    # Get current location
    current_location = tracking_service.get_current_location(booking_id, tracker_type)

    # Get tracking session info
    session_key = f"{tracker_type}_{booking_id}"
    session_info = tracking_service.active_sessions.get(session_key, {})

    return {
        "booking_id": booking_id,
        "tracker_type": tracker_type,
        "is_active": tracking_service.is_tracking_active(booking_id, tracker_type),
        "current_location": current_location,
        "eta_minutes": session_info.get("eta_minutes"),
        "started_at": session_info.get("started_at")
    }


@router.get("/{booking_id}/history")
async def get_location_history(
    booking_id: int,
    limit: int = 50,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get location history for a booking

    - Returns trail of locations
    - Useful for displaying route on map
    """
    # Verify access
    booking = db.query(ServiceBooking).filter(
        ServiceBooking.id == booking_id
    ).first()

    rental = None
    if not booking:
        rental = db.query(RentalBooking).filter(
            RentalBooking.id == booking_id
        ).first()

    if not booking and not rental:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )

    tracker_type = "technician" if booking else "vehicle"

    history = tracking_service.get_location_history(booking_id, tracker_type, limit)

    return {
        "booking_id": booking_id,
        "tracker_type": tracker_type,
        "history": history,
        "count": len(history)
    }


@router.post("/{booking_id}/start")
async def start_tracking(
    booking_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Start tracking session manually

    - Usually auto-started when first location update received
    - Can be called explicitly
    """
    if current_user.role not in [UserRole.TECHNICIAN, UserRole.ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized"
        )

    # Verify booking
    booking = db.query(ServiceBooking).filter(
        ServiceBooking.id == booking_id
    ).first()

    rental = None
    if not booking:
        rental = db.query(RentalBooking).filter(
            RentalBooking.id == booking_id
        ).first()

    if not booking and not rental:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )

    tracker_type = "technician" if booking else "vehicle"

    result = tracking_service.start_tracking(booking_id, tracker_type)

    return result


@router.post("/{booking_id}/stop")
async def stop_tracking(
    booking_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Stop tracking session"""
    if current_user.role not in [UserRole.TECHNICIAN, UserRole.ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized"
        )

    booking = db.query(ServiceBooking).filter(
        ServiceBooking.id == booking_id
    ).first()

    rental = None
    if not booking:
        rental = db.query(RentalBooking).filter(
            RentalBooking.id == booking_id
        ).first()

    if not booking and not rental:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )

    tracker_type = "technician" if booking else "vehicle"

    tracking_service.stop_tracking(booking_id, tracker_type)

    return {"message": "Tracking stopped"}
