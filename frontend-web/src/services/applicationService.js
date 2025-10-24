/**
 * Application Service - Handles role application API calls
 */
import api from './api';

export const applicationService = {
  /**
   * Get all applications (Admin only)
   */
  async getApplications(params = {}) {
    const queryParams = new URLSearchParams();
    if (params.status) queryParams.append('status_filter', params.status);
    if (params.type) queryParams.append('type_filter', params.type);
    if (params.skip !== undefined) queryParams.append('skip', params.skip);
    if (params.limit !== undefined) queryParams.append('limit', params.limit);

    const url = `/applications/admin/applications${queryParams.toString() ? '?' + queryParams.toString() : ''}`;
    const response = await api.get(url);
    return response.data;
  },

  /**
   * Get specific application details
   */
  async getApplication(applicationId) {
    const response = await api.get(`/applications/admin/applications/${applicationId}`);
    return response.data;
  },

  /**
   * Review application documents
   */
  async reviewApplication(applicationId, reviewData) {
    const response = await api.put(
      `/applications/admin/applications/${applicationId}/review`,
      reviewData
    );
    return response.data;
  },

  /**
   * Approve application
   */
  async approveApplication(applicationId, adminNotes = '') {
    const response = await api.post(
      `/applications/admin/applications/${applicationId}/approve`,
      { admin_notes: adminNotes }
    );
    return response.data;
  },

  /**
   * Reject application
   */
  async rejectApplication(applicationId, rejectionReason, adminNotes = '') {
    const response = await api.post(
      `/applications/admin/applications/${applicationId}/reject`,
      {
        rejection_reason: rejectionReason,
        admin_notes: adminNotes
      }
    );
    return response.data;
  },

  /**
   * Apply as technician (User)
   */
  async applyAsTechnician(applicationData) {
    const response = await api.post('/applications/apply/technician', applicationData);
    return response.data;
  },

  /**
   * Apply as vendor (User)
   */
  async applyAsVendor(applicationData) {
    const response = await api.post('/applications/apply/vendor', applicationData);
    return response.data;
  },

  /**
   * Apply as rental manager (User)
   */
  async applyAsRentalManager(applicationData) {
    const response = await api.post('/applications/apply/rental-manager', applicationData);
    return response.data;
  },

  /**
   * Get my applications (User)
   */
  async getMyApplications() {
    const response = await api.get('/applications/my-applications');
    return response.data;
  }
};
