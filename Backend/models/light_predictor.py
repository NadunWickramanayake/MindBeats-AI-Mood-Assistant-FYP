"""
Lightweight emotion predictor: pure NumPy, no TensorFlow.

Re-implements the trained network
    Embedding(14980, 200) -> Dropout -> Conv1D(128, k=5, relu) -> MaxPool1D(4)
    -> Bidirectional(GRU(128)) -> Dense(4, softmax)
using the weights exported by scripts/export_lightweight.py
(models/weights.npz + models/meta.json).  Uses ~100 MB RAM instead of ~1 GB.
"""
import os
import re
import json
import numpy as np

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def _sigmoid(x):
    return 1.0 / (1.0 + np.exp(-np.clip(x, -60.0, 60.0)))


def _gru_last_state(x, kernel, recurrent, bias, reverse=False):
    """Keras GRU (reset_after=True, tanh/sigmoid). x: (T, F). Returns the final hidden state."""
    units = recurrent.shape[0]
    x_proj = x @ kernel + bias[0]                      # (T, 3*units), gate order: z, r, h
    h = np.zeros(units, dtype=np.float32)
    steps = range(x.shape[0] - 1, -1, -1) if reverse else range(x.shape[0])
    for t in steps:
        h_proj = h @ recurrent + bias[1]
        z = _sigmoid(x_proj[t, :units] + h_proj[:units])
        r = _sigmoid(x_proj[t, units:2 * units] + h_proj[units:2 * units])
        cand = np.tanh(x_proj[t, 2 * units:] + r * h_proj[2 * units:])
        h = z * h + (1.0 - z) * cand
    return h


def _conv1d_valid_relu(x, kernel, bias):
    """x: (T, C_in), kernel: (K, C_in, C_out) -> (T-K+1, C_out)."""
    k = kernel.shape[0]
    windows = np.lib.stride_tricks.sliding_window_view(x, k, axis=0)   # (T-K+1, C_in, K)
    out = np.einsum("tck,kcf->tf", windows, kernel, optimize=True) + bias
    return np.maximum(out, 0.0)


def _maxpool1d(x, pool):
    n = x.shape[0] // pool
    return x[: n * pool].reshape(n, pool, x.shape[1]).max(axis=1)


class EmotionPredictor:
    MAX_LEN = 256
    POOL = 4

    def __init__(self, models_dir=BASE_DIR):
        try:
            w = np.load(os.path.join(models_dir, "weights.npz"))
            self.emb = w["embedding"].astype(np.float32)
            self.conv_k = w["conv_kernel"].astype(np.float32)
            self.conv_b = w["conv_bias"].astype(np.float32)
            self.f_k, self.f_r, self.f_b = (w["gru_f_kernel"].astype(np.float32),
                                            w["gru_f_recurrent"].astype(np.float32),
                                            w["gru_f_bias"].astype(np.float32))
            self.b_k, self.b_r, self.b_b = (w["gru_b_kernel"].astype(np.float32),
                                            w["gru_b_recurrent"].astype(np.float32),
                                            w["gru_b_bias"].astype(np.float32))
            self.dense_k = w["dense_kernel"].astype(np.float32)
            self.dense_b = w["dense_bias"].astype(np.float32)
            with open(os.path.join(models_dir, "meta.json"), "r", encoding="utf-8") as f:
                meta = json.load(f)
        except Exception as e:
            raise RuntimeError(f"Model loading failed: {e}")

        self.word_index = meta["word_index"]
        self.num_words = meta.get("num_words")
        self.oov_token = meta.get("oov_token")
        self.filters = meta.get("filters", '!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n')
        self.lower = meta.get("lower", True)
        self.split = meta.get("split", " ")
        self.classes = meta["classes"]
        self._oov_index = self.word_index.get(self.oov_token) if self.oov_token else None
        self._filter_table = str.maketrans({c: self.split for c in self.filters})

    # ---- text -> ids (mirrors Keras Tokenizer + pad_sequences) ----
    @staticmethod
    def clean(text):
        return re.sub(r"[^a-zA-Z ]", "", text).lower()

    def texts_to_ids(self, text):
        if self.lower:
            text = text.lower()
        words = [w for w in text.translate(self._filter_table).split(self.split) if w]
        ids = []
        for w in words:
            i = self.word_index.get(w)
            if i is not None:
                if self.num_words and i >= self.num_words:
                    if self._oov_index is not None:
                        ids.append(self._oov_index)
                else:
                    ids.append(i)
            elif self._oov_index is not None:
                ids.append(self._oov_index)
        return ids

    def pad(self, ids):
        ids = ids[-self.MAX_LEN:]                       # truncating="pre"
        out = np.zeros(self.MAX_LEN, dtype=np.int64)    # padding="pre"
        if ids:
            out[-len(ids):] = ids
        return out

    def encode(self, text):
        return self.pad(self.texts_to_ids(self.clean(text)))

    # ---- network ----
    def predict_proba_ids(self, ids):
        x = self.emb[np.asarray(ids)]                              # (256, 200)
        x = _conv1d_valid_relu(x, self.conv_k, self.conv_b)        # (252, 128)
        x = _maxpool1d(x, self.POOL)                               # (63, 128)
        h_f = _gru_last_state(x, self.f_k, self.f_r, self.f_b, reverse=False)
        h_b = _gru_last_state(x, self.b_k, self.b_r, self.b_b, reverse=True)
        h = np.concatenate([h_f, h_b])                             # (256,)
        logits = h @ self.dense_k + self.dense_b
        e = np.exp(logits - logits.max())
        return e / e.sum()

    def predict_proba(self, text):
        return self.predict_proba_ids(self.encode(text))

    def predict_emotion(self, text):
        try:
            p = self.predict_proba(text)
            idx = int(np.argmax(p))
            return self.classes[idx], float(p[idx])
        except Exception as e:
            raise RuntimeError(f"Prediction failed: {e}")
