import React, { useState } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { FiMail, FiLock, FiArrowRight } from 'react-icons/fi';
import { useAuth } from '../hooks/useAuth';
import Button from '../components/ui/Button';
import Input from '../components/ui/Input';
import Card from '../components/ui/Card';
import zipLogo from '../assets/zip-logo.jpg';

const Login = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { login } = useAuth();

  const [formData, setFormData] = useState({
    email: '',
    password: '',
  });
  const [errors, setErrors] = useState({});
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: '' }));
    }
  };

  const validateForm = () => {
    const newErrors = {};
    if (!formData.email) {
      newErrors.email = 'Email is required';
    }
    if (!formData.password) {
      newErrors.password = 'Password is required';
    }
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!validateForm()) return;

    setLoading(true);
    try {
      const data = await login(formData);

      // Get user data from authService to check role
      const response = await fetch('http://localhost:8000/api/v1/auth/me', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        }
      });
      const userData = await response.json();

      // Redirect based on role
      const from = location.state?.from?.pathname;
      if (from) {
        // If there's a specific redirect, use it
        navigate(from, { replace: true });
      } else if (userData.role === 'admin') {
        // Admins go to admin dashboard
        navigate('/admin', { replace: true });
      } else {
        // Other users go to customer dashboard
        navigate('/dashboard', { replace: true });
      }
    } catch (error) {
      console.error('Login error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center px-4 py-12 bg-gradient-to-br from-gray-900 via-gray-800 to-black relative overflow-hidden">
      {/* Background Pattern */}
      <div className="absolute inset-0 opacity-5">
        <div className="absolute inset-0" style={{
          backgroundImage: 'radial-gradient(circle at 2px 2px, white 1px, transparent 0)',
          backgroundSize: '40px 40px'
        }}></div>
      </div>

      {/* Red Gradient Overlay */}
      <div className="absolute inset-0 bg-gradient-to-r from-red-600/10 via-transparent to-red-600/10"></div>

      <div className="max-w-md w-full relative z-10">
        <div className="text-center mb-8 animate-fade-in-up">
          <Link to="/" className="inline-block mb-6 group">
            <div className="flex items-center justify-center space-x-3">
              <div className="relative">
                <div className="absolute inset-0 bg-red-500/30 blur-xl rounded-full animate-pulse-slow"></div>
                <img
                  src={zipLogo}
                  alt="ZIP Platform"
                  className="relative w-16 h-16 rounded-2xl shadow-2xl shadow-red-500/50 group-hover:scale-110 transition-transform duration-300 border-2 border-red-500/30"
                />
              </div>
              <div>
                <span className="text-white font-bold text-3xl block">ZIP Platform</span>
                <span className="text-red-400 text-xs uppercase tracking-wider">Auto Services</span>
              </div>
            </div>
          </Link>
          <h2 className="text-4xl font-bold text-white mb-3 mt-8">
            Welcome Back! 👋
          </h2>
          <p className="text-gray-400 text-lg">
            Sign in to continue your automotive journey
          </p>

          {/* Feature Highlights */}
          <div className="mt-6 flex flex-wrap justify-center gap-3">
            <div className="bg-white/10 backdrop-blur-sm border border-white/20 rounded-full px-4 py-2 text-sm text-white font-medium hover:bg-white/20 transition-all">
              🚗 Rent Vehicles
            </div>
            <div className="bg-white/10 backdrop-blur-sm border border-white/20 rounded-full px-4 py-2 text-sm text-white font-medium hover:bg-white/20 transition-all">
              🔧 Book Services
            </div>
            <div className="bg-white/10 backdrop-blur-sm border border-white/20 rounded-full px-4 py-2 text-sm text-white font-medium hover:bg-white/20 transition-all">
              🛒 Shop Parts
            </div>
          </div>
        </div>

        <Card className="animate-fade-in-up" style={{ animationDelay: '0.1s' }}>
          <form onSubmit={handleSubmit} className="space-y-6 p-8">
            <Input
              label="Email Address"
              name="email"
              type="email"
              value={formData.email}
              onChange={handleChange}
              error={errors.email}
              icon={FiMail}
              placeholder="you@example.com"
              autoComplete="email"
            />

            <Input
              label="Password"
              name="password"
              type="password"
              value={formData.password}
              onChange={handleChange}
              error={errors.password}
              icon={FiLock}
              placeholder="••••••••"
              autoComplete="current-password"
            />

            <div className="flex items-center justify-between text-sm">
              <label className="flex items-center text-gray-400">
                <input
                  type="checkbox"
                  className="mr-2 rounded border-dark-700 bg-dark-800 text-red-500 focus:ring-red-500 focus:ring-offset-midnight-950"
                />
                Remember me
              </label>
              <Link to="/forgot-password" className="text-red-500 hover:text-red-400">
                Forgot password?
              </Link>
            </div>

            <div className="relative overflow-hidden rounded-xl bg-gradient-to-r from-red-500 to-red-600 p-[2px] hover:from-red-600 hover:to-orange-500 transition-all duration-300 shadow-lg hover:shadow-2xl">
              <button
                type="submit"
                disabled={loading}
                className="relative w-full px-6 py-4 rounded-xl font-bold text-lg transition-all bg-white text-red-600 hover:bg-transparent hover:text-white disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
              >
                {loading ? (
                  <>
                    <div className="w-5 h-5 border-2 border-current border-t-transparent rounded-full animate-spin"></div>
                    Signing In...
                  </>
                ) : (
                  <>
                    Sign In
                    <FiArrowRight className="group-hover:translate-x-1 transition-transform" />
                  </>
                )}
              </button>
            </div>

            {/* Trust Indicators */}
            <div className="mt-8 pt-6 border-t border-gray-700">
              <div className="grid grid-cols-3 gap-4 text-center">
                <div className="group hover:scale-105 transition-transform">
                  <div className="text-2xl mb-2">🔒</div>
                  <p className="text-xs text-gray-400 font-medium">Secure Login</p>
                </div>
                <div className="group hover:scale-105 transition-transform">
                  <div className="text-2xl mb-2">⚡</div>
                  <p className="text-xs text-gray-400 font-medium">Fast Access</p>
                </div>
                <div className="group hover:scale-105 transition-transform">
                  <div className="text-2xl mb-2">✓</div>
                  <p className="text-xs text-gray-400 font-medium">5K+ Users</p>
                </div>
              </div>
            </div>
          </form>

          <div className="mt-8 pt-6 border-t border-gray-700 text-center">
            <p className="text-gray-400">
              Don't have an account?{' '}
              <Link to="/register" className="text-red-500 hover:text-red-400 font-bold hover:underline transition-all">
                Create Account
              </Link>
            </p>
          </div>
        </Card>
      </div>
    </div>
  );
};

export default Login;
