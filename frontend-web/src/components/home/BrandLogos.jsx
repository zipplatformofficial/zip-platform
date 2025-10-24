import React from 'react';

const BrandLogos = () => {
  const brands = [
    { name: 'TOYOTA', logo: 'https://cdn.worldvectorlogo.com/logos/toyota-1.svg' },
    { name: 'HONDA', logo: 'https://cdn.worldvectorlogo.com/logos/honda-2.svg' },
    { name: 'NISSAN', logo: 'https://cdn.worldvectorlogo.com/logos/nissan-6.svg' },
    { name: 'MERCEDES', logo: 'https://cdn.worldvectorlogo.com/logos/mercedes-benz-9.svg' },
    { name: 'BMW', logo: 'https://cdn.worldvectorlogo.com/logos/bmw.svg' },
    { name: 'MAZDA', logo: 'https://cdn.worldvectorlogo.com/logos/mazda-2.svg' },
    { name: 'HYUNDAI', logo: 'https://cdn.worldvectorlogo.com/logos/hyundai-motor-company.svg' },
    { name: 'KIA', logo: 'https://cdn.worldvectorlogo.com/logos/kia-logo-2560x1440.svg' },
    { name: 'FORD', logo: 'https://cdn.worldvectorlogo.com/logos/ford-6.svg' },
    { name: 'AUDI', logo: 'https://cdn.worldvectorlogo.com/logos/audi-2.svg' },
    { name: 'VOLKSWAGEN', logo: 'https://cdn.worldvectorlogo.com/logos/volkswagen-vw.svg' },
    { name: 'LEXUS', logo: 'https://cdn.worldvectorlogo.com/logos/lexus-3.svg' },
  ];

  return (
    <div className="py-16 bg-white border-y border-gray-200 overflow-hidden">
      <div className="max-w-7xl mx-auto px-4">
        <div className="text-center mb-12">
          <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-3">
            Popular <span className="text-transparent bg-clip-text bg-gradient-to-r from-red-500 to-orange-500">Brands</span>
          </h2>
          <p className="text-gray-600 text-lg">We service and support top automobile brands worldwide</p>
        </div>

        {/* Scrolling Logos Container */}
        <div className="relative">
          {/* Gradient overlays for fade effect */}
          <div className="absolute left-0 top-0 bottom-0 w-32 bg-gradient-to-r from-white to-transparent z-10"></div>
          <div className="absolute right-0 top-0 bottom-0 w-32 bg-gradient-to-l from-white to-transparent z-10"></div>

          {/* Scrolling wrapper */}
          <div className="flex animate-scroll-rtl">
            {/* First set of logos */}
            <div className="flex space-x-12 px-6">
              {brands.map((brand, index) => (
                <div
                  key={`first-${index}`}
                  className="flex items-center justify-center min-w-[180px] h-24 group cursor-pointer"
                >
                  <img
                    src={brand.logo}
                    alt={brand.name}
                    className="h-16 w-auto grayscale hover:grayscale-0 transition-all duration-300 group-hover:scale-110"
                    onError={(e) => {
                      e.target.style.display = 'none';
                      e.target.parentElement.innerHTML = `<span class="text-2xl font-bold text-gray-700 group-hover:text-red-500 transition-colors">${brand.name}</span>`;
                    }}
                  />
                </div>
              ))}
            </div>
            {/* Duplicate set for seamless loop */}
            <div className="flex space-x-12 px-6">
              {brands.map((brand, index) => (
                <div
                  key={`second-${index}`}
                  className="flex items-center justify-center min-w-[180px] h-24 group cursor-pointer"
                >
                  <img
                    src={brand.logo}
                    alt={brand.name}
                    className="h-16 w-auto grayscale hover:grayscale-0 transition-all duration-300 group-hover:scale-110"
                    onError={(e) => {
                      e.target.style.display = 'none';
                      e.target.parentElement.innerHTML = `<span class="text-2xl font-bold text-gray-700 group-hover:text-red-500 transition-colors">${brand.name}</span>`;
                    }}
                  />
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default BrandLogos;
