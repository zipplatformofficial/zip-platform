import api from './api';

export const rentalService = {
  async getVehicles(params = {}) {
    const response = await api.get('/rentals/vehicles', { params });
    return response.data;
  },

  async getVehicle(id) {
    const response = await api.get(`/rentals/vehicles/${id}`);
    return response.data;
  },

  async checkAvailability(vehicleId, startDate, endDate) {
    const response = await api.post('/rentals/check-availability', {
      vehicle_id: vehicleId,
      start_date: startDate,
      end_date: endDate,
    });
    return response.data;
  },

  async createBooking(bookingData) {
    const response = await api.post('/rentals/bookings', bookingData);
    return response.data;
  },

  async getMyRentals() {
    const response = await api.get('/rentals/bookings');
    return response.data;
  },

  async getRental(id) {
    const response = await api.get(`/rentals/bookings/${id}`);
    return response.data;
  },

  async cancelRental(id) {
    const response = await api.put(`/rentals/bookings/${id}/cancel`);
    return response.data;
  },

  async returnVehicle(id, returnData) {
    const response = await api.post(`/rentals/bookings/${id}/return`, returnData);
    return response.data;
  },
};

export default rentalService;
