import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import { AuthProvider } from './context/AuthContext';
import { CartProvider } from './context/CartContext';
import { LanguageProvider } from './context/LanguageContext';
import ProtectedRoute from './components/auth/ProtectedRoute';
import Navbar from './components/layout/Navbar';
import Footer from './components/layout/Footer';

// Public Pages
import HomeEnhanced from './pages/HomeEnhanced';
import Login from './pages/Login';
import Register from './pages/Register';

// Maintenance
import Services from './pages/maintenance/Services';
import MyBookings from './pages/maintenance/MyBookings';

// Rentals
import VehiclesEnhanced from './pages/rentals/VehiclesEnhanced';

// Store
import Products from './pages/store/Products';
import Cart from './pages/store/Cart';

// Dashboard
import Dashboard from './pages/Dashboard';
import Profile from './pages/Profile';
import MyOrders from './pages/dashboard/MyOrders';
import MyRentals from './pages/dashboard/MyRentals';
import Settings from './pages/dashboard/Settings';
import PaymentMethods from './pages/dashboard/PaymentMethods';
import Wishlist from './pages/dashboard/Wishlist';

// Admin
import AdminLayout from './components/layout/AdminLayout';
import AdminDashboard from './pages/admin/AdminDashboard';
import Analytics from './pages/admin/Analytics';
import Users from './pages/admin/Users';
import Applications from './pages/admin/Applications';
import ApplicationReview from './pages/admin/ApplicationReview';
import Technicians from './pages/admin/Technicians';
import Vendors from './pages/admin/Vendors';
import RentalManagers from './pages/admin/RentalManagers';
import MaintenanceServices from './pages/admin/MaintenanceServices';
import ServiceBookings from './pages/admin/ServiceBookings';
import RentalFleet from './pages/admin/RentalFleet';
import RentalBookings from './pages/admin/RentalBookings';
import StoreProducts from './pages/admin/StoreProducts';
import Orders from './pages/admin/Orders';
import Payments from './pages/admin/Payments';
import Transactions from './pages/admin/Transactions';
import Notifications from './pages/admin/Notifications';
import AdminSettings from './pages/admin/AdminSettings';

// Customer Layout
import CustomerLayout from './components/layout/CustomerLayout';

import './index.css';

function App() {
  return (
    <Router>
      <LanguageProvider>
        <AuthProvider>
          <CartProvider>
            <div className="min-h-screen bg-midnight-950 flex flex-col">
              <Toaster
                position="top-right"
                toastOptions={{
                  duration: 3000,
                  style: {
                    background: '#1E293B',
                    color: '#fff',
                    border: '1px solid #334155',
                  },
                  success: {
                    iconTheme: {
                      primary: '#ED1C24',
                      secondary: '#fff',
                    },
                  },
                }}
              />
              <Navbar />
              <main className="flex-grow">
                <Routes>
                {/* Public Routes */}
                <Route path="/" element={<HomeEnhanced />} />
                <Route path="/login" element={<Login />} />
                <Route path="/register" element={<Register />} />

                {/* Maintenance Routes */}
                <Route path="/maintenance" element={<Services />} />
                <Route path="/maintenance/bookings" element={
                  <ProtectedRoute><MyBookings /></ProtectedRoute>
                } />

                {/* Rental Routes */}
                <Route path="/rentals" element={<VehiclesEnhanced />} />

                {/* Store Routes */}
                <Route path="/store" element={<Products />} />
                <Route path="/cart" element={<Cart />} />

                {/* Dashboard Routes - Customer Layout */}
                <Route path="/dashboard" element={<ProtectedRoute><CustomerLayout /></ProtectedRoute>}>
                  <Route index element={<Dashboard />} />
                  <Route path="profile" element={<Profile />} />
                  <Route path="bookings" element={<MyBookings />} />
                  <Route path="orders" element={<MyOrders />} />
                  <Route path="rentals" element={<MyRentals />} />
                  <Route path="wishlist" element={<Wishlist />} />
                  <Route path="payment-methods" element={<PaymentMethods />} />
                  <Route path="settings" element={<Settings />} />
                </Route>

                {/* Admin Routes - Admin Layout */}
                <Route path="/admin" element={<ProtectedRoute><AdminLayout /></ProtectedRoute>}>
                  <Route index element={<AdminDashboard />} />
                  <Route path="analytics" element={<Analytics />} />
                  <Route path="users" element={<Users />} />
                  <Route path="applications" element={<Applications />} />
                  <Route path="applications/:id" element={<ApplicationReview />} />
                  <Route path="technicians" element={<Technicians />} />
                  <Route path="vendors" element={<Vendors />} />
                  <Route path="rental-managers" element={<RentalManagers />} />
                  <Route path="maintenance-services" element={<MaintenanceServices />} />
                  <Route path="service-bookings" element={<ServiceBookings />} />
                  <Route path="rental-fleet" element={<RentalFleet />} />
                  <Route path="rental-bookings" element={<RentalBookings />} />
                  <Route path="store-products" element={<StoreProducts />} />
                  <Route path="orders" element={<Orders />} />
                  <Route path="payments" element={<Payments />} />
                  <Route path="transactions" element={<Transactions />} />
                  <Route path="notifications" element={<Notifications />} />
                  <Route path="settings" element={<AdminSettings />} />
                </Route>
              </Routes>
            </main>
              <Footer />
            </div>
          </CartProvider>
        </AuthProvider>
      </LanguageProvider>
    </Router>
  );
}

export default App;
