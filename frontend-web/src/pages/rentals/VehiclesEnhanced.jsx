import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { FiSliders, FiX, FiSearch, FiCalendar, FiMapPin, FiGrid, FiList, FiEye, FiBarChart2 } from 'react-icons/fi';
import { rentalService } from '../../services/rentalService';
import VehicleCardEnhanced from '../../components/rentals/VehicleCardEnhanced';
import QuickViewModal from '../../components/rentals/QuickViewModal';
import CompareModal from '../../components/rentals/CompareModal';
import { VehicleCardSkeleton } from '../../components/ui/SkeletonLoader';
import Input from '../../components/ui/Input';
import Button from '../../components/ui/Button';
import Loading from '../../components/ui/Loading';
import Modal from '../../components/ui/Modal';
import { formatCurrency } from '../../utils/formatters';
import toast from 'react-hot-toast';
import { useAuth } from '../../hooks/useAuth';

const VehiclesEnhanced = () => {
  const navigate = useNavigate();
  const { isAuthenticated } = useAuth();
  const [vehicles, setVehicles] = useState([]);
  const [filteredVehicles, setFilteredVehicles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedVehicle, setSelectedVehicle] = useState(null);
  const [showBookingModal, setShowBookingModal] = useState(false);
  const [showFilters, setShowFilters] = useState(false);

  // New states for Quick View and Comparison
  const [showQuickView, setShowQuickView] = useState(false);
  const [quickViewVehicle, setQuickViewVehicle] = useState(null);
  const [compareVehicles, setCompareVehicles] = useState([]);
  const [showCompareModal, setShowCompareModal] = useState(false);

  const [filters, setFilters] = useState({
    make: '',
    minPrice: '',
    maxPrice: '',
    seats: '',
    transmission: '',
    availability: 'all',
  });

  const [bookingData, setBookingData] = useState({
    start_date: '',
    end_date: '',
    pickup_location: '',
    notes: ''
  });
  const [totalCost, setTotalCost] = useState(0);

  useEffect(() => {
    fetchVehicles();
  }, []);

  useEffect(() => {
    applyFilters();
  }, [vehicles, filters]);

  useEffect(() => {
    if (selectedVehicle && bookingData.start_date && bookingData.end_date) {
      calculateCost();
    }
  }, [bookingData.start_date, bookingData.end_date, selectedVehicle]);

  const fetchVehicles = async () => {
    try {
      setLoading(true);
      const data = await rentalService.getVehicles();
      const vehiclesArray = Array.isArray(data) ? data : [];
      setVehicles(vehiclesArray);
      setFilteredVehicles(vehiclesArray);
    } catch (error) {
      toast.error('Failed to load vehicles');
      console.error('Error fetching vehicles:', error);
      setVehicles([]); // Set empty array on error to prevent filter errors
      setFilteredVehicles([]);
    } finally {
      setLoading(false);
    }
  };

  const applyFilters = () => {
    let filtered = [...vehicles];

    if (filters.make) {
      filtered = filtered.filter(v =>
        v.make.toLowerCase().includes(filters.make.toLowerCase())
      );
    }

    if (filters.minPrice) {
      filtered = filtered.filter(v => v.daily_rate >= parseFloat(filters.minPrice));
    }

    if (filters.maxPrice) {
      filtered = filtered.filter(v => v.daily_rate <= parseFloat(filters.maxPrice));
    }

    if (filters.seats) {
      filtered = filtered.filter(v => v.seats >= parseInt(filters.seats));
    }

    if (filters.transmission) {
      filtered = filtered.filter(v =>
        v.transmission?.toLowerCase() === filters.transmission.toLowerCase()
      );
    }

    if (filters.availability === 'available') {
      filtered = filtered.filter(v => v.is_available);
    } else if (filters.availability === 'rented') {
      filtered = filtered.filter(v => !v.is_available);
    }

    setFilteredVehicles(filtered);
  };

  const resetFilters = () => {
    setFilters({
      make: '',
      minPrice: '',
      maxPrice: '',
      seats: '',
      transmission: '',
      availability: 'all',
    });
  };

  const calculateCost = () => {
    const start = new Date(bookingData.start_date);
    const end = new Date(bookingData.end_date);
    const days = Math.ceil((end - start) / (1000 * 60 * 60 * 24));
    if (days > 0) {
      setTotalCost(days * selectedVehicle.daily_rate);
    }
  };

  const handleBookVehicle = (vehicle) => {
    if (!isAuthenticated) {
      toast.error('Please login to rent a vehicle');
      navigate('/login');
      return;
    }
    setSelectedVehicle(vehicle);
    setShowBookingModal(true);
  };

  const handleBookingSubmit = async (e) => {
    e.preventDefault();

    try {
      const bookingPayload = {
        vehicle_id: selectedVehicle.id,
        start_date: bookingData.start_date,
        end_date: bookingData.end_date,
        pickup_location: bookingData.pickup_location,
        notes: bookingData.notes
      };

      await rentalService.createBooking(bookingPayload);
      toast.success('Vehicle booked successfully!');
      setShowBookingModal(false);
      navigate('/dashboard/rentals');
    } catch (error) {
      toast.error('Failed to book vehicle');
    }
  };

  // Quick View handlers
  const handleQuickView = (vehicle) => {
    setQuickViewVehicle(vehicle);
    setShowQuickView(true);
  };

  // Compare handlers
  const handleToggleCompare = (vehicle) => {
    const isAlreadyComparing = compareVehicles.some(v => v.id === vehicle.id);

    if (isAlreadyComparing) {
      setCompareVehicles(compareVehicles.filter(v => v.id !== vehicle.id));
      toast.success('Removed from comparison');
    } else {
      if (compareVehicles.length >= 3) {
        toast.error('You can only compare up to 3 vehicles');
        return;
      }
      setCompareVehicles([...compareVehicles, vehicle]);
      toast.success('Added to comparison');
    }
  };

  const handleRemoveFromCompare = (vehicleId) => {
    setCompareVehicles(compareVehicles.filter(v => v.id !== vehicleId));
  };

  const handleOpenCompare = () => {
    if (compareVehicles.length === 0) {
      toast.error('Please select at least one vehicle to compare');
      return;
    }
    setShowCompareModal(true);
  };

  return (
    <div className="min-h-screen bg-gray-50 pt-20 pb-12">
      {/* Floating Compare Bar */}
      {compareVehicles.length > 0 && (
        <div className="fixed bottom-6 left-1/2 -translate-x-1/2 z-40 animate-slide-in-right">
          <div className="bg-gradient-to-r from-red-500 to-orange-500 text-white rounded-full shadow-2xl px-6 py-4 flex items-center gap-4">
            <FiBarChart2 className="h-6 w-6" />
            <span className="font-bold">
              {compareVehicles.length} vehicle{compareVehicles.length > 1 ? 's' : ''} selected
            </span>
            <button
              onClick={handleOpenCompare}
              className="px-4 py-2 bg-white text-red-500 rounded-full font-bold hover:bg-gray-100 transition-all"
            >
              Compare Now
            </button>
            <button
              onClick={() => setCompareVehicles([])}
              className="p-2 hover:bg-white/20 rounded-full transition-all"
            >
              <FiX className="h-5 w-5" />
            </button>
          </div>
        </div>
      )}
      {/* Enhanced Hero Section */}
      <div className="relative bg-gradient-to-br from-gray-900 via-gray-800 to-black text-white overflow-hidden">
        {/* Background Pattern */}
        <div className="absolute inset-0 opacity-10">
          <div className="absolute inset-0" style={{
            backgroundImage: 'radial-gradient(circle at 2px 2px, white 1px, transparent 0)',
            backgroundSize: '40px 40px'
          }}></div>
        </div>

        {/* Red Gradient Overlay */}
        <div className="absolute inset-0 bg-gradient-to-r from-red-600/20 via-transparent to-transparent"></div>

        <div className="relative max-w-7xl mx-auto px-4 py-12 sm:py-16 md:py-20">
          <div className="text-center mb-8 sm:mb-10 md:mb-12">
            {/* Badge */}
            <div className="inline-block mb-6 animate-fade-in-up">
              <span className="bg-red-500/20 text-red-400 px-6 py-3 rounded-full text-sm font-bold border border-red-500/30 backdrop-blur-sm">
                🚗 PREMIUM CAR RENTALS
              </span>
            </div>

            {/* Main Heading */}
            <h1 className="text-3xl sm:text-4xl md:text-5xl lg:text-6xl xl:text-7xl font-bold mb-4 sm:mb-6 leading-tight animate-fade-in-up" style={{ animationDelay: '0.1s' }}>
              Rent Your{' '}
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-red-500 via-orange-500 to-red-400 animate-gradient">
                Dream Car
              </span>
            </h1>

            <p className="text-lg sm:text-xl md:text-2xl text-gray-300 mb-8 sm:mb-10 md:mb-12 max-w-3xl mx-auto leading-relaxed animate-fade-in-up px-4" style={{ animationDelay: '0.2s' }}>
              Choose from our premium fleet of {vehicles.length}+ well-maintained vehicles. Your perfect ride awaits!
            </p>

            {/* Quick Stats */}
            <div className="flex flex-wrap justify-center gap-4 sm:gap-6 md:gap-8 mb-8 sm:mb-10 md:mb-12 animate-fade-in-up" style={{ animationDelay: '0.3s' }}>
              <div className="text-center px-2">
                <div className="text-2xl sm:text-3xl md:text-4xl font-bold text-red-500 mb-1 sm:mb-2">{vehicles.length}+</div>
                <div className="text-xs sm:text-sm text-gray-400 uppercase tracking-wider">Vehicles</div>
              </div>
              <div className="text-center px-2">
                <div className="text-2xl sm:text-3xl md:text-4xl font-bold text-red-500 mb-1 sm:mb-2">24/7</div>
                <div className="text-xs sm:text-sm text-gray-400 uppercase tracking-wider">Support</div>
              </div>
              <div className="text-center px-2">
                <div className="text-2xl sm:text-3xl md:text-4xl font-bold text-red-500 mb-1 sm:mb-2">4.9★</div>
                <div className="text-xs sm:text-sm text-gray-400 uppercase tracking-wider">Rating</div>
              </div>
              <div className="text-center px-2">
                <div className="text-2xl sm:text-3xl md:text-4xl font-bold text-red-500 mb-1 sm:mb-2">5K+</div>
                <div className="text-xs sm:text-sm text-gray-400 uppercase tracking-wider">Customers</div>
              </div>
            </div>

            {/* Quick Search Bar */}
            <div className="max-w-4xl mx-auto animate-fade-in-up" style={{ animationDelay: '0.4s' }}>
              <div className="bg-white/95 backdrop-blur-lg rounded-2xl shadow-2xl p-4 sm:p-6">
                <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-3 sm:gap-4">
                  <div className="relative">
                    <FiSearch className="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400 h-5 w-5" />
                    <input
                      type="text"
                      placeholder="Search by brand..."
                      className="w-full pl-12 pr-4 py-3 rounded-xl border-2 border-gray-200 focus:border-red-500 focus:ring-4 focus:ring-red-500/20 outline-none transition-all text-gray-900"
                      value={filters.make}
                      onChange={(e) => setFilters({ ...filters, make: e.target.value })}
                    />
                  </div>
                  <div className="relative">
                    <FiMapPin className="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400 h-5 w-5" />
                    <select
                      className="w-full pl-12 pr-4 py-3 rounded-xl border-2 border-gray-200 focus:border-red-500 focus:ring-4 focus:ring-red-500/20 outline-none transition-all text-gray-900 bg-white appearance-none"
                      value={filters.transmission}
                      onChange={(e) => setFilters({ ...filters, transmission: e.target.value })}
                    >
                      <option value="">All Transmission</option>
                      <option value="automatic">Automatic</option>
                      <option value="manual">Manual</option>
                    </select>
                  </div>
                  <div className="relative">
                    <select
                      className="w-full px-4 py-3 rounded-xl border-2 border-gray-200 focus:border-red-500 focus:ring-4 focus:ring-red-500/20 outline-none transition-all text-gray-900 bg-white"
                      value={filters.seats}
                      onChange={(e) => setFilters({ ...filters, seats: e.target.value })}
                    >
                      <option value="">Any Seats</option>
                      <option value="2">2+ Seats</option>
                      <option value="4">4+ Seats</option>
                      <option value="5">5+ Seats</option>
                      <option value="7">7+ Seats</option>
                    </select>
                  </div>
                  <Button
                    variant="primary"
                    size="lg"
                    className="w-full sm:col-span-2 md:col-span-1 py-3 shadow-xl hover:shadow-2xl"
                    onClick={applyFilters}
                  >
                    <FiSearch className="mr-2" />
                    Search
                  </Button>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Wave Divider */}
        <div className="absolute bottom-0 left-0 right-0">
          <svg className="w-full h-16 text-gray-50" preserveAspectRatio="none" viewBox="0 0 1440 54">
            <path fill="currentColor" d="M0,32L80,37.3C160,43,320,53,480,48C640,43,800,21,960,16C1120,11,1280,21,1360,26.7L1440,32L1440,54L1360,54C1280,54,1120,54,960,54C800,54,640,54,480,54C320,54,160,54,80,54L0,54Z"></path>
          </svg>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 py-8">
        {/* Filter Button (Mobile) */}
        <div className="mb-6 lg:hidden">
          <Button
            variant="outline"
            onClick={() => setShowFilters(!showFilters)}
            className="w-full"
          >
            <FiSliders className="mr-2" />
            {showFilters ? 'Hide Filters' : 'Show Filters'}
          </Button>
        </div>

        <div className="flex gap-8">
          {/* Enhanced Filters Sidebar */}
          <div className={`${showFilters ? 'block' : 'hidden'} lg:block w-full lg:w-80 flex-shrink-0`}>
            <div className="bg-white rounded-3xl shadow-xl p-6 sticky top-24 border-2 border-gray-100">
              <div className="flex items-center justify-between mb-6">
                <div className="flex items-center gap-2">
                  <FiSliders className="h-5 w-5 text-red-500" />
                  <h3 className="text-xl font-bold text-gray-900">Filters</h3>
                </div>
                <button
                  onClick={resetFilters}
                  className="text-red-500 text-sm font-bold hover:text-red-600 hover:scale-105 transition-transform px-3 py-1 rounded-lg hover:bg-red-50"
                >
                  Reset All
                </button>
              </div>

              <div className="space-y-6">
                {/* Price Range */}
                <div className="pb-6 border-b border-gray-200">
                  <label className="block text-sm font-bold text-gray-900 mb-3 uppercase tracking-wide">
                    💰 Price Range (Daily)
                  </label>
                  <div className="grid grid-cols-2 gap-3">
                    <div className="relative">
                      <span className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-500 text-sm">GH₵</span>
                      <input
                        type="number"
                        placeholder="Min"
                        className="w-full pl-10 pr-3 py-3 rounded-xl border-2 border-gray-200 focus:border-red-500 focus:ring-4 focus:ring-red-500/20 outline-none transition-all text-gray-900"
                        value={filters.minPrice}
                        onChange={(e) => setFilters({ ...filters, minPrice: e.target.value })}
                      />
                    </div>
                    <div className="relative">
                      <span className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-500 text-sm">GH₵</span>
                      <input
                        type="number"
                        placeholder="Max"
                        className="w-full pl-10 pr-3 py-3 rounded-xl border-2 border-gray-200 focus:border-red-500 focus:ring-4 focus:ring-red-500/20 outline-none transition-all text-gray-900"
                        value={filters.maxPrice}
                        onChange={(e) => setFilters({ ...filters, maxPrice: e.target.value })}
                      />
                    </div>
                  </div>
                </div>

                {/* Seats */}
                <div className="pb-6 border-b border-gray-200">
                  <label className="block text-sm font-bold text-gray-900 mb-3 uppercase tracking-wide">
                    👥 Number of Seats
                  </label>
                  <div className="grid grid-cols-4 gap-2">
                    {['Any', '2+', '4+', '5+', '7+'].map((seat, idx) => (
                      <button
                        key={seat}
                        onClick={() => setFilters({ ...filters, seats: idx === 0 ? '' : seat.replace('+', '') })}
                        className={`py-3 px-2 rounded-xl text-sm font-bold transition-all ${
                          (idx === 0 && filters.seats === '') || filters.seats === seat.replace('+', '')
                            ? 'bg-red-500 text-white shadow-lg scale-105'
                            : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                        }`}
                      >
                        {seat}
                      </button>
                    ))}
                  </div>
                </div>

                {/* Transmission */}
                <div className="pb-6 border-b border-gray-200">
                  <label className="block text-sm font-bold text-gray-900 mb-3 uppercase tracking-wide">
                    ⚙️ Transmission
                  </label>
                  <div className="grid grid-cols-3 gap-2">
                    {[
                      { label: 'All', value: '' },
                      { label: 'Auto', value: 'automatic' },
                      { label: 'Manual', value: 'manual' }
                    ].map((trans) => (
                      <button
                        key={trans.value}
                        onClick={() => setFilters({ ...filters, transmission: trans.value })}
                        className={`py-3 px-3 rounded-xl text-sm font-bold transition-all ${
                          filters.transmission === trans.value
                            ? 'bg-red-500 text-white shadow-lg scale-105'
                            : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                        }`}
                      >
                        {trans.label}
                      </button>
                    ))}
                  </div>
                </div>

                {/* Availability */}
                <div>
                  <label className="block text-sm font-bold text-gray-900 mb-3 uppercase tracking-wide">
                    ✅ Availability
                  </label>
                  <div className="grid grid-cols-3 gap-2">
                    {[
                      { label: 'All', value: 'all' },
                      { label: 'Available', value: 'available' },
                      { label: 'Rented', value: 'rented' }
                    ].map((avail) => (
                      <button
                        key={avail.value}
                        onClick={() => setFilters({ ...filters, availability: avail.value })}
                        className={`py-3 px-3 rounded-xl text-sm font-bold transition-all ${
                          filters.availability === avail.value
                            ? 'bg-red-500 text-white shadow-lg scale-105'
                            : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                        }`}
                      >
                        {avail.label}
                      </button>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Vehicles Grid */}
          <div className="flex-1">
            <div className="mb-4 text-sm sm:text-base text-gray-600 font-medium px-2">
              {loading ? (
                'Loading vehicles...'
              ) : (
                `Showing ${filteredVehicles.length} of ${vehicles.length} vehicles`
              )}
            </div>

            {loading ? (
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-2 xl:grid-cols-3 gap-4 sm:gap-6">
                {[1, 2, 3, 4, 5, 6].map((i) => (
                  <VehicleCardSkeleton key={i} />
                ))}
              </div>
            ) : filteredVehicles.length > 0 ? (
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-2 xl:grid-cols-3 gap-4 sm:gap-6">
                {filteredVehicles.map((vehicle) => (
                  <div key={vehicle.id} className="relative group">
                    <VehicleCardEnhanced
                      vehicle={vehicle}
                      onBook={handleBookVehicle}
                    />
                    {/* Quick Action Buttons */}
                    <div className="absolute top-4 right-4 flex gap-2 opacity-0 group-hover:opacity-100 transition-all duration-300 z-10">
                      <button
                        onClick={() => handleQuickView(vehicle)}
                        className="p-2 bg-white/90 backdrop-blur-sm rounded-full shadow-lg hover:bg-white hover:scale-110 transition-all"
                        title="Quick View"
                      >
                        <FiEye className="h-5 w-5 text-gray-700" />
                      </button>
                      <button
                        onClick={() => handleToggleCompare(vehicle)}
                        className={`p-2 rounded-full shadow-lg hover:scale-110 transition-all ${
                          compareVehicles.some(v => v.id === vehicle.id)
                            ? 'bg-red-500 text-white'
                            : 'bg-white/90 backdrop-blur-sm text-gray-700 hover:bg-white'
                        }`}
                        title="Add to Compare"
                      >
                        <FiBarChart2 className="h-5 w-5" />
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="bg-white rounded-2xl p-12 text-center">
                <p className="text-gray-500 text-lg mb-4">No vehicles match your filters</p>
                <Button variant="outline" onClick={resetFilters}>
                  Reset Filters
                </Button>
              </div>
            )}
          </div>
        </div>

        {/* Booking Modal */}
        <Modal
          isOpen={showBookingModal}
          onClose={() => setShowBookingModal(false)}
          title={`Rent ${selectedVehicle?.make} ${selectedVehicle?.model}`}
          size="lg"
        >
          <form onSubmit={handleBookingSubmit} className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <Input
                label="Start Date"
                type="date"
                required
                value={bookingData.start_date}
                onChange={(e) => setBookingData({ ...bookingData, start_date: e.target.value })}
                min={new Date().toISOString().split('T')[0]}
              />
              <Input
                label="End Date"
                type="date"
                required
                value={bookingData.end_date}
                onChange={(e) => setBookingData({ ...bookingData, end_date: e.target.value })}
                min={bookingData.start_date || new Date().toISOString().split('T')[0]}
              />
            </div>

            <Input
              label="Pickup Location"
              placeholder="Enter pickup location"
              required
              value={bookingData.pickup_location}
              onChange={(e) => setBookingData({ ...bookingData, pickup_location: e.target.value })}
            />

            <Input
              label="Additional Notes (Optional)"
              placeholder="Any special requirements..."
              value={bookingData.notes}
              onChange={(e) => setBookingData({ ...bookingData, notes: e.target.value })}
            />

            {totalCost > 0 && (
              <div className="bg-gray-50 rounded-xl p-6">
                <div className="flex justify-between items-center mb-2">
                  <span className="text-gray-600">Daily Rate</span>
                  <span className="font-semibold">{formatCurrency(selectedVehicle.daily_rate)}</span>
                </div>
                <div className="flex justify-between items-center mb-2">
                  <span className="text-gray-600">Number of Days</span>
                  <span className="font-semibold">
                    {Math.ceil((new Date(bookingData.end_date) - new Date(bookingData.start_date)) / (1000 * 60 * 60 * 24))}
                  </span>
                </div>
                <div className="border-t border-gray-300 pt-3 mt-3 flex justify-between items-center">
                  <span className="text-lg font-bold text-gray-900">Total Cost</span>
                  <span className="text-2xl font-bold text-red-500">
                    {formatCurrency(totalCost)}
                  </span>
                </div>
              </div>
            )}

            <div className="flex gap-3 pt-4">
              <Button
                type="button"
                variant="ghost"
                onClick={() => setShowBookingModal(false)}
                className="flex-1"
              >
                Cancel
              </Button>
              <Button
                type="submit"
                variant="primary"
                className="flex-1"
              >
                Confirm Booking
              </Button>
            </div>
          </form>
        </Modal>

        {/* Quick View Modal */}
        <QuickViewModal
          vehicle={quickViewVehicle}
          isOpen={showQuickView}
          onClose={() => setShowQuickView(false)}
          onBook={handleBookVehicle}
        />

        {/* Compare Modal */}
        <CompareModal
          vehicles={compareVehicles}
          isOpen={showCompareModal}
          onClose={() => setShowCompareModal(false)}
          onRemove={handleRemoveFromCompare}
          onBook={handleBookVehicle}
        />
      </div>
    </div>
  );
};

export default VehiclesEnhanced;
