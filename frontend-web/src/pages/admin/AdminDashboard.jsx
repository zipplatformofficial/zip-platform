import React, { useState, useEffect } from 'react';
import {
  FiUsers, FiEye, FiDollarSign, FiShoppingBag, FiTrendingUp, FiTrendingDown,
  FiAlertTriangle, FiCheckCircle, FiClock, FiActivity, FiShield, FiPackage,
  FiTruck, FiTool, FiFileText, FiMapPin, FiCreditCard, FiZap
} from 'react-icons/fi';
import {
  LineChart, Line, BarChart, Bar, PieChart, Pie, Cell,
  XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Area, AreaChart
} from 'recharts';
import Card, { CardContent, CardTitle } from '../../components/ui/Card';
import { adminService } from '../../services/adminService';
import toast from 'react-hot-toast';

const AdminDashboard = () => {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchStats();
    // Refresh stats every 30 seconds
    const interval = setInterval(fetchStats, 30000);
    return () => clearInterval(interval);
  }, []);

  const fetchStats = async () => {
    try {
      setError(null);
      const data = await adminService.getStats();
      setStats(data);
    } catch (error) {
      setError(error.message || 'Failed to load dashboard stats');
      toast.error('Failed to load dashboard stats');
      console.error('Stats error:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="p-8 flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-t-2 border-b-2 border-red-500 mx-auto mb-4"></div>
          <p className="text-gray-400">Loading dashboard...</p>
        </div>
      </div>
    );
  }

  if (error && !stats) {
    return (
      <div className="p-8 flex items-center justify-center min-h-screen">
        <div className="text-center">
          <FiAlertTriangle className="h-16 w-16 text-red-500 mx-auto mb-4" />
          <h2 className="text-2xl font-bold text-white mb-2">Failed to Load Dashboard</h2>
          <p className="text-gray-400 mb-6">{error}</p>
          <button
            onClick={fetchStats}
            className="px-6 py-3 bg-red-500 text-white rounded-lg hover:bg-red-600 transition-colors"
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  if (!stats) {
    return (
      <div className="p-8 flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-t-2 border-b-2 border-red-500 mx-auto mb-4"></div>
          <p className="text-gray-400">Loading dashboard...</p>
        </div>
      </div>
    );
  }

  // Safe defaults for stats object
  const safeStats = {
    users: {
      total: 0,
      active: 0,
      verified: 0,
      new_today: 0,
      by_role: {},
      ...stats.users
    },
    visitors: {
      total: 0,
      today: 0,
      total_page_views: 0,
      today_page_views: 0,
      ...stats.visitors
    },
    bookings: {
      service_bookings: { total: 0, today: 0, ...(stats.bookings?.service_bookings || {}) },
      rental_bookings: { total: 0, today: 0, ...(stats.bookings?.rental_bookings || {}) },
      store_orders: { total: 0, today: 0, ...(stats.bookings?.store_orders || {}) },
      total: 0,
      today_total: 0,
      ...stats.bookings
    },
    revenue: {
      total: 0,
      today: 0,
      platform_commission: 0,
      currency: 'GHS',
      ...stats.revenue
    },
    payments: {
      total: 0,
      successful: 0,
      success_rate: 0,
      failed_today: 0,
      ...stats.payments
    },
    catalog: {
      products: { total: 0, active: 0 },
      rental_vehicles: { total: 0, available: 0 },
      maintenance_services: 0,
      ...stats.catalog
    },
    providers: {
      technicians: { total: 0, verified: 0, active_today: 0, ...(stats.providers?.technicians || {}) },
      vendors: { total: 0, verified: 0, ...(stats.providers?.vendors || {}) },
      ...stats.providers
    },
    applications: {
      total: 0,
      pending: 0,
      under_review: 0,
      approved: 0,
      rejected: 0,
      new_today: 0,
      ...stats.applications
    },
    fraud: {
      total_alerts: 0,
      active_alerts: 0,
      confirmed_cases: 0,
      alerts_today: 0,
      total_amount_involved: 0,
      blocked_amount: 0,
      by_type: {},
      ...stats.fraud
    },
    recent_activity: {
      payments: [],
      applications: [],
      fraud_alerts: [],
      ...stats.recent_activity
    },
    system_health: {
      status: 'unknown',
      total_records: 0,
      active_sessions: 0,
      error_rate: 0,
      ...stats.system_health
    },
    trends: {
      dates: [],
      revenue: [],
      users: [],
      visitors: [],
      bookings: [],
      fraud_alerts: [],
      ...stats.trends
    }
  };

  // Colors for charts
  const COLORS = {
    primary: '#EF4444',
    secondary: '#F97316',
    success: '#10B981',
    warning: '#F59E0B',
    danger: '#DC2626',
    info: '#3B82F6',
    purple: '#8B5CF6',
    pink: '#EC4899',
  };

  const CHART_COLORS = [
    COLORS.primary,
    COLORS.secondary,
    COLORS.success,
    COLORS.info,
    COLORS.purple,
    COLORS.pink,
    COLORS.warning,
  ];

  // Calculate growth percentages (mock for now - would compare with previous period)
  const calculateGrowth = (current, previous = current * 0.8) => {
    if (previous === 0) return 0;
    return ((current - previous) / previous * 100).toFixed(1);
  };

  // Prepare fraud data for pie chart
  const fraudData = Object.entries(safeStats.fraud.by_type).map(([name, value]) => ({
    name: name.replace(/_/g, ' ').toUpperCase(),
    value
  }));

  // Prepare role distribution data
  const roleData = Object.entries(safeStats.users.by_role).map(([name, value]) => ({
    name: name.toUpperCase(),
    value
  }));

  return (
    <div className="p-8 bg-midnight-950 min-h-screen">
      <div className="max-w-[1600px] mx-auto">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between mb-2">
            <h1 className="text-4xl font-bold text-white">Admin Dashboard</h1>
            <div className="flex items-center gap-2">
              <div className={`px-3 py-1 rounded-full flex items-center gap-2 ${
                safeStats.system_health.status === 'healthy'
                  ? 'bg-green-500/10 text-green-500'
                  : 'bg-red-500/10 text-red-500'
              }`}>
                <div className="w-2 h-2 rounded-full bg-current animate-pulse"></div>
                <span className="text-sm font-medium">{safeStats.system_health.status}</span>
              </div>
            </div>
          </div>
          <p className="text-gray-400">Comprehensive platform analytics and monitoring</p>
        </div>

        {/* Critical Alerts */}
        {safeStats.fraud.active_alerts > 0 && (
          <div className="mb-6 p-4 bg-red-500/10 border border-red-500/30 rounded-lg">
            <div className="flex items-center gap-3">
              <FiAlertTriangle className="h-6 w-6 text-red-500" />
              <div className="flex-1">
                <h3 className="text-red-500 font-semibold">
                  {safeStats.fraud.active_alerts} Active Fraud Alert{safeStats.fraud.active_alerts > 1 ? 's' : ''}
                </h3>
                <p className="text-red-400 text-sm">
                  GH₵ {safeStats.fraud.blocked_amount.toLocaleString()} blocked • Immediate attention required
                </p>
              </div>
              <button className="px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 transition-colors">
                Review Alerts
              </button>
            </div>
          </div>
        )}

        {/* Key Metrics - Top Row */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {/* Total Revenue */}
          <Card hover className="bg-gradient-to-br from-red-500/10 to-orange-500/10 border-red-500/20">
            <CardContent className="p-6">
              <div className="flex items-center justify-between mb-4">
                <div className="w-12 h-12 rounded-lg bg-gradient-to-br from-red-500 to-orange-500 flex items-center justify-center">
                  <FiDollarSign className="h-6 w-6 text-white" />
                </div>
                <div className="flex items-center gap-1 text-green-500 text-sm font-medium">
                  <FiTrendingUp className="h-4 w-4" />
                  +{calculateGrowth(safeStats.revenue.total)}%
                </div>
              </div>
              <h3 className="text-gray-400 text-sm font-medium mb-1">Total Revenue</h3>
              <p className="text-3xl font-bold text-white mb-1">
                GH₵ {safeStats.revenue.total.toLocaleString()}
              </p>
              <p className="text-green-500 text-sm">
                +GH₵ {safeStats.revenue.today.toLocaleString()} today
              </p>
            </CardContent>
          </Card>

          {/* Total Users */}
          <Card hover className="bg-gradient-to-br from-blue-500/10 to-cyan-500/10 border-blue-500/20">
            <CardContent className="p-6">
              <div className="flex items-center justify-between mb-4">
                <div className="w-12 h-12 rounded-lg bg-gradient-to-br from-blue-500 to-cyan-500 flex items-center justify-center">
                  <FiUsers className="h-6 w-6 text-white" />
                </div>
                <div className="flex items-center gap-1 text-green-500 text-sm font-medium">
                  <FiTrendingUp className="h-4 w-4" />
                  +{calculateGrowth(safeStats.users.total)}%
                </div>
              </div>
              <h3 className="text-gray-400 text-sm font-medium mb-1">Total Users</h3>
              <p className="text-3xl font-bold text-white mb-1">
                {safeStats.users.total.toLocaleString()}
              </p>
              <p className="text-blue-400 text-sm">
                {safeStats.users.active.toLocaleString()} active • {safeStats.users.new_today} new today
              </p>
            </CardContent>
          </Card>

          {/* Total Visitors */}
          <Card hover className="bg-gradient-to-br from-purple-500/10 to-pink-500/10 border-purple-500/20">
            <CardContent className="p-6">
              <div className="flex items-center justify-between mb-4">
                <div className="w-12 h-12 rounded-lg bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center">
                  <FiEye className="h-6 w-6 text-white" />
                </div>
                <div className="flex items-center gap-1 text-green-500 text-sm font-medium">
                  <FiActivity className="h-4 w-4" />
                  Live
                </div>
              </div>
              <h3 className="text-gray-400 text-sm font-medium mb-1">Total Visitors</h3>
              <p className="text-3xl font-bold text-white mb-1">
                {safeStats.visitors.total.toLocaleString()}
              </p>
              <p className="text-purple-400 text-sm">
                {safeStats.visitors.today.toLocaleString()} today • {safeStats.visitors.today_page_views.toLocaleString()} views
              </p>
            </CardContent>
          </Card>

          {/* Total Bookings */}
          <Card hover className="bg-gradient-to-br from-green-500/10 to-emerald-500/10 border-green-500/20">
            <CardContent className="p-6">
              <div className="flex items-center justify-between mb-4">
                <div className="w-12 h-12 rounded-lg bg-gradient-to-br from-green-500 to-emerald-500 flex items-center justify-center">
                  <FiShoppingBag className="h-6 w-6 text-white" />
                </div>
                <div className="flex items-center gap-1 text-green-500 text-sm font-medium">
                  <FiTrendingUp className="h-4 w-4" />
                  +{calculateGrowth(safeStats.bookings.total)}%
                </div>
              </div>
              <h3 className="text-gray-400 text-sm font-medium mb-1">Total Bookings</h3>
              <p className="text-3xl font-bold text-white mb-1">
                {safeStats.bookings.total.toLocaleString()}
              </p>
              <p className="text-green-400 text-sm">
                {safeStats.bookings.today_total} new today
              </p>
            </CardContent>
          </Card>
        </div>

        {/* Secondary Metrics Row */}
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4 mb-8">
          <MetricCard
            icon={FiTool}
            label="Maintenance"
            value={safeStats.bookings.service_bookings.total}
            subValue={`${safeStats.bookings.service_bookings.today} today`}
            color="from-yellow-500 to-orange-500"
          />
          <MetricCard
            icon={FiTruck}
            label="Rentals"
            value={safeStats.bookings.rental_bookings.total}
            subValue={`${safeStats.bookings.rental_bookings.today} today`}
            color="from-cyan-500 to-blue-500"
          />
          <MetricCard
            icon={FiPackage}
            label="Store Orders"
            value={safeStats.bookings.store_orders.total}
            subValue={`${safeStats.bookings.store_orders.today} today`}
            color="from-pink-500 to-rose-500"
          />
          <MetricCard
            icon={FiCreditCard}
            label="Success Rate"
            value={`${safeStats.payments.success_rate}%`}
            subValue={`${safeStats.payments.failed_today} failed today`}
            color="from-green-500 to-emerald-500"
          />
          <MetricCard
            icon={FiFileText}
            label="Applications"
            value={safeStats.applications.pending}
            subValue={`${safeStats.applications.new_today} new today`}
            color="from-indigo-500 to-purple-500"
            badge={safeStats.applications.pending}
          />
          <MetricCard
            icon={FiShield}
            label="Fraud Alerts"
            value={safeStats.fraud.total_alerts}
            subValue={`${safeStats.fraud.alerts_today} today`}
            color="from-red-500 to-pink-500"
            isDanger={safeStats.fraud.active_alerts > 0}
          />
        </div>

        {/* Charts Row */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          {/* Revenue Trend */}
          <Card>
            <CardTitle className="p-6 pb-4">
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="text-xl font-bold text-white">Revenue Trend (7 Days)</h3>
                  <p className="text-gray-400 text-sm mt-1">Daily revenue performance</p>
                </div>
                <FiDollarSign className="h-6 w-6 text-gray-400" />
              </div>
            </CardTitle>
            <CardContent className="p-6 pt-0">
              <ResponsiveContainer width="100%" height={250}>
                <AreaChart data={safeStats.trends.dates.map((date, i) => ({
                  date: new Date(date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
                  revenue: safeStats.trends.revenue[i] || 0
                }))}>
                  <defs>
                    <linearGradient id="colorRevenue" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor={COLORS.primary} stopOpacity={0.3}/>
                      <stop offset="95%" stopColor={COLORS.primary} stopOpacity={0}/>
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                  <XAxis dataKey="date" stroke="#64748B" style={{ fontSize: '12px' }} />
                  <YAxis stroke="#64748B" style={{ fontSize: '12px' }} />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: '#1E293B',
                      border: '1px solid #334155',
                      borderRadius: '8px',
                      color: '#fff'
                    }}
                  />
                  <Area
                    type="monotone"
                    dataKey="revenue"
                    stroke={COLORS.primary}
                    strokeWidth={2}
                    fillOpacity={1}
                    fill="url(#colorRevenue)"
                  />
                </AreaChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>

          {/* Visitors & Users Trend */}
          <Card>
            <CardTitle className="p-6 pb-4">
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="text-xl font-bold text-white">Traffic Trend (7 Days)</h3>
                  <p className="text-gray-400 text-sm mt-1">Visitors and active users</p>
                </div>
                <FiActivity className="h-6 w-6 text-gray-400" />
              </div>
            </CardTitle>
            <CardContent className="p-6 pt-0">
              <ResponsiveContainer width="100%" height={250}>
                <LineChart data={safeStats.trends.dates.map((date, i) => ({
                  date: new Date(date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
                  visitors: safeStats.trends.visitors[i] || 0,
                  users: safeStats.trends.users[i] || 0
                }))}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                  <XAxis dataKey="date" stroke="#64748B" style={{ fontSize: '12px' }} />
                  <YAxis stroke="#64748B" style={{ fontSize: '12px' }} />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: '#1E293B',
                      border: '1px solid #334155',
                      borderRadius: '8px',
                      color: '#fff'
                    }}
                  />
                  <Legend />
                  <Line type="monotone" dataKey="visitors" stroke={COLORS.info} strokeWidth={2} name="Visitors" />
                  <Line type="monotone" dataKey="users" stroke={COLORS.success} strokeWidth={2} name="Active Users" />
                </LineChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </div>

        {/* Second Charts Row */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
          {/* Fraud Detection by Type */}
          {fraudData.length > 0 && (
            <Card>
              <CardTitle className="p-6 pb-4">
                <div className="flex items-center justify-between">
                  <div>
                    <h3 className="text-xl font-bold text-white">Fraud Detection</h3>
                    <p className="text-gray-400 text-sm mt-1">By type</p>
                  </div>
                  <FiShield className="h-6 w-6 text-red-500" />
                </div>
              </CardTitle>
              <CardContent className="p-6 pt-0">
                <ResponsiveContainer width="100%" height={200}>
                  <PieChart>
                    <Pie
                      data={fraudData}
                      cx="50%"
                      cy="50%"
                      labelLine={false}
                      label={({name, percent}) => `${name}: ${(percent * 100).toFixed(0)}%`}
                      outerRadius={80}
                      fill="#8884d8"
                      dataKey="value"
                    >
                      {fraudData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={CHART_COLORS[index % CHART_COLORS.length]} />
                      ))}
                    </Pie>
                    <Tooltip
                      contentStyle={{
                        backgroundColor: '#1E293B',
                        border: '1px solid #334155',
                        borderRadius: '8px',
                        color: '#fff'
                      }}
                    />
                  </PieChart>
                </ResponsiveContainer>
                <div className="mt-4 p-3 bg-red-500/10 border border-red-500/20 rounded-lg">
                  <div className="flex items-center justify-between text-sm">
                    <span className="text-gray-400">Blocked Amount</span>
                    <span className="text-red-500 font-semibold">GH₵ {safeStats.fraud.blocked_amount.toLocaleString()}</span>
                  </div>
                </div>
              </CardContent>
            </Card>
          )}

          {/* User Roles Distribution */}
          {roleData.length > 0 && (
            <Card>
              <CardTitle className="p-6 pb-4">
                <div className="flex items-center justify-between">
                  <div>
                    <h3 className="text-xl font-bold text-white">User Roles</h3>
                    <p className="text-gray-400 text-sm mt-1">Distribution</p>
                  </div>
                  <FiUsers className="h-6 w-6 text-gray-400" />
                </div>
              </CardTitle>
              <CardContent className="p-6 pt-0">
                <ResponsiveContainer width="100%" height={250}>
                  <BarChart data={roleData}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                    <XAxis dataKey="name" stroke="#64748B" style={{ fontSize: '10px' }} angle={-45} textAnchor="end" height={80} />
                    <YAxis stroke="#64748B" style={{ fontSize: '12px' }} />
                    <Tooltip
                      contentStyle={{
                        backgroundColor: '#1E293B',
                        border: '1px solid #334155',
                        borderRadius: '8px',
                        color: '#fff'
                      }}
                    />
                    <Bar dataKey="value" fill={COLORS.primary} radius={[8, 8, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          )}

          {/* Bookings Trend */}
          <Card>
            <CardTitle className="p-6 pb-4">
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="text-xl font-bold text-white">Bookings Trend</h3>
                  <p className="text-gray-400 text-sm mt-1">Last 7 days</p>
                </div>
                <FiShoppingBag className="h-6 w-6 text-gray-400" />
              </div>
            </CardTitle>
            <CardContent className="p-6 pt-0">
              <ResponsiveContainer width="100%" height={250}>
                <LineChart data={safeStats.trends.dates.map((date, i) => ({
                  date: new Date(date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
                  bookings: safeStats.trends.bookings[i] || 0
                }))}>
                  <defs>
                    <linearGradient id="colorBookings" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor={COLORS.success} stopOpacity={0.3}/>
                      <stop offset="95%" stopColor={COLORS.success} stopOpacity={0}/>
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                  <XAxis dataKey="date" stroke="#64748B" style={{ fontSize: '12px' }} />
                  <YAxis stroke="#64748B" style={{ fontSize: '12px' }} />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: '#1E293B',
                      border: '1px solid #334155',
                      borderRadius: '8px',
                      color: '#fff'
                    }}
                  />
                  <Area
                    type="monotone"
                    dataKey="bookings"
                    stroke={COLORS.success}
                    strokeWidth={2}
                    fillOpacity={1}
                    fill="url(#colorBookings)"
                  />
                </LineChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </div>

        {/* Recent Activity & System Health */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Recent Activity Feed */}
          <Card>
            <CardTitle className="p-6 pb-4">
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="text-xl font-bold text-white">Recent Activity</h3>
                  <p className="text-gray-400 text-sm mt-1">Latest platform events</p>
                </div>
                <FiZap className="h-6 w-6 text-gray-400" />
              </div>
            </CardTitle>
            <CardContent className="p-6 pt-0">
              <div className="space-y-3">
                {/* Recent Payments */}
                {safeStats.recent_activity.payments.map((payment) => (
                  <ActivityItem
                    key={`payment-${payment.id}`}
                    icon={FiCreditCard}
                    iconColor={payment.status === 'completed' ? 'text-green-500' : 'text-red-500'}
                    title={`Payment ${payment.status}`}
                    description={`GH₵ ${payment.amount} via ${payment.method.replace(/_/g, ' ')}`}
                    time={new Date(payment.created_at).toLocaleString()}
                  />
                ))}

                {/* Recent Applications */}
                {safeStats.recent_activity.applications.slice(0, 3).map((app) => (
                  <ActivityItem
                    key={`app-${app.id}`}
                    icon={FiFileText}
                    iconColor="text-blue-500"
                    title={`New ${app.role} application`}
                    description={`Status: ${app.status}`}
                    time={new Date(app.created_at).toLocaleString()}
                  />
                ))}

                {/* Recent Fraud Alerts */}
                {safeStats.recent_activity.fraud_alerts.slice(0, 2).map((fraud) => (
                  <ActivityItem
                    key={`fraud-${fraud.id}`}
                    icon={FiAlertTriangle}
                    iconColor="text-red-500"
                    title={`Fraud Alert: ${fraud.type.replace(/_/g, ' ')}`}
                    description={`Severity: ${fraud.severity} • GH₵ ${fraud.amount || 0}`}
                    time={new Date(fraud.created_at).toLocaleString()}
                  />
                ))}
              </div>
            </CardContent>
          </Card>

          {/* System Health & Platform Commission */}
          <div className="space-y-6">
            {/* System Health */}
            <Card>
              <CardTitle className="p-6 pb-4">
                <div className="flex items-center justify-between">
                  <div>
                    <h3 className="text-xl font-bold text-white">System Health</h3>
                    <p className="text-gray-400 text-sm mt-1">Platform status</p>
                  </div>
                  <div className={`w-3 h-3 rounded-full ${
                    safeStats.system_health.status === 'healthy' ? 'bg-green-500' : 'bg-red-500'
                  } animate-pulse`}></div>
                </div>
              </CardTitle>
              <CardContent className="p-6 pt-0">
                <div className="space-y-3">
                  <HealthMetric label="Database Records" value={safeStats.system_health.total_records.toLocaleString()} status="healthy" />
                  <HealthMetric label="Active Sessions" value={safeStats.system_health.active_sessions.toLocaleString()} status="healthy" />
                  <HealthMetric label="Error Rate" value={`${safeStats.system_health.error_rate}%`} status={safeStats.system_health.error_rate < 1 ? "healthy" : "warning"} />
                  <HealthMetric label="System Status" value={safeStats.system_health.status.toUpperCase()} status={safeStats.system_health.status} />
                </div>
              </CardContent>
            </Card>

            {/* Platform Commission */}
            <Card className="bg-gradient-to-br from-green-500/10 to-emerald-500/10 border-green-500/20">
              <CardContent className="p-6">
                <div className="flex items-center justify-between mb-4">
                  <div className="w-14 h-14 rounded-xl bg-gradient-to-br from-green-500 to-emerald-500 flex items-center justify-center">
                    <FiDollarSign className="h-8 w-8 text-white" />
                  </div>
                  <FiTrendingUp className="h-6 w-6 text-green-500" />
                </div>
                <h3 className="text-gray-400 text-sm font-medium mb-2">Platform Commission</h3>
                <p className="text-4xl font-bold text-white mb-2">
                  GH₵ {safeStats.revenue.platform_commission.toLocaleString()}
                </p>
                <p className="text-green-500 text-sm">
                  Total earnings from all transactions
                </p>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
};

// Metric Card Component
const MetricCard = ({ icon: Icon, label, value, subValue, color, badge, isDanger }) => (
  <Card hover className={isDanger ? 'border-red-500/30' : ''}>
    <CardContent className="p-4">
      <div className="flex items-start justify-between mb-3">
        <div className={`w-10 h-10 rounded-lg bg-gradient-to-br ${color} flex items-center justify-center`}>
          <Icon className="h-5 w-5 text-white" />
        </div>
        {badge !== undefined && (
          <span className="px-2 py-0.5 bg-red-500 text-white text-xs rounded-full">{badge}</span>
        )}
      </div>
      <h3 className="text-gray-400 text-xs font-medium mb-1">{label}</h3>
      <p className={`text-2xl font-bold mb-1 ${isDanger ? 'text-red-500' : 'text-white'}`}>{value}</p>
      <p className="text-gray-500 text-xs">{subValue}</p>
    </CardContent>
  </Card>
);

// Activity Item Component
const ActivityItem = ({ icon: Icon, iconColor, title, description, time }) => (
  <div className="flex items-start gap-3 p-3 rounded-lg hover:bg-dark-800/50 transition-colors">
    <div className={`w-8 h-8 rounded-lg bg-dark-800 flex items-center justify-center flex-shrink-0`}>
      <Icon className={`h-4 w-4 ${iconColor}`} />
    </div>
    <div className="flex-1 min-w-0">
      <p className="text-white text-sm font-medium">{title}</p>
      <p className="text-gray-400 text-xs">{description}</p>
      <p className="text-gray-500 text-xs mt-1">{time}</p>
    </div>
  </div>
);

// Health Metric Component
const HealthMetric = ({ label, value, status }) => (
  <div className="flex items-center justify-between p-3 rounded-lg bg-dark-800/50">
    <span className="text-gray-400 text-sm">{label}</span>
    <div className="flex items-center gap-2">
      <span className="text-white font-medium text-sm">{value}</span>
      <FiCheckCircle className={`h-4 w-4 ${
        status === 'healthy' ? 'text-green-500' :
        status === 'warning' ? 'text-yellow-500' : 'text-red-500'
      }`} />
    </div>
  </div>
);

export default AdminDashboard;
