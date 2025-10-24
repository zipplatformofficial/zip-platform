import React from 'react';

const Loading = ({ size = 'md', className = '', fullScreen = false }) => {
  const sizes = {
    sm: 'h-4 w-4',
    md: 'h-8 w-8',
    lg: 'h-12 w-12',
    xl: 'h-16 w-16',
  };

  const spinner = (
    <div className={`${sizes[size]} ${className}`}>
      <svg className="animate-spin text-red-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
      </svg>
    </div>
  );

  if (fullScreen) {
    return (
      <div className="fixed inset-0 bg-midnight-950 flex items-center justify-center z-50">
        <div className="text-center">
          {spinner}
          <p className="mt-4 text-gray-400">Loading...</p>
        </div>
      </div>
    );
  }

  return spinner;
};

export const LoadingDots = ({ className = '' }) => (
  <div className={`flex space-x-2 ${className}`}>
    <div className="w-2 h-2 bg-red-500 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
    <div className="w-2 h-2 bg-red-500 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
    <div className="w-2 h-2 bg-red-500 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
  </div>
);

export const LoadingSkeleton = ({ className = '', count = 1 }) => (
  <div className={className}>
    {[...Array(count)].map((_, i) => (
      <div key={i} className="animate-pulse">
        <div className="h-4 bg-dark-800 rounded mb-3"></div>
      </div>
    ))}
  </div>
);

export default Loading;
