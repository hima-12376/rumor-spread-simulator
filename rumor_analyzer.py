from transformers import pipeline
import streamlit as st

@st.cache_resource
def load_classifier():
    return pipeline(
        "text-classification",
        model="cardiffnlp/twitter-roberta-base-sentiment-latest"
    )

def classify_rumor(text):
    classifier = load_classifier()   # load model only
    result = classifier(text)        # fresh prediction each time
    return result[0]['label'], result[0]['score']