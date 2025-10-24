import React, { useState, useEffect } from 'react';

const RotatingCarHero = () => {
  const cars = [
    'https://images.unsplash.com/photo-1583121274602-3e2820c69888?w=800', // BMW
    'https://images.unsplash.com/photo-1617531653332-bd46c24f2068?w=800', // Mercedes
    'https://images.unsplash.com/photo-1618843479313-40f8afb4b4d8?w=800', // Toyota
    'https://images.unsplash.com/photo-1552519507-da3b142c6e3d?w=800', // Audi
    'https://images.unsplash.com/photo-1606664515524-ed2f786a0bd6?w=800', // Honda
  ];

  const [currentIndex, setCurrentIndex] = useState(0);
  const [isAnimating, setIsAnimating] = useState(false);

  useEffect(() => {
    const interval = setInterval(() => {
      setIsAnimating(true);
      setTimeout(() => {
        setCurrentIndex((prev) => (prev + 1) % cars.length);
        setIsAnimating(false);
      }, 500);
    }, 4000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="absolute top-1/2 right-10 transform -translate-y-1/2 w-1/2 z-10 hidden lg:block">
      {cars.map((car, index) => (
        <img
          key={index}
          src={car}
          alt={`Dream Car ${index + 1}`}
          className={`absolute inset-0 w-full drop-shadow-2xl transition-all duration-700 ${
            index === currentIndex
              ? isAnimating
                ? 'opacity-0 scale-95'
                : 'opacity-100 scale-100'
              : 'opacity-0 scale-95 pointer-events-none'
          }`}
          style={{
            transform: index === currentIndex && !isAnimating ? 'translateX(0)' : 'translateX(50px)',
          }}
        />
      ))}
    </div>
  );
};

export default RotatingCarHero;
