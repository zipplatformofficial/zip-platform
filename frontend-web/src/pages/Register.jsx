import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { FiMail, FiLock, FiUser, FiPhone, FiTag, FiArrowRight } from "react-icons/fi"; // Added FiTag for user type
import { useAuth } from "../hooks/useAuth";
import Button from "../components/ui/Button";
import Input from "../components/ui/Input";
import Card from "../components/ui/Card";
import zipLogo from '../assets/zip-logo.jpg';

const Register = () => {
  const navigate = useNavigate();
  const { register } = useAuth();

  const [formData, setFormData] = useState({
    full_name: "",
    email: "",
    phone: "",
    password: "",
    confirmPassword: "",
    // --- New State for required API fields ---
    user_type: "individual", // Default to individual
    // Location is required, so we'll hardcode a default location for testing
    // You should integrate geolocation or address lookup later
    location: {
      lat: 5.6037,
      lng: -0.187,
      address: "Accra, Ghana",
    },
  });
  const [errors, setErrors] = useState({});
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
    if (errors[name]) {
      setErrors((prev) => ({ ...prev, [name]: "" }));
    }
  };

  const validateForm = () => {
    const newErrors = {};
    const { full_name, email, phone, password, confirmPassword } = formData;

    // Check for required fields
    if (!full_name) newErrors.full_name = "Full name is required";
    if (!email) newErrors.email = "Email is required";
    if (!phone) newErrors.phone = "Phone number is required";
    if (!password) newErrors.password = "Password is required";

    // Email format validation
    if (email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      newErrors.email = "Invalid email format";
    }

    // Phone validation (Basic check for digits - improve later)
    if (phone && !/^(\+?233|0)[0-9]{9}$/.test(phone.trim())) {
      newErrors.phone = "Invalid Ghana phone number format";
    }

    // --- Updated Password Validation to meet API requirements (min 8, 1 uppercase, 1 digit) ---
    const passwordRegex = /^(?=.*[A-Z])(?=.*\d).{8,}$/;
    if (password) {
      if (password.length < 8) {
        newErrors.password = "Password must be at least 8 characters.";
      } else if (!passwordRegex.test(password)) {
        newErrors.password =
          "Password must contain 1 uppercase letter and 1 digit.";
      }
    }

    // Confirm password check
    if (password !== confirmPassword) {
      newErrors.confirmPassword = "Passwords do not match";
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!validateForm()) return;

    setLoading(true);
    try {
      // 1. Destructure to remove confirmPassword
      const { confirmPassword, ...dataToSend } = formData;

      // 2. The dataToSend now matches the API's required shape:
      //    { full_name, email, phone, password, user_type, location }
      //    Note: The 'phone' field value MUST now be a valid phone number.

      await register(dataToSend);
      navigate("/dashboard");
    } catch (error) {
      // Improved error logging to catch the detailed 422 message from the backend
      const errorMessage = error.response?.data?.detail
        ? JSON.stringify(error.response.data.detail)
        : error.message;

      console.error("Registration error:", errorMessage);

      // Optionally display a generic or detailed error message to the user
      setErrors({ api: errorMessage });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex bg-midnight-950 relative overflow-hidden pt-20 lg:pt-0" style={{ zoom: window.innerWidth >= 1024 ? '0.8' : '1' }}>
      {/* Background Pattern */}
      <div className="absolute inset-0 opacity-5">
        <div className="absolute inset-0" style={{
          backgroundImage: 'radial-gradient(circle at 2px 2px, white 1px, transparent 0)',
          backgroundSize: '40px 40px'
        }}></div>
      </div>

      {/* Left Column - Branding & Image */}
      <div className="hidden lg:flex lg:w-1/2 relative bg-gradient-to-br from-orange-600 via-red-500 to-red-600 p-12 items-center justify-center overflow-hidden">
        {/* Animated Background Elements */}
        <div className="absolute inset-0 opacity-20">
          <div className="absolute top-20 left-20 w-72 h-72 bg-yellow-300 rounded-full blur-3xl animate-pulse"></div>
          <div className="absolute bottom-20 right-20 w-96 h-96 bg-white rounded-full blur-3xl animate-pulse" style={{ animationDelay: '1s' }}></div>
        </div>

        <div className="relative z-10 max-w-lg text-white">
          <Link to="/" className="inline-block mb-8 group">
            <div className="flex items-center space-x-4">
              <img
                src={zipLogo}
                alt="ZIP Platform"
                className="w-20 h-20 rounded-3xl shadow-2xl group-hover:scale-110 transition-transform duration-300 border-4 border-white/30"
              />
              <div>
                <span className="text-white font-black text-5xl block">ZIP</span>
                <span className="text-white/90 text-sm uppercase tracking-widest">Platform</span>
              </div>
            </div>
          </Link>

          <h1 className="text-5xl md:text-6xl font-black mb-6 leading-tight">
            Join 5,000+ Happy Customers
          </h1>

          <p className="text-xl text-white/90 mb-12 leading-relaxed">
            Create your account today and unlock access to premium automotive services across Ghana.
          </p>

          {/* Benefits List */}
          <div className="space-y-4">
            <div className="flex items-start space-x-4">
              <div className="text-4xl">✓</div>
              <div>
                <h3 className="font-bold text-lg mb-1">Free to Join</h3>
                <p className="text-white/80 text-sm">No hidden fees or charges to create your account</p>
              </div>
            </div>
            <div className="flex items-start space-x-4">
              <div className="text-4xl">🔒</div>
              <div>
                <h3 className="font-bold text-lg mb-1">Secure & Private</h3>
                <p className="text-white/80 text-sm">Your data is protected with industry-standard encryption</p>
              </div>
            </div>
            <div className="flex items-start space-x-4">
              <div className="text-4xl">⚡</div>
              <div>
                <h3 className="font-bold text-lg mb-1">Instant Access</h3>
                <p className="text-white/80 text-sm">Start booking services immediately after signup</p>
              </div>
            </div>
            <div className="flex items-start space-x-4">
              <div className="text-4xl">🎁</div>
              <div>
                <h3 className="font-bold text-lg mb-1">Welcome Bonus</h3>
                <p className="text-white/80 text-sm">Get special discounts on your first booking</p>
              </div>
            </div>
          </div>

          {/* Trust Badge */}
          <div className="mt-12 bg-white/10 backdrop-blur-sm rounded-2xl p-6 border border-white/20">
            <div className="flex items-center gap-4">
              <div className="text-5xl">⭐</div>
              <div>
                <div className="text-2xl font-black mb-1">4.9/5</div>
                <div className="text-sm text-white/80">Average rating from 2,500+ reviews</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Right Column - Registration Form */}
      <div className="flex-1 flex items-center justify-center p-8 lg:p-12 relative z-10">
        <div className="w-full max-w-md">
          {/* Mobile Logo */}
          <div className="lg:hidden text-center mb-8">
            <Link to="/" className="inline-block mb-6 group">
              <div className="flex items-center justify-center space-x-3">
                <img
                  src={zipLogo}
                  alt="ZIP Platform"
                  className="w-16 h-16 rounded-2xl shadow-2xl group-hover:scale-110 transition-transform duration-300"
                />
                <div>
                  <span className="text-white font-bold text-3xl block">ZIP Platform</span>
                  <span className="text-red-400 text-xs uppercase tracking-wider">Auto Services</span>
                </div>
              </div>
            </Link>
          </div>

          <div className="mb-8">
            <h2 className="text-4xl font-bold text-white mb-3">
              Create Account ✨
            </h2>
            <p className="text-gray-400 text-lg">
              Join thousands of satisfied customers today!
            </p>
          </div>

          <Card className="border-dark-700/50">
            <form onSubmit={handleSubmit} className="space-y-5 p-8">
            {/* API Error Display */}
            {errors.api && (
              <div className="p-3 bg-red-800 bg-opacity-30 text-red-300 rounded text-sm">
                Registration failed: {errors.api}
              </div>
            )}

            {/* Existing Inputs */}
            <Input
              label="Full Name"
              name="full_name"
              type="text"
              value={formData.full_name}
              onChange={handleChange}
              error={errors.full_name}
              icon={FiUser}
              placeholder="John Doe"
              autoComplete="name"
            />

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
              label="Phone Number (e.g. 0241234567)"
              name="phone"
              type="tel"
              value={formData.phone}
              onChange={handleChange}
              error={errors.phone}
              icon={FiPhone}
              placeholder="024 XXX XXXX"
              autoComplete="tel"
            />

            {/* --- NEW REQUIRED INPUT: USER TYPE --- */}
            <div className="space-y-1">
              <label
                htmlFor="user_type"
                className="block text-sm font-medium text-gray-300"
              >
                User Type
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <FiTag className="h-5 w-5 text-gray-500" />
                </div>
                <select
                  id="user_type"
                  name="user_type"
                  value={formData.user_type}
                  onChange={handleChange}
                  className="w-full pl-10 pr-3 py-2 border rounded-lg bg-dark-800 border-dark-700 text-white focus:ring-red-500 focus:border-red-500"
                >
                  <option value="individual">Individual (Customer)</option>
                  <option value="corporate">Corporate</option>
                  <option value="ride_hailing_driver">
                    Ride-Hailing Driver
                  </option>
                  {/* Optionally add technician/vendor if they can register this way */}
                </select>
              </div>
            </div>
            {/* End NEW INPUT */}

            <Input
              label="Password (Min 8 chars, 1 Uppercase, 1 Digit)"
              name="password"
              type="password"
              value={formData.password}
              onChange={handleChange}
              error={errors.password}
              icon={FiLock}
              placeholder="••••••••"
              autoComplete="new-password"
            />

            <Input
              label="Confirm Password"
              name="confirmPassword"
              type="password"
              value={formData.confirmPassword}
              onChange={handleChange}
              error={errors.confirmPassword}
              icon={FiLock}
              placeholder="••••••••"
              autoComplete="new-password"
            />

            <div className="text-sm text-gray-400">
              <label className="flex items-start">
                <input
                  type="checkbox"
                  className="mt-1 mr-2 rounded border-dark-700 bg-dark-800 text-red-500 focus:ring-red-500 focus:ring-offset-midnight-950"
                  required
                />
                <span>
                  I agree to the{" "}
                  <Link to="/terms" className="text-red-500 hover:text-red-400">
                    Terms of Service
                  </Link>{" "}
                  and{" "}
                  <Link
                    to="/privacy"
                    className="text-red-500 hover:text-red-400"
                  >
                    Privacy Policy
                  </Link>
                </span>
              </label>
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
                    Creating Account...
                  </>
                ) : (
                  <>
                    Create Account
                    <FiArrowRight className="group-hover:translate-x-1 transition-transform" />
                  </>
                )}
              </button>
            </div>
          </form>

          <div className="mt-6 pt-6 border-t border-dark-700 text-center px-8">
            <p className="text-gray-400">
              Already have an account?{" "}
              <Link
                to="/login"
                className="text-red-500 hover:text-red-400 font-bold hover:underline transition-all"
              >
                Sign In
              </Link>
            </p>
          </div>
        </Card>

        {/* Trust Badge */}
        <div className="mt-8 text-center text-sm text-gray-500">
          <p className="flex items-center justify-center gap-2">
            <span className="text-green-500">🔒</span>
            Your information is protected and will never be shared
          </p>
        </div>
        </div>
      </div>
    </div>
  );
};

export default Register;
