import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { FiShield, FiClock, FiDollarSign, FiHeadphones, FiStar, FiArrowRight, FiCheckCircle, FiCalendar, FiMapPin, FiSearch, FiSmartphone } from 'react-icons/fi';
import { FaApple, FaGooglePlay } from 'react-icons/fa';
import Button from '../components/ui/Button';
import Card, { CardContent } from '../components/ui/Card';
import StatsSection from '../components/home/StatsSection';
import BrandLogos from '../components/home/BrandLogos';
import Reviews from '../components/home/Reviews';
import SocialProof from '../components/home/SocialProof';
import { useNavigate } from 'react-router-dom';
import { useLanguage } from '../context/LanguageContext';
import zipLogo from '../assets/zip-logo.jpg';

const HomeEnhanced = () => {
  const navigate = useNavigate();
  const { t } = useLanguage();

  // Rotating cars state
  const cars = [
    'https://images.unsplash.com/photo-1583121274602-3e2820c69888?w=1200&q=80',
    'https://images.unsplash.com/photo-1617531653332-bd46c24f2068?w=1200&q=80',
    'https://images.unsplash.com/photo-1618843479313-40f8afb4b4d8?w=1200&q=80',
    'https://images.unsplash.com/photo-1552519507-da3b142c6e3d?w=1200&q=80',
    'https://images.unsplash.com/photo-1606664515524-ed2f786a0bd6?w=1200&q=80',
  ];

  const [currentCarIndex, setCurrentCarIndex] = useState(0);
  const [isTransitioning, setIsTransitioning] = useState(false);

  useEffect(() => {
    const interval = setInterval(() => {
      setIsTransitioning(true);
      setTimeout(() => {
        setCurrentCarIndex((prev) => (prev + 1) % cars.length);
        setIsTransitioning(false);
      }, 600);
    }, 4000);

    return () => clearInterval(interval);
  }, []);

  // Search form state
  const [searchData, setSearchData] = useState({
    category: 'rental',
    location: '',
    startDate: '',
  });

  const handleSearch = (e) => {
    e.preventDefault();
    if (searchData.category === 'rental') {
      navigate('/rentals');
    } else if (searchData.category === 'maintenance') {
      navigate('/maintenance');
    } else {
      navigate('/store');
    }
  };

  const whyChooseUs = [
    {
      icon: FiDollarSign,
      title: 'Best Price Guaranteed',
      description: 'Competitive pricing with no hidden fees. Get the best value for your money.',
      color: 'text-green-500',
    },
    {
      icon: FiShield,
      title: 'Safety & Insurance',
      description: 'All vehicles are fully insured and regularly maintained for your safety.',
      color: 'text-blue-500',
    },
    {
      icon: FiClock,
      title: '24/7 Support',
      description: 'Round-the-clock customer support to assist you whenever you need help.',
      color: 'text-purple-500',
    },
    {
      icon: FiHeadphones,
      title: 'Professional Service',
      description: 'Certified technicians and experienced staff dedicated to quality service.',
      color: 'text-red-500',
    },
  ];

  const testimonials = [
    {
      name: 'Kwame Mensah',
      role: 'Business Owner',
      image: 'https://randomuser.me/api/portraits/men/32.jpg',
      comment: 'Exceptional service! The mobile maintenance team came to my office and fixed my car while I worked. Very professional and affordable.',
      rating: 5,
    },
    {
      name: 'Ama Asante',
      role: 'Regular Customer',
      image: 'https://randomuser.me/api/portraits/women/44.jpg',
      comment: 'Rented a car for my family trip to Cape Coast. The vehicle was in excellent condition and the process was seamless. Highly recommended!',
      rating: 5,
    },
    {
      name: 'Kofi Addo',
      role: 'Car Enthusiast',
      image: 'https://randomuser.me/api/portraits/men/67.jpg',
      comment: 'Great selection of genuine auto parts at unbeatable prices. Fast delivery and excellent customer service. My go-to shop!',
      rating: 5,
    },
  ];

  const services = [
    {
      title: 'Mobile Car Maintenance',
      description: 'Professional car care at your doorstep',
      image: 'https://images.unsplash.com/photo-1619642751034-765dfdf7c58e?w=500',
      features: ['Oil Change', 'Brake Service', 'AC Repair', 'Engine Diagnostics'],
      link: '/maintenance',
    },
    {
      title: 'Car Rentals',
      description: 'Quality vehicles for any occasion',
      image: 'https://images.unsplash.com/photo-1449965408869-eaa3f722e40d?w=500',
      features: ['Daily Rentals', 'Weekly Deals', 'Airport Pickup', 'GPS Included'],
      link: '/rentals',
    },
    {
      title: 'Auto Parts Store',
      description: 'Genuine parts and accessories',
      image: 'https://images.unsplash.com/photo-1486262715619-67b85e0b08d3?w=500',
      features: ['Genuine Parts', 'Fast Delivery', 'Expert Advice', 'Warranty'],
      link: '/store',
    },
  ];

  return (
    <div className="min-h-screen bg-white" style={{ zoom: '85%' }}>
      {/* NEW HERO SECTION */}
      <section className="relative min-h-screen flex items-center overflow-hidden bg-gradient-to-br from-gray-900 via-gray-800 to-black">
        {/* Animated Background Pattern */}
        <div className="absolute inset-0 opacity-10">
          <div className="absolute inset-0" style={{
            backgroundImage: 'radial-gradient(circle at 2px 2px, white 1px, transparent 0)',
            backgroundSize: '40px 40px'
          }}></div>
        </div>

        {/* Red Gradient Overlay */}
        <div className="absolute inset-0 bg-gradient-to-r from-red-600/20 via-transparent to-transparent"></div>

        {/* Rotating Car Background */}
        <div className="absolute inset-0">
          {cars.map((car, index) => (
            <div
              key={index}
              className={`absolute inset-0 transition-all duration-1000 ease-in-out ${
                index === currentCarIndex
                  ? 'opacity-30 scale-100'
                  : 'opacity-0 scale-110'
              }`}
              style={{
                backgroundImage: `url(${car})`,
                backgroundSize: 'cover',
                backgroundPosition: 'center',
                filter: 'blur(8px)',
              }}
            ></div>
          ))}
        </div>

        <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-32 w-full">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            {/* Left Content */}
            <div className="text-white">
              <div className="inline-block mb-4 animate-fade-in-up">
                <span className="bg-primary-500/20 text-primary-400 px-4 py-2 rounded-full text-sm font-semibold border border-primary-500/30 backdrop-blur-sm hover:scale-105 transition-transform duration-300">
                  {t('heroTag')}
                </span>
              </div>

              <h1 className="text-5xl md:text-6xl lg:text-7xl font-bold mb-6 leading-tight animate-fade-in-up" style={{ animationDelay: '0.1s' }}>
                {t('heroTitle')}
                <br />
                <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary-500 via-primary-400 to-orange-400 animate-gradient">
                  {t('heroTitleHighlight')}
                </span>
              </h1>

              <p className="text-xl md:text-2xl text-gray-300 mb-8 leading-relaxed max-w-xl animate-fade-in-up" style={{ animationDelay: '0.2s' }}>
                {t('heroSubtitle')}
              </p>

              {/* Quick Stats */}
              <div className="grid grid-cols-3 gap-6 mb-8 animate-fade-in-up" style={{ animationDelay: '0.3s' }}>
                <div className="text-center hover:scale-110 transition-transform duration-300">
                  <div className="text-3xl font-bold text-primary-500 animate-pulse-slow">500+</div>
                  <div className="text-sm text-gray-400">{t('vehicles')}</div>
                </div>
                <div className="text-center hover:scale-110 transition-transform duration-300">
                  <div className="text-3xl font-bold text-primary-500 animate-pulse-slow" style={{ animationDelay: '0.5s' }}>5K+</div>
                  <div className="text-sm text-gray-400">{t('customers')}</div>
                </div>
                <div className="text-center hover:scale-110 transition-transform duration-300">
                  <div className="text-3xl font-bold text-primary-500 animate-pulse-slow" style={{ animationDelay: '1s' }}>100%</div>
                  <div className="text-sm text-gray-400">{t('satisfaction')}</div>
                </div>
              </div>

              {/* CTA Buttons */}
              <div className="flex flex-col sm:flex-row gap-4">
                <Link to="/rentals">
                  <Button variant="primary" size="lg" className="shadow-2xl shadow-primary-500/50 hover:shadow-primary-500/70 transition-all min-w-[200px]">
                    {t('browseVehicles')}
                    <FiArrowRight className="ml-2" />
                  </Button>
                </Link>
                <Link to="/maintenance">
                  <Button variant="outline" size="lg" className="border-2 border-white text-white hover:bg-white hover:text-gray-900 min-w-[200px]">
                    {t('bookService')}
                  </Button>
                </Link>
              </div>
            </div>

            {/* Right Content - Mobile Mockup */}
            <div className="relative lg:block">
              <div className="relative flex justify-center items-center">
                {/* Glowing Circle Background */}
                <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-red-500/20 rounded-full blur-3xl animate-pulse-slow"></div>

                {/* Mobile Phone Mockup */}
                <div className="relative z-10 scale-75 sm:scale-90 lg:scale-100">
                  {/* Phone Frame */}
                  <div className="relative w-72 sm:w-80 h-[520px] sm:h-[600px] bg-gray-900 rounded-[3rem] shadow-2xl border-4 sm:border-8 border-gray-800 overflow-hidden">
                    {/* Notch */}
                    <div className="absolute top-0 left-1/2 transform -translate-x-1/2 w-40 h-7 bg-gray-900 rounded-b-3xl z-20"></div>

                    {/* Screen Content */}
                    <div className="relative h-full w-full bg-gradient-to-br from-gray-800 to-gray-900 overflow-hidden">
                      {/* App Screenshot - Logo and Branding */}
                      <div className="absolute inset-0 flex flex-col items-center justify-center p-8">
                        {/* ZIP Logo */}
                        <div className="mb-6 relative">
                          <div className="absolute inset-0 bg-red-500/30 blur-2xl rounded-full"></div>
                          <img
                            src={zipLogo}
                            alt="ZIP Platform"
                            className="relative w-32 h-32 rounded-3xl shadow-2xl shadow-red-500/50 animate-float border-4 border-red-500/30"
                          />
                        </div>

                        {/* App Name */}
                        <h3 className="text-3xl font-bold text-white mb-2 animate-fade-in-up">ZIP Platform</h3>
                        <p className="text-gray-400 text-center text-sm mb-8 animate-fade-in-up" style={{ animationDelay: '0.1s' }}>
                          Your Complete Auto Solution
                        </p>

                        {/* Feature Pills */}
                        <div className="space-y-3 w-full animate-fade-in-up" style={{ animationDelay: '0.2s' }}>
                          <div className="bg-white/10 backdrop-blur-sm rounded-2xl p-4 border border-white/20 hover:bg-white/20 transition-all">
                            <div className="flex items-center">
                              <div className="w-10 h-10 bg-red-500/20 rounded-xl flex items-center justify-center mr-3">
                                <span className="text-2xl">🚗</span>
                              </div>
                              <div>
                                <p className="text-white font-semibold text-sm">Rent Vehicles</p>
                                <p className="text-gray-400 text-xs">Browse & book instantly</p>
                              </div>
                            </div>
                          </div>

                          <div className="bg-white/10 backdrop-blur-sm rounded-2xl p-4 border border-white/20 hover:bg-white/20 transition-all">
                            <div className="flex items-center">
                              <div className="w-10 h-10 bg-red-500/20 rounded-xl flex items-center justify-center mr-3">
                                <span className="text-2xl">🔧</span>
                              </div>
                              <div>
                                <p className="text-white font-semibold text-sm">Book Services</p>
                                <p className="text-gray-400 text-xs">Mobile maintenance</p>
                              </div>
                            </div>
                          </div>

                          <div className="bg-white/10 backdrop-blur-sm rounded-2xl p-4 border border-white/20 hover:bg-white/20 transition-all">
                            <div className="flex items-center">
                              <div className="w-10 h-10 bg-red-500/20 rounded-xl flex items-center justify-center mr-3">
                                <span className="text-2xl">🛒</span>
                              </div>
                              <div>
                                <p className="text-white font-semibold text-sm">Shop Parts</p>
                                <p className="text-gray-400 text-xs">Genuine auto parts</p>
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>

                      {/* Decorative Elements */}
                      <div className="absolute top-4 right-4">
                        <div className="flex space-x-2">
                          <div className="w-1 h-1 bg-white/50 rounded-full"></div>
                          <div className="w-1 h-1 bg-white/50 rounded-full"></div>
                          <div className="w-1 h-1 bg-white/50 rounded-full"></div>
                        </div>
                      </div>
                    </div>

                    {/* Bottom indicator */}
                    <div className="absolute bottom-2 left-1/2 transform -translate-x-1/2 w-32 h-1.5 bg-white/30 rounded-full z-20"></div>
                  </div>

                  {/* Floating App Store Badges */}
                  <div className="hidden lg:flex absolute -right-8 top-1/2 transform -translate-y-1/2 flex-col space-y-4">
                    <div className="bg-black rounded-2xl px-5 py-3 shadow-2xl hover:scale-110 transition-all cursor-pointer border border-gray-700 animate-fade-in-right hover:shadow-red-500/50">
                      <div className="flex items-center space-x-3">
                        <FaApple className="text-4xl text-white" />
                        <div>
                          <p className="text-[9px] text-gray-400 uppercase tracking-wide">Download on the</p>
                          <p className="text-sm font-bold text-white">App Store</p>
                        </div>
                      </div>
                    </div>
                    <div className="bg-black rounded-2xl px-5 py-3 shadow-2xl hover:scale-110 transition-all cursor-pointer border border-gray-700 animate-fade-in-right hover:shadow-green-500/50" style={{ animationDelay: '0.2s' }}>
                      <div className="flex items-center space-x-3">
                        <FaGooglePlay className="text-4xl text-green-500" />
                        <div>
                          <p className="text-[9px] text-gray-400 uppercase tracking-wide">Get it on</p>
                          <p className="text-sm font-bold text-white">Google Play</p>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Search Form */}
          <div className="mt-16">
            <div className="bg-white/95 backdrop-blur-lg rounded-3xl shadow-2xl p-8 max-w-5xl mx-auto">
              <form onSubmit={handleSearch}>
                <div className="grid md:grid-cols-4 gap-6">
                  {/* Category */}
                  <div>
                    <label className="block text-sm font-bold text-gray-700 mb-3 uppercase tracking-wide">
                      {t('selectService')}
                    </label>
                    <select
                      className="w-full px-4 py-4 rounded-xl border-2 border-gray-200 focus:border-primary-500 focus:ring-4 focus:ring-primary-500/20 outline-none transition-all bg-white text-gray-900 font-medium"
                      value={searchData.category}
                      onChange={(e) => setSearchData({ ...searchData, category: e.target.value })}
                    >
                      <option value="rental">🚗 {t('carRental')}</option>
                      <option value="maintenance">🔧 {t('autoMaintenance')}</option>
                      <option value="store">🛒 {t('autoParts')}</option>
                    </select>
                  </div>

                  {/* Location */}
                  <div>
                    <label className="block text-sm font-bold text-gray-700 mb-3 uppercase tracking-wide">
                      {t('location')}
                    </label>
                    <div className="relative">
                      <FiMapPin className="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400 h-5 w-5" />
                      <input
                        type="text"
                        placeholder="Accra, Ghana"
                        className="w-full pl-12 pr-4 py-4 rounded-xl border-2 border-gray-200 focus:border-primary-500 focus:ring-4 focus:ring-primary-500/20 outline-none transition-all"
                        value={searchData.location}
                        onChange={(e) => setSearchData({ ...searchData, location: e.target.value })}
                      />
                    </div>
                  </div>

                  {/* Date */}
                  <div>
                    <label className="block text-sm font-bold text-gray-700 mb-3 uppercase tracking-wide">
                      {t('pickupDate')}
                    </label>
                    <div className="relative">
                      <FiCalendar className="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400 h-5 w-5" />
                      <input
                        type="date"
                        className="w-full pl-12 pr-4 py-4 rounded-xl border-2 border-gray-200 focus:border-primary-500 focus:ring-4 focus:ring-primary-500/20 outline-none transition-all"
                        value={searchData.startDate}
                        onChange={(e) => setSearchData({ ...searchData, startDate: e.target.value })}
                      />
                    </div>
                  </div>

                  {/* Search Button */}
                  <div className="flex items-end">
                    <Button type="submit" variant="primary" size="lg" className="w-full py-4 text-lg font-bold shadow-xl shadow-primary-500/30 hover:shadow-2xl hover:shadow-primary-500/50">
                      <FiSearch className="mr-2" />
                      {t('search')}
                    </Button>
                  </div>
                </div>
              </form>
            </div>
          </div>
        </div>

        {/* Scroll Indicator */}
        <div className="absolute bottom-8 left-1/2 transform -translate-x-1/2 animate-bounce">
          <div className="w-6 h-10 border-2 border-white/50 rounded-full flex justify-center">
            <div className="w-1 h-3 bg-white/50 rounded-full mt-2"></div>
          </div>
        </div>
      </section>

      {/* Mobile App Download Section */}
      <section className="py-12 sm:py-16 md:py-20 px-4 bg-gradient-to-br from-gray-900 via-gray-800 to-black text-white relative overflow-hidden">
        {/* Background Pattern */}
        <div className="absolute inset-0 opacity-5">
          <div className="absolute inset-0" style={{
            backgroundImage: 'radial-gradient(circle at 2px 2px, white 1px, transparent 0)',
            backgroundSize: '40px 40px'
          }}></div>
        </div>

        <div className="max-w-7xl mx-auto relative z-10">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            {/* Left Side - Content */}
            <div className="order-2 lg:order-1">
              <div className="inline-flex items-center bg-red-500/20 border border-red-500/30 rounded-full px-4 py-2 mb-6">
                <FiSmartphone className="mr-2 text-red-400" />
                <span className="text-sm font-semibold text-red-400">Download Our Mobile App</span>
              </div>

              <h2 className="text-4xl md:text-5xl font-bold mb-6 leading-tight">
                Take ZIP Platform
                <br />
                <span className="text-transparent bg-clip-text bg-gradient-to-r from-red-500 to-orange-400">
                  Anywhere You Go
                </span>
              </h2>

              <p className="text-xl text-gray-300 mb-8 leading-relaxed">
                Access all our services on-the-go. Book maintenance, rent vehicles, and shop for parts right from your phone. Available on iOS and Android.
              </p>

              {/* Features */}
              <div className="space-y-4 mb-10">
                <div className="flex items-start">
                  <div className="flex-shrink-0 w-6 h-6 bg-red-500/20 rounded-lg flex items-center justify-center mr-3 mt-1">
                    <FiCheckCircle className="text-red-400 w-4 h-4" />
                  </div>
                  <div>
                    <h4 className="font-semibold mb-1">Real-time Booking</h4>
                    <p className="text-gray-400 text-sm">Book services and rentals instantly with live availability</p>
                  </div>
                </div>
                <div className="flex items-start">
                  <div className="flex-shrink-0 w-6 h-6 bg-red-500/20 rounded-lg flex items-center justify-center mr-3 mt-1">
                    <FiCheckCircle className="text-red-400 w-4 h-4" />
                  </div>
                  <div>
                    <h4 className="font-semibold mb-1">GPS Tracking</h4>
                    <p className="text-gray-400 text-sm">Track your service technician or rental vehicle in real-time</p>
                  </div>
                </div>
                <div className="flex items-start">
                  <div className="flex-shrink-0 w-6 h-6 bg-red-500/20 rounded-lg flex items-center justify-center mr-3 mt-1">
                    <FiCheckCircle className="text-red-400 w-4 h-4" />
                  </div>
                  <div>
                    <h4 className="font-semibold mb-1">Secure Payments</h4>
                    <p className="text-gray-400 text-sm">Multiple payment options with bank-level security</p>
                  </div>
                </div>
              </div>

              {/* App Store Buttons */}
              <div className="flex flex-col sm:flex-row gap-4">
                <a
                  href="#"
                  className="inline-flex items-center justify-center bg-white text-gray-900 px-6 py-4 rounded-2xl font-semibold hover:bg-gray-100 transition-all shadow-xl hover:shadow-2xl hover:scale-105 group"
                >
                  <FaApple className="text-4xl mr-3" />
                  <div className="text-left">
                    <p className="text-xs text-gray-600">Download on the</p>
                    <p className="text-lg font-bold">App Store</p>
                  </div>
                </a>
                <a
                  href="#"
                  className="inline-flex items-center justify-center bg-white text-gray-900 px-6 py-4 rounded-2xl font-semibold hover:bg-gray-100 transition-all shadow-xl hover:shadow-2xl hover:scale-105 group"
                >
                  <FaGooglePlay className="text-4xl mr-3 text-green-600" />
                  <div className="text-left">
                    <p className="text-xs text-gray-600">Get it on</p>
                    <p className="text-lg font-bold">Google Play</p>
                  </div>
                </a>
              </div>

              {/* Download Stats */}
              <div className="flex items-center gap-8 mt-8 pt-8 border-t border-gray-700">
                <div>
                  <div className="text-3xl font-bold text-red-400">10K+</div>
                  <div className="text-sm text-gray-400">Downloads</div>
                </div>
                <div>
                  <div className="text-3xl font-bold text-red-400">4.8</div>
                  <div className="text-sm text-gray-400 flex items-center">
                    <FiStar className="fill-yellow-400 text-yellow-400 mr-1" />
                    Rating
                  </div>
                </div>
                <div>
                  <div className="text-3xl font-bold text-red-400">99%</div>
                  <div className="text-sm text-gray-400">Satisfaction</div>
                </div>
              </div>
            </div>

            {/* Right Side - Phone Mockup */}
            <div className="order-1 lg:order-2 flex justify-center lg:justify-end">
              <div className="relative scale-75 sm:scale-90 lg:scale-100">
                {/* Glow Effect */}
                <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-red-500/20 rounded-full blur-3xl animate-pulse-slow"></div>

                {/* Phone */}
                <div className="relative w-64 sm:w-72 h-[500px] sm:h-[580px] bg-gray-900 rounded-[2.5rem] shadow-2xl border-4 sm:border-8 border-gray-800 overflow-hidden transform hover:scale-105 transition-transform duration-500">
                  {/* Notch */}
                  <div className="absolute top-0 left-1/2 transform -translate-x-1/2 w-36 h-6 bg-gray-900 rounded-b-3xl z-20"></div>

                  {/* Screen */}
                  <div className="relative h-full w-full bg-gradient-to-br from-gray-100 to-white overflow-y-auto">
                    {/* Status Bar */}
                    <div className="sticky top-0 flex justify-between items-center px-8 pt-8 pb-4 bg-gradient-to-b from-white to-transparent z-10">
                      <span className="text-xs font-semibold text-gray-800">9:41</span>
                      <div className="flex items-center space-x-1">
                        <div className="w-4 h-3 border border-gray-800 rounded-sm"></div>
                        <div className="w-1 h-1 bg-gray-800 rounded-full"></div>
                      </div>
                    </div>

                    {/* App Content */}
                    <div className="px-6 pb-6">
                      {/* Logo */}
                      <div className="flex justify-center mb-4">
                        <img
                          src={zipLogo}
                          alt="ZIP"
                          className="w-20 h-20 rounded-2xl shadow-lg"
                        />
                      </div>

                      {/* Welcome Text */}
                      <h3 className="text-2xl font-bold text-gray-900 text-center mb-2">Welcome to ZIP</h3>
                      <p className="text-sm text-gray-600 text-center mb-6">Your complete automotive solution</p>

                      {/* Service Cards */}
                      <div className="space-y-3">
                        <div className="bg-gradient-to-br from-red-500 to-red-600 rounded-2xl p-4 text-white shadow-lg">
                          <div className="flex items-center justify-between">
                            <div>
                              <p className="text-xs opacity-90 mb-1">Quick Action</p>
                              <p className="font-bold text-lg">Rent a Vehicle</p>
                            </div>
                            <div className="text-4xl">🚗</div>
                          </div>
                        </div>

                        <div className="bg-white border-2 border-gray-200 rounded-2xl p-4 shadow-sm">
                          <div className="flex items-center justify-between">
                            <div>
                              <p className="text-xs text-gray-600 mb-1">Maintenance</p>
                              <p className="font-bold text-gray-900">Book Service</p>
                            </div>
                            <div className="text-3xl">🔧</div>
                          </div>
                        </div>

                        <div className="bg-white border-2 border-gray-200 rounded-2xl p-4 shadow-sm">
                          <div className="flex items-center justify-between">
                            <div>
                              <p className="text-xs text-gray-600 mb-1">Shop</p>
                              <p className="font-bold text-gray-900">Auto Parts</p>
                            </div>
                            <div className="text-3xl">🛒</div>
                          </div>
                        </div>
                      </div>

                      {/* Quick Stats */}
                      <div className="grid grid-cols-2 gap-3 mt-4">
                        <div className="bg-gray-100 rounded-xl p-3 text-center">
                          <p className="text-xs text-gray-600">Active Rentals</p>
                          <p className="text-xl font-bold text-gray-900">350+</p>
                        </div>
                        <div className="bg-gray-100 rounded-xl p-3 text-center">
                          <p className="text-xs text-gray-600">Services Done</p>
                          <p className="text-xl font-bold text-gray-900">2.5K+</p>
                        </div>
                      </div>
                    </div>
                  </div>

                  {/* Bottom Indicator */}
                  <div className="absolute bottom-2 left-1/2 transform -translate-x-1/2 w-28 h-1 bg-gray-300 rounded-full z-20"></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <StatsSection />

      {/* Our Services */}
      <section className="py-20 px-4 bg-gradient-to-b from-white to-gray-50">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
              Our Featured <span className="text-red-500">Services</span>
            </h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Everything you need for your automotive needs in one place
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            {services.map((service, index) => (
              <Link key={index} to={service.link}>
                <div className="group relative bg-white rounded-3xl shadow-xl hover:shadow-2xl transition-all duration-500 overflow-hidden hover:-translate-y-3 animate-fade-in-up border-2 border-transparent hover:border-red-500/20" style={{ animationDelay: `${index * 0.1}s` }}>
                  {/* Gradient overlay on hover */}
                  <div className="absolute inset-0 bg-gradient-to-br from-red-500/0 to-red-500/0 group-hover:from-red-500/5 group-hover:to-orange-500/5 transition-all duration-500 rounded-3xl"></div>

                  <div className="relative h-72 overflow-hidden rounded-t-3xl">
                    <img
                      src={service.image}
                      alt={service.title}
                      className="w-full h-full object-cover group-hover:scale-110 transition-all duration-700"
                    />
                    {/* Stronger gradient overlay */}
                    <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/40 to-transparent"></div>

                    {/* Animated badge */}
                    <div className="absolute top-4 right-4">
                      <div className="bg-red-500 text-white px-4 py-2 rounded-full text-xs font-bold shadow-lg group-hover:scale-110 transition-transform duration-300">
                        POPULAR
                      </div>
                    </div>

                    {/* Title overlay */}
                    <div className="absolute bottom-0 left-0 right-0 p-6">
                      <div className="flex items-center mb-2">
                        <div className="w-12 h-12 bg-red-500 rounded-2xl flex items-center justify-center mr-3 group-hover:scale-110 group-hover:rotate-12 transition-all duration-300">
                          <span className="text-2xl">{index === 0 ? '🔧' : index === 1 ? '🚗' : '🛒'}</span>
                        </div>
                        <h3 className="text-2xl font-bold text-white flex-1">{service.title}</h3>
                      </div>
                      <p className="text-gray-200 text-sm leading-relaxed">{service.description}</p>
                    </div>
                  </div>

                  <div className="relative p-6 bg-white">
                    {/* Features with improved styling */}
                    <ul className="space-y-3 mb-6">
                      {service.features.map((feature, idx) => (
                        <li key={idx} className="flex items-center text-gray-700 group/item hover:text-red-500 transition-colors">
                          <div className="flex-shrink-0 w-6 h-6 bg-green-100 rounded-full flex items-center justify-center mr-3 group-hover/item:bg-green-500 transition-colors">
                            <FiCheckCircle className="h-4 w-4 text-green-600 group-hover/item:text-white transition-colors" />
                          </div>
                          <span className="font-medium">{feature}</span>
                        </li>
                      ))}
                    </ul>

                    {/* CTA Button with better styling */}
                    <div className="relative overflow-hidden rounded-xl bg-gradient-to-r from-red-500 to-red-600 p-[2px] group-hover:from-red-600 group-hover:to-orange-500 transition-all duration-300">
                      <div className="bg-white rounded-xl px-6 py-3 group-hover:bg-transparent transition-all duration-300">
                        <div className="flex items-center justify-center text-red-600 group-hover:text-white font-bold transition-all duration-300">
                          <span>{t('learnMore')}</span>
                          <FiArrowRight className="ml-2 group-hover:translate-x-2 transition-transform duration-300" />
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </Link>
            ))}
          </div>
        </div>
      </section>

      {/* Why Choose Us */}
      <section className="py-20 px-4 bg-gray-50">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
              Why Choose <span className="text-red-500">ZIP Platform</span>
            </h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              We provide exceptional service with attention to detail
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            {whyChooseUs.map((item, index) => {
              const Icon = item.icon;
              return (
                <div key={index} className="bg-white rounded-2xl p-8 shadow-sm hover:shadow-xl transition-all duration-300 hover:-translate-y-1 animate-fade-in-up" style={{ animationDelay: `${index * 0.1}s` }}>
                  <div className={`inline-flex items-center justify-center w-16 h-16 rounded-full bg-gray-100 mb-6 ${item.color} hover:scale-110 transition-transform duration-300`}>
                    <Icon className="h-8 w-8 animate-pulse-slow" />
                  </div>
                  <h3 className="text-xl font-bold text-gray-900 mb-3">{item.title}</h3>
                  <p className="text-gray-600">{item.description}</p>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* Brand Logos */}
      <BrandLogos />

      {/* Testimonials */}
      <section className="py-20 px-4 bg-white">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
              Trusted By More Than <span className="text-red-500">5000+ Customers</span>
            </h2>
            <p className="text-xl text-gray-600">Here's what our satisfied customers have to say</p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            {testimonials.map((testimonial, index) => (
              <div key={index} className="bg-white rounded-2xl p-8 shadow-lg border border-gray-100 hover:shadow-2xl hover:-translate-y-1 transition-all duration-300 animate-fade-in-up" style={{ animationDelay: `${index * 0.1}s` }}>
                <div className="flex mb-4">
                  {[...Array(testimonial.rating)].map((_, i) => (
                    <FiStar key={i} className="h-5 w-5 text-yellow-400 fill-current hover:scale-125 transition-transform duration-200" />
                  ))}
                </div>
                <p className="text-gray-700 mb-6 italic leading-relaxed">
                  "{testimonial.comment}"
                </p>
                <div className="flex items-center">
                  <img
                    src={testimonial.image}
                    alt={testimonial.name}
                    className="w-14 h-14 rounded-full mr-4 object-cover hover:scale-110 transition-transform duration-300 shadow-md"
                  />
                  <div>
                    <p className="font-bold text-gray-900">{testimonial.name}</p>
                    <p className="text-gray-500 text-sm">{testimonial.role}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Reviews Section */}
      <Reviews />

      {/* CTA Section */}
      <section className="py-20 px-4 bg-gradient-to-br from-primary-500 to-primary-600">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-4xl md:text-5xl font-bold text-white mb-6">
            {t('getStarted')}?
          </h2>
          <p className="text-xl text-primary-100 mb-8 max-w-2xl mx-auto">
            Join thousands of satisfied customers across Ghana and experience the best automotive services
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link to="/register">
              <Button variant="secondary" size="lg" className="bg-white text-primary-500 hover:bg-gray-100 min-w-[200px]">
                {t('createAccount')}
              </Button>
            </Link>
            <Link to="/rentals">
              <Button variant="outline" size="lg" className="border-2 border-white text-white hover:bg-white hover:text-primary-500 min-w-[200px]">
                {t('browseVehicles')}
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* Social Proof Notifications */}
      <SocialProof />
    </div>
  );
};

export default HomeEnhanced;
