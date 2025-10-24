import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { FiX, FiHeart, FiShare2, FiUsers, FiSettings, FiDroplet, FiStar, FiMapPin } from 'react-icons/fi';
import Button from '../ui/Button';

const QuickViewModal = ({ vehicle, isOpen, onClose, onBook }) => {
  const [currentImageIndex, setCurrentImageIndex] = useState(0);
  const [isFavorite, setIsFavorite] = useState(false);

  if (!vehicle) return null;

  // Mock multiple images (in production, this would come from vehicle.images array)
  const images = [vehicle.image, vehicle.image, vehicle.image];

  const specs = [
    { icon: FiUsers, label: 'Seats', value: vehicle.seats || '5' },
    { icon: FiSettings, label: 'Transmission', value: vehicle.transmission || 'Automatic' },
    { icon: FiDroplet, label: 'Fuel', value: vehicle.fuel_type || 'Petrol' },
    { icon: FiMapPin, label: 'Location', value: vehicle.location || 'Accra' }
  ];

  const features = [
    'Air Conditioning',
    'Bluetooth',
    'GPS Navigation',
    'Backup Camera',
    'Leather Seats',
    'Sunroof',
    'USB Ports',
    'Cruise Control'
  ];

  const handleShare = () => {
    if (navigator.share) {
      navigator.share({
        title: `${vehicle.make} ${vehicle.model}`,
        text: `Check out this ${vehicle.make} ${vehicle.model} on ZIP Platform`,
        url: window.location.href
      });
    }
  };

  return (
    <AnimatePresence>
      {isOpen && (
        <>
          {/* Backdrop */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
            className="fixed inset-0 bg-black/70 backdrop-blur-sm z-50"
          />

          {/* Modal */}
          <motion.div
            initial={{ opacity: 0, scale: 0.9, y: 50 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.9, y: 50 }}
            transition={{ type: 'spring', damping: 25, stiffness: 300 }}
            className="fixed inset-4 md:inset-auto md:top-1/2 md:left-1/2 md:-translate-x-1/2 md:-translate-y-1/2 md:w-full md:max-w-5xl md:max-h-[90vh] bg-white rounded-3xl shadow-2xl z-50 overflow-hidden"
          >
            {/* Header */}
            <div className="absolute top-4 right-4 flex items-center gap-2 z-10">
              <button
                onClick={() => setIsFavorite(!isFavorite)}
                className="p-3 bg-white/90 backdrop-blur-sm rounded-full hover:bg-white transition-all shadow-lg hover:scale-110"
              >
                <FiHeart
                  className={`h-5 w-5 ${
                    isFavorite ? 'fill-red-500 text-red-500' : 'text-gray-700'
                  }`}
                />
              </button>
              <button
                onClick={handleShare}
                className="p-3 bg-white/90 backdrop-blur-sm rounded-full hover:bg-white transition-all shadow-lg hover:scale-110"
              >
                <FiShare2 className="h-5 w-5 text-gray-700" />
              </button>
              <button
                onClick={onClose}
                className="p-3 bg-white/90 backdrop-blur-sm rounded-full hover:bg-white transition-all shadow-lg hover:scale-110"
              >
                <FiX className="h-5 w-5 text-gray-700" />
              </button>
            </div>

            <div className="grid md:grid-cols-2 h-full overflow-y-auto">
              {/* Left - Image Gallery */}
              <div className="relative bg-gray-100 h-64 md:h-full">
                <img
                  src={images[currentImageIndex]}
                  alt={`${vehicle.make} ${vehicle.model}`}
                  className="w-full h-full object-cover"
                />

                {/* Image Indicators */}
                <div className="absolute bottom-4 left-1/2 -translate-x-1/2 flex gap-2">
                  {images.map((_, idx) => (
                    <button
                      key={idx}
                      onClick={() => setCurrentImageIndex(idx)}
                      className={`w-2 h-2 rounded-full transition-all ${
                        idx === currentImageIndex
                          ? 'bg-white w-6'
                          : 'bg-white/50 hover:bg-white/70'
                      }`}
                    />
                  ))}
                </div>

                {/* Availability Badge */}
                <div className="absolute top-4 left-4">
                  <span className="px-3 py-1 bg-green-500 text-white text-xs font-bold rounded-full shadow-lg">
                    Available Now
                  </span>
                </div>
              </div>

              {/* Right - Details */}
              <div className="p-6 md:p-8 overflow-y-auto">
                {/* Title and Rating */}
                <div className="mb-4">
                  <h2 className="text-3xl font-bold text-gray-900 mb-2">
                    {vehicle.make} {vehicle.model}
                  </h2>
                  <div className="flex items-center gap-3">
                    <div className="flex items-center gap-1">
                      <FiStar className="h-4 w-4 fill-yellow-400 text-yellow-400" />
                      <span className="text-sm font-semibold text-gray-900">
                        {vehicle.rating || '4.8'}
                      </span>
                    </div>
                    <span className="text-sm text-gray-500">
                      ({vehicle.reviews || '124'} reviews)
                    </span>
                  </div>
                </div>

                {/* Specs Grid */}
                <div className="grid grid-cols-2 gap-4 mb-6">
                  {specs.map((spec, idx) => (
                    <div
                      key={idx}
                      className="flex items-center gap-3 p-3 bg-gray-50 rounded-xl"
                    >
                      <div className="p-2 bg-gradient-to-br from-red-500 to-orange-500 rounded-lg">
                        <spec.icon className="h-5 w-5 text-white" />
                      </div>
                      <div>
                        <p className="text-xs text-gray-500">{spec.label}</p>
                        <p className="text-sm font-semibold text-gray-900">
                          {spec.value}
                        </p>
                      </div>
                    </div>
                  ))}
                </div>

                {/* Features */}
                <div className="mb-6">
                  <h3 className="text-lg font-bold text-gray-900 mb-3">
                    Features
                  </h3>
                  <div className="grid grid-cols-2 gap-2">
                    {features.map((feature, idx) => (
                      <div
                        key={idx}
                        className="flex items-center gap-2 text-sm text-gray-700"
                      >
                        <div className="w-1.5 h-1.5 bg-red-500 rounded-full" />
                        {feature}
                      </div>
                    ))}
                  </div>
                </div>

                {/* Description */}
                <div className="mb-6">
                  <h3 className="text-lg font-bold text-gray-900 mb-2">
                    Description
                  </h3>
                  <p className="text-sm text-gray-600 leading-relaxed">
                    {vehicle.description ||
                      `Experience luxury and comfort with this premium ${vehicle.make} ${vehicle.model}.
                      Perfect for business trips, family outings, or special occasions.
                      Well-maintained, fully insured, and equipped with modern safety features.`}
                  </p>
                </div>

                {/* Pricing and CTA */}
                <div className="border-t border-gray-200 pt-6">
                  <div className="flex items-center justify-between mb-4">
                    <div>
                      <p className="text-sm text-gray-500 mb-1">Starting from</p>
                      <div className="flex items-baseline gap-2">
                        <span className="text-3xl font-bold bg-gradient-to-r from-red-500 to-orange-500 bg-clip-text text-transparent">
                          GH₵{vehicle.price_per_day}
                        </span>
                        <span className="text-gray-500">/day</span>
                      </div>
                    </div>
                  </div>

                  <div className="flex gap-3">
                    <Button
                      onClick={() => {
                        onBook(vehicle);
                        onClose();
                      }}
                      className="flex-1 bg-gradient-to-r from-red-500 to-orange-500 text-white hover:from-red-600 hover:to-orange-600 shadow-lg hover:shadow-xl transition-all"
                    >
                      Book Now
                    </Button>
                    <button className="px-6 py-3 border-2 border-gray-300 rounded-xl font-semibold text-gray-700 hover:border-red-500 hover:text-red-500 transition-all">
                      Details
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
};

export default QuickViewModal;
