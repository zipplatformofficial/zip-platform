import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { FiCalendar, FiTruck, FiPackage, FiDollarSign } from 'react-icons/fi';
import { useAuth } from '../hooks/useAuth';
import Card, { CardContent, CardTitle } from '../components/ui/Card';
import Loading from '../components/ui/Loading';
import { authService } from '../services/authService';
import toast from 'react-hot-toast';

const Dashboard = () => {
  const { user } = useAuth();
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchUserStats();
  }, []);

  const fetchUserStats = async () => {
    try {
      setLoading(true);
      const response = await authService.getCurrentUser();
      // You can fetch additional stats from a dedicated endpoint if available
      setStats(response);
    } catch (error) {
      toast.error('Failed to load dashboard stats');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <Loading fullScreen />;
  }

  const statCards = [
    {
      title: 'Service Bookings',
      value: '0',
      icon: FiCalendar,
      link: '/dashboard/bookings',
      color: 'from-blue-500 to-blue-600',
    },
    {
      title: 'Active Rentals',
      value: '0',
      icon: FiTruck,
      link: '/dashboard/rentals',
      color: 'from-green-500 to-green-600',
    },
    {
      title: 'Store Orders',
      value: '0',
      icon: FiPackage,
      link: '/dashboard/orders',
      color: 'from-purple-500 to-purple-600',
    },
    {
      title: 'Loyalty Points',
      value: stats?.loyalty_points || '0',
      icon: FiDollarSign,
      link: '#',
      color: 'from-red-500 to-red-600',
    },
  ];

  return (
    <div className="p-8">
      <div className="max-w-7xl mx-auto">
            <div className="mb-8">
              <h1 className="text-3xl font-bold text-white mb-2">
                Welcome back, {user?.full_name}!
              </h1>
              <p className="text-gray-400">Here's what's happening with your account</p>
            </div>

            <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
              {statCards.map((stat, index) => {
                const Icon = stat.icon;
                return (
                  <Link key={index} to={stat.link}>
                    <Card hover className="h-full">
                      <CardContent className="p-6">
                        <div className="flex items-center justify-between mb-4">
                          <div className={`w-12 h-12 rounded-lg bg-gradient-to-br ${stat.color} flex items-center justify-center shadow-lg`}>
                            <Icon className="h-6 w-6 text-white" />
                          </div>
                        </div>
                        <CardTitle className="text-3xl mb-1">{stat.value}</CardTitle>
                        <p className="text-gray-400 text-sm">{stat.title}</p>
                      </CardContent>
                    </Card>
                  </Link>
                );
              })}
            </div>

            <div className="grid lg:grid-cols-2 gap-6">
              <Card>
                <CardContent className="p-6">
                  <CardTitle className="mb-4">Recent Activity</CardTitle>
                  <div className="text-center py-8 text-gray-400">
                    No recent activity
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardContent className="p-6">
                  <CardTitle className="mb-4">Quick Actions</CardTitle>
                  <div className="space-y-3">
                    <Link to="/maintenance" className="block p-3 bg-dark-800 hover:bg-dark-700 rounded-lg transition-colors">
                      <p className="text-white font-medium">Book a Service</p>
                      <p className="text-gray-400 text-sm">Schedule car maintenance</p>
                    </Link>
                    <Link to="/rentals" className="block p-3 bg-dark-800 hover:bg-dark-700 rounded-lg transition-colors">
                      <p className="text-white font-medium">Rent a Vehicle</p>
                      <p className="text-gray-400 text-sm">Browse available vehicles</p>
                    </Link>
                    <Link to="/store" className="block p-3 bg-dark-800 hover:bg-dark-700 rounded-lg transition-colors">
                      <p className="text-white font-medium">Shop Parts</p>
                      <p className="text-gray-400 text-sm">Browse auto parts store</p>
                    </Link>
                  </div>
                </CardContent>
              </Card>
            </div>
      </div>
    </div>
  );
};

export default Dashboard;
