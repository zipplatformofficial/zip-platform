import React, { useState, useEffect } from 'react';
import { maintenanceService } from '../../services/maintenanceService';
import Card, { CardContent, CardTitle } from '../../components/ui/Card';
import Badge from '../../components/ui/Badge';
import Button from '../../components/ui/Button';
import Loading from '../../components/ui/Loading';
import { formatDate, formatCurrency } from '../../utils/formatters';
import toast from 'react-hot-toast';

const MyBookings = () => {
  const [bookings, setBookings] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchBookings();
  }, []);

  const fetchBookings = async () => {
    try {
      setLoading(true);
      const data = await maintenanceService.getMyBookings();
      setBookings(data);
    } catch (error) {
      toast.error('Failed to load bookings');
    } finally {
      setLoading(false);
    }
  };

  const handleCancelBooking = async (id) => {
    if (!window.confirm('Are you sure you want to cancel this booking?')) return;

    try {
      await maintenanceService.cancelBooking(id);
      toast.success('Booking cancelled successfully');
      fetchBookings();
    } catch (error) {
      toast.error('Failed to cancel booking');
    }
  };

  const getStatusColor = (status) => {
    const colors = {
      pending: 'warning',
      confirmed: 'info',
      in_progress: 'primary',
      completed: 'success',
      cancelled: 'danger',
    };
    return colors[status] || 'default';
  };

  if (loading) {
    return <Loading fullScreen />;
  }

  return (
    <div className="min-h-screen bg-midnight-950 pt-20 pb-12 px-4">
      <div className="max-w-5xl mx-auto">
        <h1 className="text-3xl font-bold text-white mb-8">My Service Bookings</h1>

        {bookings.length > 0 ? (
          <div className="space-y-4">
            {bookings.map((booking) => (
              <Card key={booking.id}>
                <CardContent>
                  <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
                    <div className="flex-1">
                      <div className="flex items-center gap-3 mb-2">
                        <CardTitle className="text-lg">{booking.service?.name}</CardTitle>
                        <Badge variant={getStatusColor(booking.status)}>
                          {booking.status}
                        </Badge>
                      </div>
                      <div className="text-sm text-gray-400 space-y-1">
                        <p>Date: {formatDate(booking.scheduled_date)}</p>
                        <p>Time: {booking.scheduled_time}</p>
                        <p>Location: {booking.location}</p>
                        <p>Vehicle: {booking.vehicle_info?.make} {booking.vehicle_info?.model}</p>
                        {booking.total_cost && (
                          <p className="text-red-500 font-medium">
                            Total: {formatCurrency(booking.total_cost)}
                          </p>
                        )}
                      </div>
                    </div>

                    <div className="flex gap-2">
                      {booking.status === 'pending' && (
                        <Button
                          variant="danger"
                          size="sm"
                          onClick={() => handleCancelBooking(booking.id)}
                        >
                          Cancel
                        </Button>
                      )}
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        ) : (
          <Card>
            <div className="text-center py-12">
              <p className="text-gray-400 text-lg mb-4">No bookings yet</p>
              <Button variant="primary" onClick={() => window.location.href = '/maintenance'}>
                Book a Service
              </Button>
            </div>
          </Card>
        )}
      </div>
    </div>
  );
};

export default MyBookings;
