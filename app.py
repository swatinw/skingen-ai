import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv
from PIL import Image

# Load .env and API key
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
client = OpenAI()

# Streamlit config
st.set_page_config(page_title="SkinGen AI", layout="wide")

# Custom pastel-pink theme CSS
st.markdown("""
    <style>
    .stButton>button {
        background-color: #d98c9f;
        color: white;
        border-radius: 10px;
        font-weight: bold;
    }
    .stSelectbox div, .stTextArea textarea {
        border-radius: 8px;
    }
    .app-header {
        display: flex;
        align-items: center;
        margin-bottom: 1rem;
    }
    .app-header img {
        width: 90px;
        margin-right: 20px;
    }
    .app-title {
        font-size: 1.8rem;
        font-weight: bold;
        color: #2e2e2e;
    }
    .app-subtitle {
        font-size: 1rem;
        font-style: italic;
        color: #666666;
        margin-top: -8px;
    }
    </style>
""", unsafe_allow_html=True)

# --- Header with logo and brand text ---
header_col = st.columns([1])[0]
with header_col:
    st.markdown("<div class='app-header'>", unsafe_allow_html=True)
    try:
        logo = Image.open("assets/skingen_logo.png")
        st.image(logo, width=90)
    except Exception as e:
        st.warning(f"⚠️ Logo not found. {e}")
    st.markdown("""
        <div>
            <div class='app-title'>SkinGen AI</div>
            <div class='app-subtitle'>Since 2025 · Your personalized DIY skincare planner</div>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --- Main Form ---
st.markdown("### 🧴 Tell us about your skin")
with st.form("skin_form"):
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        skin_type = st.selectbox("Skin Type", ["Dry", "Oily", "Combination", "Sensitive", "Normal"])
        goal = st.selectbox("Skincare Goal", ["Glow", "Acne Control", "Anti-Aging", "Hydration", "Even Tone"])
        ingredients = st.text_area("Home Ingredients (optional)", placeholder="e.g. honey, turmeric, aloe vera")
        submit_btn = st.form_submit_button("✨ Generate My Routine")

# --- GPT Routine Generation ---
if submit_btn:
    with st.spinner("Creating your custom skincare routine..."):
        prompt = f"""
        Act as a skincare and DIY beauty expert.
        Skin type: {skin_type}
        Skincare goal: {goal}
        Available ingredients: {ingredients if ingredients else "none"}

        Please provide:
        1. A gentle morning skincare routine
        2. A restorative night routine
        3. Two easy DIY skincare recipes using available ingredients (or simple kitchen items)
        """
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
            result = response.choices[0].message.content
            st.subheader("🌞 Your Personalized Routine")
            st.markdown(result)

            # --- Visual Enhancements ---
            st.markdown("## 🖼 Explore Your Routine Visually")

            # Static visual image (download and place in assets/)
            st.image("assets/morning_routine_visual.png", caption="Your gentle morning skincare flow")

            # YouTube video suggestions based on skincare goal
            st.markdown("### 🎥 Recommended Routine Video")

            goal_videos = {
                "Glow": "https://www.youtube.com/watch?v=ZgEqyJFzQXg",
                "Acne Control": "https://www.youtube.com/watch?v=wHAsW9uFCYI",
                "Anti-Aging": "https://www.youtube.com/watch?v=yRIM5QxM6eI",
                "Hydration": "https://www.youtube.com/watch?v=GzEdAVsxzrU",
                "Even Tone": "https://www.youtube.com/watch?v=l6VpZuFgWbM"
            }

            video_url = goal_videos.get(goal)
            if video_url:
                st.video(video_url)

        except Exception as e:
            st.error(f"Error generating response: {e}")
