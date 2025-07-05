import streamlit as st
import openai
import os
from dotenv import load_dotenv
from PIL import Image

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Set Streamlit page config
st.set_page_config(page_title="SkinGen AI", layout="centered")

# Load and display logo
logo_path = "assets/skingen_logo.png"  # or use skingen_logo_since2025.png if preferred
try:
    logo = Image.open(logo_path)
    st.image(logo, width=160)
except Exception as e:
    st.warning(f"Logo not found at '{logo_path}'. Please check the file path.")

# App Title & Subtitle
st.title("🌿 SkinGen AI")
st.markdown("Your personalized DIY skin & beauty routine planner\n\n_Since 2025_")

# Sidebar user input
st.sidebar.header("🧴 Tell us about your skin")
skin_type = st.sidebar.selectbox("Skin Type", ["Dry", "Oily", "Combination", "Sensitive", "Normal"])
goal = st.sidebar.selectbox("Skincare Goal", ["Glow", "Acne Control", "Anti-Aging", "Hydration", "Even Tone"])
ingredients = st.sidebar.text_area("Home Ingredients (optional)", placeholder="e.g. honey, turmeric, aloe vera")

# Generate Routine Button
if st.sidebar.button("✨ Generate My Routine"):
    with st.spinner("Creating your custom skincare routine..."):
        # Build GPT prompt
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
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
            result = response['choices'][0]['message']['content']
            st.subheader("🌞 Your Personalized Routine")
            st.markdown(result)

        except Exception as e:
            st.error(f"Error generating response: {e}")
