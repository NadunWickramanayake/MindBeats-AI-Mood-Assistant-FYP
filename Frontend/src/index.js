import React from 'react';
import ReactDOM from 'react-dom/client';  // Use `react-dom/client` for React 18
import App from './App';
import './index.css';

const root = ReactDOM.createRoot(document.getElementById('root'));  // Create a root element
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
