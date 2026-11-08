# Personalized Learning Path Recommendation Using Knowledge Tracing

Runnable academic prototype: Python, TensorFlow/Keras DKT, Streamlit, SQLite, Pandas and NumPy.

## Windows installation and run
Use Python 3.10 or 3.11. Open a terminal in this folder:

```bash
python -m venv venv
venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python train_model.py
streamlit run app.py
```

Open the local URL printed by Streamlit (normally http://localhost:8501).

## First use
1. Create/select a learner in the sidebar.
2. Open Take a Quiz, select a course and concept, and answer questions.
3. Submit; attempts are stored in `data/learning_path.db`.
4. Open Dashboard to view mastery and recommended concepts.
5. Export history as CSV if required.

## Notes
The training script creates synthetic sequences to demonstrate an LSTM-based DKT workflow. Synthetic results are not evidence of real-world learning effectiveness. For research evaluation, replace synthetic data with an appropriately licensed dataset (e.g. ASSISTments or EdNet), use chronological student-level splits, and report AUC, accuracy, F1, log loss and ranking metrics. The app uses a smoothed attempt-history estimate if a trained model is not available.

## Troubleshooting
- Python 3.10/3.11 is recommended for TensorFlow compatibility.
- If `python` is unavailable, try `py`.
- Keep the terminal open while running Streamlit.
- To reset demo records, stop the app and delete `data/learning_path.db`.
