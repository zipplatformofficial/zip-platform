import React from 'react';
import { Link, useLocation, Outlet } from 'react-router-dom';
import {
  FiHome,
  FiUsers,
  FiFileText,
  FiCalendar,
  FiTruck,
  FiShoppingBag,
  FiTool,
  FiPackage,
  FiSettings,
  FiBarChart2,
  FiBell,
  FiDollarSign,
  FiGrid,
} from 'react-icons/fi';
import { useAuth } from '../../hooks/useAuth';

const AdminLayout = () => {
  const location = useLocation();
  const { user } = useAuth();

  const adminNavigation = [
    {
      section: 'Overview',
      items: [
        { name: 'Dashboard', path: '/admin', icon: FiHome, exact: true },
        { name: 'Analytics', path: '/admin/analytics', icon: FiBarChart2 },
      ]
    },
    {
      section: 'User Management',
      items: [
        { name: 'Users', path: '/admin/users', icon: FiUsers },
        { name: 'Applications', path: '/admin/applications', icon: FiFileText, badge: 'new' },
      ]
    },
    {
      section: 'Service Providers',
      items: [
        { name: 'Technicians', path: '/admin/technicians', icon: FiTool },
        { name: 'Vendors', path: '/admin/vendors', icon: FiPackage },
        { name: 'Rental Managers', path: '/admin/rental-managers', icon: FiTruck },
      ]
    },
    {
      section: 'Operations',
      items: [
        { name: 'Maintenance Services', path: '/admin/maintenance-services', icon: FiCalendar },
        { name: 'Service Bookings', path: '/admin/service-bookings', icon: FiCalendar },
        { name: 'Rental Fleet', path: '/admin/rental-fleet', icon: FiTruck },
        { name: 'Rental Bookings', path: '/admin/rental-bookings', icon: FiTruck },
        { name: 'Store Products', path: '/admin/store-products', icon: FiGrid },
        { name: 'Store Orders', path: '/admin/orders', icon: FiShoppingBag },
      ]
    },
    {
      section: 'Financial',
      items: [
        { name: 'Payments', path: '/admin/payments', icon: FiDollarSign },
        { name: 'Transactions', path: '/admin/transactions', icon: FiDollarSign },
      ]
    },
    {
      section: 'System',
      items: [
        { name: 'Notifications', path: '/admin/notifications', icon: FiBell },
        { name: 'Settings', path: '/admin/settings', icon: FiSettings },
      ]
    },
  ];

  const isActive = (path, exact = false) => {
    if (exact) {
      return location.pathname === path;
    }
    return location.pathname.startsWith(path);
  };

  return (
    <div className="min-h-screen bg-midnight-950 pt-16">
      <div className="flex">
        {/* Admin Sidebar */}
        <aside className="fixed left-0 top-16 bottom-0 w-64 bg-dark-900 border-r border-dark-700 overflow-y-auto">
          <div className="p-4">
            {/* Admin Badge */}
            <div className="mb-6 p-4 bg-gradient-to-r from-red-500/10 to-orange-500/10 border border-red-500/20 rounded-lg">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-full bg-gradient-to-br from-red-500 to-orange-500 flex items-center justify-center">
                  <span className="text-white font-bold text-sm">
                    {user?.full_name?.charAt(0) || 'A'}
                  </span>
                </div>
                <div>
                  <p className="text-white font-semibold text-sm">{user?.full_name}</p>
                  <p className="text-red-500 text-xs font-medium uppercase">Administrator</p>
                </div>
              </div>
            </div>

            {/* Navigation Sections */}
            {adminNavigation.map((section, idx) => (
              <div key={idx} className="mb-6">
                <h3 className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2 px-3">
                  {section.section}
                </h3>
                <nav className="space-y-1">
                  {section.items.map((item) => {
                    const Icon = item.icon;
                    const active = isActive(item.path, item.exact);
                    return (
                      <Link
                        key={item.path}
                        to={item.path}
                        className={`flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all ${
                          active
                            ? 'bg-red-500 text-white shadow-lg shadow-red-500/20'
                            : 'text-gray-300 hover:bg-dark-800 hover:text-white'
                        }`}
                      >
                        <Icon className="h-4 w-4 flex-shrink-0" />
                        <span className="flex-1">{item.name}</span>
                        {item.badge && (
                          <span className="px-2 py-0.5 bg-red-500 text-white text-xs rounded-full">
                            {item.badge}
                          </span>
                        )}
                      </Link>
                    );
                  })}
                </nav>
              </div>
            ))}
          </div>
        </aside>

        {/* Main Content Area */}
        <main className="flex-1 ml-64">
          <Outlet />
        </main>
      </div>
    </div>
  );
};

export default AdminLayout;
