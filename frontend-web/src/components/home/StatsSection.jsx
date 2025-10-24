import React from 'react';
import { FiUsers, FiTruck, FiAward, FiThumbsUp } from 'react-icons/fi';

const StatsSection = () => {
  const stats = [
    {
      icon: FiAward,
      number: '10+',
      label: 'Years Experience',
      color: 'from-red-500 to-orange-500',
    },
    {
      icon: FiTruck,
      number: '500+',
      label: 'Vehicles Available',
      color: 'from-blue-500 to-cyan-500',
    },
    {
      icon: FiUsers,
      number: '5000+',
      label: 'Happy Customers',
      color: 'from-green-500 to-emerald-500',
    },
    {
      icon: FiThumbsUp,
      number: '100%',
      label: 'Customer Satisfaction',
      color: 'from-purple-500 to-pink-500',
    },
  ];

  return (
    <div className="bg-dark-900 py-16">
      <div className="max-w-7xl mx-auto px-4">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
          {stats.map((stat, index) => {
            const Icon = stat.icon;
            return (
              <div key={index} className="text-center">
                <div className={`w-20 h-20 mx-auto rounded-full bg-gradient-to-br ${stat.color} flex items-center justify-center mb-4 shadow-lg`}>
                  <Icon className="h-10 w-10 text-white" />
                </div>
                <div className="text-4xl md:text-5xl font-bold text-white mb-2">
                  {stat.number}
                </div>
                <div className="text-gray-400 font-medium">
                  {stat.label}
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};

export default StatsSection;
