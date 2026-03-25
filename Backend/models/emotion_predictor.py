import re
import string
import numpy as np
import pickle
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences


class EmotionPredictor:
    def __init__(self):
        try:
            # Load resources
            with open('models/labelEncoder.pickle', 'rb') as f:
                self.le = pickle.load(f)

            with open('models/tokenizer.pickle', 'rb') as f:
                self.tokenizer = pickle.load(f)

            self.model = load_model('models/Emotion_Tracking_Model.h5')
            self.str_punc = string.punctuation.replace(',', '').replace("'", '')

        except Exception as e:
            raise RuntimeError(f"Model loading failed: {str(e)}")

    def clean(self, text):
        text = re.sub(r'[^a-zA-Z ]', '', text)
        return text.lower()

    def predict_emotion(self, text):
        try:
            cleaned_text = self.clean(text)
            sequence = self.tokenizer.texts_to_sequences([cleaned_text])
            padded = pad_sequences(sequence, maxlen=256, truncating='pre')
            prediction = self.model.predict(padded)
            return self.le.inverse_transform([np.argmax(prediction)])[0], np.max(prediction)
        except Exception as e:
            raise RuntimeError(f"Prediction failed: {str(e)}")