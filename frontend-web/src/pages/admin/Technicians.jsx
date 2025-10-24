import React from 'react';
import { FiTool } from 'react-icons/fi';
import Card, { CardContent } from '../../components/ui/Card';

const Technicians = () => {
  return (
    <div className="p-8">
      <div className="max-w-7xl mx-auto">
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-white mb-2">Technicians Management</h1>
          <p className="text-gray-400">Manage verified technicians and their services</p>
        </div>

        <Card>
          <CardContent className="p-12 text-center">
            <FiTool className="h-16 w-16 text-gray-600 mx-auto mb-4" />
            <h3 className="text-xl font-semibold text-white mb-2">Technicians List</h3>
            <p className="text-gray-400">This page will show all verified technicians</p>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default Technicians;
