import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv
from PIL import Image

# Load environment variables
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
client = OpenAI()

# Page settings
st.set_page_config(page_title="SkinGen AI", layout="wide")

# Optional CSS for pastel pink luxury style (optional, complementing config.toml)
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
    </style>
""", unsafe_allow_html=True)

# --- Top Section ---
top_col1, top_col2 = st.columns([2, 1])

with top_col1:
    st.markdown("<h2 style='text-align: center;'>Your personalized DIY skin & beauty routine planner</h2>", unsafe_allow_html=True)

with top_col2:
    try:
        logo = Image.open("assets/skingen_logo.png")
        st.image(logo, width=100)
    except Exception as e:
        st.warning(f"⚠️ Logo not found. {e}")

    st.markdown("<h3 style='text-align: right; margin-top: 0;'>SkinGen AI</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: right; font-style: italic;'>Since 2025</p>", unsafe_allow_html=True)

# --- Centered Form ---
st.markdown("### 🧴 Tell us about your skin")
with st.form("skin_form"):
    col_a, col_b, col_c = st.columns([1, 2, 1])
    with col_b:
        skin_type = st.selectbox("Skin Type", ["Dry", "Oily", "Combination", "Sensitive", "Normal"])
        goal = st.selectbox("Skincare Goal", ["Glow", "Acne Control", "Anti-Aging", "Hydration", "Even Tone"])
        ingredients = st.text_area("Home Ingredients (optional)", placeholder="e.g. honey, turmeric, aloe vera")
        submit_btn = st.form_submit_button("✨ Generate My Routine")

# --- Generate Routine ---
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
