"""Train a small LSTM-based Deep Knowledge Tracing demonstration model."""
from pathlib import Path
import numpy as np
import tensorflow as tf
from config import COURSES
from knowledge_tracing import MODEL_PATH

SEQ_LEN = 20
EPOCHS = 8

def make_data(samples=1200, seed=42):
    rng = np.random.default_rng(seed)
    concepts = [x["name"] for x in COURSES["Python Fundamentals"]]
    n = len(concepts)
    X = np.zeros((samples, SEQ_LEN, 2*n), dtype=np.float32)
    y = np.zeros((samples, n), dtype=np.float32)
    for s in range(samples):
        skill = rng.uniform(0.25, 0.95, size=n)
        for t in range(SEQ_LEN):
            c = int(rng.integers(0, n))
            correct = int(rng.random() < skill[c])
            X[s, t, 2*c + correct] = 1.0
            skill[c] = min(0.98, skill[c] + (0.015 if correct else 0.005))
        y[s] = skill
    return X, y, concepts

def main():
    tf.keras.utils.set_random_seed(42)
    X, y, concepts = make_data()
    model = tf.keras.Sequential([
        tf.keras.layers.Input(shape=(SEQ_LEN, X.shape[-1])),
        tf.keras.layers.LSTM(64),
        tf.keras.layers.Dense(32, activation="relu"),
        tf.keras.layers.Dense(len(concepts), activation="sigmoid")
    ])
    model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["mae"])
    model.fit(X, y, epochs=EPOCHS, batch_size=32, validation_split=0.2, verbose=1)
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    model.save(MODEL_PATH)
    print("Saved DKT model to", MODEL_PATH)
    print("Output concept order:", concepts)

if __name__ == "__main__":
    main()
