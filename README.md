# MindBeats: Emotion-Aware Music Recommendation System
MindBeats is an AI-powered full-stack application developed as a Final Year Project for the BEng (Hons) Software Engineering degree at the University of Westminster. It addresses the gap in real-time emotional support by combining deep learning-based emotion detection with a conversational chatbot and personalized music recommendations.

# 🚀 Key Features
Real-Time Emotion Detection: Utilizes a custom hybrid deep learning model combining Convolutional Neural Networks (CNN) and Bidirectional GRU layers to classify user emotional states from text.

High Accuracy: The model achieves a prediction accuracy of 96.09%.

Dynamic Conversational Interface: Implements a chatbot that generates context-sensitive follow-up questions using the Gemini API to deeply understand the user's mood.

Personalized Music Curation: Maps detected emotional trends to specific Spotify playlists to provide immediate mood-regulating support.

# 🛠️ Technology Stack
Frontend: React.js.

Backend: Python Flask RESTful API.

Machine Learning: TensorFlow/Keras, CNN + BiGRU layers.

APIs: Google Gemini API for dynamic dialogue generation.

# 🏗️ Installation & Setup
1. Prerequisites
Python 3.9+

Node.js (v18+) and npm

Google Gemini API Key

2. Backend Setup
Navigate to the backend directory and set up the Python environment:

Bash
cd Backend
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
Environment Variables:
Create a .env file in the Backend folder and add your API key:

Plaintext
GEMINI_API_KEY=your_actual_key_here
3. Frontend Setup
Navigate to the frontend directory:

Bash
cd Frontend/emotion-music-recommendation
npm install
# 🚀 Running the Application
Start the Backend
From the Backend folder (with your virtual environment active):

Bash
python app.py
The server will start at http://127.0.0.1:5000.

Start the Frontend
From the Frontend/emotion-music-recommendation folder:

Bash
npm start
The application will open at http://localhost:3000.

# 📜 License & Acknowledgements
This project was developed by Nadun Wickramanayake under the supervision of Prof. Damitha Karunaratna at the Informatics Institute of Technology (IIT) in collaboration with the University of Westminster.

Developed for academic purposes as a Final Year Project, April 2025.
