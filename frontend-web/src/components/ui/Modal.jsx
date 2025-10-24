import React, { useEffect } from 'react';
import { FiX } from 'react-icons/fi';

const Modal = ({
  isOpen,
  onClose,
  title,
  children,
  size = 'md',
  showCloseButton = true,
  closeOnOutsideClick = true,
}) => {
  const sizes = {
    sm: 'max-w-md',
    md: 'max-w-lg',
    lg: 'max-w-2xl',
    xl: 'max-w-4xl',
    full: 'max-w-full mx-4',
  };

  useEffect(() => {
    if (isOpen) {
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = 'unset';
    }
    return () => {
      document.body.style.overflow = 'unset';
    };
  }, [isOpen]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto animate-fade-in">
      <div className="flex min-h-screen items-center justify-center p-4">
        {/* Backdrop */}
        <div
          className="fixed inset-0 bg-black/80 backdrop-blur-sm transition-all duration-300"
          onClick={closeOnOutsideClick ? onClose : undefined}
        ></div>

        {/* Modal */}
        <div className={`relative card ${sizes[size]} w-full animate-scale-in shadow-2xl border border-red-500/20`}>
          {/* Header */}
          {(title || showCloseButton) && (
            <div className="flex items-center justify-between p-6 border-b border-dark-700 bg-gradient-to-r from-dark-900 to-dark-800">
              {title && (
                <h3 className="text-xl font-bold text-white animate-fade-in-up">{title}</h3>
              )}
              {showCloseButton && (
                <button
                  onClick={onClose}
                  className="text-gray-400 hover:text-white transition-all duration-300 p-1 rounded-lg hover:bg-red-500/20 hover:scale-110"
                >
                  <FiX className="h-5 w-5" />
                </button>
              )}
            </div>
          )}

          {/* Content */}
          <div className="p-6 animate-fade-in">
            {children}
          </div>
        </div>
      </div>
    </div>
  );
};

export const ModalFooter = ({ children, className = '' }) => (
  <div className={`flex items-center justify-end gap-3 pt-4 border-t border-dark-700 ${className}`}>
    {children}
  </div>
);

export default Modal;
