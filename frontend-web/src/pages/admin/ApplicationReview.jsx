import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  FiCheckCircle,
  FiXCircle,
  FiArrowLeft,
  FiImage,
  FiFileText,
  FiUser,
  FiBriefcase,
  FiSave
} from 'react-icons/fi';
import { applicationService } from '../../services/applicationService';
import Card, { CardContent, CardTitle } from '../../components/ui/Card';
import Loading from '../../components/ui/Loading';
import Button from '../../components/ui/Button';
import toast from 'react-hot-toast';

const ApplicationReview = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [application, setApplication] = useState(null);
  const [loading, setLoading] = useState(true);
  const [processing, setProcessing] = useState(false);

  // Review state
  const [ghanaCardVerified, setGhanaCardVerified] = useState(false);
  const [driversLicenseVerified, setDriversLicenseVerified] = useState(false);
  const [businessVerified, setBusinessVerified] = useState(false);
  const [adminNotes, setAdminNotes] = useState('');
  const [rejectionReason, setRejectionReason] = useState('');
  const [showRejectModal, setShowRejectModal] = useState(false);

  useEffect(() => {
    fetchApplication();
  }, [id]);

  const fetchApplication = async () => {
    try {
      setLoading(true);
      const data = await applicationService.getApplication(id);
      setApplication(data);

      // Set initial verification states
      setGhanaCardVerified(data.ghana_card_verified);
      setDriversLicenseVerified(data.drivers_license_verified);
      setBusinessVerified(data.business_verified);
      setAdminNotes(data.admin_notes || '');
    } catch (error) {
      toast.error('Failed to load application');
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const handleReview = async () => {
    try {
      setProcessing(true);
      await applicationService.reviewApplication(id, {
        ghana_card_verified: ghanaCardVerified,
        drivers_license_verified: driversLicenseVerified,
        business_verified: businessVerified,
        admin_notes: adminNotes
      });
      toast.success('Application reviewed successfully');
      await fetchApplication();
    } catch (error) {
      toast.error('Failed to review application');
      console.error(error);
    } finally {
      setProcessing(false);
    }
  };

  const handleApprove = async () => {
    if (!application.all_documents_verified) {
      toast.error('Please verify all required documents before approving');
      return;
    }

    if (!window.confirm('Are you sure you want to approve this application? This will upgrade the user\'s role.')) {
      return;
    }

    try {
      setProcessing(true);
      await applicationService.approveApplication(id, adminNotes);
      toast.success('Application approved! User has been upgraded and notified.');
      navigate('/admin/applications');
    } catch (error) {
      toast.error('Failed to approve application');
      console.error(error);
    } finally {
      setProcessing(false);
    }
  };

  const handleReject = async () => {
    if (!rejectionReason.trim()) {
      toast.error('Please provide a rejection reason');
      return;
    }

    try {
      setProcessing(true);
      await applicationService.rejectApplication(id, rejectionReason, adminNotes);
      toast.success('Application rejected. User has been notified.');
      setShowRejectModal(false);
      navigate('/admin/applications');
    } catch (error) {
      toast.error('Failed to reject application');
      console.error(error);
    } finally {
      setProcessing(false);
    }
  };

  const getStatusBadge = (status) => {
    const statusConfig = {
      pending: { color: 'bg-yellow-500/10 text-yellow-500', text: 'Pending' },
      under_review: { color: 'bg-blue-500/10 text-blue-500', text: 'Under Review' },
      approved: { color: 'bg-green-500/10 text-green-500', text: 'Approved' },
      rejected: { color: 'bg-red-500/10 text-red-500', text: 'Rejected' }
    };

    const config = statusConfig[status] || statusConfig.pending;
    return (
      <span className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${config.color}`}>
        {config.text}
      </span>
    );
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const DocumentPreview = ({ label, url, verified, onVerifyToggle }) => (
    <div className="space-y-2">
      <div className="flex items-center justify-between">
        <label className="text-sm font-medium text-gray-300">{label}</label>
        <button
          onClick={onVerifyToggle}
          className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-sm font-medium transition-colors ${
            verified
              ? 'bg-green-500/10 text-green-500 hover:bg-green-500/20'
              : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
          }`}
          disabled={application?.status === 'approved' || application?.status === 'rejected'}
        >
          {verified ? (
            <>
              <FiCheckCircle className="h-4 w-4" />
              Verified
            </>
          ) : (
            <>
              <FiXCircle className="h-4 w-4" />
              Not Verified
            </>
          )}
        </button>
      </div>
      {url ? (
        <div className="relative group">
          <img
            src={url}
            alt={label}
            className="w-full h-64 object-cover rounded-lg border border-dark-700"
          />
          <a
            href={url}
            target="_blank"
            rel="noopener noreferrer"
            className="absolute inset-0 bg-black/50 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center rounded-lg"
          >
            <span className="text-white font-medium">View Full Size</span>
          </a>
        </div>
      ) : (
        <div className="w-full h-64 bg-dark-800 rounded-lg border border-dark-700 flex items-center justify-center">
          <FiImage className="h-12 w-12 text-gray-600" />
        </div>
      )}
    </div>
  );

  if (loading) {
    return <Loading fullScreen />;
  }

  if (!application) {
    return (
      <div className="min-h-screen bg-midnight-950 pt-20 pb-12 px-4 flex items-center justify-center">
        <Card>
          <CardContent className="p-12 text-center">
            <FiFileText className="h-16 w-16 text-gray-600 mx-auto mb-4" />
            <h3 className="text-xl font-semibold text-white mb-2">Application Not Found</h3>
            <Button onClick={() => navigate('/admin/applications')} className="mt-4">
              Back to Applications
            </Button>
          </CardContent>
        </Card>
      </div>
    );
  }

  const isEditable = application.status !== 'approved' && application.status !== 'rejected';

  return (
    <div className="p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <Button
            variant="ghost"
            onClick={() => navigate('/admin/applications')}
            className="mb-4"
          >
            <FiArrowLeft className="h-4 w-4 mr-2" />
            Back to Applications
          </Button>

          <div className="flex items-start justify-between gap-4">
            <div>
              <h1 className="text-4xl font-bold text-white mb-2">
                Application #{application.id}
              </h1>
              <p className="text-gray-400">
                {application.application_type.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}
              </p>
            </div>
            {getStatusBadge(application.status)}
          </div>
        </div>

        <div className="grid lg:grid-cols-3 gap-6">
          {/* Main Content */}
          <div className="lg:col-span-2 space-y-6">
            {/* Ghana Card Documents */}
            <Card>
              <CardTitle className="px-6 pt-6 pb-4">
                <div className="flex items-center gap-2">
                  <FiUser className="h-5 w-5 text-red-500" />
                  Ghana Card Verification (Required for All)
                </div>
              </CardTitle>
              <CardContent className="px-6 pb-6 space-y-6">
                <div>
                  <label className="text-sm font-medium text-gray-300 block mb-2">Ghana Card Number</label>
                  <div className="text-xl font-bold text-white">{application.ghana_card_number}</div>
                </div>

                <div className="grid md:grid-cols-2 gap-6">
                  <DocumentPreview
                    label="Ghana Card (Front)"
                    url={application.ghana_card_front}
                    verified={ghanaCardVerified}
                    onVerifyToggle={() => setGhanaCardVerified(!ghanaCardVerified)}
                  />
                  <DocumentPreview
                    label="Ghana Card (Back)"
                    url={application.ghana_card_back}
                    verified={ghanaCardVerified}
                    onVerifyToggle={() => setGhanaCardVerified(!ghanaCardVerified)}
                  />
                </div>

                <DocumentPreview
                  label="Selfie with Ghana Card"
                  url={application.selfie_with_card}
                  verified={ghanaCardVerified}
                  onVerifyToggle={() => setGhanaCardVerified(!ghanaCardVerified)}
                />
              </CardContent>
            </Card>

            {/* Driver's License (if applicable) */}
            {(application.drivers_license_number || application.application_type === 'rental_manager') && (
              <Card>
                <CardTitle className="px-6 pt-6 pb-4">
                  <div className="flex items-center gap-2">
                    <FiFileText className="h-5 w-5 text-red-500" />
                    Driver's License
                    {application.application_type === 'rental_manager' && (
                      <span className="text-xs bg-red-500/10 text-red-500 px-2 py-0.5 rounded">Required</span>
                    )}
                  </div>
                </CardTitle>
                <CardContent className="px-6 pb-6 space-y-6">
                  {application.drivers_license_number && (
                    <div>
                      <label className="text-sm font-medium text-gray-300 block mb-2">License Number</label>
                      <div className="text-lg font-bold text-white">{application.drivers_license_number}</div>
                    </div>
                  )}

                  <div className="grid md:grid-cols-2 gap-6">
                    <DocumentPreview
                      label="License (Front)"
                      url={application.drivers_license_front}
                      verified={driversLicenseVerified}
                      onVerifyToggle={() => setDriversLicenseVerified(!driversLicenseVerified)}
                    />
                    <DocumentPreview
                      label="License (Back)"
                      url={application.drivers_license_back}
                      verified={driversLicenseVerified}
                      onVerifyToggle={() => setDriversLicenseVerified(!driversLicenseVerified)}
                    />
                  </div>
                </CardContent>
              </Card>
            )}

            {/* Business Documents (for Vendor) */}
            {application.application_type === 'vendor' && (
              <Card>
                <CardTitle className="px-6 pt-6 pb-4">
                  <div className="flex items-center gap-2">
                    <FiBriefcase className="h-5 w-5 text-red-500" />
                    Business Information
                    <span className="text-xs bg-red-500/10 text-red-500 px-2 py-0.5 rounded">Required</span>
                  </div>
                </CardTitle>
                <CardContent className="px-6 pb-6 space-y-6">
                  <div className="grid md:grid-cols-2 gap-4">
                    <div>
                      <label className="text-sm font-medium text-gray-300 block mb-2">Business Name</label>
                      <div className="text-lg font-semibold text-white">{application.business_name}</div>
                    </div>
                    <div>
                      <label className="text-sm font-medium text-gray-300 block mb-2">Registration Number</label>
                      <div className="text-lg font-semibold text-white">{application.business_registration_number}</div>
                    </div>
                    {application.business_phone && (
                      <div>
                        <label className="text-sm font-medium text-gray-300 block mb-2">Business Phone</label>
                        <div className="text-white">{application.business_phone}</div>
                      </div>
                    )}
                    {application.business_email && (
                      <div>
                        <label className="text-sm font-medium text-gray-300 block mb-2">Business Email</label>
                        <div className="text-white">{application.business_email}</div>
                      </div>
                    )}
                  </div>

                  {application.business_address && (
                    <div>
                      <label className="text-sm font-medium text-gray-300 block mb-2">Business Address</label>
                      <div className="text-white">
                        {application.business_address.street}, {application.business_address.city}
                        <br />
                        {application.business_address.region} - {application.business_address.gps}
                      </div>
                    </div>
                  )}

                  <DocumentPreview
                    label="Business Registration Document"
                    url={application.business_registration_document}
                    verified={businessVerified}
                    onVerifyToggle={() => setBusinessVerified(!businessVerified)}
                  />
                </CardContent>
              </Card>
            )}

            {/* Technician Details */}
            {application.application_type === 'technician' && (
              <Card>
                <CardTitle className="px-6 pt-6 pb-4">
                  <div className="flex items-center gap-2">
                    <FiBriefcase className="h-5 w-5 text-red-500" />
                    Technician Details
                  </div>
                </CardTitle>
                <CardContent className="px-6 pb-6 space-y-4">
                  {application.years_experience && (
                    <div>
                      <label className="text-sm font-medium text-gray-300 block mb-2">Years of Experience</label>
                      <div className="text-lg font-semibold text-white">{application.years_experience} years</div>
                    </div>
                  )}

                  {application.specializations && (
                    <div>
                      <label className="text-sm font-medium text-gray-300 block mb-2">Specializations</label>
                      <div className="flex flex-wrap gap-2">
                        {application.specializations.map((spec, idx) => (
                          <span key={idx} className="px-3 py-1 bg-red-500/10 text-red-500 rounded-full text-sm">
                            {spec}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}

                  {application.bio && (
                    <div>
                      <label className="text-sm font-medium text-gray-300 block mb-2">Bio</label>
                      <div className="text-white whitespace-pre-wrap">{application.bio}</div>
                    </div>
                  )}
                </CardContent>
              </Card>
            )}
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Application Info */}
            <Card>
              <CardTitle className="px-6 pt-6 pb-4">Application Info</CardTitle>
              <CardContent className="px-6 pb-6 space-y-4 text-sm">
                <div>
                  <div className="text-gray-400 mb-1">Submitted</div>
                  <div className="text-white font-medium">{formatDate(application.created_at)}</div>
                </div>

                {application.reviewed_at && (
                  <div>
                    <div className="text-gray-400 mb-1">Reviewed</div>
                    <div className="text-white font-medium">{formatDate(application.reviewed_at)}</div>
                  </div>
                )}

                <div>
                  <div className="text-gray-400 mb-1">All Documents Verified</div>
                  <div className={`font-medium ${application.all_documents_verified ? 'text-green-500' : 'text-gray-400'}`}>
                    {application.all_documents_verified ? 'Yes' : 'No'}
                  </div>
                </div>

                {application.applicant_notes && (
                  <div>
                    <div className="text-gray-400 mb-1">Applicant Notes</div>
                    <div className="text-white">{application.applicant_notes}</div>
                  </div>
                )}
              </CardContent>
            </Card>

            {/* Admin Notes */}
            <Card>
              <CardTitle className="px-6 pt-6 pb-4">Admin Notes</CardTitle>
              <CardContent className="px-6 pb-6">
                <textarea
                  value={adminNotes}
                  onChange={(e) => setAdminNotes(e.target.value)}
                  placeholder="Add notes about this application..."
                  className="w-full h-32 px-4 py-3 bg-dark-800 border border-dark-700 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-red-500 resize-none"
                  disabled={!isEditable}
                />
              </CardContent>
            </Card>

            {/* Actions */}
            {isEditable && (
              <Card>
                <CardTitle className="px-6 pt-6 pb-4">Actions</CardTitle>
                <CardContent className="px-6 pb-6 space-y-3">
                  <Button
                    onClick={handleReview}
                    variant="outline"
                    className="w-full"
                    disabled={processing}
                  >
                    <FiSave className="h-4 w-4 mr-2" />
                    Save Review
                  </Button>

                  <Button
                    onClick={handleApprove}
                    variant="primary"
                    className="w-full"
                    disabled={processing || !application.all_documents_verified}
                  >
                    <FiCheckCircle className="h-4 w-4 mr-2" />
                    Approve Application
                  </Button>

                  <Button
                    onClick={() => setShowRejectModal(true)}
                    variant="danger"
                    className="w-full"
                    disabled={processing}
                  >
                    <FiXCircle className="h-4 w-4 mr-2" />
                    Reject Application
                  </Button>
                </CardContent>
              </Card>
            )}
          </div>
        </div>
      </div>

      {/* Reject Modal */}
      {showRejectModal && (
        <div className="fixed inset-0 bg-black/70 flex items-center justify-center z-50 p-4">
          <Card className="max-w-lg w-full">
            <CardTitle className="px-6 pt-6 pb-4">Reject Application</CardTitle>
            <CardContent className="px-6 pb-6 space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  Rejection Reason (will be sent to applicant)
                </label>
                <textarea
                  value={rejectionReason}
                  onChange={(e) => setRejectionReason(e.target.value)}
                  placeholder="E.g., Ghana Card image is not clear. Please resubmit with clearer photo."
                  className="w-full h-32 px-4 py-3 bg-dark-800 border border-dark-700 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-red-500 resize-none"
                />
              </div>

              <div className="flex gap-3">
                <Button
                  onClick={() => setShowRejectModal(false)}
                  variant="ghost"
                  className="flex-1"
                  disabled={processing}
                >
                  Cancel
                </Button>
                <Button
                  onClick={handleReject}
                  variant="danger"
                  className="flex-1"
                  disabled={processing || !rejectionReason.trim()}
                >
                  Reject Application
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  );
};

export default ApplicationReview;
