import React from 'react';
import { Link } from 'react-router-dom';

const Footer = () => {
  return (
    <footer className="py-6 w-full border-t">
      <div className="container mx-auto px-4 md:px-6">
        <div className="flex flex-col sm:flex-row justify-between items-center">
          <p className="text-xs text-gray-500">© 2024 Event Management System. All rights reserved.</p>
          <nav className="flex gap-4 sm:gap-6 mt-4 sm:mt-0">
            <Link className="text-xs hover:underline underline-offset-4" to="/terms">
              Terms of Service
            </Link>
            <Link className="text-xs hover:underline underline-offset-4" to="/privacy">
              Privacy
            </Link>
          </nav>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
