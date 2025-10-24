import React, { useState } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { FiMenu, FiX, FiUser, FiShoppingCart, FiLogOut } from 'react-icons/fi';
import { useAuth } from '../../hooks/useAuth';
import { useCart } from '../../hooks/useCart';
import { useLanguage } from '../../context/LanguageContext';
import Button from '../ui/Button';
import LanguageSwitcher from '../LanguageSwitcher';

const Navbar = () => {
  const [isOpen, setIsOpen] = useState(false);
  const { user, logout } = useAuth();
  const { cart } = useCart();
  const { t } = useLanguage();
  const navigate = useNavigate();
  const location = useLocation();

  const navigation = [
    { name: t('home'), path: '/' },
    { name: t('maintenance'), path: '/maintenance' },
    { name: t('rentals'), path: '/rentals' },
    { name: t('store'), path: '/store' },
  ];

  const isActive = (path) => location.pathname === path;

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  const cartItemCount = cart?.items?.length || 0;

  return (
    <nav className="fixed top-0 left-0 right-0 z-40 bg-midnight-950/95 backdrop-blur-md border-b border-dark-700">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center">
            <img
              src="/src/assets/bg-remove/zip-logo-removebg.png"
              alt="ZIP Platform"
              className="h-16 w-auto"
            />
          </Link>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-8">
            {navigation.map((item) => (
              <Link
                key={item.path}
                to={item.path}
                className={`text-sm font-medium transition-colors ${
                  isActive(item.path)
                    ? 'text-red-500'
                    : 'text-gray-300 hover:text-white'
                }`}
              >
                {item.name}
              </Link>
            ))}
          </div>

          {/* Right Side Actions */}
          <div className="hidden md:flex items-center space-x-4">
            <LanguageSwitcher />
            {user ? (
              <>
                <Link to="/cart" className="relative p-2 text-gray-300 hover:text-white transition-colors">
                  <FiShoppingCart className="h-6 w-6" />
                  {cartItemCount > 0 && (
                    <span className="absolute -top-1 -right-1 bg-primary-500 text-white text-xs rounded-full h-5 w-5 flex items-center justify-center">
                      {cartItemCount}
                    </span>
                  )}
                </Link>
                <Link to="/dashboard" className="text-gray-300 hover:text-white transition-colors">
                  <FiUser className="h-6 w-6" />
                </Link>
                <Button variant="ghost" size="sm" onClick={handleLogout}>
                  <FiLogOut className="h-4 w-4 mr-2" />
                  {t('logout')}
                </Button>
              </>
            ) : (
              <>
                <Link to="/login">
                  <Button variant="ghost" size="sm">{t('login')}</Button>
                </Link>
                <Link to="/register">
                  <Button variant="primary" size="sm">{t('signup')}</Button>
                </Link>
              </>
            )}
          </div>

          {/* Mobile menu button */}
          <button
            onClick={() => setIsOpen(!isOpen)}
            className="md:hidden p-2 rounded-lg text-gray-300 hover:text-white hover:bg-dark-800 transition-colors"
          >
            {isOpen ? <FiX className="h-6 w-6" /> : <FiMenu className="h-6 w-6" />}
          </button>
        </div>
      </div>

      {/* Mobile Navigation */}
      {isOpen && (
        <div className="md:hidden border-t border-dark-700 bg-dark-900">
          <div className="px-4 py-6 space-y-4">
            {navigation.map((item) => (
              <Link
                key={item.path}
                to={item.path}
                onClick={() => setIsOpen(false)}
                className={`block px-3 py-2 rounded-lg text-base font-medium transition-colors ${
                  isActive(item.path)
                    ? 'bg-primary-500/10 text-primary-500'
                    : 'text-gray-300 hover:bg-dark-800 hover:text-white'
                }`}
              >
                {item.name}
              </Link>
            ))}

            <div className="pt-4 border-t border-dark-700 space-y-3">
              <div className="px-3">
                <LanguageSwitcher />
              </div>

              {user ? (
                <>
                  <Link
                    to="/cart"
                    onClick={() => setIsOpen(false)}
                    className="flex items-center px-3 py-2 rounded-lg text-base font-medium text-gray-300 hover:bg-dark-800 hover:text-white transition-colors"
                  >
                    <FiShoppingCart className="h-5 w-5 mr-3" />
                    Cart {cartItemCount > 0 && `(${cartItemCount})`}
                  </Link>
                  <Link
                    to="/dashboard"
                    onClick={() => setIsOpen(false)}
                    className="flex items-center px-3 py-2 rounded-lg text-base font-medium text-gray-300 hover:bg-dark-800 hover:text-white transition-colors"
                  >
                    <FiUser className="h-5 w-5 mr-3" />
                    {t('dashboard')}
                  </Link>
                  <button
                    onClick={() => {
                      handleLogout();
                      setIsOpen(false);
                    }}
                    className="w-full flex items-center px-3 py-2 rounded-lg text-base font-medium text-gray-300 hover:bg-dark-800 hover:text-white transition-colors"
                  >
                    <FiLogOut className="h-5 w-5 mr-3" />
                    {t('logout')}
                  </button>
                </>
              ) : (
                <>
                  <Link to="/login" onClick={() => setIsOpen(false)}>
                    <Button variant="ghost" size="md" className="w-full">{t('login')}</Button>
                  </Link>
                  <Link to="/register" onClick={() => setIsOpen(false)}>
                    <Button variant="primary" size="md" className="w-full">{t('signup')}</Button>
                  </Link>
                </>
              )}
            </div>
          </div>
        </div>
      )}
    </nav>
  );
};

export default Navbar;
