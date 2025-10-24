import React from 'react';
import { Link, useLocation, Outlet } from 'react-router-dom';
import {
  FiHome,
  FiCalendar,
  FiTool,
  FiDollarSign,
  FiSettings,
  FiClock,
  FiCheckCircle,
  FiUser,
} from 'react-icons/fi';
import { useAuth } from '../../hooks/useAuth';

const TechnicianLayout = () => {
  const location = useLocation();
  const { user } = useAuth();

  const menuItems = [
    { name: 'Dashboard', path: '/technician', icon: FiHome, exact: true },
    { name: 'Active Jobs', path: '/technician/jobs/active', icon: FiClock },
    { name: 'Job History', path: '/technician/jobs/history', icon: FiCheckCircle },
    { name: 'Schedule', path: '/technician/schedule', icon: FiCalendar },
    { name: 'Services', path: '/technician/services', icon: FiTool },
    { name: 'Earnings', path: '/technician/earnings', icon: FiDollarSign },
    { name: 'Profile', path: '/technician/profile', icon: FiUser },
    { name: 'Settings', path: '/technician/settings', icon: FiSettings },
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
            <div className="mb-6 p-4 bg-gradient-to-r from-yellow-500/10 to-orange-500/10 border border-yellow-500/20 rounded-lg">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-full bg-gradient-to-br from-yellow-500 to-orange-500 flex items-center justify-center">
                  <FiTool className="text-white h-5 w-5" />
                </div>
                <div>
                  <p className="text-white font-semibold text-sm">{user?.full_name}</p>
                  <p className="text-yellow-500 text-xs font-medium">Technician</p>
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
                        ? 'bg-yellow-500/10 text-yellow-500'
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

export default TechnicianLayout;
