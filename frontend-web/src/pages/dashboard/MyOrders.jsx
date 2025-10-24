import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { FiPackage, FiClock, FiCheckCircle, FiXCircle, FiTruck, FiEye } from 'react-icons/fi';
import Sidebar from '../../components/layout/Sidebar';
import Card, { CardContent, CardTitle } from '../../components/ui/Card';
import Loading from '../../components/ui/Loading';
import Button from '../../components/ui/Button';
import { storeService } from '../../services/storeService';
import toast from 'react-hot-toast';

const MyOrders = () => {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('all'); // all, pending, confirmed, delivered, cancelled

  useEffect(() => {
    fetchOrders();
  }, []);

  const fetchOrders = async () => {
    try {
      setLoading(true);
      const data = await storeService.getMyOrders();
      setOrders(data);
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to load orders');
    } finally {
      setLoading(false);
    }
  };

  const handleCancelOrder = async (orderId) => {
    if (!window.confirm('Are you sure you want to cancel this order?')) return;

    try {
      await storeService.cancelOrder(orderId);
      toast.success('Order cancelled successfully');
      fetchOrders();
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to cancel order');
    }
  };

  const getStatusIcon = (status) => {
    switch (status?.toLowerCase()) {
      case 'pending':
        return <FiClock className="h-5 w-5 text-yellow-500" />;
      case 'confirmed':
        return <FiCheckCircle className="h-5 w-5 text-blue-500" />;
      case 'processing':
        return <FiTruck className="h-5 w-5 text-purple-500" />;
      case 'delivered':
        return <FiCheckCircle className="h-5 w-5 text-green-500" />;
      case 'cancelled':
        return <FiXCircle className="h-5 w-5 text-red-500" />;
      default:
        return <FiPackage className="h-5 w-5 text-gray-500" />;
    }
  };

  const getStatusColor = (status) => {
    switch (status?.toLowerCase()) {
      case 'pending':
        return 'bg-yellow-500/10 text-yellow-500 border-yellow-500/20';
      case 'confirmed':
        return 'bg-blue-500/10 text-blue-500 border-blue-500/20';
      case 'processing':
        return 'bg-purple-500/10 text-purple-500 border-purple-500/20';
      case 'delivered':
        return 'bg-green-500/10 text-green-500 border-green-500/20';
      case 'cancelled':
        return 'bg-red-500/10 text-red-500 border-red-500/20';
      default:
        return 'bg-gray-500/10 text-gray-500 border-gray-500/20';
    }
  };

  const filteredOrders = orders.filter(order => {
    if (filter === 'all') return true;
    return order.status?.toLowerCase() === filter;
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
              <h1 className="text-2xl sm:text-3xl font-bold text-white mb-2">My Orders</h1>
              <p className="text-sm sm:text-base text-gray-400">Track and manage your auto parts orders</p>
            </div>

            {/* Filter Tabs */}
            <div className="mb-4 sm:mb-6 flex flex-wrap gap-2">
              {['all', 'pending', 'confirmed', 'processing', 'delivered', 'cancelled'].map((status) => (
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
                  {status === 'all' && orders.length > 0 && (
                    <span className="ml-2 px-2 py-0.5 bg-dark-700 rounded-full text-xs">
                      {orders.length}
                    </span>
                  )}
                </button>
              ))}
            </div>

            {/* Orders List */}
            {filteredOrders.length === 0 ? (
              <Card>
                <CardContent className="p-12 text-center">
                  <FiPackage className="h-16 w-16 text-gray-600 mx-auto mb-4" />
                  <h3 className="text-xl font-semibold text-white mb-2">No orders found</h3>
                  <p className="text-gray-400 mb-6">
                    {filter === 'all'
                      ? "You haven't placed any orders yet"
                      : `No ${filter} orders found`
                    }
                  </p>
                  <Link to="/store">
                    <Button variant="primary">Browse Auto Parts Store</Button>
                  </Link>
                </CardContent>
              </Card>
            ) : (
              <div className="space-y-4">
                {filteredOrders.map((order) => (
                  <Card key={order.id} hover>
                    <CardContent className="p-4 sm:p-6">
                      <div className="flex flex-col sm:flex-row items-start justify-between mb-4 gap-4">
                        <div className="flex items-start space-x-3 sm:space-x-4 flex-1">
                          <div className="p-2 sm:p-3 bg-dark-800 rounded-lg">
                            {getStatusIcon(order.status)}
                          </div>
                          <div className="flex-1">
                            <div className="flex flex-col sm:flex-row sm:items-center gap-2 mb-2">
                              <h3 className="text-base sm:text-lg font-semibold text-white">
                                Order #{order.id}
                              </h3>
                              <span className={`px-2 sm:px-3 py-1 rounded-full text-xs font-medium border ${getStatusColor(order.status)} w-fit`}>
                                {order.status || 'Pending'}
                              </span>
                            </div>
                            <p className="text-xs sm:text-sm text-gray-400">
                              Placed on {new Date(order.created_at).toLocaleDateString('en-US', {
                                year: 'numeric',
                                month: 'long',
                                day: 'numeric',
                              })}
                            </p>
                          </div>
                        </div>
                        <div className="text-left sm:text-right w-full sm:w-auto">
                          <p className="text-xl sm:text-2xl font-bold text-white">
                            GH₵ {order.total_amount?.toFixed(2) || '0.00'}
                          </p>
                          <p className="text-xs sm:text-sm text-gray-400">
                            {order.items?.length || 0} item(s)
                          </p>
                        </div>
                      </div>

                      {/* Order Items Summary */}
                      {order.items && order.items.length > 0 && (
                        <div className="mb-4 p-4 bg-dark-800 rounded-lg">
                          <h4 className="text-sm font-medium text-gray-400 mb-3">Order Items:</h4>
                          <div className="space-y-2">
                            {order.items.slice(0, 3).map((item, index) => (
                              <div key={index} className="flex justify-between text-sm">
                                <span className="text-gray-300">
                                  {item.product_name || `Product #${item.product_id}`} × {item.quantity}
                                </span>
                                <span className="text-white font-medium">
                                  GH₵ {(item.unit_price * item.quantity).toFixed(2)}
                                </span>
                              </div>
                            ))}
                            {order.items.length > 3 && (
                              <p className="text-xs text-gray-500 pt-2">
                                +{order.items.length - 3} more item(s)
                              </p>
                            )}
                          </div>
                        </div>
                      )}

                      {/* Delivery Info */}
                      {order.delivery_address && (
                        <div className="mb-4 p-3 bg-dark-800/50 rounded-lg border border-dark-700">
                          <p className="text-xs font-medium text-gray-400 mb-1">Delivery Address:</p>
                          <p className="text-sm text-gray-300">{order.delivery_address}</p>
                        </div>
                      )}

                      {/* Action Buttons */}
                      <div className="flex flex-col sm:flex-row items-stretch sm:items-center gap-3">
                        <Link to={`/dashboard/orders/${order.id}`} className="flex-1">
                          <Button variant="outline" size="sm" className="w-full">
                            <FiEye className="mr-2" />
                            <span className="hidden sm:inline">View Details</span>
                            <span className="sm:hidden">View</span>
                          </Button>
                        </Link>
                        {order.status?.toLowerCase() === 'pending' && (
                          <Button
                            variant="danger"
                            size="sm"
                            onClick={() => handleCancelOrder(order.id)}
                            className="flex-1 w-full"
                          >
                            <FiXCircle className="mr-2" />
                            <span className="hidden sm:inline">Cancel Order</span>
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

export default MyOrders;
