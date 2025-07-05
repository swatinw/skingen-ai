import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv
from PIL import Image
from fpdf import FPDF
import base64

# Load environment variables
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
client = OpenAI()

# Page configuration
st.set_page_config(page_title="SkinGen AI", layout="wide")

# Custom styling
st.markdown("""
    <style>
    body {
        background-color: #fdf6f0 !important;  /* pastel beige */
    }
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

# Header
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

# Form
st.markdown("### 🧴 Tell us about your skin")
with st.form("skin_form"):
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        skin_type = st.selectbox("Skin Type", ["Dry", "Oily", "Combination", "Sensitive", "Normal"])
        goal = st.selectbox("Skincare Goal", ["Glow", "Acne Control", "Anti-Aging", "Hydration", "Even Tone"])
        ingredients = st.text_area("Home Ingredients (optional)", placeholder="e.g. honey, turmeric, aloe vera")
        submit_btn = st.form_submit_button("✨ Generate My Routine")

# PDF Generator Function
def generate_pdf(skin_type, goal, routine_text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.set_text_color(217, 140, 159)
    pdf.set_font("Arial", style='B', size=16)
    pdf.cell(200, 10, "SkinGen AI - Personalized Skincare Routine", ln=True, align='C')

    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", size=12)
    pdf.ln(10)
    pdf.cell(200, 10, f"Skin Type: {skin_type}", ln=True)
    pdf.cell(200, 10, f"Goal: {goal}", ln=True)
    pdf.ln(10)

    for line in routine_text.split('\n'):
        pdf.multi_cell(0, 10, line)

    pdf_data = pdf.output(dest='S').encode('latin1')
    b64 = base64.b64encode(pdf_data).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="skingen_routine.pdf">📄 Download Routine as PDF</a>'
    return href

# Routine Generation
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

            # PDF Export
            pdf_link = generate_pdf(skin_type, goal, result)
            st.markdown("---")
            st.markdown("### 📥 Download Your Routine")
            st.markdown(pdf_link, unsafe_allow_html=True)

            # Visual Enhancements
            st.markdown("## 🖼 Explore Your Routine Visually")
            st.image("assets/morning_routine_visual.png", caption="Your gentle morning skincare flow")

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
