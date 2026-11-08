from pathlib import Path
import numpy as np

MODEL_PATH = Path(__file__).parent / "models" / "dkt_model.keras"

def history_mastery(history, concepts):
    result = {}
    for concept in concepts:
        rows = history[history["concept"] == concept] if not history.empty else history
        result[concept] = float((rows["is_correct"].sum() + 2) / (len(rows) + 4)) if len(rows) else 0.50
    return result

def predict_dkt(history, concepts):
    if not MODEL_PATH.exists() or history.empty:
        return None
    try:
        import tensorflow as tf
        model = tf.keras.models.load_model(MODEL_PATH)
        n = len(concepts)
        index = {name: i for i, name in enumerate(concepts)}
        tokens = [2 * index[r["concept"]] + int(r["is_correct"])
                  for _, r in history.iterrows() if r["concept"] in index]
        if not tokens:
            return None
        length = int(model.input_shape[1])
        x = np.zeros((1, length, 2*n), dtype=np.float32)
        for t, token in enumerate(tokens[-length:]):
            x[0, t, token] = 1.0
        pred = model.predict(x, verbose=0)[0]
        return {name: float(np.clip(pred[i], 0, 1)) for i, name in enumerate(concepts)}
    except Exception:
        return None

def estimate_mastery(history, concepts):
    dkt = predict_dkt(history, concepts)
    return (dkt, True) if dkt is not None else (history_mastery(history, concepts), False)
