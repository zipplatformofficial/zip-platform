import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { FiStar, FiThumbsUp, FiChevronLeft, FiChevronRight } from 'react-icons/fi';

const Reviews = () => {
  const [currentIndex, setCurrentIndex] = useState(0);

  const reviews = [
    {
      id: 1,
      name: 'Kwame Mensah',
      avatar: 'https://ui-avatars.com/api/?name=Kwame+Mensah&background=ef4444&color=fff',
      rating: 5,
      date: '2 days ago',
      verified: true,
      service: 'Car Rental',
      vehicle: 'Toyota Camry',
      review:
        'Exceptional service! The Toyota Camry was in pristine condition and the booking process was seamless. ZIP Platform has made car rental so easy in Ghana. Highly recommend!',
      helpful: 45,
      image: 'https://images.unsplash.com/photo-1549317661-bd32c8ce0db2?w=400'
    },
    {
      id: 2,
      name: 'Ama Sarpong',
      avatar: 'https://ui-avatars.com/api/?name=Ama+Sarpong&background=f97316&color=fff',
      rating: 5,
      date: '5 days ago',
      verified: true,
      service: 'Mobile Maintenance',
      vehicle: 'Honda Accord',
      review:
        'The mobile maintenance team arrived on time and did an amazing job servicing my Honda. Professional, courteous, and thorough. This is the future of car maintenance in Ghana!',
      helpful: 32,
      image: 'https://images.unsplash.com/photo-1486262715619-67b85e0b08d3?w=400'
    },
    {
      id: 3,
      name: 'Kofi Asante',
      avatar: 'https://ui-avatars.com/api/?name=Kofi+Asante&background=8b5cf6&color=fff',
      rating: 5,
      date: '1 week ago',
      verified: true,
      service: 'Auto Parts',
      vehicle: 'Mercedes Benz',
      review:
        'Ordered genuine brake pads for my Mercedes. Fast delivery, competitive prices, and excellent customer service. ZIP Platform is revolutionizing the auto industry in Ghana!',
      helpful: 28,
      image: null
    },
    {
      id: 4,
      name: 'Abena Osei',
      avatar: 'https://ui-avatars.com/api/?name=Abena+Osei&background=ec4899&color=fff',
      rating: 5,
      date: '1 week ago',
      verified: true,
      service: 'Car Rental',
      vehicle: 'BMW X5',
      review:
        'Rented the BMW X5 for a business trip to Kumasi. The car was luxurious, clean, and performed flawlessly. Customer support was responsive throughout my journey. 10/10 experience!',
      helpful: 51,
      image: 'https://images.unsplash.com/photo-1555215695-3004980ad54e?w=400'
    },
    {
      id: 5,
      name: 'Yaw Boateng',
      avatar: 'https://ui-avatars.com/api/?name=Yaw+Boateng&background=06b6d4&color=fff',
      rating: 5,
      date: '2 weeks ago',
      verified: true,
      service: 'Mobile Maintenance',
      vehicle: 'Toyota Corolla',
      review:
        'Had my Toyota serviced at my office parking lot. The convenience is unmatched! Technicians were skilled and explained everything clearly. ZIP is a game-changer!',
      helpful: 39,
      image: null
    },
    {
      id: 6,
      name: 'Efua Amoah',
      avatar: 'https://ui-avatars.com/api/?name=Efua+Amoah&background=10b981&color=fff',
      rating: 5,
      date: '3 weeks ago',
      verified: true,
      service: 'Car Rental',
      vehicle: 'Nissan Altima',
      review:
        'Great platform! Easy to navigate, transparent pricing, and the car exceeded my expectations. The insurance coverage gave me peace of mind. Will definitely use ZIP again!',
      helpful: 42,
      image: 'https://images.unsplash.com/photo-1552519507-da3b142c6e3d?w=400'
    }
  ];

  const itemsPerPage = 3;
  const maxIndex = Math.max(0, Math.ceil(reviews.length / itemsPerPage) - 1);

  const nextSlide = () => {
    setCurrentIndex((prev) => (prev >= maxIndex ? 0 : prev + 1));
  };

  const prevSlide = () => {
    setCurrentIndex((prev) => (prev <= 0 ? maxIndex : prev - 1));
  };

  const visibleReviews = reviews.slice(
    currentIndex * itemsPerPage,
    currentIndex * itemsPerPage + itemsPerPage
  );

  return (
    <section className="py-20 bg-gradient-to-b from-gray-50 to-white relative overflow-hidden">
      {/* Background decoration */}
      <div className="absolute inset-0 opacity-5">
        <div
          className="absolute inset-0"
          style={{
            backgroundImage: 'radial-gradient(circle at 2px 2px, #ef4444 1px, transparent 0)',
            backgroundSize: '40px 40px'
          }}
        />
      </div>

      <div className="container mx-auto px-4 relative z-10">
        {/* Header */}
        <div className="text-center mb-16">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
          >
            <span className="inline-block px-4 py-2 bg-red-100 text-red-600 rounded-full text-sm font-semibold mb-4">
              ⭐ Customer Reviews
            </span>
            <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
              What Our Customers Say
            </h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Join thousands of satisfied customers who trust ZIP Platform for their automotive needs
            </p>

            {/* Stats */}
            <div className="flex items-center justify-center gap-8 mt-8">
              <div>
                <div className="flex items-center gap-1 mb-1">
                  {[1, 2, 3, 4, 5].map((star) => (
                    <FiStar
                      key={star}
                      className="h-5 w-5 fill-yellow-400 text-yellow-400"
                    />
                  ))}
                </div>
                <p className="text-sm text-gray-600">
                  <span className="font-bold text-gray-900">4.9</span> out of 5
                </p>
              </div>
              <div className="h-12 w-px bg-gray-300" />
              <div>
                <p className="text-3xl font-bold text-gray-900">5,000+</p>
                <p className="text-sm text-gray-600">Happy Customers</p>
              </div>
              <div className="h-12 w-px bg-gray-300" />
              <div>
                <p className="text-3xl font-bold text-gray-900">10,000+</p>
                <p className="text-sm text-gray-600">5-Star Reviews</p>
              </div>
            </div>
          </motion.div>
        </div>

        {/* Reviews Carousel */}
        <div className="relative">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
            {visibleReviews.map((review, idx) => (
              <motion.div
                key={review.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: idx * 0.1, duration: 0.5 }}
                className="bg-white rounded-2xl shadow-xl border border-gray-100 overflow-hidden hover:shadow-2xl transition-all duration-300 hover:-translate-y-2"
              >
                {/* Review Image */}
                {review.image && (
                  <div className="h-40 overflow-hidden">
                    <img
                      src={review.image}
                      alt={review.vehicle}
                      className="w-full h-full object-cover"
                    />
                  </div>
                )}

                <div className="p-6">
                  {/* Header */}
                  <div className="flex items-start justify-between mb-4">
                    <div className="flex items-center gap-3">
                      <img
                        src={review.avatar}
                        alt={review.name}
                        className="w-12 h-12 rounded-full border-2 border-red-500"
                      />
                      <div>
                        <div className="flex items-center gap-2">
                          <h4 className="font-bold text-gray-900">
                            {review.name}
                          </h4>
                          {review.verified && (
                            <span className="text-xs bg-green-100 text-green-700 px-2 py-0.5 rounded-full font-semibold">
                              ✓ Verified
                            </span>
                          )}
                        </div>
                        <p className="text-xs text-gray-500">{review.date}</p>
                      </div>
                    </div>
                  </div>

                  {/* Rating */}
                  <div className="flex items-center gap-1 mb-3">
                    {[1, 2, 3, 4, 5].map((star) => (
                      <FiStar
                        key={star}
                        className={`h-4 w-4 ${
                          star <= review.rating
                            ? 'fill-yellow-400 text-yellow-400'
                            : 'text-gray-300'
                        }`}
                      />
                    ))}
                  </div>

                  {/* Service Badge */}
                  <div className="flex items-center gap-2 mb-3">
                    <span className="text-xs bg-red-100 text-red-600 px-3 py-1 rounded-full font-semibold">
                      {review.service}
                    </span>
                    <span className="text-xs text-gray-500">
                      {review.vehicle}
                    </span>
                  </div>

                  {/* Review Text */}
                  <p className="text-sm text-gray-700 leading-relaxed mb-4">
                    {review.review}
                  </p>

                  {/* Footer */}
                  <div className="flex items-center justify-between pt-4 border-t border-gray-100">
                    <button className="flex items-center gap-2 text-sm text-gray-600 hover:text-red-600 transition-colors">
                      <FiThumbsUp className="h-4 w-4" />
                      <span>Helpful ({review.helpful})</span>
                    </button>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>

          {/* Navigation */}
          <div className="flex items-center justify-center gap-4">
            <button
              onClick={prevSlide}
              disabled={currentIndex === 0}
              className="p-3 bg-white border-2 border-gray-200 rounded-full hover:border-red-500 hover:text-red-500 transition-all disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:border-gray-200 disabled:hover:text-gray-900"
            >
              <FiChevronLeft className="h-6 w-6" />
            </button>

            {/* Dots */}
            <div className="flex gap-2">
              {Array.from({ length: maxIndex + 1 }).map((_, idx) => (
                <button
                  key={idx}
                  onClick={() => setCurrentIndex(idx)}
                  className={`h-2 rounded-full transition-all ${
                    idx === currentIndex
                      ? 'w-8 bg-gradient-to-r from-red-500 to-orange-500'
                      : 'w-2 bg-gray-300 hover:bg-gray-400'
                  }`}
                />
              ))}
            </div>

            <button
              onClick={nextSlide}
              disabled={currentIndex === maxIndex}
              className="p-3 bg-white border-2 border-gray-200 rounded-full hover:border-red-500 hover:text-red-500 transition-all disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:border-gray-200 disabled:hover:text-gray-900"
            >
              <FiChevronRight className="h-6 w-6" />
            </button>
          </div>
        </div>

        {/* CTA */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center mt-12"
        >
          <p className="text-gray-600 mb-4">
            Want to share your experience with ZIP Platform?
          </p>
          <button className="px-8 py-3 bg-gradient-to-r from-red-500 to-orange-500 text-white rounded-full font-semibold hover:from-red-600 hover:to-orange-600 shadow-lg hover:shadow-xl transition-all">
            Write a Review
          </button>
        </motion.div>
      </div>
    </section>
  );
};

export default Reviews;
