import React from 'react';
import { Link, useLocation, Outlet } from 'react-router-dom';
import {
  FiHome,
  FiUser,
  FiCalendar,
  FiTruck,
  FiPackage,
  FiSettings,
  FiHeart,
  FiCreditCard,
} from 'react-icons/fi';
import { useAuth } from '../../hooks/useAuth';

const CustomerLayout = () => {
  const location = useLocation();
  const { user } = useAuth();

  const menuItems = [
    { name: 'Dashboard', path: '/dashboard', icon: FiHome, exact: true },
    { name: 'Profile', path: '/dashboard/profile', icon: FiUser },
    { name: 'My Bookings', path: '/dashboard/bookings', icon: FiCalendar },
    { name: 'My Rentals', path: '/dashboard/rentals', icon: FiTruck },
    { name: 'My Orders', path: '/dashboard/orders', icon: FiPackage },
    { name: 'Wishlist', path: '/dashboard/wishlist', icon: FiHeart },
    { name: 'Payment Methods', path: '/dashboard/payment-methods', icon: FiCreditCard },
    { name: 'Settings', path: '/dashboard/settings', icon: FiSettings },
  ];

  const isActive = (path, exact = false) => {
    if (exact) {
      return location.pathname === path;
    }
    return location.pathname === path;
  };

  return (
    <div className="min-h-screen bg-midnight-950 pt-16">
      <div className="flex">
        <aside className="w-64 bg-dark-900 border-r border-dark-700 min-h-screen fixed left-0 top-16">
          <div className="p-4">
            {/* User Info */}
            <div className="mb-6 p-4 bg-dark-800 rounded-lg">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-full bg-gradient-to-br from-blue-500 to-purple-500 flex items-center justify-center">
                  <span className="text-white font-bold text-sm">
                    {user?.full_name?.charAt(0) || 'U'}
                  </span>
                </div>
                <div>
                  <p className="text-white font-semibold text-sm truncate">{user?.full_name}</p>
                  <p className="text-gray-400 text-xs">Customer</p>
                </div>
              </div>
            </div>

            {/* Navigation */}
            <nav className="space-y-1">
              {menuItems.map((item) => {
                const Icon = item.icon;
                const active = isActive(item.path, item.exact);

                return (
                  <Link
                    key={item.path}
                    to={item.path}
                    className={`flex items-center space-x-3 px-4 py-3 rounded-lg transition-all ${
                      active
                        ? 'bg-red-500/10 text-red-500 shadow-red-glow'
                        : 'text-gray-400 hover:bg-dark-800 hover:text-white'
                    }`}
                  >
                    <Icon className="h-5 w-5" />
                    <span className="font-medium">{item.name}</span>
                  </Link>
                );
              })}
            </nav>
          </div>
        </aside>

        <main className="flex-1 ml-64">
          <Outlet />
        </main>
      </div>
    </div>
  );
};

export default CustomerLayout;
