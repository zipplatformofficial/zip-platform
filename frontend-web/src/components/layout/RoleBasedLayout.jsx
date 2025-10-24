import React from 'react';
import { Navigate } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth';
import AdminLayout from './AdminLayout';
import TechnicianLayout from './TechnicianLayout';
import VendorLayout from './VendorLayout';
import RentalManagerLayout from './RentalManagerLayout';
import CustomerLayout from './CustomerLayout';

/**
 * Role-based layout wrapper that renders the appropriate layout
 * based on the current user's role
 */
const RoleBasedLayout = () => {
  const { user, loading } = useAuth();

  if (loading) {
    return (
      <div className="min-h-screen bg-midnight-950 flex items-center justify-center">
        <div className="text-white">Loading...</div>
      </div>
    );
  }

  if (!user) {
    return <Navigate to="/login" replace />;
  }

  // Render layout based on user role
  switch (user.role) {
    case 'admin':
      return <AdminLayout />;
    case 'technician':
      return <TechnicianLayout />;
    case 'vendor':
      return <VendorLayout />;
    case 'rental_manager':
      return <RentalManagerLayout />;
    case 'customer':
    default:
      return <CustomerLayout />;
  }
};

export default RoleBasedLayout;
