import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import './ResourcesPage.css';

const emotionPlaylists = {
  joy: {
    displayName: "Joyful Mood ✨",
    color: '#FF9A8B',
    gradient: 'linear-gradient(135deg, #FF9A8B 0%, #FF6B95 50%, #FF8E53 100%)',
    playlists: [
      {
        title: "Happy Vibes",
        emoji: "🎉",
        embed: "https://open.spotify.com/embed/playlist/37i9dQZF1DXdPec7aLTmlC",
        tracks: [
          { title: "Happy", artist: "Pharrell Williams", duration: "3:53" },
          { title: "Can't Stop the Feeling!", artist: "Justin Timberlake", duration: "3:56" },
          { title: "Good Vibrations", artist: "The Beach Boys", duration: "3:37" },
          { title: "Dancing Queen", artist: "ABBA", duration: "3:50" }
        ]
      },
      {
        title: "Dance Party",
        emoji: "💃",
        embed: "https://open.spotify.com/embed/playlist/37i9dQZF1DX0XUsuxWHRQd",
        tracks: [
          { title: "Uptown Funk", artist: "Mark Ronson", duration: "4:30" },
          { title: "I Gotta Feeling", artist: "Black Eyed Peas", duration: "4:49" },
          { title: "Shut Up and Dance", artist: "WALK THE MOON", duration: "3:19" },
          { title: "24K Magic", artist: "Bruno Mars", duration: "3:46" }
        ]
      }
    ],
    science: "Upbeat tempos (120-150 BPM) boost dopamine production by up to 9%, enhancing happiness and energy levels."
  },
  sadness: {
    displayName: "Melancholic Mood 🌊",
    color: '#6DD5ED',
    gradient: 'linear-gradient(135deg, #6DD5ED 0%, #2193B0 50%, #00D4FF 100%)',
    playlists: [
      {
        title: "Healing Sounds",
        emoji: "🌧️",
        embed: "https://open.spotify.com/embed/playlist/37i9dQZF1DX3rxVfibe1L0",
        tracks: [
          { title: "Someone Like You", artist: "Adele", duration: "4:45" },
          { title: "Hurt", artist: "Johnny Cash", duration: "3:38" },
          { title: "Say Something", artist: "A Great Big World", duration: "3:49" },
          { title: "Skinny Love", artist: "Bon Iver", duration: "3:59" }
        ]
      },
      {
        title: "Rainy Days",
        emoji: "☔",
        embed: "https://open.spotify.com/embed/playlist/37i9dQZF1DX8ymr6UES7vc",
        tracks: [
          { title: "The Night We Met", artist: "Lord Huron", duration: "3:28" },
          { title: "All I Want", artist: "Kodaline", duration: "5:05" },
          { title: "Fix You", artist: "Coldplay", duration: "4:55" },
          { title: "Breathe Me", artist: "Sia", duration: "4:34" }
        ]
      }
    ],
    science: "Slow-tempo music (60-80 BPM) synchronizes with a grieving heart rate, providing emotional validation and release."
  },
  anger: {
    displayName: "Energetic Mood 🔥",
    color: '#FF416C',
    gradient: 'linear-gradient(135deg, #FF416C 0%, #FF4B2B 50%, #FF8E53 100%)',
    playlists: [
      {
        title: "Cathartic Release",
        emoji: "⚡",
        embed: "https://open.spotify.com/embed/playlist/37i9dQZF1DX2pSTOxoPbx9",
        tracks: [
          { title: "Break Stuff", artist: "Limp Bizkit", duration: "2:46" },
          { title: "Killing in the Name", artist: "Rage Against the Machine", duration: "5:13" },
          { title: "Given Up", artist: "Linkin Park", duration: "3:09" },
          { title: "Bodies", artist: "Drowning Pool", duration: "3:21" }
        ]
      },
      {
        title: "Intense Focus",
        emoji: "🎯",
        embed: "https://open.spotify.com/embed/playlist/37i9dQZF1DX6OgmB2fwLGd",
        tracks: [
          { title: "Lose Yourself", artist: "Eminem", duration: "5:20" },
          { title: "Till I Collapse", artist: "Eminem", duration: "4:57" },
          { title: "Remember the Name", artist: "Fort Minor", duration: "3:50" },
          { title: "X Gon' Give It To Ya", artist: "DMX", duration: "3:37" }
        ]
      }
    ],
    science: "High-intensity music (90-120 BPM) helps channel angry energy into physical release, reducing cortisol levels by 25%."
  },
  fear: {
    displayName: "Calming Mood 🌌",
    color: '#7F7FD5',
    gradient: 'linear-gradient(135deg, #7F7FD5 0%, #7B2CBF 50%, #3C096C 100%)',
    playlists: [
      {
        title: "Peaceful Mind",
        emoji: "🌀",
        embed: "https://open.spotify.com/embed/playlist/37i9dQZF1DX4sWSpwq3LiO",
        tracks: [
          { title: "Weightless", artist: "Marconi Union", duration: "8:59" },
          { title: "Clair de Lune", artist: "Claude Debussy", duration: "5:04" },
          { title: "Spiegel im Spiegel", artist: "Arvo Pärt", duration: "9:24" },
          { title: "Gymnopédie No.1", artist: "Erik Satie", duration: "3:21" }
        ]
      },
      {
        title: "Nature Sounds",
        emoji: "🌳",
        embed: "https://open.spotify.com/embed/playlist/37i9dQZF1DWUKPeBypcpcP",
        tracks: [
          { title: "Forest Stream", artist: "Nature Recordings", duration: "45:00" },
          { title: "Ocean Waves", artist: "Natural Soundscape", duration: "52:30" },
          { title: "Mountain Wind", artist: "Wilderness Audio", duration: "38:15" },
          { title: "Rainforest Ambience", artist: "Jungle Sounds", duration: "41:20" }
        ]
      }
    ],
    science: "Ambient soundscapes reduce anxiety by 65% by lowering heart rate and encouraging deep breathing patterns."
  }
};

