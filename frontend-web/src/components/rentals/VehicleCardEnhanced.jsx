import React from 'react';
import { FiUsers, FiSettings, FiZap, FiDollarSign, FiMapPin, FiStar } from 'react-icons/fi';
import Button from '../ui/Button';
import Badge from '../ui/Badge';
import { formatCurrency } from '../../utils/formatters';

const VehicleCardEnhanced = ({ vehicle, onBook }) => {
  const specs = [
    { icon: FiUsers, label: `${vehicle.seats} Seats`, value: vehicle.seats },
    { icon: FiSettings, label: vehicle.transmission || 'Auto', value: vehicle.transmission },
    { icon: FiZap, label: vehicle.fuel_type || 'Petrol', value: vehicle.fuel_type },
    { icon: FiMapPin, label: vehicle.location || 'Accra', value: vehicle.location },
  ];

  return (
    <div className="group relative bg-white rounded-3xl shadow-xl hover:shadow-2xl transition-all duration-500 overflow-hidden hover:-translate-y-2 border-2 border-transparent hover:border-red-500/20 animate-fade-in-up">
      {/* Gradient overlay on hover */}
      <div className="absolute inset-0 bg-gradient-to-br from-red-500/0 to-red-500/0 group-hover:from-red-500/5 group-hover:to-orange-500/5 transition-all duration-500 rounded-3xl pointer-events-none z-10"></div>

      {/* Image Section */}
      <div className="relative h-64 overflow-hidden bg-gradient-to-br from-gray-100 to-gray-200">
        {vehicle.photos && vehicle.photos[0] ? (
          <img
            src={vehicle.photos[0]}
            alt={`${vehicle.make} ${vehicle.model}`}
            className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-700"
          />
        ) : (
          <div className="w-full h-full flex items-center justify-center bg-gradient-to-br from-gray-200 to-gray-300">
            <FiZap className="h-20 w-20 text-gray-400 animate-pulse-slow" />
          </div>
        )}

        {/* Dark gradient overlay */}
        <div className="absolute inset-0 bg-gradient-to-t from-black/40 via-transparent to-transparent"></div>

        {/* Availability Badge */}
        <div className="absolute top-4 left-4 z-20">
          <div className={`px-4 py-2 rounded-full text-xs font-bold shadow-lg backdrop-blur-sm ${
            vehicle.is_available
              ? 'bg-green-500 text-white'
              : 'bg-red-500 text-white'
          }`}>
            {vehicle.is_available ? '✓ AVAILABLE' : '✗ RENTED'}
          </div>
        </div>

        {/* Rating Badge */}
        {vehicle.average_rating && (
          <div className="absolute top-4 right-4 bg-white/95 backdrop-blur-sm rounded-full px-3 py-2 flex items-center gap-1 shadow-lg z-20 group-hover:scale-110 transition-transform">
            <FiStar className="h-4 w-4 text-yellow-500 fill-current" />
            <span className="text-sm font-bold text-gray-900">{vehicle.average_rating.toFixed(1)}</span>
          </div>
        )}

        {/* Year badge at bottom */}
        <div className="absolute bottom-4 left-4 bg-black/70 backdrop-blur-sm text-white px-3 py-1 rounded-full text-xs font-bold z-20">
          {vehicle.year}
        </div>
      </div>

      {/* Content Section */}
      <div className="relative p-6 bg-white z-20">
        {/* Title */}
        <div className="mb-5">
          <h3 className="text-2xl font-bold text-gray-900 mb-1 group-hover:text-red-600 transition-colors">
            {vehicle.make} {vehicle.model}
          </h3>
          <p className="text-gray-500 text-sm font-medium">{vehicle.license_plate || 'Premium Vehicle'}</p>
        </div>

        {/* Specs Grid */}
        <div className="grid grid-cols-2 gap-3 mb-6">
          {specs.map((spec, index) => {
            const Icon = spec.icon;
            return (
              <div key={index} className="flex items-center gap-2 text-gray-700 group/item hover:text-red-500 transition-colors">
                <div className={`w-10 h-10 rounded-xl flex items-center justify-center flex-shrink-0 transition-all ${
                  index === 0 ? 'bg-blue-100 text-blue-600 group-hover/item:bg-blue-500 group-hover/item:text-white' :
                  index === 1 ? 'bg-purple-100 text-purple-600 group-hover/item:bg-purple-500 group-hover/item:text-white' :
                  index === 2 ? 'bg-green-100 text-green-600 group-hover/item:bg-green-500 group-hover/item:text-white' :
                  'bg-orange-100 text-orange-600 group-hover/item:bg-orange-500 group-hover/item:text-white'
                }`}>
                  <Icon className="h-5 w-5" />
                </div>
                <span className="text-sm font-bold">{spec.label}</span>
              </div>
            );
          })}
        </div>

        {/* Price and Action */}
        <div className="flex items-center justify-between pt-5 border-t-2 border-gray-100">
          <div>
            <p className="text-gray-500 text-xs font-bold uppercase tracking-wider mb-1">Daily Rate</p>
            <div className="flex items-baseline gap-1">
              <span className="text-4xl font-bold bg-gradient-to-r from-red-500 to-orange-500 bg-clip-text text-transparent">
                {formatCurrency(vehicle.daily_rate).split('.')[0]}
              </span>
              <span className="text-gray-500 text-sm font-semibold">/day</span>
            </div>
          </div>

          <div className="relative overflow-hidden rounded-xl bg-gradient-to-r from-red-500 to-red-600 p-[2px] group-hover:from-red-600 group-hover:to-orange-500 transition-all duration-300">
            <button
              onClick={() => onBook(vehicle)}
              disabled={!vehicle.is_available}
              className={`relative px-6 py-3 rounded-xl font-bold transition-all ${
                vehicle.is_available
                  ? 'bg-white text-red-600 hover:bg-transparent hover:text-white'
                  : 'bg-gray-100 text-gray-400 cursor-not-allowed'
              }`}
            >
              {vehicle.is_available ? 'Rent Now' : 'Unavailable'}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default VehicleCardEnhanced;
