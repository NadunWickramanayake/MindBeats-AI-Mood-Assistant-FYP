
import React from 'react';
import { useNavigate } from 'react-router-dom';
import './HomePage.css';

const HomePage = () => {
  const navigate = useNavigate();

  return (
    <div className="home-container">
      <div className="particles-background">
        {[...Array(30)].map((_, i) => (
          <div key={i} className="particle" style={{
            top: `${Math.random() * 100}%`,
            left: `${Math.random() * 100}%`,
            width: `${5 + Math.random() * 15}px`,
            height: `${5 + Math.random() * 15}px`,
            animationDelay: `${Math.random() * 5}s`,
            opacity: 0.3 + Math.random() * 0.7,
            background: '#FF9A8B'
          }} />
        ))}
      </div>

      <div className="glass-card">
        <div className="hero-section">
          <h1>Welcome to <span>MindBeats</span></h1>
          <p className="tagline">Your personal music recommendation assistant</p>
          
          <div className="feature-cards">
            <div className="feature-card">
              <div className="feature-icon">🎵</div>
              <h3>Personalized Music</h3>
              <p>Get recommendations tailored to your current mood</p>
            </div>
            
            <div className="feature-card">
              <div className="feature-icon">💬</div>
              <h3>Interactive Chat</h3>
              <p>Engage with our AI-powered emotion detector</p>
            </div>
            
            <div className="feature-card">
              <div className="feature-icon">📊</div>
              <h3>Mood Tracking</h3>
              <p>Discover patterns in your emotional journey</p>
            </div>
          </div>

          <button 
            className="cta-button"
            onClick={() => navigate('/chat')}
          >
            Start Your Mood Journey
          </button>
        </div>
      </div>
    </div>
  );
};

export default HomePage;