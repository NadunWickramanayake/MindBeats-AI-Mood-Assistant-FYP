
import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Navbar from './components/NavbarPage/Navbar';
import Home from './components/HomePage/Home';
import SignIn from './components/SignInPage/SignIn';
import Chatbot from './components/Chatbot/Chatbot';
import ResourcesPage from './components/ResourcesPage/ResourcesPage';
import './App.css';

function App() {
  return (
    <Router>
      {/* Navbar Component */}
      <Navbar />

      {/* Routes */}
      <Routes>
        {/* Home Page */}
        <Route path="/" element={<Home />} />

        {/* Sign-In Page */}
        <Route path="/signin" element={<SignIn />} />

        {/* Chatbot Page */}
        <Route path="/chat" element={<Chatbot />} />

     
        {/* Resources Page */}
        <Route path="/resources" element={<ResourcesPage />} />
      </Routes>
    </Router>
  );
}

export default App;