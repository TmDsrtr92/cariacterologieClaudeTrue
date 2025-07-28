import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import DarkModeToggle from '../ui/DarkModeToggle';

const Header: React.FC = () => {
  const location = useLocation();

  const isActive = (path: string) => location.pathname === path;

  return (
    <header className="bg-dark-800 border-b border-dark-700 sticky top-0 z-40">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          {/* Logo/Brand */}
          <div className="flex items-center">
            <Link 
              to="/" 
              className="text-xl font-light text-dark-50 hover:text-primary-blue transition-colors"
            >
              Cariacterologie Claude
            </Link>
          </div>

          {/* Navigation */}
          <nav className="hidden md:flex items-center space-x-8">
            <Link
              to="/"
              className={`font-light transition-colors ${
                isActive('/') 
                  ? 'text-primary-blue' 
                  : 'text-dark-300 hover:text-dark-100'
              }`}
            >
              Q&A Chat
            </Link>
            <Link
              to="/styleguide"
              className={`font-light transition-colors ${
                isActive('/styleguide') 
                  ? 'text-primary-blue' 
                  : 'text-dark-300 hover:text-dark-100'
              }`}
            >
              Style Guide
            </Link>
          </nav>

          {/* Right side actions */}
          <div className="flex items-center space-x-4">
            <DarkModeToggle />
            
            {/* Mobile menu button */}
            <button className="md:hidden p-2 rounded-lg hover:bg-dark-700 transition-colors">
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            </button>
          </div>
        </div>

        {/* Mobile Navigation */}
        <div className="md:hidden pb-4">
          <div className="flex flex-col space-y-2">
            <Link
              to="/"
              className={`px-3 py-2 rounded-lg font-light transition-colors ${
                isActive('/') 
                  ? 'bg-primary-purple text-white' 
                  : 'text-dark-300 hover:text-dark-100 hover:bg-dark-700'
              }`}
            >
              Q&A Chat
            </Link>
            <Link
              to="/styleguide"
              className={`px-3 py-2 rounded-lg font-light transition-colors ${
                isActive('/styleguide') 
                  ? 'bg-primary-purple text-white' 
                  : 'text-dark-300 hover:text-dark-100 hover:bg-dark-700'
              }`}
            >
              Style Guide
            </Link>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;