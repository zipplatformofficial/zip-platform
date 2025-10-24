import React from 'react';
import { FiBell } from 'react-icons/fi';
import Card, { CardContent } from '../../components/ui/Card';

const Notifications = () => {
  return (
    <div className="p-8">
      <div className="max-w-7xl mx-auto">
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-white mb-2">Notifications</h1>
          <p className="text-gray-400">Manage platform notifications</p>
        </div>

        <Card>
          <CardContent className="p-12 text-center">
            <FiBell className="h-16 w-16 text-gray-600 mx-auto mb-4" />
            <h3 className="text-xl font-semibold text-white mb-2">Notification Center</h3>
            <p className="text-gray-400">Send and manage system notifications</p>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default Notifications;
