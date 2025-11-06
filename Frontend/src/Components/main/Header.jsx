import React from 'react';
import { Link } from 'react-router-dom';
import { CalendarDays, User, LogOut } from 'lucide-react';

const Header = ({ username }) => {
  return (
    <header className="px-4 lg:px-6 h-14 flex items-center justify-between border-b">
      <Link className="flex items-center justify-center" to="/">
        <CalendarDays className="h-6 w-6 mr-2" />
        <span className="font-bold">Event Management System</span>
      </Link>
      <nav className="flex items-center gap-4 sm:gap-6">
        {username ? (
          <>
            <span className="text-sm font-medium flex items-center">
              <User className="h-4 w-4 mr-1" />
              {username}
            </span>
            <button className="text-sm font-medium hover:underline underline-offset-4 flex items-center">
              <LogOut className="h-4 w-4 mr-1" />
              Logout
            </button>
          </>
        ) : (
          <>
            <Link className="text-sm font-medium hover:underline underline-offset-4" to="/features">
              Features
            </Link>
            <Link className="text-sm font-medium hover:underline underline-offset-4" to="/pricing">
              Pricing
            </Link>
            <Link className="text-sm font-medium hover:underline underline-offset-4" to="/about">
              About
            </Link>
            <Link className="text-sm font-medium hover:underline underline-offset-4" to="/contact">
              Contact
            </Link>
          </>
        )}
      </nav>
    </header>
  );
};

export default Header;