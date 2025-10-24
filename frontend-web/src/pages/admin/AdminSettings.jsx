import React from 'react';
import { FiSettings } from 'react-icons/fi';
import Card, { CardContent } from '../../components/ui/Card';

const AdminSettings = () => {
  return (
    <div className="p-8">
      <div className="max-w-7xl mx-auto">
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-white mb-2">Admin Settings</h1>
          <p className="text-gray-400">Configure platform settings</p>
        </div>

        <Card>
          <CardContent className="p-12 text-center">
            <FiSettings className="h-16 w-16 text-gray-600 mx-auto mb-4" />
            <h3 className="text-xl font-semibold text-white mb-2">Platform Settings</h3>
            <p className="text-gray-400">Configure system settings and preferences</p>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default AdminSettings;
