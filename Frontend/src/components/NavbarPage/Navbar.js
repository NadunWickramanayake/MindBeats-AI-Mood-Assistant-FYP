
import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import './Navbar.css';

const Navbar = () => {
  const location = useLocation();

  return (
    <nav className="glass-navbar">
      <div className="nav-logo">
        <span>MindBeats</span>
      </div>
      
      <div className="nav-links">
        <Link 
          to="/" 
          className={`nav-link ${location.pathname === '/' ? 'active' : ''}`}
        >
          Home
        </Link>
        <Link 
          to="/chat" 
          className={`nav-link ${location.pathname === '/chat' ? 'active' : ''}`}
        >
          Mood Chat
        </Link>
        <Link 
          to="/resources" 
          className={`nav-link ${location.pathname === '/resources' ? 'active' : ''}`}
        >
          My Playlists
        </Link>
      </div>

      {/* Empty spacer keeps the links centered. Sign In is planned as a future update. */}
      <div className="nav-auth"></div>
    </nav>
  );
};

export default Navbar;