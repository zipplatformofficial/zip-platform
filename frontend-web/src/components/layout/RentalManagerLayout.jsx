import React from 'react';
import { Link, useLocation, Outlet } from 'react-router-dom';
import {
  FiHome,
  FiTruck,
  FiCalendar,
  FiDollarSign,
  FiSettings,
  FiBarChart2,
  FiPlus,
  FiUser,
  FiTool,
} from 'react-icons/fi';
import { useAuth } from '../../hooks/useAuth';

const RentalManagerLayout = () => {
  const location = useLocation();
  const { user } = useAuth();

  const menuItems = [
    { name: 'Dashboard', path: '/rental-manager', icon: FiHome, exact: true },
    { name: 'Fleet', path: '/rental-manager/fleet', icon: FiTruck },
    { name: 'Add Vehicle', path: '/rental-manager/fleet/new', icon: FiPlus },
    { name: 'Bookings', path: '/rental-manager/bookings', icon: FiCalendar },
    { name: 'Maintenance', path: '/rental-manager/maintenance', icon: FiTool },
    { name: 'Analytics', path: '/rental-manager/analytics', icon: FiBarChart2 },
    { name: 'Revenue', path: '/rental-manager/revenue', icon: FiDollarSign },
    { name: 'Profile', path: '/rental-manager/profile', icon: FiUser },
    { name: 'Settings', path: '/rental-manager/settings', icon: FiSettings },
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
            <div className="mb-6 p-4 bg-gradient-to-r from-purple-500/10 to-indigo-500/10 border border-purple-500/20 rounded-lg">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-full bg-gradient-to-br from-purple-500 to-indigo-500 flex items-center justify-center">
                  <FiTruck className="text-white h-5 w-5" />
                </div>
                <div>
                  <p className="text-white font-semibold text-sm">{user?.full_name}</p>
                  <p className="text-purple-500 text-xs font-medium">Rental Manager</p>
                </div>
              </div>
            </div>

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
                        ? 'bg-purple-500/10 text-purple-500'
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

export default RentalManagerLayout;
