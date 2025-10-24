import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { FiSearch } from 'react-icons/fi';
import { maintenanceService } from '../../services/maintenanceService';
import ServiceCard from '../../components/maintenance/ServiceCard';
import Input from '../../components/ui/Input';
import Loading from '../../components/ui/Loading';
import Button from '../../components/ui/Button';
import Modal from '../../components/ui/Modal';
import toast from 'react-hot-toast';
import { useAuth } from '../../hooks/useAuth';

const Services = () => {
  const navigate = useNavigate();
  const { isAuthenticated } = useAuth();
  const [services, setServices] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedService, setSelectedService] = useState(null);
  const [showBookingModal, setShowBookingModal] = useState(false);
  const [bookingData, setBookingData] = useState({
    scheduled_date: '',
    scheduled_time: '',
    location: '',
    vehicle_info: {
      make: '',
      model: '',
      year: '',
      registration: ''
    },
    notes: ''
  });

  useEffect(() => {
    fetchServices();
  }, []);

  const fetchServices = async () => {
    try {
      setLoading(true);
      const data = await maintenanceService.getServices();
      setServices(data);
    } catch (error) {
      toast.error('Failed to load services');
    } finally {
      setLoading(false);
    }
  };

  const handleBookService = (service) => {
    if (!isAuthenticated) {
      toast.error('Please login to book a service');
      navigate('/login');
      return;
    }
    setSelectedService(service);
    setShowBookingModal(true);
  };

  const handleBookingSubmit = async (e) => {
    e.preventDefault();

    try {
      const bookingPayload = {
        service_id: selectedService.id,
        scheduled_date: bookingData.scheduled_date,
        scheduled_time: bookingData.scheduled_time,
        location: bookingData.location,
        vehicle_info: bookingData.vehicle_info,
        notes: bookingData.notes
      };

      await maintenanceService.createBooking(bookingPayload);
      toast.success('Service booked successfully!');
      setShowBookingModal(false);
      navigate('/dashboard/bookings');
    } catch (error) {
      toast.error('Failed to book service');
    }
  };

  const filteredServices = services.filter(service =>
    service.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    service.description.toLowerCase().includes(searchTerm.toLowerCase())
  );

  if (loading) {
    return <Loading fullScreen />;
  }

  return (
    <div className="min-h-screen bg-midnight-950 pt-20 pb-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8 sm:mb-12">
          <h1 className="text-3xl sm:text-4xl md:text-5xl font-bold text-white mb-3 sm:mb-4 animate-fade-in-up">
            Mobile Car Maintenance Services
          </h1>
          <p className="text-lg sm:text-xl text-gray-400 mb-6 sm:mb-8 px-4 animate-fade-in-up" style={{ animationDelay: '0.1s' }}>
            Professional car maintenance at your doorstep
          </p>

          {/* Search */}
          <div className="max-w-md mx-auto px-4 sm:px-0 animate-fade-in-up" style={{ animationDelay: '0.2s' }}>
            <Input
              placeholder="Search services..."
              icon={FiSearch}
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>
        </div>

        {/* Services Grid */}
        {filteredServices.length > 0 ? (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6">
            {filteredServices.map((service) => (
              <ServiceCard
                key={service.id}
                service={service}
                onBook={handleBookService}
              />
            ))}
          </div>
        ) : (
          <div className="text-center py-12">
            <p className="text-gray-400 text-base sm:text-lg">No services found</p>
          </div>
        )}

        {/* Booking Modal */}
        <Modal
          isOpen={showBookingModal}
          onClose={() => setShowBookingModal(false)}
          title={`Book ${selectedService?.name}`}
          size="lg"
        >
          <form onSubmit={handleBookingSubmit} className="space-y-4">
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <Input
                label="Date"
                type="date"
                required
                value={bookingData.scheduled_date}
                onChange={(e) => setBookingData({ ...bookingData, scheduled_date: e.target.value })}
                min={new Date().toISOString().split('T')[0]}
              />
              <Input
                label="Time"
                type="time"
                required
                value={bookingData.scheduled_time}
                onChange={(e) => setBookingData({ ...bookingData, scheduled_time: e.target.value })}
              />
            </div>

            <Input
              label="Location"
              placeholder="Enter service location"
              required
              value={bookingData.location}
              onChange={(e) => setBookingData({ ...bookingData, location: e.target.value })}
            />

            <div className="border-t border-dark-700 pt-4">
              <h4 className="text-white font-medium mb-3">Vehicle Information</h4>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <Input
                  label="Make"
                  placeholder="Toyota"
                  required
                  value={bookingData.vehicle_info.make}
                  onChange={(e) => setBookingData({
                    ...bookingData,
                    vehicle_info: { ...bookingData.vehicle_info, make: e.target.value }
                  })}
                />
                <Input
                  label="Model"
                  placeholder="Camry"
                  required
                  value={bookingData.vehicle_info.model}
                  onChange={(e) => setBookingData({
                    ...bookingData,
                    vehicle_info: { ...bookingData.vehicle_info, model: e.target.value }
                  })}
                />
                <Input
                  label="Year"
                  type="number"
                  placeholder="2020"
                  required
                  value={bookingData.vehicle_info.year}
                  onChange={(e) => setBookingData({
                    ...bookingData,
                    vehicle_info: { ...bookingData.vehicle_info, year: e.target.value }
                  })}
                />
                <Input
                  label="Registration"
                  placeholder="GR-1234-20"
                  required
                  value={bookingData.vehicle_info.registration}
                  onChange={(e) => setBookingData({
                    ...bookingData,
                    vehicle_info: { ...bookingData.vehicle_info, registration: e.target.value }
                  })}
                />
              </div>
            </div>

            <Input
              label="Additional Notes (Optional)"
              placeholder="Any specific requirements..."
              value={bookingData.notes}
              onChange={(e) => setBookingData({ ...bookingData, notes: e.target.value })}
            />

            <div className="flex flex-col sm:flex-row gap-3 pt-4">
              <Button
                type="button"
                variant="ghost"
                onClick={() => setShowBookingModal(false)}
                className="flex-1 w-full"
              >
                Cancel
              </Button>
              <Button
                type="submit"
                variant="primary"
                className="flex-1 w-full"
              >
                Confirm Booking
              </Button>
            </div>
          </form>
        </Modal>
      </div>
    </div>
  );
};

export default Services;
