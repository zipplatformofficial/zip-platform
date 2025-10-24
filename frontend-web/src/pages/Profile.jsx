import React, { useState } from 'react';
import { useAuth } from '../hooks/useAuth';
import Card, { CardContent, CardTitle } from '../components/ui/Card';
import Input from '../components/ui/Input';
import Button from '../components/ui/Button';
import Sidebar from '../components/layout/Sidebar';
import { FiUser, FiMail, FiPhone, FiMapPin } from 'react-icons/fi';
import toast from 'react-hot-toast';

const Profile = () => {
  const { user, updateUser } = useAuth();
  const [editing, setEditing] = useState(false);
  const [formData, setFormData] = useState({
    full_name: user?.full_name || '',
    phone: user?.phone || '',
    location: user?.location?.address || '',
  });
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      await updateUser(formData);
      setEditing(false);
    } catch (error) {
      console.error('Update error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-midnight-950 pt-16">
      <div className="flex">
        <Sidebar />

        <main className="flex-1 ml-64 p-8">
          <div className="max-w-4xl mx-auto">
            <h1 className="text-3xl font-bold text-white mb-8">My Profile</h1>

            <div className="grid gap-6">
              <Card>
                <CardContent className="p-6">
                  <div className="flex items-center justify-between mb-6">
                    <CardTitle>Personal Information</CardTitle>
                    {!editing && (
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => setEditing(true)}
                      >
                        Edit Profile
                      </Button>
                    )}
                  </div>

                  {editing ? (
                    <form onSubmit={handleSubmit} className="space-y-4">
                      <Input
                        label="Full Name"
                        icon={FiUser}
                        value={formData.full_name}
                        onChange={(e) => setFormData({ ...formData, full_name: e.target.value })}
                        required
                      />

                      <Input
                        label="Email"
                        icon={FiMail}
                        value={user?.email}
                        disabled
                      />

                      <Input
                        label="Phone"
                        icon={FiPhone}
                        value={formData.phone}
                        onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
                        required
                      />

                      <Input
                        label="Location"
                        icon={FiMapPin}
                        value={formData.location}
                        onChange={(e) => setFormData({ ...formData, location: e.target.value })}
                      />

                      <div className="flex gap-3 pt-4">
                        <Button
                          type="button"
                          variant="ghost"
                          onClick={() => setEditing(false)}
                        >
                          Cancel
                        </Button>
                        <Button
                          type="submit"
                          variant="primary"
                          loading={loading}
                        >
                          Save Changes
                        </Button>
                      </div>
                    </form>
                  ) : (
                    <div className="space-y-4">
                      <div>
                        <label className="text-sm text-gray-400">Full Name</label>
                        <p className="text-white font-medium">{user?.full_name}</p>
                      </div>
                      <div>
                        <label className="text-sm text-gray-400">Email</label>
                        <p className="text-white font-medium">{user?.email}</p>
                      </div>
                      <div>
                        <label className="text-sm text-gray-400">Phone</label>
                        <p className="text-white font-medium">{user?.phone}</p>
                      </div>
                      <div>
                        <label className="text-sm text-gray-400">Role</label>
                        <p className="text-white font-medium capitalize">{user?.role}</p>
                      </div>
                      <div>
                        <label className="text-sm text-gray-400">Loyalty Points</label>
                        <p className="text-red-500 font-bold text-xl">{user?.loyalty_points || 0}</p>
                      </div>
                    </div>
                  )}
                </CardContent>
              </Card>

              <Card>
                <CardContent className="p-6">
                  <CardTitle className="mb-4">Account Security</CardTitle>
                  <Button variant="outline">
                    Change Password
                  </Button>
                </CardContent>
              </Card>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
};

export default Profile;
