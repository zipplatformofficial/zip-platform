import api from './api';

export const maintenanceService = {
  async getServices() {
    const response = await api.get('/maintenance/services');
    return response.data;
  },

  async getService(id) {
    const response = await api.get(`/maintenance/services/${id}`);
    return response.data;
  },

  async createBooking(bookingData) {
    const response = await api.post('/maintenance/bookings', bookingData);
    return response.data;
  },

  async getMyBookings() {
    const response = await api.get('/maintenance/bookings');
    return response.data;
  },

  async getBooking(id) {
    const response = await api.get(`/maintenance/bookings/${id}`);
    return response.data;
  },

  async cancelBooking(id) {
    const response = await api.put(`/maintenance/bookings/${id}/cancel`);
    return response.data;
  },

  async updateBooking(id, data) {
    const response = await api.put(`/maintenance/bookings/${id}`, data);
    return response.data;
  },
};

export default maintenanceService;
