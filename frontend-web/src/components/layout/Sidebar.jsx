import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import {
  FiHome,
  FiUser,
  FiTool,
  FiTruck,
  FiShoppingBag,
  FiSettings,
  FiCalendar,
  FiPackage
} from 'react-icons/fi';

const Sidebar = () => {
  const location = useLocation();

  const menuItems = [
    { name: 'Dashboard', path: '/dashboard', icon: FiHome },
    { name: 'Profile', path: '/dashboard/profile', icon: FiUser },
    { name: 'My Bookings', path: '/dashboard/bookings', icon: FiCalendar },
    { name: 'My Rentals', path: '/dashboard/rentals', icon: FiTruck },
    { name: 'My Orders', path: '/dashboard/orders', icon: FiPackage },
    { name: 'Settings', path: '/dashboard/settings', icon: FiSettings },
  ];

  const isActive = (path) => location.pathname === path;

  return (
    <aside className="w-64 bg-dark-900 border-r border-dark-700 min-h-screen fixed left-0 top-16">
      <nav className="p-4 space-y-2">
        {menuItems.map((item) => {
          const Icon = item.icon;
          const active = isActive(item.path);

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
    </aside>
  );
};

export default Sidebar;
