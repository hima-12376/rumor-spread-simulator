import streamlit as st
import matplotlib.pyplot as plt
import networkx as nx

from rumor_analyzer import classify_rumor
from emotion_model import get_emotion_score
from demographic_model import predict_demographic
from spread_simulator import simulate_spread
from feedback_model import compute_validity
from video_ai_detector import detect_ai_video
from fake_news_detector import check_fake_news   # NEW IMPORT

st.set_page_config(layout="wide")

# ----------- DARK CSS THEME -----------
st.markdown("""
<style>
.stApp {
    background-color: #0E1117;
}

h1 {
    color: #00FFD1;
    text-shadow: 0px 0px 10px #00FFD1;
}

[data-testid="stMetricValue"] {
    color: #00FFD1;
}

.stButton>button {
    background-color: #00FFD1;
    color: black;
    border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)

st.title("🧠 Multimodal Misinformation Monitoring Dashboard")

col1, col2 = st.columns([1,2])

# ---------------- LEFT PANEL ----------------
with col1:
    st.subheader("📝 Rumor Input")

    rumor = st.text_area("Enter Rumor Statement")

    uploaded_video = st.file_uploader(
        "Upload Video for AI Detection",
        type=["mp4","mov","avi"]
    )

    upvotes = st.number_input("👍 Trust", min_value=0)
    downvotes = st.number_input("👎 Distrust", min_value=0)

    simulate = st.button("Run Analysis")

# ---------------- CENTER PANEL ----------------
with col2:

    if simulate:

        if rumor.strip() == "":
            st.warning("Enter rumor first")

        else:

            topic, conf = classify_rumor(rumor)
            amp = get_emotion_score(rumor)
            validity = compute_validity(upvotes, downvotes)
            demo = predict_demographic(amp, validity)
            G = simulate_spread(amp, validity)

            # -------- TEXT ANALYSIS --------
            st.subheader("🧾 Linguistic Rumor Analysis")

            c1, c2, c3 = st.columns(3)

            c1.metric("Detected Topic", topic)
            c2.metric("Emotion Amplification", round(amp,2))
            c3.metric("Credibility Score", round(validity,2))

            st.write("👥 Most Impacted Demographic:", demo)

            # -------- WEB NEWS CHECK --------
            st.subheader("📰 Web-Based News Verification")

            news_verdict = check_fake_news(rumor)
            st.write(news_verdict)

            # -------- VIDEO ANALYSIS --------
            if uploaded_video is not None:
                st.subheader("🎥 Video Authenticity Analysis")
                verdict = detect_ai_video(uploaded_video)
                st.success(verdict)

            # -------- NETWORK SPREAD --------
            st.subheader("🌐 Network Spread Simulation")

            colors = []

            for node in G.nodes():
                if G.nodes[node]['state'] == 'I':
                    colors.append('#FF4B4B')
                else:
                    colors.append('#00FFD1')

            plt.figure(figsize=(6,6))
            nx.draw(G, node_color=colors, node_size=40)

            st.pyplot(plt)