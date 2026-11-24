r"""
Run ONCE on your own computer (needs TensorFlow, i.e. your existing venv):

    cd Backend
    venv\Scripts\activate
    python scripts/export_lightweight.py

It converts the Keras model into models/weights.npz + models/meta.json
(used by the lightweight NumPy predictor) and then VERIFIES that the NumPy
version gives the same answers as the real Keras model.
"""
import os
import sys
import json
import pickle
import numpy as np

os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "2")
HERE = os.path.dirname(os.path.abspath(__file__))
MODELS = os.path.normpath(os.path.join(HERE, "..", "models"))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..")))

from tensorflow.keras.models import load_model
try:
    from keras.utils import pad_sequences
except ImportError:
    from tensorflow.keras.preprocessing.sequence import pad_sequences

print("Loading original Keras model ...")
model = load_model(os.path.join(MODELS, "Emotion_Tracking_Model.h5"))
with open(os.path.join(MODELS, "tokenizer.pickle"), "rb") as f:
    tok = pickle.load(f)
with open(os.path.join(MODELS, "labelEncoder.pickle"), "rb") as f:
    le = pickle.load(f)


def find(cls_name):
    found = [l for l in model.layers if l.__class__.__name__ == cls_name]
    if len(found) != 1:
        sys.exit(f"Expected exactly one {cls_name} layer, found {len(found)} - model differs from expected.")
    return found[0]


emb = find("Embedding").get_weights()[0]
conv_k, conv_b = find("Conv1D").get_weights()
bi = find("Bidirectional")
f_k, f_r, f_b = bi.forward_layer.get_weights()
b_k, b_r, b_b = bi.backward_layer.get_weights()
d_k, d_b = find("Dense").get_weights()

print("Shapes:", emb.shape, conv_k.shape, f_k.shape, f_r.shape, f_b.shape, d_k.shape)
assert f_b.ndim == 2 and f_b.shape[0] == 2, "GRU bias shape unexpected (reset_after=True expected)"

np.savez_compressed(
    os.path.join(MODELS, "weights.npz"),
    embedding=emb, conv_kernel=conv_k, conv_bias=conv_b,
    gru_f_kernel=f_k, gru_f_recurrent=f_r, gru_f_bias=f_b,
    gru_b_kernel=b_k, gru_b_recurrent=b_r, gru_b_bias=b_b,
    dense_kernel=d_k, dense_bias=d_b,
)
meta = {
    "word_index": {str(k): int(v) for k, v in tok.word_index.items()},
    "num_words": getattr(tok, "num_words", None),
    "oov_token": getattr(tok, "oov_token", None),
    "filters": getattr(tok, "filters", None),
    "lower": getattr(tok, "lower", True),
    "split": getattr(tok, "split", " "),
    "classes": [str(c) for c in le.classes_],
}
with open(os.path.join(MODELS, "meta.json"), "w", encoding="utf-8") as f:
    json.dump(meta, f)
print("Saved models/weights.npz and models/meta.json")

# ------------------------------------------------------------------ verification
from models.light_predictor import EmotionPredictor
light = EmotionPredictor(MODELS)

samples = [
    "I feel really happy today", "I am so excited and joyful about my results",
    "I feel hopeless and I cannot stop crying", "I am very sad and lonely tonight",
    "I am so angry at my boss right now", "this makes me furious",
    "I am terrified of the exam tomorrow", "I feel anxious and scared about everything",
    "okay", "", "x " * 400,
    "Today was a mix of everything: stress at work, a nice dinner with friends, and a long walk.",
]
worst, mismatches, tok_mismatch = 0.0, 0, 0
for s in samples:
    cleaned = light.clean(s)
    k_seq = pad_sequences(tok.texts_to_sequences([cleaned]), maxlen=256, truncating="pre")
    l_seq = light.encode(s)[None, :]
    if not np.array_equal(k_seq, l_seq):
        tok_mismatch += 1
    k_prob = model.predict(k_seq, verbose=0)[0]
    l_prob = light.predict_proba_ids(k_seq[0])
    worst = max(worst, float(np.max(np.abs(k_prob - l_prob))))
    mismatches += int(np.argmax(k_prob) != np.argmax(l_prob))

rng = np.random.default_rng(0)
for _ in range(10):
    ids = rng.integers(0, emb.shape[0], size=(1, 256))
    k_prob = model.predict(ids, verbose=0)[0]
    l_prob = light.predict_proba_ids(ids[0])
    worst = max(worst, float(np.max(np.abs(k_prob - l_prob))))
    mismatches += int(np.argmax(k_prob) != np.argmax(l_prob))

print(f"\nTokenizer mismatches : {tok_mismatch}")
print(f"Prediction mismatches: {mismatches}")
print(f"Largest probability difference vs Keras: {worst:.2e}")
if tok_mismatch == 0 and mismatches == 0 and worst < 1e-3:
    print("\nRESULT: PASS  - the lightweight model matches your original model.")
    sys.exit(0)
print("\nRESULT: FAIL  - do NOT deploy. Copy this whole output and send it to me.")
sys.exit(1)
