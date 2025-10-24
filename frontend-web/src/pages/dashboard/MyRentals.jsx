import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { FiTruck, FiClock, FiCheckCircle, FiXCircle, FiCalendar, FiMapPin, FiEye } from 'react-icons/fi';
import Sidebar from '../../components/layout/Sidebar';
import Card, { CardContent, CardTitle } from '../../components/ui/Card';
import Loading from '../../components/ui/Loading';
import Button from '../../components/ui/Button';
import { rentalService } from '../../services/rentalService';
import toast from 'react-hot-toast';

const MyRentals = () => {
  const [rentals, setRentals] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('all'); // all, pending, active, completed, cancelled

  useEffect(() => {
    fetchRentals();
  }, []);

  const fetchRentals = async () => {
    try {
      setLoading(true);
      const data = await rentalService.getMyRentals();
      setRentals(data);
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to load rentals');
    } finally {
      setLoading(false);
    }
  };

  const handleCancelRental = async (rentalId) => {
    if (!window.confirm('Are you sure you want to cancel this rental?')) return;

    try {
      await rentalService.cancelRental(rentalId);
      toast.success('Rental cancelled successfully');
      fetchRentals();
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to cancel rental');
    }
  };

  const getStatusIcon = (status) => {
    switch (status?.toLowerCase()) {
      case 'pending':
        return <FiClock className="h-5 w-5 text-yellow-500" />;
      case 'active':
      case 'confirmed':
        return <FiCheckCircle className="h-5 w-5 text-green-500" />;
      case 'completed':
        return <FiCheckCircle className="h-5 w-5 text-blue-500" />;
      case 'cancelled':
        return <FiXCircle className="h-5 w-5 text-red-500" />;
      default:
        return <FiTruck className="h-5 w-5 text-gray-500" />;
    }
  };

  const getStatusColor = (status) => {
    switch (status?.toLowerCase()) {
      case 'pending':
        return 'bg-yellow-500/10 text-yellow-500 border-yellow-500/20';
      case 'active':
      case 'confirmed':
        return 'bg-green-500/10 text-green-500 border-green-500/20';
      case 'completed':
        return 'bg-blue-500/10 text-blue-500 border-blue-500/20';
      case 'cancelled':
        return 'bg-red-500/10 text-red-500 border-red-500/20';
      default:
        return 'bg-gray-500/10 text-gray-500 border-gray-500/20';
    }
  };

  const calculateDuration = (startDate, endDate) => {
    const start = new Date(startDate);
    const end = new Date(endDate);
    const days = Math.ceil((end - start) / (1000 * 60 * 60 * 24));
    return days;
  };

  const filteredRentals = rentals.filter(rental => {
    if (filter === 'all') return true;
    return rental.status?.toLowerCase() === filter;
  });

  if (loading) {
    return <Loading fullScreen />;
  }

  return (
    <div className="min-h-screen bg-midnight-950 pt-16">
      <div className="flex">
        <Sidebar />

        <main className="flex-1 ml-0 lg:ml-64 p-4 sm:p-6 lg:p-8">
          <div className="max-w-7xl mx-auto">
            {/* Header */}
            <div className="mb-6 sm:mb-8">
              <h1 className="text-2xl sm:text-3xl font-bold text-white mb-2">My Rentals</h1>
              <p className="text-sm sm:text-base text-gray-400">Track and manage your vehicle rentals</p>
            </div>

            {/* Filter Tabs */}
            <div className="mb-4 sm:mb-6 flex flex-wrap gap-2">
              {['all', 'pending', 'active', 'completed', 'cancelled'].map((status) => (
                <button
                  key={status}
                  onClick={() => setFilter(status)}
                  className={`px-3 sm:px-4 py-2 rounded-lg text-sm sm:text-base font-medium transition-all capitalize ${
                    filter === status
                      ? 'bg-red-500 text-white shadow-red-glow'
                      : 'bg-dark-800 text-gray-400 hover:bg-dark-700 hover:text-white'
                  }`}
                >
                  {status}
                  {status === 'all' && rentals.length > 0 && (
                    <span className="ml-2 px-2 py-0.5 bg-dark-700 rounded-full text-xs">
                      {rentals.length}
                    </span>
                  )}
                </button>
              ))}
            </div>

            {/* Rentals List */}
            {filteredRentals.length === 0 ? (
              <Card>
                <CardContent className="p-12 text-center">
                  <FiTruck className="h-16 w-16 text-gray-600 mx-auto mb-4" />
                  <h3 className="text-xl font-semibold text-white mb-2">No rentals found</h3>
                  <p className="text-gray-400 mb-6">
                    {filter === 'all'
                      ? "You haven't rented any vehicles yet"
                      : `No ${filter} rentals found`
                    }
                  </p>
                  <Link to="/rentals">
                    <Button variant="primary">Browse Available Vehicles</Button>
                  </Link>
                </CardContent>
              </Card>
            ) : (
              <div className="space-y-4">
                {filteredRentals.map((rental) => (
                  <Card key={rental.id} hover>
                    <CardContent className="p-4 sm:p-6">
                      <div className="flex flex-col sm:flex-row items-start justify-between mb-4 gap-4">
                        <div className="flex items-start space-x-3 sm:space-x-4 flex-1">
                          <div className="p-2 sm:p-3 bg-dark-800 rounded-lg">
                            {getStatusIcon(rental.status)}
                          </div>
                          <div className="flex-1">
                            <div className="flex flex-col sm:flex-row sm:items-center gap-2 mb-2">
                              <h3 className="text-base sm:text-lg font-semibold text-white">
                                {rental.vehicle_name || `Vehicle #${rental.vehicle_id}`}
                              </h3>
                              <span className={`px-2 sm:px-3 py-1 rounded-full text-xs font-medium border ${getStatusColor(rental.status)} w-fit`}>
                                {rental.status || 'Pending'}
                              </span>
                            </div>
                            <p className="text-xs sm:text-sm text-gray-400">
                              Booking #{rental.id}
                            </p>
                          </div>
                        </div>
                        <div className="text-left sm:text-right w-full sm:w-auto">
                          <p className="text-xl sm:text-2xl font-bold text-white">
                            GH₵ {rental.total_amount?.toFixed(2) || '0.00'}
                          </p>
                          <p className="text-xs sm:text-sm text-gray-400">
                            {calculateDuration(rental.start_date, rental.end_date)} day(s)
                          </p>
                        </div>
                      </div>

                      {/* Rental Details */}
                      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-4">
                        {/* Pickup */}
                        <div className="p-4 bg-dark-800 rounded-lg">
                          <div className="flex items-center space-x-2 mb-2">
                            <FiCalendar className="h-4 w-4 text-green-500" />
                            <p className="text-xs font-medium text-gray-400">Pickup Date</p>
                          </div>
                          <p className="text-sm text-white font-medium">
                            {new Date(rental.start_date).toLocaleDateString('en-US', {
                              weekday: 'short',
                              year: 'numeric',
                              month: 'short',
                              day: 'numeric',
                            })}
                          </p>
                        </div>

                        {/* Return */}
                        <div className="p-4 bg-dark-800 rounded-lg">
                          <div className="flex items-center space-x-2 mb-2">
                            <FiCalendar className="h-4 w-4 text-red-500" />
                            <p className="text-xs font-medium text-gray-400">Return Date</p>
                          </div>
                          <p className="text-sm text-white font-medium">
                            {new Date(rental.end_date).toLocaleDateString('en-US', {
                              weekday: 'short',
                              year: 'numeric',
                              month: 'short',
                              day: 'numeric',
                            })}
                          </p>
                        </div>
                      </div>

                      {/* Pickup & Return Locations */}
                      {(rental.pickup_location || rental.return_location) && (
                        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-4">
                          {rental.pickup_location && (
                            <div className="p-3 bg-dark-800/50 rounded-lg border border-dark-700">
                              <div className="flex items-center space-x-2 mb-1">
                                <FiMapPin className="h-4 w-4 text-green-500" />
                                <p className="text-xs font-medium text-gray-400">Pickup Location</p>
                              </div>
                              <p className="text-sm text-gray-300">{rental.pickup_location}</p>
                            </div>
                          )}
                          {rental.return_location && (
                            <div className="p-3 bg-dark-800/50 rounded-lg border border-dark-700">
                              <div className="flex items-center space-x-2 mb-1">
                                <FiMapPin className="h-4 w-4 text-red-500" />
                                <p className="text-xs font-medium text-gray-400">Return Location</p>
                              </div>
                              <p className="text-sm text-gray-300">{rental.return_location}</p>
                            </div>
                          )}
                        </div>
                      )}

                      {/* Action Buttons */}
                      <div className="flex flex-col sm:flex-row items-stretch sm:items-center gap-3">
                        <Link to={`/dashboard/rentals/${rental.id}`} className="flex-1">
                          <Button variant="outline" size="sm" className="w-full">
                            <FiEye className="mr-2" />
                            <span className="hidden sm:inline">View Details</span>
                            <span className="sm:hidden">View</span>
                          </Button>
                        </Link>
                        {rental.status?.toLowerCase() === 'pending' && (
                          <Button
                            variant="danger"
                            size="sm"
                            onClick={() => handleCancelRental(rental.id)}
                            className="flex-1 w-full"
                          >
                            <FiXCircle className="mr-2" />
                            <span className="hidden sm:inline">Cancel Rental</span>
                            <span className="sm:hidden">Cancel</span>
                          </Button>
                        )}
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            )}
          </div>
        </main>
      </div>
    </div>
  );
};

export default MyRentals;
