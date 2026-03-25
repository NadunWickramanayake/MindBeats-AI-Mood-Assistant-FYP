
import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import './Chatbot.css';

const Chatbot = () => {
  const [messages, setMessages] = useState([]);
  const [inputText, setInputText] = useState('');
  const [step, setStep] = useState(0);
  const [emotions, setEmotions] = useState([]);
  const [chatEnded, setChatEnded] = useState(false);
  const messagesEndRef = useRef(null);
  const navigate = useNavigate();

  useEffect(() => {
    setMessages([{ text: 'Hello! How are you feeling today?', isBot: true }]);
  }, []);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleEndChat = () => {
    const finalEmotion = mostFrequentEmotion();
    setChatEnded(true);
    navigate('/resources', { state: { finalEmotion } });
  };

  const handleSendMessage = async () => {
    if (chatEnded || !inputText.trim() || step >= 7) return;

    const userMessage = { text: inputText, isBot: false };
    setMessages(prev => [...prev, userMessage]);
    
    try {
      const response = await axios.post('http://127.0.0.1:5000/predict', { text: inputText });
      const detectedEmotion = response.data.emotion.toLowerCase();
      
      const botMessage = { 
        text: response.data.follow_up, 
        isBot: true,
        emotion: detectedEmotion,
        confidence: response.data.confidence
      };
      
      setMessages(prev => [...prev, botMessage]);
      setEmotions(prev => [...prev, detectedEmotion]);
      setStep(prev => prev + 1);
    } catch (error) {
      setMessages(prev => [...prev, { 
        text: "I'm having trouble understanding. Could you try rephrasing?", 
        isBot: true 
      }]);
    }

    setInputText('');

    if (step === 6) {
      const finalEmotion = mostFrequentEmotion();
      setTimeout(() => {
        setMessages(prev => [...prev, { 
          text: `Based on our conversation, I detect you're feeling ${finalEmotion}. Let me recommend some music!`,
          isBot: true,
          isFinal: true,
          emotion: finalEmotion
        }]);
      }, 1000);
    }
  };

  const mostFrequentEmotion = () => {
    const counts = {};
    let max = 0;
    let emotion = '';
    
    for (let e of emotions) {
      const lowerE = e.toLowerCase();
      counts[lowerE] = (counts[lowerE] || 0) + 1;
      if (counts[lowerE] > max) {
        max = counts[lowerE];
        emotion = lowerE;
      }
    }
    return emotion || 'neutral';
  };

  return (
    <div className="chatbot-container">
      <div className="particles-background">
        {[...Array(20)].map((_, i) => (
          <div key={i} className="particle" style={{
            top: `${Math.random() * 100}%`,
            left: `${Math.random() * 100}%`,
            width: `${5 + Math.random() * 10}px`,
            height: `${5 + Math.random() * 10}px`,
            animationDelay: `${Math.random() * 5}s`,
            opacity: 0.3 + Math.random() * 0.7,
            background: '#6B73FF'
          }} />
        ))}
      </div>

      <div className="glass-chat-container">
        <div className="chat-header">
          <h2>Mood Detection Chat</h2>
          <div className="progress-container">
            <div className="progress-bar" style={{ width: `${(step / 7) * 100}%` }} />
          </div>
        </div>

        <div className="messages-container">
          {messages.map((msg, index) => (
            <div 
              key={index} 
              className={`message ${msg.isBot ? 'bot' : 'user'} ${msg.isFinal ? 'final' : ''}`}
            >
              <div className="bubble">
                <p>{msg.text}</p>
                {msg.isFinal && (
                  <span className="emotion-badge">{msg.emotion}</span>
                )}
              </div>
            </div>
          ))}
          <div ref={messagesEndRef} />
        </div>

        <div className="input-container">
          <div className="input-group">
            <input
              type="text"
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
              placeholder={chatEnded ? 'Chat ended' : 'Type your response...'}
              disabled={chatEnded}
            />
            <button 
              onClick={handleSendMessage} 
              disabled={chatEnded || step >= 7}
              className="send-button"
            >
              {chatEnded ? '✓' : '→'}
            </button>
          </div>
          <button 
            className="end-chat-button"
            onClick={handleEndChat}
            disabled={chatEnded}
          >
            {chatEnded ? 'Analysis Complete' : 'End Chat'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default Chatbot;