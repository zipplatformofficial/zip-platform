import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { FiCheck, FiMapPin, FiX } from 'react-icons/fi';

const SocialProof = () => {
  const [notifications, setNotifications] = useState([]);
  const [nextId, setNextId] = useState(1);

  // Mock data for notifications
  const mockNotifications = [
    {
      name: 'Kwame A.',
      action: 'booked',
      item: 'Toyota Camry',
      location: 'Accra',
      time: 'Just now'
    },
    {
      name: 'Ama S.',
      action: 'rented',
      item: 'Honda Accord',
      location: 'Kumasi',
      time: '2 min ago'
    },
    {
      name: 'Kofi M.',
      action: 'booked service for',
      item: 'Mercedes Benz',
      location: 'Tema',
      time: '5 min ago'
    },
    {
      name: 'Abena K.',
      action: 'purchased',
      item: 'Brake Pads',
      location: 'Takoradi',
      time: '7 min ago'
    },
    {
      name: 'Yaw B.',
      action: 'booked',
      item: 'BMW X5',
      location: 'Accra',
      time: '10 min ago'
    },
    {
      name: 'Efua A.',
      action: 'rented',
      item: 'Toyota Corolla',
      location: 'Cape Coast',
      time: '12 min ago'
    }
  ];

  useEffect(() => {
    // Show a random notification every 8-15 seconds
    const showNotification = () => {
      const randomNotification =
        mockNotifications[Math.floor(Math.random() * mockNotifications.length)];

      const newNotification = {
        id: nextId,
        ...randomNotification
      };

      setNotifications((prev) => [...prev, newNotification]);
      setNextId((prev) => prev + 1);

      // Auto-remove after 6 seconds
      setTimeout(() => {
        setNotifications((prev) => prev.filter((n) => n.id !== newNotification.id));
      }, 6000);
    };

    // Initial delay before first notification
    const initialDelay = setTimeout(showNotification, 3000);

    // Show notifications at random intervals
    const interval = setInterval(() => {
      showNotification();
    }, Math.random() * 7000 + 8000); // Random between 8-15 seconds

    return () => {
      clearTimeout(initialDelay);
      clearInterval(interval);
    };
  }, [nextId]);

  const handleClose = (id) => {
    setNotifications((prev) => prev.filter((n) => n.id !== id));
  };

  return (
    <div className="fixed bottom-6 left-6 z-40 space-y-3 pointer-events-none">
      <AnimatePresence>
        {notifications.map((notification) => (
          <motion.div
            key={notification.id}
            initial={{ opacity: 0, x: -100, scale: 0.9 }}
            animate={{ opacity: 1, x: 0, scale: 1 }}
            exit={{ opacity: 0, x: -100, scale: 0.9 }}
            transition={{ type: 'spring', damping: 20, stiffness: 300 }}
            className="pointer-events-auto"
          >
            <div className="bg-white rounded-2xl shadow-2xl border border-gray-200 p-4 pr-12 max-w-sm backdrop-blur-lg relative overflow-hidden">
              {/* Gradient accent bar */}
              <div className="absolute top-0 left-0 w-1 h-full bg-gradient-to-b from-red-500 to-orange-500" />

              {/* Close button */}
              <button
                onClick={() => handleClose(notification.id)}
                className="absolute top-2 right-2 p-1 hover:bg-gray-100 rounded-full transition-all"
              >
                <FiX className="h-4 w-4 text-gray-400" />
              </button>

              <div className="flex items-start gap-3">
                {/* Icon */}
                <div className="flex-shrink-0 w-10 h-10 bg-gradient-to-br from-green-500 to-green-600 rounded-full flex items-center justify-center shadow-lg">
                  <FiCheck className="h-5 w-5 text-white" />
                </div>

                {/* Content */}
                <div className="flex-1 min-w-0">
                  <p className="text-sm text-gray-900 font-medium">
                    <span className="font-bold">{notification.name}</span>{' '}
                    {notification.action}{' '}
                    <span className="font-semibold text-red-600">
                      {notification.item}
                    </span>
                  </p>
                  <div className="flex items-center gap-3 mt-1 text-xs text-gray-500">
                    <span className="flex items-center gap-1">
                      <FiMapPin className="h-3 w-3" />
                      {notification.location}
                    </span>
                    <span>•</span>
                    <span>{notification.time}</span>
                  </div>
                </div>
              </div>

              {/* Progress bar */}
              <motion.div
                initial={{ width: '100%' }}
                animate={{ width: '0%' }}
                transition={{ duration: 6, ease: 'linear' }}
                className="absolute bottom-0 left-0 h-0.5 bg-gradient-to-r from-red-500 to-orange-500"
              />
            </div>
          </motion.div>
        ))}
      </AnimatePresence>
    </div>
  );
};

export default SocialProof;
