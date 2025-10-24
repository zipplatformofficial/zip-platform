import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { FiX, FiCheck, FiX as FiXIcon, FiUsers, FiSettings, FiDroplet, FiStar } from 'react-icons/fi';
import Button from '../ui/Button';

const CompareModal = ({ vehicles, isOpen, onClose, onRemove, onBook }) => {
  if (!vehicles || vehicles.length === 0) return null;

  const specs = [
    { key: 'price_per_day', label: 'Price per Day', format: (v) => `GH₵${v}` },
    { key: 'seats', label: 'Seats', format: (v) => v || '5' },
    { key: 'transmission', label: 'Transmission', format: (v) => v || 'Automatic' },
    { key: 'fuel_type', label: 'Fuel Type', format: (v) => v || 'Petrol' },
    { key: 'year', label: 'Year', format: (v) => v || '2023' },
    { key: 'rating', label: 'Rating', format: (v) => `${v || '4.5'} ⭐` }
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
            initial={{ opacity: 0, y: 100 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 100 }}
            transition={{ type: 'spring', damping: 25, stiffness: 300 }}
            className="fixed inset-4 md:inset-8 bg-white rounded-3xl shadow-2xl z-50 overflow-hidden flex flex-col"
          >
            {/* Header */}
            <div className="flex items-center justify-between p-6 border-b border-gray-200">
              <div>
                <h2 className="text-2xl font-bold text-gray-900">
                  Compare Vehicles
                </h2>
                <p className="text-sm text-gray-500 mt-1">
                  {vehicles.length} {vehicles.length === 1 ? 'vehicle' : 'vehicles'} selected
                </p>
              </div>
              <button
                onClick={onClose}
                className="p-2 hover:bg-gray-100 rounded-full transition-all"
              >
                <FiX className="h-6 w-6 text-gray-700" />
              </button>
            </div>

            {/* Comparison Table */}
            <div className="flex-1 overflow-auto p-6">
              <div className="grid gap-6" style={{ gridTemplateColumns: `repeat(${vehicles.length}, minmax(250px, 1fr))` }}>
                {/* Vehicle Cards */}
                {vehicles.map((vehicle) => (
                  <div
                    key={vehicle.id}
                    className="bg-gradient-to-br from-gray-50 to-gray-100 rounded-2xl overflow-hidden border-2 border-gray-200"
                  >
                    {/* Image */}
                    <div className="relative h-48 bg-gray-200">
                      <img
                        src={vehicle.image}
                        alt={`${vehicle.make} ${vehicle.model}`}
                        className="w-full h-full object-cover"
                      />
                      {/* Remove button */}
                      <button
                        onClick={() => onRemove(vehicle.id)}
                        className="absolute top-2 right-2 p-2 bg-white/90 backdrop-blur-sm rounded-full hover:bg-white shadow-lg hover:scale-110 transition-all"
                      >
                        <FiX className="h-4 w-4 text-gray-700" />
                      </button>
                    </div>

                    {/* Vehicle Info */}
                    <div className="p-4 space-y-4">
                      {/* Title */}
                      <div>
                        <h3 className="text-lg font-bold text-gray-900">
                          {vehicle.make} {vehicle.model}
                        </h3>
                        <div className="flex items-center gap-2 mt-1">
                          <FiStar className="h-4 w-4 fill-yellow-400 text-yellow-400" />
                          <span className="text-sm font-semibold text-gray-700">
                            {vehicle.rating || '4.8'}
                          </span>
                        </div>
                      </div>

                      {/* Specs */}
                      <div className="space-y-3">
                        {specs.map((spec) => (
                          <div
                            key={spec.key}
                            className="flex justify-between items-center pb-2 border-b border-gray-200 last:border-0"
                          >
                            <span className="text-sm text-gray-600">
                              {spec.label}
                            </span>
                            <span className="text-sm font-semibold text-gray-900">
                              {spec.format(vehicle[spec.key])}
                            </span>
                          </div>
                        ))}
                      </div>

                      {/* Features Checklist */}
                      <div>
                        <h4 className="text-sm font-bold text-gray-900 mb-2">
                          Features
                        </h4>
                        <div className="space-y-1">
                          {features.map((feature) => {
                            // Mock: randomly assign features (in production, this would come from vehicle.features)
                            const hasFeature = Math.random() > 0.3;
                            return (
                              <div
                                key={feature}
                                className="flex items-center gap-2 text-xs"
                              >
                                {hasFeature ? (
                                  <FiCheck className="h-4 w-4 text-green-500 flex-shrink-0" />
                                ) : (
                                  <FiXIcon className="h-4 w-4 text-gray-300 flex-shrink-0" />
                                )}
                                <span
                                  className={
                                    hasFeature ? 'text-gray-700' : 'text-gray-400'
                                  }
                                >
                                  {feature}
                                </span>
                              </div>
                            );
                          })}
                        </div>
                      </div>

                      {/* Price and CTA */}
                      <div className="pt-4 border-t border-gray-200">
                        <div className="mb-3">
                          <p className="text-xs text-gray-500 mb-1">
                            Starting from
                          </p>
                          <p className="text-2xl font-bold bg-gradient-to-r from-red-500 to-orange-500 bg-clip-text text-transparent">
                            GH₵{vehicle.price_per_day}
                            <span className="text-sm text-gray-500">/day</span>
                          </p>
                        </div>
                        <Button
                          onClick={() => {
                            onBook(vehicle);
                            onClose();
                          }}
                          className="w-full bg-gradient-to-r from-red-500 to-orange-500 text-white hover:from-red-600 hover:to-orange-600"
                        >
                          Book Now
                        </Button>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Footer */}
            <div className="p-6 border-t border-gray-200 bg-gray-50">
              <div className="flex items-center justify-between">
                <p className="text-sm text-gray-600">
                  Select up to 3 vehicles to compare
                </p>
                <button
                  onClick={onClose}
                  className="px-6 py-2 text-sm font-semibold text-gray-700 hover:text-gray-900 transition-colors"
                >
                  Close Comparison
                </button>
              </div>
            </div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
};

export default CompareModal;
