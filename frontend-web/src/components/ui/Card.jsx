import React from 'react';

const Card = ({
  children,
  hover = false,
  className = '',
  padding = true,
  ...props
}) => {
  const baseStyles = 'card rounded-xl shadow-dark-xl backdrop-blur-sm transition-all duration-300 animate-fade-in';
  const hoverStyles = hover ? 'card-hover cursor-pointer hover:shadow-2xl hover:-translate-y-1 hover:border-red-500/30' : '';
  const paddingStyles = padding ? 'p-6' : '';

  return (
    <div
      className={`${baseStyles} ${hoverStyles} ${paddingStyles} ${className}`}
      {...props}
    >
      {children}
    </div>
  );
};

export const CardHeader = ({ children, className = '' }) => (
  <div className={`mb-4 ${className}`}>
    {children}
  </div>
);

export const CardTitle = ({ children, className = '' }) => (
  <h3 className={`text-xl font-bold text-white mb-2 animate-fade-in-up ${className}`}>
    {children}
  </h3>
);

export const CardDescription = ({ children, className = '' }) => (
  <p className={`text-gray-400 text-sm ${className}`}>
    {children}
  </p>
);

export const CardContent = ({ children, className = '' }) => (
  <div className={`${className}`}>
    {children}
  </div>
);

export const CardFooter = ({ children, className = '' }) => (
  <div className={`mt-4 pt-4 border-t border-dark-700 ${className}`}>
    {children}
  </div>
);

export default Card;
