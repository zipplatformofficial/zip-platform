import api from './api';

export const adminService = {
  // User Management
  async getAllUsers(params = {}) {
    const response = await api.get('/admin/users', { params });
    return response.data;
  },

  async getUserById(userId) {
    const response = await api.get(`/admin/users/${userId}`);
    return response.data;
  },

  async activateUser(userId) {
    const response = await api.post(`/admin/users/${userId}/activate`);
    return response.data;
  },

  async deactivateUser(userId) {
    const response = await api.post(`/admin/users/${userId}/deactivate`);
    return response.data;
  },

  // Bookings Management
  async getAllServiceBookings(params = {}) {
    const response = await api.get('/admin/maintenance/bookings', { params });
    return response.data;
  },

  async getAllRentalBookings(params = {}) {
    const response = await api.get('/admin/rentals/bookings', { params });
    return response.data;
  },

  async getAllOrders(params = {}) {
    const response = await api.get('/admin/store/orders', { params });
    return response.data;
  },

  // Technicians Management
  async getAllTechnicians(params = {}) {
    const response = await api.get('/admin/technicians', { params });
    return response.data;
  },

  async verifyTechnician(technicianId) {
    const response = await api.post(`/admin/technicians/${technicianId}/verify`);
    return response.data;
  },

  // Vendors Management
  async verifyVendor(vendorId) {
    const response = await api.post(`/admin/vendors/${vendorId}/verify`);
    return response.data;
  },

  async deactivateVendor(vendorId) {
    const response = await api.post(`/admin/vendors/${vendorId}/deactivate`);
    return response.data;
  },

  // Applications Management
  async getAllApplications(params = {}) {
    const response = await api.get('/applications/admin/applications', { params });
    return response.data;
  },

  async getApplicationById(applicationId) {
    const response = await api.get(`/applications/admin/applications/${applicationId}`);
    return response.data;
  },

  async reviewApplication(applicationId, reviewData) {
    const response = await api.put(`/applications/admin/applications/${applicationId}/review`, reviewData);
    return response.data;
  },

  async approveApplication(applicationId, approvalData) {
    const response = await api.post(`/applications/admin/applications/${applicationId}/approve`, approvalData);
    return response.data;
  },

  async rejectApplication(applicationId, rejectionData) {
    const response = await api.post(`/applications/admin/applications/${applicationId}/reject`, rejectionData);
    return response.data;
  },

  // Analytics & Statistics
  async getStats() {
    const response = await api.get('/admin/stats/overview');
    return response.data;
  },

  async getPlatformStats() {
    const response = await api.get('/admin/stats/overview');
    return response.data;
  },
};

export default adminService;
