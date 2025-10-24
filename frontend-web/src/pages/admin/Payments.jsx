import React from 'react';
import { FiDollarSign } from 'react-icons/fi';
import Card, { CardContent } from '../../components/ui/Card';

const Payments = () => {
  return (
    <div className="p-8">
      <div className="max-w-7xl mx-auto">
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-white mb-2">Payments</h1>
          <p className="text-gray-400">Manage platform payments</p>
        </div>

        <Card>
          <CardContent className="p-12 text-center">
            <FiDollarSign className="h-16 w-16 text-gray-600 mx-auto mb-4" />
            <h3 className="text-xl font-semibold text-white mb-2">Payment Management</h3>
            <p className="text-gray-400">View all payments and payouts</p>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default Payments;
