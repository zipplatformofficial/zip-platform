import React, { useState, useEffect } from 'react';
import { FiTool, FiPlus, FiEdit2, FiTrash2, FiSearch, FiX } from 'react-icons/fi';
import Card, { CardContent } from '../../components/ui/Card';
import Button from '../../components/ui/Button';
import Input from '../../components/ui/Input';
import toast from 'react-hot-toast';
import api from '../../services/api';

const MaintenanceServices = () => {
  const [services, setServices] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [showModal, setShowModal] = useState(false);
  const [editingService, setEditingService] = useState(null);
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    estimated_duration: '',
    base_price: '',
    service_type: 'OIL_CHANGE',
  });

  const serviceTypes = [
    { value: 'OIL_CHANGE', label: 'Oil Change' },
    { value: 'TIRE_SERVICE', label: 'Tire Service' },
    { value: 'BRAKE_SERVICE', label: 'Brake Service' },
    { value: 'ENGINE_DIAGNOSTIC', label: 'Engine Diagnostic' },
    { value: 'AC_SERVICE', label: 'AC Service' },
    { value: 'BATTERY_SERVICE', label: 'Battery Service' },
    { value: 'TRANSMISSION', label: 'Transmission' },
    { value: 'ELECTRICAL', label: 'Electrical' },
    { value: 'SUSPENSION', label: 'Suspension' },
    { value: 'DETAILING', label: 'Detailing' },
    { value: 'INSPECTION', label: 'Inspection' },
    { value: 'OTHER', label: 'Other' },
  ];

  useEffect(() => {
    fetchServices();
  }, []);

  const fetchServices = async () => {
    try {
      setLoading(true);
      const response = await api.get('/maintenance/services');
      setServices(Array.isArray(response.data) ? response.data : []);
    } catch (error) {
      toast.error('Failed to load services');
      console.error('Error fetching services:', error);
      setServices([]); // Set empty array on error
    } finally{
      setLoading(false);
    }
  };

  const handleOpenModal = (service = null) => {
    if (service) {
      setEditingService(service);
      setFormData({
        name: service.name,
        description: service.description || '',
        estimated_duration: service.estimated_duration || '',
        base_price: service.base_price,
        service_type: service.service_type,
      });
    } else {
      setEditingService(null);
      setFormData({
        name: '',
        description: '',
        estimated_duration: '',
        base_price: '',
        service_type: 'OIL_CHANGE',
      });
    }
    setShowModal(true);
  };

  const handleCloseModal = () => {
    setShowModal(false);
    setEditingService(null);
    setFormData({
      name: '',
      description: '',
      estimated_duration: '',
      base_price: '',
      service_type: 'OIL_CHANGE',
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const serviceData = {
        ...formData,
        estimated_duration: parseInt(formData.estimated_duration),
        base_price: parseFloat(formData.base_price),
      };

      if (editingService) {
        await api.put(`/maintenance/services/${editingService.id}`, serviceData);
        toast.success('Service updated successfully');
      } else {
        await api.post('/maintenance/services', serviceData);
        toast.success('Service created successfully');
      }

      handleCloseModal();
      fetchServices();
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to save service');
      console.error('Error saving service:', error);
    }
  };

  const handleDelete = async (serviceId) => {
    if (!window.confirm('Are you sure you want to delete this service?')) {
      return;
    }

    try {
      await api.delete(`/maintenance/services/${serviceId}`);
      toast.success('Service deleted successfully');
      fetchServices();
    } catch (error) {
      toast.error('Failed to delete service');
      console.error('Error deleting service:', error);
    }
  };

  const filteredServices = services.filter(service =>
    service.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    service.description?.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8 flex items-center justify-between">
          <div>
            <h1 className="text-4xl font-bold text-white mb-2">Maintenance Services Catalog</h1>
            <p className="text-gray-400">Manage available maintenance services</p>
          </div>
          <Button variant="primary" onClick={() => handleOpenModal()}>
            <FiPlus className="h-4 w-4 mr-2" />
            Add New Service
          </Button>
        </div>

        {/* Search Bar */}
        <div className="mb-6">
          <Input
            placeholder="Search services..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            icon={FiSearch}
          />
        </div>

        {/* Services Grid */}
        {loading ? (
          <div className="text-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-red-500 mx-auto"></div>
            <p className="text-gray-400 mt-4">Loading services...</p>
          </div>
        ) : filteredServices.length === 0 ? (
          <Card>
            <CardContent className="p-12 text-center">
              <FiTool className="h-16 w-16 text-gray-600 mx-auto mb-4" />
              <h3 className="text-xl font-semibold text-white mb-2">No Services Found</h3>
              <p className="text-gray-400 mb-6">
                {searchTerm ? 'No services match your search' : 'Start by adding your first maintenance service'}
              </p>
              {!searchTerm && (
                <Button variant="primary" onClick={() => handleOpenModal()}>
                  <FiPlus className="h-4 w-4 mr-2" />
                  Add First Service
                </Button>
              )}
            </CardContent>
          </Card>
        ) : (
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredServices.map((service) => (
              <Card key={service.id} hover>
                <CardContent className="p-6">
                  <div className="flex items-start justify-between mb-4">
                    <div className="w-12 h-12 rounded-lg bg-gradient-to-br from-yellow-500 to-orange-500 flex items-center justify-center">
                      <FiTool className="h-6 w-6 text-white" />
                    </div>
                    <div className="flex gap-2">
                      <button
                        onClick={() => handleOpenModal(service)}
                        className="w-8 h-8 rounded-lg bg-dark-800 hover:bg-blue-500 flex items-center justify-center transition-colors"
                      >
                        <FiEdit2 className="h-4 w-4 text-white" />
                      </button>
                      <button
                        onClick={() => handleDelete(service.id)}
                        className="w-8 h-8 rounded-lg bg-dark-800 hover:bg-red-500 flex items-center justify-center transition-colors"
                      >
                        <FiTrash2 className="h-4 w-4 text-white" />
                      </button>
                    </div>
                  </div>

                  <h3 className="text-xl font-bold text-white mb-2">{service.name}</h3>

                  <div className="mb-3">
                    <span className="px-3 py-1 bg-blue-500/10 text-blue-500 text-xs rounded-full">
                      {service.service_type.replace(/_/g, ' ')}
                    </span>
                  </div>

                  {service.description && (
                    <p className="text-gray-400 text-sm mb-4 line-clamp-2">{service.description}</p>
                  )}

                  <div className="flex items-center justify-between pt-4 border-t border-dark-700">
                    <div>
                      <p className="text-gray-400 text-xs mb-1">Duration</p>
                      <p className="text-white font-semibold">{service.estimated_duration || 'N/A'} min</p>
                    </div>
                    <div className="text-right">
                      <p className="text-gray-400 text-xs mb-1">Price</p>
                      <p className="text-2xl font-bold text-white">GH₵ {service.base_price}</p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        )}
      </div>

      {/* Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-black/70 backdrop-blur-sm flex items-center justify-center z-50 p-4">
          <div className="w-full max-w-2xl max-h-[90vh] overflow-y-auto bg-dark-900 rounded-xl border border-dark-700 shadow-2xl">
            <div className="p-6 pb-4 flex items-center justify-between border-b border-dark-700">
              <h2 className="text-2xl font-bold text-white">
                {editingService ? 'Edit Service' : 'Add New Service'}
              </h2>
              <button
                onClick={handleCloseModal}
                className="w-8 h-8 rounded-lg bg-dark-800 hover:bg-red-500 flex items-center justify-center transition-colors"
              >
                <FiX className="h-5 w-5 text-white" />
              </button>
            </div>

            <div className="p-6">
              <form onSubmit={handleSubmit} className="space-y-6">
                <Input
                  label="Service Name"
                  value={formData.name}
                  onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  placeholder="e.g., Full Synthetic Oil Change"
                  required
                />

                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">
                    Service Type
                  </label>
                  <select
                    value={formData.service_type}
                    onChange={(e) => setFormData({ ...formData, service_type: e.target.value })}
                    className="w-full px-4 py-3 bg-dark-800 border border-dark-700 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-red-500"
                    required
                  >
                    {serviceTypes.map(type => (
                      <option key={type.value} value={type.value}>
                        {type.label}
                      </option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">
                    Description
                  </label>
                  <textarea
                    value={formData.description}
                    onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                    placeholder="Describe the service..."
                    rows={4}
                    className="w-full px-4 py-3 bg-dark-800 border border-dark-700 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-red-500"
                  />
                </div>

                <div className="grid md:grid-cols-2 gap-4">
                  <Input
                    label="Estimated Duration (minutes)"
                    type="number"
                    value={formData.estimated_duration}
                    onChange={(e) => setFormData({ ...formData, estimated_duration: e.target.value })}
                    placeholder="60"
                    min="1"
                    required
                  />

                  <Input
                    label="Base Price (GH₵)"
                    type="number"
                    step="0.01"
                    value={formData.base_price}
                    onChange={(e) => setFormData({ ...formData, base_price: e.target.value })}
                    placeholder="150.00"
                    min="0"
                    required
                  />
                </div>

                <div className="flex gap-4 pt-4">
                  <Button type="button" variant="outline" onClick={handleCloseModal} className="flex-1">
                    Cancel
                  </Button>
                  <Button type="submit" variant="primary" className="flex-1">
                    {editingService ? 'Update Service' : 'Create Service'}
                  </Button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default MaintenanceServices;
