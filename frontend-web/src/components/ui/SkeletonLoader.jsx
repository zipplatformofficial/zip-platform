import React from 'react';

// Base Skeleton component
export const Skeleton = ({ className = '', variant = 'rectangular', animation = 'pulse' }) => {
  const baseClasses = 'bg-gradient-to-r from-gray-200 via-gray-300 to-gray-200 bg-[length:200%_100%]';

  const animationClasses = {
    pulse: 'animate-pulse',
    wave: 'animate-shimmer',
    none: ''
  };

  const variantClasses = {
    rectangular: 'rounded-lg',
    circular: 'rounded-full',
    text: 'rounded'
  };

  return (
    <div
      className={`${baseClasses} ${animationClasses[animation]} ${variantClasses[variant]} ${className}`}
      aria-label="Loading..."
    />
  );
};

// Vehicle Card Skeleton
export const VehicleCardSkeleton = () => {
  return (
    <div className="bg-white rounded-3xl shadow-lg overflow-hidden border-2 border-gray-100">
      {/* Image skeleton */}
      <Skeleton className="h-56 w-full" animation="wave" />

      <div className="p-6 space-y-4">
        {/* Title skeleton */}
        <Skeleton className="h-7 w-3/4" />

        {/* Rating skeleton */}
        <div className="flex items-center gap-2">
          <Skeleton className="h-4 w-20" />
          <Skeleton className="h-4 w-16" />
        </div>

        {/* Specs skeleton */}
        <div className="grid grid-cols-3 gap-4">
          {[1, 2, 3].map((i) => (
            <div key={i} className="flex items-center gap-2">
              <Skeleton variant="circular" className="h-8 w-8" />
              <Skeleton className="h-4 w-12" />
            </div>
          ))}
        </div>

        {/* Price and button skeleton */}
        <div className="flex items-center justify-between pt-4">
          <div className="space-y-1">
            <Skeleton className="h-8 w-24" />
            <Skeleton className="h-3 w-16" />
          </div>
          <Skeleton className="h-12 w-32 rounded-xl" />
        </div>
      </div>
    </div>
  );
};

// Service Card Skeleton
export const ServiceCardSkeleton = () => {
  return (
    <div className="bg-white rounded-2xl shadow-lg overflow-hidden border-2 border-gray-100">
      <Skeleton className="h-48 w-full" animation="wave" />
      <div className="p-6 space-y-3">
        <Skeleton className="h-6 w-2/3" />
        <Skeleton className="h-4 w-full" />
        <Skeleton className="h-4 w-4/5" />
        <Skeleton className="h-10 w-full rounded-lg mt-4" />
      </div>
    </div>
  );
};

// Dashboard Stats Card Skeleton
export const StatsCardSkeleton = () => {
  return (
    <div className="bg-white rounded-xl shadow-md p-6 space-y-3">
      <div className="flex items-center justify-between">
        <Skeleton className="h-5 w-24" />
        <Skeleton variant="circular" className="h-10 w-10" />
      </div>
      <Skeleton className="h-8 w-20" />
      <Skeleton className="h-3 w-32" />
    </div>
  );
};

// Table Row Skeleton
export const TableRowSkeleton = ({ columns = 4 }) => {
  return (
    <tr className="border-b border-gray-100">
      {Array.from({ length: columns }).map((_, i) => (
        <td key={i} className="px-6 py-4">
          <Skeleton className="h-5 w-full" />
        </td>
      ))}
    </tr>
  );
};

// List Item Skeleton
export const ListItemSkeleton = () => {
  return (
    <div className="flex items-center gap-4 p-4 bg-white rounded-lg border border-gray-100">
      <Skeleton variant="circular" className="h-12 w-12" />
      <div className="flex-1 space-y-2">
        <Skeleton className="h-5 w-3/4" />
        <Skeleton className="h-4 w-1/2" />
      </div>
      <Skeleton className="h-8 w-20 rounded-lg" />
    </div>
  );
};

// Page Skeleton (Full page loader)
export const PageSkeleton = ({ type = 'list' }) => {
  if (type === 'grid') {
    return (
      <div className="container mx-auto px-4 py-8">
        <Skeleton className="h-10 w-64 mb-6" />
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {[1, 2, 3, 4, 5, 6].map((i) => (
            <VehicleCardSkeleton key={i} />
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8 space-y-4">
      <Skeleton className="h-10 w-64 mb-6" />
      {[1, 2, 3, 4, 5].map((i) => (
        <ListItemSkeleton key={i} />
      ))}
    </div>
  );
};

export default Skeleton;
