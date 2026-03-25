from flask import Flask, request, jsonify
from flask_cors import CORS
from models.emotion_predictor import EmotionPredictor
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

predictor = EmotionPredictor()
genai.configure(api_key="AIzaSyBjtBk-52C1uOmS5Qv1eSBPqbdl-jbBNhw")

# updated gemini model gemini-1.5-flash to gemini-2.5-flash-lite due to unsupprted issue in 2026

gemini_model = genai.GenerativeModel("gemini-2.5-flash-lite")
@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    text = data['text']

    try:
        # Get emotion prediction
        emotion, confidence = predictor.predict_emotion(text)
        
        # Generate follow-up question using Gemini
        prompt = f"""The user is feeling {emotion.lower()}. Generate a thoughtful, 
        non-repetitive follow-up question that helps explore this emotion deeper. 
        Make it sound natural and conversational."""
        
        response = gemini_model.generate_content(prompt)
        
        return jsonify({
            'emotion': emotion.lower(),
            'confidence': float(confidence),
            'follow_up': response.text
        })
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)
