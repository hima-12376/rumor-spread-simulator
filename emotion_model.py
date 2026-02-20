from transformers import pipeline
import streamlit as st

@st.cache_resource
def load_emotion_model():
    return pipeline(
        "text-classification",
        model="bhadresh-savani/distilbert-base-uncased-emotion",
        return_all_scores=True
    )

label_map = {
    "LABEL_0": "sadness",
    "LABEL_1": "joy",
    "LABEL_2": "love",
    "LABEL_3": "anger",
    "LABEL_4": "fear",
    "LABEL_5": "surprise"
}

def get_emotion_score(text):

    emotion = load_emotion_model()   # load model only
    result = emotion(text)           # fresh prediction each time

    if isinstance(result[0], list):
        scores = result[0]
    else:
        scores = result

    amp = 0

    for r in scores:
        raw_label = r.get('label', '')
        score = r.get('score', 0)

        label = label_map.get(raw_label, raw_label).lower()

        if label == 'fear':
            amp += score * 0.5
        elif label == 'anger':
            amp += score * 0.4
        elif label == 'surprise':
            amp += score * 0.3
        elif label == 'sadness':
            amp += score * 0.2
        elif label == 'joy':
            amp += score * 0.05
        elif label == 'love':
            amp += score * 0.05

    return amp