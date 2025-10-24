import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { FiSearch, FiCalendar, FiMapPin } from 'react-icons/fi';
import Button from '../ui/Button';

const HeroSearch = () => {
  const navigate = useNavigate();
  const [searchData, setSearchData] = useState({
    category: 'rental',
    location: '',
    startDate: '',
    endDate: '',
  });

  const handleSearch = (e) => {
    e.preventDefault();
    if (searchData.category === 'rental') {
      navigate('/rentals');
    } else if (searchData.category === 'maintenance') {
      navigate('/maintenance');
    } else {
      navigate('/store');
    }
  };

  return (
    <div className="bg-white rounded-2xl shadow-2xl p-8 max-w-5xl mx-auto -mt-10 relative z-10">
      <form onSubmit={handleSearch}>
        <div className="grid md:grid-cols-4 gap-4 mb-4">
          {/* Category Select */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              SELECT CATEGORY
            </label>
            <select
              className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-red-500 focus:border-transparent bg-gray-50"
              value={searchData.category}
              onChange={(e) => setSearchData({ ...searchData, category: e.target.value })}
            >
              <option value="rental">Car Rental</option>
              <option value="maintenance">Maintenance</option>
              <option value="store">Auto Parts</option>
            </select>
          </div>

          {/* Location */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              PICK UP LOCATION
            </label>
            <div className="relative">
              <FiMapPin className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
              <input
                type="text"
                placeholder="Enter location"
                className="w-full pl-10 pr-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-red-500 focus:border-transparent bg-gray-50"
                value={searchData.location}
                onChange={(e) => setSearchData({ ...searchData, location: e.target.value })}
              />
            </div>
          </div>

          {/* Start Date */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              START DATE
            </label>
            <div className="relative">
              <FiCalendar className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
              <input
                type="date"
                className="w-full pl-10 pr-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-red-500 focus:border-transparent bg-gray-50"
                value={searchData.startDate}
                onChange={(e) => setSearchData({ ...searchData, startDate: e.target.value })}
              />
            </div>
          </div>

          {/* End Date */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              END DATE
            </label>
            <div className="relative">
              <FiCalendar className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
              <input
                type="date"
                className="w-full pl-10 pr-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-red-500 focus:border-transparent bg-gray-50"
                value={searchData.endDate}
                onChange={(e) => setSearchData({ ...searchData, endDate: e.target.value })}
              />
            </div>
          </div>
        </div>

        <Button type="submit" variant="primary" size="lg" className="w-full">
          <FiSearch className="mr-2" />
          FIND YOUR {searchData.category.toUpperCase()}
        </Button>
      </form>
    </div>
  );
};

export default HeroSearch;
