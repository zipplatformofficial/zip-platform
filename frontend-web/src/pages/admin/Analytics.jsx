import React from 'react';
import { FiBarChart2, FiTrendingUp, FiUsers, FiDollarSign } from 'react-icons/fi';
import Card, { CardContent, CardTitle } from '../../components/ui/Card';

const Analytics = () => {
  return (
    <div className="p-8">
      <div className="max-w-7xl mx-auto">
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-white mb-2">Analytics Dashboard</h1>
          <p className="text-gray-400">Platform performance metrics and insights</p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <Card>
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-gray-400 text-sm mb-1">Total Revenue</p>
                  <h3 className="text-2xl font-bold text-white">GH₵ 45,231</h3>
                  <p className="text-green-500 text-xs mt-1">+12.5% from last month</p>
                </div>
                <div className="w-12 h-12 rounded-lg bg-green-500/10 flex items-center justify-center">
                  <FiDollarSign className="h-6 w-6 text-green-500" />
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-gray-400 text-sm mb-1">Active Users</p>
                  <h3 className="text-2xl font-bold text-white">1,234</h3>
                  <p className="text-green-500 text-xs mt-1">+8.2% this week</p>
                </div>
                <div className="w-12 h-12 rounded-lg bg-blue-500/10 flex items-center justify-center">
                  <FiUsers className="h-6 w-6 text-blue-500" />
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-gray-400 text-sm mb-1">Bookings</p>
                  <h3 className="text-2xl font-bold text-white">342</h3>
                  <p className="text-green-500 text-xs mt-1">+15.3% increase</p>
                </div>
                <div className="w-12 h-12 rounded-lg bg-purple-500/10 flex items-center justify-center">
                  <FiTrendingUp className="h-6 w-6 text-purple-500" />
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-gray-400 text-sm mb-1">Conversion Rate</p>
                  <h3 className="text-2xl font-bold text-white">3.24%</h3>
                  <p className="text-green-500 text-xs mt-1">+0.5% improvement</p>
                </div>
                <div className="w-12 h-12 rounded-lg bg-orange-500/10 flex items-center justify-center">
                  <FiBarChart2 className="h-6 w-6 text-orange-500" />
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        <div className="grid lg:grid-cols-2 gap-6">
          <Card>
            <CardTitle className="p-6 pb-0">Revenue Trends</CardTitle>
            <CardContent className="p-6">
              <div className="h-64 flex items-center justify-center border-2 border-dashed border-dark-700 rounded-lg">
                <p className="text-gray-500">Chart placeholder - Integrate chart library</p>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardTitle className="p-6 pb-0">User Growth</CardTitle>
            <CardContent className="p-6">
              <div className="h-64 flex items-center justify-center border-2 border-dashed border-dark-700 rounded-lg">
                <p className="text-gray-500">Chart placeholder - Integrate chart library</p>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default Analytics;
