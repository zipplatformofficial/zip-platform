import React, { useState, useEffect } from 'react';
import { FiUser, FiLock, FiBell, FiGlobe, FiCreditCard, FiShield, FiSave } from 'react-icons/fi';
import Sidebar from '../../components/layout/Sidebar';
import Card, { CardContent, CardTitle } from '../../components/ui/Card';
import Loading from '../../components/ui/Loading';
import Button from '../../components/ui/Button';
import Input from '../../components/ui/Input';
import { useAuth } from '../../hooks/useAuth';
import { authService } from '../../services/authService';
import toast from 'react-hot-toast';

const Settings = () => {
  const { user } = useAuth();
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState('account');

  // Account Settings
  const [accountData, setAccountData] = useState({
    full_name: '',
    email: '',
    phone: '',
  });

  // Password Change
  const [passwordData, setPasswordData] = useState({
    current_password: '',
    new_password: '',
    confirm_password: '',
  });

  // Notifications
  const [notifications, setNotifications] = useState({
    email_notifications: true,
    sms_notifications: true,
    booking_reminders: true,
    promotional_emails: false,
  });

  // Language
  const [language, setLanguage] = useState('en');

  useEffect(() => {
    if (user) {
      setAccountData({
        full_name: user.full_name || '',
        email: user.email || '',
        phone: user.phone || '',
      });
      setLanguage(user.language_preference || 'en');
    }
  }, [user]);

  const handleAccountUpdate = async (e) => {
    e.preventDefault();
    try {
      setLoading(true);
      await authService.updateProfile(accountData);
      toast.success('Account information updated successfully');
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to update account');
    } finally {
      setLoading(false);
    }
  };

  const handlePasswordChange = async (e) => {
    e.preventDefault();

    if (passwordData.new_password !== passwordData.confirm_password) {
      toast.error('New passwords do not match');
      return;
    }

    if (passwordData.new_password.length < 8) {
      toast.error('Password must be at least 8 characters');
      return;
    }

    try {
      setLoading(true);
      await authService.changePassword(passwordData.current_password, passwordData.new_password);
      toast.success('Password changed successfully');
      setPasswordData({
        current_password: '',
        new_password: '',
        confirm_password: '',
      });
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to change password');
    } finally {
      setLoading(false);
    }
  };

  const handleNotificationsUpdate = async () => {
    try {
      setLoading(true);
      // This endpoint would need to be implemented on the backend
      toast.success('Notification preferences updated');
    } catch (error) {
      toast.error('Failed to update notification preferences');
    } finally {
      setLoading(false);
    }
  };

  const handleLanguageUpdate = async () => {
    try {
      setLoading(true);
      await authService.updateProfile({ language_preference: language });
      toast.success('Language preference updated');
    } catch (error) {
      toast.error('Failed to update language preference');
    } finally {
      setLoading(false);
    }
  };

  const tabs = [
    { id: 'account', name: 'Account', icon: FiUser },
    { id: 'security', name: 'Security', icon: FiShield },
    { id: 'notifications', name: 'Notifications', icon: FiBell },
    { id: 'language', name: 'Language', icon: FiGlobe },
  ];

  return (
    <div className="min-h-screen bg-midnight-950 pt-16">
      <div className="flex">
        <Sidebar />

        <main className="flex-1 ml-0 lg:ml-64 p-4 sm:p-6 lg:p-8">
          <div className="max-w-5xl mx-auto">
            {/* Header */}
            <div className="mb-6 sm:mb-8">
              <h1 className="text-2xl sm:text-3xl font-bold text-white mb-2">Settings</h1>
              <p className="text-sm sm:text-base text-gray-400">Manage your account settings and preferences</p>
            </div>

            {/* Tabs */}
            <div className="mb-4 sm:mb-6 flex overflow-x-auto space-x-2 border-b border-dark-700 pb-2">
              {tabs.map((tab) => {
                const Icon = tab.icon;
                return (
                  <button
                    key={tab.id}
                    onClick={() => setActiveTab(tab.id)}
                    className={`flex items-center space-x-2 px-3 sm:px-4 py-2 sm:py-3 text-sm sm:text-base font-medium transition-all border-b-2 whitespace-nowrap ${
                      activeTab === tab.id
                        ? 'text-red-500 border-red-500'
                        : 'text-gray-400 border-transparent hover:text-white'
                    }`}
                  >
                    <Icon className="h-4 w-4 sm:h-5 sm:w-5" />
                    <span>{tab.name}</span>
                  </button>
                );
              })}
            </div>

            {/* Account Settings */}
            {activeTab === 'account' && (
              <Card>
                <CardContent className="p-6">
                  <CardTitle className="mb-6">Account Information</CardTitle>
                  <form onSubmit={handleAccountUpdate} className="space-y-4">
                    <Input
                      label="Full Name"
                      name="full_name"
                      type="text"
                      value={accountData.full_name}
                      onChange={(e) => setAccountData({ ...accountData, full_name: e.target.value })}
                      icon={FiUser}
                      placeholder="John Doe"
                    />

                    <Input
                      label="Email Address"
                      name="email"
                      type="email"
                      value={accountData.email}
                      onChange={(e) => setAccountData({ ...accountData, email: e.target.value })}
                      icon={FiUser}
                      placeholder="you@example.com"
                      disabled
                    />

                    <Input
                      label="Phone Number"
                      name="phone"
                      type="tel"
                      value={accountData.phone}
                      onChange={(e) => setAccountData({ ...accountData, phone: e.target.value })}
                      icon={FiUser}
                      placeholder="024 XXX XXXX"
                    />

                    <div className="pt-4">
                      <Button
                        type="submit"
                        variant="primary"
                        loading={loading}
                        disabled={loading}
                      >
                        <FiSave className="mr-2" />
                        Save Changes
                      </Button>
                    </div>
                  </form>
                </CardContent>
              </Card>
            )}

            {/* Security Settings */}
            {activeTab === 'security' && (
              <Card>
                <CardContent className="p-6">
                  <CardTitle className="mb-6">Change Password</CardTitle>
                  <form onSubmit={handlePasswordChange} className="space-y-4">
                    <Input
                      label="Current Password"
                      name="current_password"
                      type="password"
                      value={passwordData.current_password}
                      onChange={(e) => setPasswordData({ ...passwordData, current_password: e.target.value })}
                      icon={FiLock}
                      placeholder="••••••••"
                      required
                    />

                    <Input
                      label="New Password"
                      name="new_password"
                      type="password"
                      value={passwordData.new_password}
                      onChange={(e) => setPasswordData({ ...passwordData, new_password: e.target.value })}
                      icon={FiLock}
                      placeholder="••••••••"
                      required
                    />

                    <Input
                      label="Confirm New Password"
                      name="confirm_password"
                      type="password"
                      value={passwordData.confirm_password}
                      onChange={(e) => setPasswordData({ ...passwordData, confirm_password: e.target.value })}
                      icon={FiLock}
                      placeholder="••••••••"
                      required
                    />

                    <div className="p-4 bg-dark-800 rounded-lg border border-dark-700">
                      <p className="text-sm text-gray-400 mb-2">Password requirements:</p>
                      <ul className="text-sm text-gray-500 space-y-1 list-disc list-inside">
                        <li>At least 8 characters long</li>
                        <li>At least one uppercase letter</li>
                        <li>At least one digit</li>
                      </ul>
                    </div>

                    <div className="pt-4">
                      <Button
                        type="submit"
                        variant="primary"
                        loading={loading}
                        disabled={loading}
                      >
                        <FiSave className="mr-2" />
                        Update Password
                      </Button>
                    </div>
                  </form>
                </CardContent>
              </Card>
            )}

            {/* Notification Settings */}
            {activeTab === 'notifications' && (
              <Card>
                <CardContent className="p-6">
                  <CardTitle className="mb-6">Notification Preferences</CardTitle>
                  <div className="space-y-4">
                    {Object.entries(notifications).map(([key, value]) => (
                      <div key={key} className="flex items-center justify-between p-4 bg-dark-800 rounded-lg">
                        <div>
                          <p className="text-white font-medium capitalize">
                            {key.replace(/_/g, ' ')}
                          </p>
                          <p className="text-sm text-gray-400 mt-1">
                            {key === 'email_notifications' && 'Receive email notifications about your account'}
                            {key === 'sms_notifications' && 'Receive SMS notifications for important updates'}
                            {key === 'booking_reminders' && 'Get reminders about upcoming bookings'}
                            {key === 'promotional_emails' && 'Receive promotional offers and updates'}
                          </p>
                        </div>
                        <button
                          onClick={() => setNotifications({ ...notifications, [key]: !value })}
                          className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                            value ? 'bg-red-500' : 'bg-dark-700'
                          }`}
                        >
                          <span
                            className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                              value ? 'translate-x-6' : 'translate-x-1'
                            }`}
                          />
                        </button>
                      </div>
                    ))}

                    <div className="pt-4">
                      <Button
                        variant="primary"
                        onClick={handleNotificationsUpdate}
                        loading={loading}
                        disabled={loading}
                      >
                        <FiSave className="mr-2" />
                        Save Preferences
                      </Button>
                    </div>
                  </div>
                </CardContent>
              </Card>
            )}

            {/* Language Settings */}
            {activeTab === 'language' && (
              <Card>
                <CardContent className="p-6">
                  <CardTitle className="mb-6">Language Preference</CardTitle>
                  <div className="space-y-4">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      {[
                        { code: 'en', name: 'English', flag: '🇬🇧' },
                        { code: 'fr', name: 'French', flag: '🇫🇷' },
                        { code: 'tw', name: 'Twi', flag: '🇬🇭' },
                        { code: 'ga', name: 'Ga', flag: '🇬🇭' },
                      ].map((lang) => (
                        <button
                          key={lang.code}
                          onClick={() => setLanguage(lang.code)}
                          className={`p-4 rounded-lg border-2 transition-all ${
                            language === lang.code
                              ? 'border-red-500 bg-red-500/10'
                              : 'border-dark-700 bg-dark-800 hover:border-dark-600'
                          }`}
                        >
                          <div className="flex items-center space-x-3">
                            <span className="text-3xl">{lang.flag}</span>
                            <div className="text-left">
                              <p className="text-white font-medium">{lang.name}</p>
                              <p className="text-sm text-gray-400">{lang.code.toUpperCase()}</p>
                            </div>
                          </div>
                        </button>
                      ))}
                    </div>

                    <div className="pt-4">
                      <Button
                        variant="primary"
                        onClick={handleLanguageUpdate}
                        loading={loading}
                        disabled={loading}
                      >
                        <FiSave className="mr-2" />
                        Save Language
                      </Button>
                    </div>
                  </div>
                </CardContent>
              </Card>
            )}
          </div>
        </main>
      </div>
    </div>
  );
};

export default Settings;
