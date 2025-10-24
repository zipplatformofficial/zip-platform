import React, { useState, useEffect } from 'react';
import { FiTruck, FiPlus, FiEdit2, FiTrash2, FiSearch, FiX } from 'react-icons/fi';
import Card, { CardContent } from '../../components/ui/Card';
import Button from '../../components/ui/Button';
import Input from '../../components/ui/Input';
import toast from 'react-hot-toast';
import api from '../../services/api';

const RentalFleet = () => {
  const [vehicles, setVehicles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [showModal, setShowModal] = useState(false);
  const [editingVehicle, setEditingVehicle] = useState(null);
  const [formData, setFormData] = useState({
    make: '',
    model: '',
    year: '',
    color: '',
    license_plate: '',
    vin: '',
    daily_rate: '',
    seating_capacity: '',
    transmission: 'AUTOMATIC',
    fuel_type: 'PETROL',
    features: '',
    insurance_policy: '',
    is_available: true,
  });

  const transmissionTypes = [
    { value: 'AUTOMATIC', label: 'Automatic' },
    { value: 'MANUAL', label: 'Manual' },
  ];

  const fuelTypes = [
    { value: 'PETROL', label: 'Petrol' },
    { value: 'DIESEL', label: 'Diesel' },
    { value: 'ELECTRIC', label: 'Electric' },
    { value: 'HYBRID', label: 'Hybrid' },
  ];

  useEffect(() => {
    fetchVehicles();
  }, []);

  const fetchVehicles = async () => {
    try {
      setLoading(true);
      const response = await api.get('/rentals/vehicles');
      setVehicles(response.data);
    } catch (error) {
      toast.error('Failed to load vehicles');
      console.error('Error fetching vehicles:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleOpenModal = (vehicle = null) => {
    if (vehicle) {
      setEditingVehicle(vehicle);
      setFormData({
        make: vehicle.make,
        model: vehicle.model,
        year: vehicle.year.toString(),
        color: vehicle.color || '',
        license_plate: vehicle.license_plate,
        vin: vehicle.vin || '',
        daily_rate: vehicle.daily_rate.toString(),
        seating_capacity: vehicle.seating_capacity?.toString() || '',
        transmission: vehicle.transmission || 'AUTOMATIC',
        fuel_type: vehicle.fuel_type || 'PETROL',
        features: Array.isArray(vehicle.features) ? vehicle.features.join(', ') : '',
        insurance_policy: vehicle.insurance_policy || '',
        is_available: vehicle.is_available !== undefined ? vehicle.is_available : true,
      });
    } else {
      setEditingVehicle(null);
      setFormData({
        make: '',
        model: '',
        year: '',
        color: '',
        license_plate: '',
        vin: '',
        daily_rate: '',
        seating_capacity: '',
        transmission: 'AUTOMATIC',
        fuel_type: 'PETROL',
        features: '',
        insurance_policy: '',
        is_available: true,
      });
    }
    setShowModal(true);
  };

  const handleCloseModal = () => {
    setShowModal(false);
    setEditingVehicle(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const vehicleData = {
        make: formData.make,
        model: formData.model,
        year: parseInt(formData.year),
        color: formData.color,
        license_plate: formData.license_plate,
        vin: formData.vin,
        daily_rate: parseFloat(formData.daily_rate),
        seating_capacity: formData.seating_capacity ? parseInt(formData.seating_capacity) : null,
        transmission: formData.transmission,
        fuel_type: formData.fuel_type,
        features: formData.features ? formData.features.split(',').map(f => f.trim()) : [],
        insurance_policy: formData.insurance_policy,
        is_available: formData.is_available,
      };

      if (editingVehicle) {
        await api.put(`/rentals/vehicles/${editingVehicle.id}`, vehicleData);
        toast.success('Vehicle updated successfully');
      } else {
        await api.post('/rentals/vehicles', vehicleData);
        toast.success('Vehicle added successfully');
      }

      handleCloseModal();
      fetchVehicles();
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to save vehicle');
      console.error('Error saving vehicle:', error);
    }
  };

  const handleDelete = async (vehicleId) => {
    if (!window.confirm('Are you sure you want to delete this vehicle?')) {
      return;
    }

    try {
      await api.delete(`/rentals/vehicles/${vehicleId}`);
      toast.success('Vehicle deleted successfully');
      fetchVehicles();
    } catch (error) {
      toast.error('Failed to delete vehicle');
      console.error('Error deleting vehicle:', error);
    }
  };

  const filteredVehicles = vehicles.filter(vehicle =>
    vehicle.make.toLowerCase().includes(searchTerm.toLowerCase()) ||
    vehicle.model.toLowerCase().includes(searchTerm.toLowerCase()) ||
    vehicle.license_plate.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8 flex items-center justify-between">
          <div>
            <h1 className="text-4xl font-bold text-white mb-2">Rental Fleet Management</h1>
            <p className="text-gray-400">Manage all rental vehicles</p>
          </div>
          <Button variant="primary" onClick={() => handleOpenModal()}>
            <FiPlus className="h-4 w-4 mr-2" />
            Add New Vehicle
          </Button>
        </div>

        {/* Search Bar */}
        <div className="mb-6">
          <Input
            placeholder="Search vehicles by make, model, or license plate..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            icon={FiSearch}
          />
        </div>

        {/* Vehicles Grid */}
        {loading ? (
          <div className="text-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-red-500 mx-auto"></div>
            <p className="text-gray-400 mt-4">Loading vehicles...</p>
          </div>
        ) : filteredVehicles.length === 0 ? (
          <Card>
            <CardContent className="p-12 text-center">
              <FiTruck className="h-16 w-16 text-gray-600 mx-auto mb-4" />
              <h3 className="text-xl font-semibold text-white mb-2">No Vehicles Found</h3>
              <p className="text-gray-400 mb-6">
                {searchTerm ? 'No vehicles match your search' : 'Start by adding your first rental vehicle'}
              </p>
              {!searchTerm && (
                <Button variant="primary" onClick={() => handleOpenModal()}>
                  <FiPlus className="h-4 w-4 mr-2" />
                  Add First Vehicle
                </Button>
              )}
            </CardContent>
          </Card>
        ) : (
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredVehicles.map((vehicle) => (
              <Card key={vehicle.id} hover>
                <CardContent className="p-6">
                  <div className="flex items-start justify-between mb-4">
                    <div className="w-12 h-12 rounded-lg bg-gradient-to-br from-cyan-500 to-blue-500 flex items-center justify-center">
                      <FiTruck className="h-6 w-6 text-white" />
                    </div>
                    <div className="flex gap-2">
                      <button
                        onClick={() => handleOpenModal(vehicle)}
                        className="w-8 h-8 rounded-lg bg-dark-800 hover:bg-blue-500 flex items-center justify-center transition-colors"
                      >
                        <FiEdit2 className="h-4 w-4 text-white" />
                      </button>
                      <button
                        onClick={() => handleDelete(vehicle.id)}
                        className="w-8 h-8 rounded-lg bg-dark-800 hover:bg-red-500 flex items-center justify-center transition-colors"
                      >
                        <FiTrash2 className="h-4 w-4 text-white" />
                      </button>
                    </div>
                  </div>

                  <h3 className="text-xl font-bold text-white mb-1">
                    {vehicle.make} {vehicle.model}
                  </h3>
                  <p className="text-gray-400 text-sm mb-3">{vehicle.year}</p>

                  <div className="flex gap-2 mb-4">
                    <span className={`px-3 py-1 text-xs rounded-full ${
                      vehicle.is_available
                        ? 'bg-green-500/10 text-green-500'
                        : 'bg-red-500/10 text-red-500'
                    }`}>
                      {vehicle.is_available ? 'Available' : 'Rented'}
                    </span>
                    <span className="px-3 py-1 bg-blue-500/10 text-blue-500 text-xs rounded-full">
                      {vehicle.transmission}
                    </span>
                  </div>

                  <div className="space-y-2 mb-4">
                    <div className="flex justify-between text-sm">
                      <span className="text-gray-400">License Plate:</span>
                      <span className="text-white font-medium">{vehicle.license_plate}</span>
                    </div>
                    {vehicle.color && (
                      <div className="flex justify-between text-sm">
                        <span className="text-gray-400">Color:</span>
                        <span className="text-white">{vehicle.color}</span>
                      </div>
                    )}
                    {vehicle.seating_capacity && (
                      <div className="flex justify-between text-sm">
                        <span className="text-gray-400">Seats:</span>
                        <span className="text-white">{vehicle.seating_capacity}</span>
                      </div>
                    )}
                  </div>

                  <div className="pt-4 border-t border-dark-700">
                    <div className="flex items-center justify-between">
                      <span className="text-gray-400 text-sm">Daily Rate</span>
                      <span className="text-2xl font-bold text-white">GH₵ {vehicle.daily_rate}</span>
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
          <div className="w-full max-w-4xl max-h-[90vh] overflow-y-auto bg-dark-900 rounded-xl border border-dark-700 shadow-2xl">
            <div className="p-6 pb-4 flex items-center justify-between border-b border-dark-700">
              <h2 className="text-2xl font-bold text-white">
                {editingVehicle ? 'Edit Vehicle' : 'Add New Vehicle'}
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
                {/* Basic Info */}
                <div className="grid md:grid-cols-3 gap-4">
                  <Input
                    label="Make"
                    value={formData.make}
                    onChange={(e) => setFormData({ ...formData, make: e.target.value })}
                    placeholder="Toyota"
                    required
                  />

                  <Input
                    label="Model"
                    value={formData.model}
                    onChange={(e) => setFormData({ ...formData, model: e.target.value })}
                    placeholder="Camry"
                    required
                  />

                  <Input
                    label="Year"
                    type="number"
                    value={formData.year}
                    onChange={(e) => setFormData({ ...formData, year: e.target.value })}
                    placeholder="2024"
                    min="1900"
                    max="2030"
                    required
                  />
                </div>

                {/* Vehicle Details */}
                <div className="grid md:grid-cols-2 gap-4">
                  <Input
                    label="Color"
                    value={formData.color}
                    onChange={(e) => setFormData({ ...formData, color: e.target.value })}
                    placeholder="White"
                  />

                  <Input
                    label="License Plate"
                    value={formData.license_plate}
                    onChange={(e) => setFormData({ ...formData, license_plate: e.target.value })}
                    placeholder="GR-1234-20"
                    required
                  />
                </div>

                <div className="grid md:grid-cols-2 gap-4">
                  <Input
                    label="VIN (Optional)"
                    value={formData.vin}
                    onChange={(e) => setFormData({ ...formData, vin: e.target.value })}
                    placeholder="1HGBH41JXMN109186"
                  />

                  <Input
                    label="Seating Capacity"
                    type="number"
                    value={formData.seating_capacity}
                    onChange={(e) => setFormData({ ...formData, seating_capacity: e.target.value })}
                    placeholder="5"
                    min="2"
                    max="15"
                  />
                </div>

                {/* Specifications */}
                <div className="grid md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-300 mb-2">
                      Transmission
                    </label>
                    <select
                      value={formData.transmission}
                      onChange={(e) => setFormData({ ...formData, transmission: e.target.value })}
                      className="w-full px-4 py-3 bg-dark-800 border border-dark-700 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-red-500"
                      required
                    >
                      {transmissionTypes.map(type => (
                        <option key={type.value} value={type.value}>
                          {type.label}
                        </option>
                      ))}
                    </select>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-300 mb-2">
                      Fuel Type
                    </label>
                    <select
                      value={formData.fuel_type}
                      onChange={(e) => setFormData({ ...formData, fuel_type: e.target.value })}
                      className="w-full px-4 py-3 bg-dark-800 border border-dark-700 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-red-500"
                      required
                    >
                      {fuelTypes.map(type => (
                        <option key={type.value} value={type.value}>
                          {type.label}
                        </option>
                      ))}
                    </select>
                  </div>
                </div>

                {/* Pricing */}
                <Input
                  label="Daily Rate (GH₵)"
                  type="number"
                  step="0.01"
                  value={formData.daily_rate}
                  onChange={(e) => setFormData({ ...formData, daily_rate: e.target.value })}
                  placeholder="200.00"
                  min="0"
                  required
                />

                {/* Features */}
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">
                    Features (comma-separated)
                  </label>
                  <Input
                    value={formData.features}
                    onChange={(e) => setFormData({ ...formData, features: e.target.value })}
                    placeholder="AC, GPS, Bluetooth, Backup Camera"
                  />
                </div>

                {/* Insurance */}
                <Input
                  label="Insurance Policy Number"
                  value={formData.insurance_policy}
                  onChange={(e) => setFormData({ ...formData, insurance_policy: e.target.value })}
                  placeholder="INS-123456"
                />

                {/* Availability */}
                <div className="flex items-center gap-3">
                  <input
                    type="checkbox"
                    id="is_available"
                    checked={formData.is_available}
                    onChange={(e) => setFormData({ ...formData, is_available: e.target.checked })}
                    className="w-5 h-5 rounded border-dark-700 bg-dark-800 text-red-500 focus:ring-red-500 focus:ring-offset-midnight-950"
                  />
                  <label htmlFor="is_available" className="text-white font-medium">
                    Vehicle is available for rent
                  </label>
                </div>

                <div className="flex gap-4 pt-4">
                  <Button type="button" variant="outline" onClick={handleCloseModal} className="flex-1">
                    Cancel
                  </Button>
                  <Button type="submit" variant="primary" className="flex-1">
                    {editingVehicle ? 'Update Vehicle' : 'Add Vehicle'}
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

export default RentalFleet;