const ResourcesPage = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState(0);
  const [currentEmotion, setCurrentEmotion] = useState(null);

  useEffect(() => {
    const rawEmotion = (location.state?.finalEmotion || 'joy').toLowerCase();
    const emotionKey = Object.keys(emotionPlaylists).find(key => 
      rawEmotion.includes(key)
    ) || 'joy';
    
    setCurrentEmotion({
      key: emotionKey,
      ...emotionPlaylists[emotionKey]
    });
  }, [location.state]);

  if (!currentEmotion) return <div className="loading-screen">Loading your musical therapy...</div>;

  const currentPlaylist = currentEmotion.playlists[activeTab];

  return (
    <div className="resources-page" style={{ background: currentEmotion.gradient }}>
      <div className="particles">
        {[...Array(20)].map((_, i) => (
          <div key={i} className="particle" style={{
            '--delay': `${Math.random() * 5}s`,
            '--size': `${Math.random() * 8 + 4}px`,
            '--opacity': Math.random() * 0.6 + 0.2
          }} />
        ))}
      </div>

      <div className="glass-panel">
        <div className="emotion-header">
          <h1>{currentEmotion.displayName}</h1>
          <p className="mood-description">Curated music for your current emotional state</p>
        </div>

        <div className="playlist-tabs">
          {currentEmotion.playlists.map((playlist, index) => (
            <button
              key={index}
              className={`tab ${index === activeTab ? 'active' : ''}`}
              onClick={() => setActiveTab(index)}
            >
              <span className="tab-emoji">{playlist.emoji}</span>
              {playlist.title}
            </button>
          ))}
        </div>

        <div className="player-section">
          <div className="spotify-container">
            <iframe
              title="spotify-player"
              src={`${currentPlaylist.embed}?utm_source=generator&theme=0`}
              width="100%"
              height="400"
              frameBorder="0"
              allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture"
              loading="lazy"
            />
          </div>

          <div className="track-list-container">
            <div className="science-card">
              <div className="science-icon">💡</div>
              <p>{currentEmotion.science}</p>
            </div>

            <div className="track-list">
              <h2>Featured Tracks</h2>
              {currentPlaylist.tracks.map((track, index) => (
                <a
                  key={index}
                  href={`https://open.spotify.com/search/${encodeURIComponent(track.title)}`}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="track-card"
                >
                  <div className="track-number">{index + 1}</div>
                  <div className="track-details">
                    <h3>{track.title}</h3>
                    <p>{track.artist}</p>
                  </div>
                  <div className="track-duration">{track.duration}</div>
                  <div className="play-icon">▶</div>
                </a>
              ))}
            </div>
          </div>
        </div>

        <button className="back-button" onClick={() => navigate(-1)}>
          <span className="arrow">←</span> Back to Mood Analysis
        </button>
      </div>
    </div>
  );
};

export default ResourcesPage;