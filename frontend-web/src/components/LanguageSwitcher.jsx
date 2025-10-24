import React, { useState, useRef, useEffect } from 'react';
import { FiGlobe, FiCheck } from 'react-icons/fi';
import { useLanguage } from '../context/LanguageContext';
import { languages } from '../i18n/translations';

const LanguageSwitcher = () => {
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef(null);
  const { currentLanguage, changeLanguage } = useLanguage();

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setIsOpen(false);
      }
    };

    if (isOpen) {
      document.addEventListener('mousedown', handleClickOutside);
    }

    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [isOpen]);

  const currentLang = languages.find(lang => lang.code === currentLanguage);

  const handleLanguageChange = (langCode) => {
    changeLanguage(langCode);
    setIsOpen(false);
  };

  return (
    <div className="relative" ref={dropdownRef}>
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center justify-between w-full sm:w-auto space-x-2 px-4 py-2.5 rounded-lg text-gray-300 hover:text-white hover:bg-dark-800 transition-colors border border-dark-700"
        aria-label="Change language"
      >
        <div className="flex items-center space-x-2">
          <FiGlobe className="h-5 w-5" />
          <span className="text-sm font-medium">{currentLang?.name}</span>
          <span className="text-lg">{currentLang?.flag}</span>
        </div>
        <svg className="w-4 h-4 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
        </svg>
      </button>

      {isOpen && (
        <div className="absolute left-0 sm:right-0 sm:left-auto mt-2 w-full sm:w-56 bg-dark-900 border border-dark-700 rounded-lg shadow-dark-xl overflow-hidden z-50">
          <div className="py-2">
            <div className="px-4 py-2 text-xs font-semibold text-gray-500 uppercase tracking-wider">
              Select Language
            </div>
            {languages.map((lang) => (
              <button
                key={lang.code}
                onClick={() => handleLanguageChange(lang.code)}
                className={`w-full flex items-center justify-between px-4 py-2.5 text-sm transition-colors ${
                  lang.code === currentLanguage
                    ? 'bg-primary-500/10 text-primary-500'
                    : 'text-gray-300 hover:bg-dark-800 hover:text-white'
                }`}
              >
                <div className="flex items-center space-x-3">
                  <span className="text-xl">{lang.flag}</span>
                  <span className="font-medium">{lang.name}</span>
                </div>
                {lang.code === currentLanguage && (
                  <FiCheck className="h-4 w-4 text-primary-500" />
                )}
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default LanguageSwitcher;
