import os
import re
import pickle
import numpy as np
from tensorflow.keras.models import load_model

try:  # Keras 3 (TensorFlow >= 2.16)
    from keras.utils import pad_sequences
except ImportError:  # older Keras
    from tensorflow.keras.preprocessing.sequence import pad_sequences

# Resolve paths relative to this file so it works from any working directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class EmotionPredictor:
    MAX_LEN = 256

    def __init__(self):
        try:
            with open(os.path.join(BASE_DIR, "labelEncoder.pickle"), "rb") as f:
                self.le = pickle.load(f)
            with open(os.path.join(BASE_DIR, "tokenizer.pickle"), "rb") as f:
                self.tokenizer = pickle.load(f)
            self.model = load_model(os.path.join(BASE_DIR, "Emotion_Tracking_Model.h5"))
        except Exception as e:
            raise RuntimeError(f"Model loading failed: {e}")

    @staticmethod
    def clean(text):
        return re.sub(r"[^a-zA-Z ]", "", text).lower()

    def predict_emotion(self, text):
        try:
            sequence = self.tokenizer.texts_to_sequences([self.clean(text)])
            padded = pad_sequences(sequence, maxlen=self.MAX_LEN, truncating="pre")
            prediction = self.model.predict(padded, verbose=0)
            idx = int(np.argmax(prediction))
            return self.le.inverse_transform([idx])[0], float(np.max(prediction))
        except Exception as e:
            raise RuntimeError(f"Prediction failed: {e}")
