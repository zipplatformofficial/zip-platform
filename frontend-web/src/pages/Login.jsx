import React, { useState } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { FiMail, FiLock, FiArrowRight } from 'react-icons/fi';
import { useAuth } from '../hooks/useAuth';
import { useLanguage } from '../context/LanguageContext';
import Button from '../components/ui/Button';
import Input from '../components/ui/Input';
import Card from '../components/ui/Card';
import zipLogo from '../assets/zip-logo.jpg';
import toast from 'react-hot-toast';

const Login = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { login } = useAuth();
  const { t } = useLanguage();

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
      newErrors.email = t('pleaseFillAllFields');
    }
    if (!formData.password) {
      newErrors.password = t('pleaseFillAllFields');
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

      toast.success(t('successfullyLoggedIn'));
      toast.success(t('welcomeToZip'));

      // Get user data from authService to check role
      const response = await fetch('/api/v1/auth/me', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        }
      });
      const userData = await response.json();

      // Redirect based on role
      const from = location.state?.from?.pathname;
      if (from) {
        navigate(from, { replace: true });
      } else if (userData.role === 'admin') {
        navigate('/admin', { replace: true });
      } else {
        navigate('/dashboard', { replace: true });
      }
    } catch (error) {
      console.error('Login error:', error);
      toast.error(t('loginFailed'));
      toast.error(t('invalidCredentials'));
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
      <div className="hidden lg:flex lg:w-1/2 relative bg-gradient-to-br from-red-600 via-red-500 to-orange-500 p-12 items-center justify-center overflow-hidden">
        {/* Animated Background Elements */}
        <div className="absolute inset-0 opacity-20">
          <div className="absolute top-20 left-20 w-72 h-72 bg-white rounded-full blur-3xl animate-pulse"></div>
          <div className="absolute bottom-20 right-20 w-96 h-96 bg-yellow-300 rounded-full blur-3xl animate-pulse" style={{ animationDelay: '1s' }}></div>
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
                <span className="text-white/90 text-sm uppercase tracking-widest">{t('platform')}</span>
              </div>
            </div>
          </Link>

          <h1 className="text-5xl md:text-6xl font-black mb-6 leading-tight">
            {t('completeAutomotiveSolution')}
          </h1>

          <p className="text-xl text-white/90 mb-12 leading-relaxed">
            {t('accessPremiumServices')}
          </p>

          {/* Feature Cards */}
          <div className="space-y-4">
            <div className="flex items-start space-x-4 bg-white/10 backdrop-blur-sm rounded-2xl p-4 border border-white/20 hover:bg-white/20 transition-all">
              <div className="text-4xl">🚗</div>
              <div>
                <h3 className="font-bold text-lg mb-1">{t('premiumRentals')}</h3>
                <p className="text-white/80 text-sm">{t('wideSelectionVehicles')}</p>
              </div>
            </div>
            <div className="flex items-start space-x-4 bg-white/10 backdrop-blur-sm rounded-2xl p-4 border border-white/20 hover:bg-white/20 transition-all">
              <div className="text-4xl">🔧</div>
              <div>
                <h3 className="font-bold text-lg mb-1">{t('mobileMaintenance')}</h3>
                <p className="text-white/80 text-sm">{t('professionalService')}</p>
              </div>
            </div>
            <div className="flex items-start space-x-4 bg-white/10 backdrop-blur-sm rounded-2xl p-4 border border-white/20 hover:bg-white/20 transition-all">
              <div className="text-4xl">🛒</div>
              <div>
                <h3 className="font-bold text-lg mb-1">{t('genuineParts')}</h3>
                <p className="text-white/80 text-sm">{t('qualityPartsDelivered')}</p>
              </div>
            </div>
          </div>

          {/* Stats */}
          <div className="mt-12 grid grid-cols-3 gap-6">
            <div className="text-center">
              <div className="text-3xl font-black mb-1">5K+</div>
              <div className="text-sm text-white/80">{t('activeUsers')}</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-black mb-1">500+</div>
              <div className="text-sm text-white/80">{t('vehicles')}</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-black mb-1">99%</div>
              <div className="text-sm text-white/80">{t('satisfaction')}</div>
            </div>
          </div>
        </div>
      </div>

      {/* Right Column - Login Form */}
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
                  <span className="text-white font-bold text-3xl block">ZIP {t('platform')}</span>
                  <span className="text-red-400 text-xs uppercase tracking-wider">{t('autoMaintenance')}</span>
                </div>
              </div>
            </Link>
          </div>

          <div className="mb-8">
            <h2 className="text-4xl font-bold text-white mb-3">
              {t('welcomeBack')} 👋
            </h2>
            <p className="text-gray-400 text-lg">
              {t('signInSubtitle')}
            </p>
          </div>

          <Card className="border-dark-700/50">
            <form onSubmit={handleSubmit} className="space-y-6 p-8">
              <Input
                label={t('emailAddress')}
                name="email"
                type="email"
                value={formData.email}
                onChange={handleChange}
                error={errors.email}
                icon={FiMail}
                placeholder={t('emailPlaceholder')}
                autoComplete="email"
              />

              <Input
                label={t('password')}
                name="password"
                type="password"
                value={formData.password}
                onChange={handleChange}
                error={errors.password}
                icon={FiLock}
                placeholder={t('passwordPlaceholder')}
                autoComplete="current-password"
              />

              <div className="flex items-center justify-between text-sm">
                <label className="flex items-center text-gray-400">
                  <input
                    type="checkbox"
                    className="mr-2 rounded border-dark-700 bg-dark-800 text-red-500 focus:ring-red-500 focus:ring-offset-midnight-950"
                  />
                  {t('rememberMe')}
                </label>
                <Link to="/forgot-password" className="text-red-500 hover:text-red-400">
                  {t('forgotPassword')}
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
                      {t('signingIn')}
                    </>
                  ) : (
                    <>
                      {t('signIn')}
                      <FiArrowRight className="group-hover:translate-x-1 transition-transform" />
                    </>
                  )}
                </button>
              </div>
            </form>

            <div className="mt-6 pt-6 border-t border-dark-700 text-center px-8">
              <p className="text-gray-400">
                {t('dontHaveAccount')}{' '}
                <Link to="/register" className="text-red-500 hover:text-red-400 font-bold hover:underline transition-all">
                  {t('createAccount')}
                </Link>
              </p>
            </div>
          </Card>

          {/* Trust Badge */}
          <div className="mt-8 text-center text-sm text-gray-500">
            <p className="flex items-center justify-center gap-2">
              <span className="text-green-500">🔒</span>
              {t('securedWithEncryption')}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;
