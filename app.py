import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv
from PIL import Image

# Load environment variables
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = OpenAI()

# Streamlit config
st.set_page_config(page_title="SkinGen AI", layout="wide")

# --- Top section with title and logo ---
col1, col2 = st.columns([4, 1])

with col1:
    st.title("🌿 SkinGen AI")
    st.markdown("_Since 2025_")
    st.markdown("Your personalized DIY skin & beauty routine planner")

with col2:
    try:
        logo = Image.open("assets/skingen_logo.png")
        st.image(logo, width=100)
    except Exception as e:
        st.warning(f"⚠️ Logo not found. {e}")

# --- Centered input form ---
st.markdown("### 🧴 Tell us about your skin")
with st.form("skin_form"):
    col3, col4, col5 = st.columns([1, 2, 1])
    with col4:
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
