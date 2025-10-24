import React from 'react';
import { FiCalendar } from 'react-icons/fi';
import Card, { CardContent } from '../../components/ui/Card';

const ServiceBookings = () => {
  return (
    <div className="p-8">
      <div className="max-w-7xl mx-auto">
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-white mb-2">Service Bookings</h1>
          <p className="text-gray-400">View all maintenance service bookings</p>
        </div>

        <Card>
          <CardContent className="p-12 text-center">
            <FiCalendar className="h-16 w-16 text-gray-600 mx-auto mb-4" />
            <h3 className="text-xl font-semibold text-white mb-2">All Service Bookings</h3>
            <p className="text-gray-400">View and manage customer service appointments</p>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default ServiceBookings;
