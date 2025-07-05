import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv
from PIL import Image

# Load environment variables
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
client = OpenAI()

# Set Streamlit page settings
st.set_page_config(page_title="SkinGen AI", layout="wide")

# Optional luxury styling override
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

# --- Top Header with Logo + Title on Left ---
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

# --- Centered Form ---
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

        except Exception as e:
            st.error(f"Error generating response: {e}")
