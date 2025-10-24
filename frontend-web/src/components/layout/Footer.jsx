import React from "react";
import { Link } from "react-router-dom";
import {
  FiMail,
  FiPhone,
  FiMapPin,
  FiFacebook,
  FiTwitter,
  FiInstagram,
  FiLinkedin,
} from "react-icons/fi";
import LanguageSwitcher from "../LanguageSwitcher";

const Footer = () => {
  const currentYear = new Date().getFullYear();

  const footerLinks = {
    services: [
      { name: "Mobile Car Maintenance", path: "/maintenance" },
      { name: "Car Rentals", path: "/rentals" },
      { name: "Auto Parts Store", path: "/store" },
      { name: "Book Service", path: "/maintenance/book" },
    ],
    company: [
      { name: "About Us", path: "/about" },
      { name: "Contact", path: "/contact" },
      { name: "Careers", path: "/careers" },
      { name: "Blog", path: "/blog" },
    ],
    support: [
      { name: "Help Center", path: "/help" },
      { name: "Terms of Service", path: "/terms" },
      { name: "Privacy Policy", path: "/privacy" },
      { name: "FAQs", path: "/faqs" },
    ],
  };

  const socialLinks = [
    { icon: FiFacebook, href: "#", label: "Facebook" },
    { icon: FiTwitter, href: "#", label: "Twitter" },
    { icon: FiInstagram, href: "#", label: "Instagram" },
    { icon: FiLinkedin, href: "#", label: "LinkedIn" },
  ];

  return (
    <footer className="bg-dark-900 border-t border-dark-700">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-8 mb-8">
          {/* Brand */}
          <div className="lg:col-span-2">
            <Link to="/" className="flex items-center mb-4">
              <img
                src="https://i.postimg.cc/yYfX6T5z/zip-logo-removebg.png"
                alt="ZIP Platform"
                className="h-10 w-auto"
              />
            </Link>
            <p className="text-gray-400 mb-4 max-w-md">
              Your one-stop solution for mobile car maintenance, rentals, and
              auto parts in Ghana.
            </p>
            <div className="space-y-2">
              <div className="flex items-center text-gray-400">
                <FiMapPin className="h-4 w-4 mr-2 text-primary-500" />
                <span className="text-sm">Accra, Ghana</span>
              </div>
              <div className="flex items-center text-gray-400">
                <FiPhone className="h-4 w-4 mr-2 text-primary-500" />
                <span className="text-sm">+233 XX XXX XXXX</span>
              </div>
              <div className="flex items-center text-gray-400">
                <FiMail className="h-4 w-4 mr-2 text-primary-500" />
                <span className="text-sm">info@zipplatform.com</span>
              </div>
            </div>

            {/* Language Switcher - Mobile Optimized */}
            <div className="mt-6">
              <h3 className="text-white font-semibold mb-3">
                Language / Langue / Kasa
              </h3>
              <LanguageSwitcher />
            </div>
          </div>

          {/* Services */}
          <div>
            <h3 className="text-white font-semibold mb-4">Services</h3>
            <ul className="space-y-2">
              {footerLinks.services.map((link) => (
                <li key={link.path}>
                  <Link
                    to={link.path}
                    className="text-gray-400 hover:text-primary-500 transition-colors text-sm"
                  >
                    {link.name}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Company */}
          <div>
            <h3 className="text-white font-semibold mb-4">Company</h3>
            <ul className="space-y-2">
              {footerLinks.company.map((link) => (
                <li key={link.path}>
                  <Link
                    to={link.path}
                    className="text-gray-400 hover:text-primary-500 transition-colors text-sm"
                  >
                    {link.name}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Support */}
          <div>
            <h3 className="text-white font-semibold mb-4">Support</h3>
            <ul className="space-y-2">
              {footerLinks.support.map((link) => (
                <li key={link.path}>
                  <Link
                    to={link.path}
                    className="text-gray-400 hover:text-primary-500 transition-colors text-sm"
                  >
                    {link.name}
                  </Link>
                </li>
              ))}
            </ul>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="pt-8 border-t border-dark-700">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <p className="text-gray-400 text-sm mb-4 md:mb-0">
              &copy; {currentYear} ZIP Platform. All rights reserved.
            </p>

            {/* Social Links */}
            <div className="flex space-x-4">
              {socialLinks.map((social) => (
                <a
                  key={social.label}
                  href={social.href}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="p-2 text-gray-400 hover:text-primary-500 hover:bg-dark-800 rounded-lg transition-all"
                  aria-label={social.label}
                >
                  <social.icon className="h-5 w-5" />
                </a>
              ))}
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
