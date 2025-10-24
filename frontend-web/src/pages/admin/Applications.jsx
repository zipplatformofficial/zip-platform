import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import {
  FiFileText,
  FiClock,
  FiCheckCircle,
  FiXCircle,
  FiEye,
  FiFilter
} from 'react-icons/fi';
import { applicationService } from '../../services/applicationService';
import Card, { CardContent, CardTitle } from '../../components/ui/Card';
import Loading from '../../components/ui/Loading';
import Button from '../../components/ui/Button';
import toast from 'react-hot-toast';

const Applications = () => {
  const [applications, setApplications] = useState([]);
  const [loading, setLoading] = useState(true);
  const [statusFilter, setStatusFilter] = useState('');
  const [typeFilter, setTypeFilter] = useState('');
  const [stats, setStats] = useState({
    pending: 0,
    under_review: 0,
    approved: 0,
    rejected: 0
  });

  useEffect(() => {
    fetchApplications();
  }, [statusFilter, typeFilter]);

  const fetchApplications = async () => {
    try {
      setLoading(true);
      const data = await applicationService.getApplications({
        status: statusFilter || undefined,
        type: typeFilter || undefined,
        limit: 50
      });
      setApplications(data);

      // Calculate stats
      const newStats = {
        pending: data.filter(app => app.status === 'pending').length,
        under_review: data.filter(app => app.status === 'under_review').length,
        approved: data.filter(app => app.status === 'approved').length,
        rejected: data.filter(app => app.status === 'rejected').length
      };
      setStats(newStats);
    } catch (error) {
      toast.error('Failed to load applications');
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const getStatusBadge = (status) => {
    const statusConfig = {
      pending: { color: 'bg-yellow-500/10 text-yellow-500', icon: FiClock, text: 'Pending' },
      under_review: { color: 'bg-blue-500/10 text-blue-500', icon: FiEye, text: 'Under Review' },
      approved: { color: 'bg-green-500/10 text-green-500', icon: FiCheckCircle, text: 'Approved' },
      rejected: { color: 'bg-red-500/10 text-red-500', icon: FiXCircle, text: 'Rejected' }
    };

    const config = statusConfig[status] || statusConfig.pending;
    const Icon = config.icon;

    return (
      <span className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-medium ${config.color}`}>
        <Icon className="h-3.5 w-3.5" />
        {config.text}
      </span>
    );
  };

  const getTypeBadge = (type) => {
    const typeConfig = {
      technician: { color: 'bg-purple-500/10 text-purple-500', text: 'Technician' },
      vendor: { color: 'bg-pink-500/10 text-pink-500', text: 'Vendor' },
      rental_manager: { color: 'bg-cyan-500/10 text-cyan-500', text: 'Rental Manager' }
    };

    const config = typeConfig[type] || typeConfig.technician;

    return (
      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${config.color}`}>
        {config.text}
      </span>
    );
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  if (loading) {
    return <Loading fullScreen />;
  }

  return (
    <div className="p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-white mb-2">Role Applications</h1>
          <p className="text-gray-400">Review and verify user role applications</p>
        </div>

        {/* Stats Cards */}
        <div className="grid md:grid-cols-4 gap-4 mb-6">
          <Card hover className="cursor-pointer" onClick={() => setStatusFilter('pending')}>
            <CardContent className="p-4">
              <div className="flex items-center gap-3">
                <div className="w-12 h-12 rounded-lg bg-yellow-500/10 flex items-center justify-center">
                  <FiClock className="h-6 w-6 text-yellow-500" />
                </div>
                <div>
                  <div className="text-2xl font-bold text-white">{stats.pending}</div>
                  <div className="text-sm text-gray-400">Pending</div>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card hover className="cursor-pointer" onClick={() => setStatusFilter('under_review')}>
            <CardContent className="p-4">
              <div className="flex items-center gap-3">
                <div className="w-12 h-12 rounded-lg bg-blue-500/10 flex items-center justify-center">
                  <FiEye className="h-6 w-6 text-blue-500" />
                </div>
                <div>
                  <div className="text-2xl font-bold text-white">{stats.under_review}</div>
                  <div className="text-sm text-gray-400">Under Review</div>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card hover className="cursor-pointer" onClick={() => setStatusFilter('approved')}>
            <CardContent className="p-4">
              <div className="flex items-center gap-3">
                <div className="w-12 h-12 rounded-lg bg-green-500/10 flex items-center justify-center">
                  <FiCheckCircle className="h-6 w-6 text-green-500" />
                </div>
                <div>
                  <div className="text-2xl font-bold text-white">{stats.approved}</div>
                  <div className="text-sm text-gray-400">Approved</div>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card hover className="cursor-pointer" onClick={() => setStatusFilter('rejected')}>
            <CardContent className="p-4">
              <div className="flex items-center gap-3">
                <div className="w-12 h-12 rounded-lg bg-red-500/10 flex items-center justify-center">
                  <FiXCircle className="h-6 w-6 text-red-500" />
                </div>
                <div>
                  <div className="text-2xl font-bold text-white">{stats.rejected}</div>
                  <div className="text-sm text-gray-400">Rejected</div>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Filters */}
        <Card className="mb-6">
          <CardContent className="p-4">
            <div className="flex flex-wrap gap-4 items-center">
              <div className="flex items-center gap-2">
                <FiFilter className="text-gray-400" />
                <span className="text-sm font-medium text-gray-300">Filters:</span>
              </div>

              <select
                value={statusFilter}
                onChange={(e) => setStatusFilter(e.target.value)}
                className="px-4 py-2 bg-dark-800 border border-dark-700 rounded-lg text-white text-sm focus:outline-none focus:ring-2 focus:ring-red-500"
              >
                <option value="">All Status</option>
                <option value="pending">Pending</option>
                <option value="under_review">Under Review</option>
                <option value="approved">Approved</option>
                <option value="rejected">Rejected</option>
              </select>

              <select
                value={typeFilter}
                onChange={(e) => setTypeFilter(e.target.value)}
                className="px-4 py-2 bg-dark-800 border border-dark-700 rounded-lg text-white text-sm focus:outline-none focus:ring-2 focus:ring-red-500"
              >
                <option value="">All Types</option>
                <option value="technician">Technician</option>
                <option value="vendor">Vendor</option>
                <option value="rental_manager">Rental Manager</option>
              </select>

              {(statusFilter || typeFilter) && (
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => {
                    setStatusFilter('');
                    setTypeFilter('');
                  }}
                >
                  Clear Filters
                </Button>
              )}

              <div className="ml-auto text-sm text-gray-400">
                Showing {applications.length} applications
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Applications List */}
        <div className="space-y-4">
          {applications.length === 0 ? (
            <Card>
              <CardContent className="p-12 text-center">
                <FiFileText className="h-16 w-16 text-gray-600 mx-auto mb-4" />
                <h3 className="text-xl font-semibold text-white mb-2">No applications found</h3>
                <p className="text-gray-400">
                  {statusFilter || typeFilter
                    ? 'Try adjusting your filters'
                    : 'Applications will appear here when users apply for roles'}
                </p>
              </CardContent>
            </Card>
          ) : (
            applications.map((application) => (
              <Card key={application.id} hover>
                <CardContent className="p-6">
                  <div className="flex items-start justify-between gap-4">
                    <div className="flex-1">
                      <div className="flex items-center gap-3 mb-2">
                        <h3 className="text-lg font-semibold text-white">
                          Application #{application.id}
                        </h3>
                        {getTypeBadge(application.application_type)}
                        {getStatusBadge(application.status)}
                      </div>

                      <div className="grid md:grid-cols-2 gap-4 mt-4">
                        <div>
                          <div className="text-sm text-gray-400 mb-1">Ghana Card Number</div>
                          <div className="text-white font-medium">{application.ghana_card_number}</div>
                        </div>

                        <div>
                          <div className="text-sm text-gray-400 mb-1">Submitted</div>
                          <div className="text-white font-medium">{formatDate(application.created_at)}</div>
                        </div>

                        {application.reviewed_at && (
                          <div>
                            <div className="text-sm text-gray-400 mb-1">Reviewed</div>
                            <div className="text-white font-medium">{formatDate(application.reviewed_at)}</div>
                          </div>
                        )}

                        {application.rejection_reason && (
                          <div className="md:col-span-2">
                            <div className="text-sm text-gray-400 mb-1">Rejection Reason</div>
                            <div className="text-red-400 font-medium">{application.rejection_reason}</div>
                          </div>
                        )}
                      </div>

                      {/* Document Verification Status */}
                      <div className="mt-4 flex flex-wrap gap-2">
                        {application.ghana_card_verified && (
                          <span className="inline-flex items-center gap-1 px-2 py-1 bg-green-500/10 text-green-500 rounded text-xs">
                            <FiCheckCircle className="h-3 w-3" />
                            Ghana Card Verified
                          </span>
                        )}
                        {application.drivers_license_verified && (
                          <span className="inline-flex items-center gap-1 px-2 py-1 bg-green-500/10 text-green-500 rounded text-xs">
                            <FiCheckCircle className="h-3 w-3" />
                            License Verified
                          </span>
                        )}
                        {application.business_verified && (
                          <span className="inline-flex items-center gap-1 px-2 py-1 bg-green-500/10 text-green-500 rounded text-xs">
                            <FiCheckCircle className="h-3 w-3" />
                            Business Verified
                          </span>
                        )}
                      </div>
                    </div>

                    <Link to={`/admin/applications/${application.id}`}>
                      <Button variant="outline" size="sm">
                        <FiEye className="h-4 w-4 mr-2" />
                        Review
                      </Button>
                    </Link>
                  </div>
                </CardContent>
              </Card>
            ))
          )}
        </div>
      </div>
    </div>
  );
};

export default Applications;
