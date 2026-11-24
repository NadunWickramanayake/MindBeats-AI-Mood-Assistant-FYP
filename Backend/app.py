import os
import logging


from flask import Flask, request, jsonify
from flask_cors import CORS

try:  # optional: load Backend/.env when running locally
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from models.light_predictor import EmotionPredictor  # NumPy-only (no TensorFlow)
import requests

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("mindbeats")

app = Flask(__name__)

# Comma-separated list of allowed frontend origins, e.g.
# ALLOWED_ORIGINS=https://mindbeats.vercel.app,http://localhost:3000
allowed = [o.strip() for o in os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",") if o.strip()]
CORS(app, origins=allowed)

MAX_TEXT_LEN = 1000

# Load the weights once at startup
predictor = EmotionPredictor()

# Gemini is optional: if the key is missing or the call fails, we fall back to a canned question.
# We call the REST API directly (via `requests`) to avoid SDK / protobuf version clashes with TensorFlow.
GEMINI_MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-2.5-flash-lite")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL_NAME}:generateContent"
if not GEMINI_API_KEY:
    log.warning("GEMINI_API_KEY not set - using fallback follow-up questions.")


def fallback_question(emotion: str) -> str:
    return f"I hear that you're feeling {emotion}. Can you tell me a bit more about what's behind that?"


def get_follow_up(emotion: str) -> str:
    if not GEMINI_API_KEY:
        return fallback_question(emotion)
    prompt = (
        f"The user is feeling {emotion}. Generate one thoughtful, non-repetitive "
        "follow-up question that helps explore this emotion deeper. "
        "Keep it natural, conversational and under 30 words."
    )
    try:
        r = requests.post(
            GEMINI_URL,
            headers={"x-goog-api-key": GEMINI_API_KEY, "Content-Type": "application/json"},
            json={"contents": [{"parts": [{"text": prompt}]}]},
            timeout=12,
        )
        r.raise_for_status()
        text = r.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
        return text or fallback_question(emotion)
    except Exception as e:  # rate limit, quota, network, safety block, bad JSON...
        log.warning("Gemini failed, using fallback: %s", e)
        return fallback_question(emotion)


@app.route("/")
def index():
    return jsonify({"service": "MindBeats API", "status": "ok"})


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json(silent=True) or {}
    text = data.get("text")

    if not isinstance(text, str) or not text.strip():
        return jsonify({"error": "Field 'text' is required."}), 400
    if len(text) > MAX_TEXT_LEN:
        return jsonify({"error": f"Text too long (max {MAX_TEXT_LEN} characters)."}), 400

    try:
        emotion, confidence = predictor.predict_emotion(text)
        emotion = str(emotion).lower()
        return jsonify({
            "emotion": emotion,
            "confidence": float(confidence),
            "follow_up": get_follow_up(emotion),
        })
    except Exception:
        log.exception("Prediction failed")
        return jsonify({"error": "Prediction failed."}), 500


if __name__ == "__main__":
    app.run(port=int(os.getenv("PORT", 5000)), debug=os.getenv("FLASK_DEBUG") == "1")
