import React, { createContext, useContext, useState, useEffect } from 'react';
import { translations } from '../i18n/translations';

const LanguageContext = createContext();

export const useLanguage = () => {
  const context = useContext(LanguageContext);
  if (!context) {
    throw new Error('useLanguage must be used within a LanguageProvider');
  }
  return context;
};

export const LanguageProvider = ({ children }) => {
  // Get initial language from localStorage or default to English
  const [currentLanguage, setCurrentLanguage] = useState(() => {
    const saved = localStorage.getItem('zip-language');
    return saved || 'en';
  });

  // Update localStorage when language changes
  useEffect(() => {
    localStorage.setItem('zip-language', currentLanguage);
    // Update HTML lang attribute for accessibility
    document.documentElement.lang = currentLanguage;
  }, [currentLanguage]);

  // Get translation for a key
  const t = (key) => {
    return translations[currentLanguage]?.[key] || translations.en[key] || key;
  };

  // Change language
  const changeLanguage = (languageCode) => {
    if (translations[languageCode]) {
      setCurrentLanguage(languageCode);
    }
  };

  const value = {
    currentLanguage,
    changeLanguage,
    t,
    translations: translations[currentLanguage],
  };

  return (
    <LanguageContext.Provider value={value}>
      {children}
    </LanguageContext.Provider>
  );
};

export default LanguageContext;
