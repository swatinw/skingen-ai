import streamlit as st
import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

st.title("🌿 DIY Skin & Beauty Routine Planner")

skin_type = st.selectbox("Your Skin Type", ["Dry", "Oily", "Combination", "Sensitive", "Normal"])
goal = st.selectbox("Your Skin Goal", ["Glow", "Acne Control", "Anti-Aging", "Hydration", "Even Tone"])
ingredients = st.text_area("Home Ingredients (comma-separated)", placeholder="e.g. honey, turmeric, aloe vera")

if st.button("Generate My Routine"):
    with st.spinner("Creating your custom routine..."):
        prompt = f"""
        Act as a skincare and DIY beauty expert.
        Skin type: {skin_type}
        Goal: {goal}
        Ingredients: {ingredients}

        Please give:
        1. A simple morning routine
        2. A simple night routine
        3. Two DIY recipes I can make at home
        """
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        result = response['choices'][0]['message']['content']
        st.markdown(result)
