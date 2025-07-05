import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv
from PIL import Image
from fpdf import FPDF
import base64
import requests

# Load environment variables
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
client = OpenAI()

st.set_page_config(page_title="SkinGen AI", layout="wide")

# Navigation Sidebar
st.sidebar.title("🧭 Navigation")
nav_option = st.sidebar.radio("Go to", ["🏠 Home", "🛍️ Shop", "👤 My Account", "📝 My Routines"])

# Header Styling and Layout
st.markdown("""
    <style>
    html, body, [class*="css"]  {
        background-color: #fdf6f0 !important;
    }
    .app-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.5rem 1rem;
    }
    .app-center {
        text-align: center;
        flex-grow: 1;
    }
    .app-icons {
        font-size: 1.5rem;
        display: flex;
        gap: 1.5rem;
        justify-content: flex-end;
    }
    .app-title { font-size: 2rem; font-weight: bold; color: #2e2e2e; margin-top: 0.5rem; }
    .app-subtitle { font-size: 1.1rem; font-style: italic; color: #666; margin-bottom: 0.5rem; }
    .footer { margin-top: 3rem; padding-top: 2rem; border-top: 1px solid #ccc; font-size: 0.9rem; color: #444; }
    .footer h5 { margin-bottom: 0.5rem; }
    .footer .column { width: 200px; display: inline-block; vertical-align: top; margin-right: 40px; }
    </style>
""", unsafe_allow_html=True)

# Header layout with logo + centered title + right icons
col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    st.markdown("🔍", unsafe_allow_html=True)

with col2:
    try:
        logo = Image.open("assets/skingen_logo.png")
        st.image(logo, width=80)
    except:
        st.warning("Logo not found")
    st.markdown("<div class='app-title'>SkinGen AI</div>", unsafe_allow_html=True)
    st.markdown("<div class='app-subtitle'>Your personalized DIY skincare planner</div>", unsafe_allow_html=True)

with col3:
    st.markdown("<div class='app-icons'>👤 ❤️ 🛍️</div>", unsafe_allow_html=True)

# Navigation Pages
if nav_option == "🏠 Home":
    if 'routine_count' not in st.session_state:
        st.session_state['routine_count'] = 0

    st.markdown("### 🧴 Tell us about your skin")
    if st.session_state['routine_count'] >= 1:
        st.warning("🚫 You've reached your daily limit of 1 free routine. Upgrade to Pro for unlimited access!")
        st.markdown("[🔓 Upgrade to Pro via Gumroad](https://your-gumroad-link.com)")
    else:
        with st.form("skin_form"):
            skin_type = st.selectbox("Skin Type", ["Dry", "Oily", "Combination", "Sensitive", "Normal"])
            goal = st.selectbox("Skincare Goal", ["Glow", "Acne Control", "Anti-Aging", "Hydration", "Even Tone"])
            ingredients = st.text_area("Home Ingredients (optional)", placeholder="e.g. honey, turmeric, aloe vera")
            email = st.text_input("📧 Want daily reminders? Enter your email")
            submit_btn = st.form_submit_button("✨ Generate My Routine")

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
            3. Two easy DIY skincare recipes
            """
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
            result = response.choices[0].message.content
            st.session_state['routine_count'] += 1
            st.subheader("🌞 Your Personalized Routine")
            st.markdown(result)
            pdf_link = generate_pdf(skin_type, goal, result)
            st.markdown("---")
            st.markdown("### 📥 Download Your Routine")
            st.markdown(pdf_link, unsafe_allow_html=True)

            if email:
                webhook_url = "https://hooks.zapier.com/hooks/catch/xxxx/yyyy"  # Replace with real webhook
                payload = {"email": email, "routine": result}
                try:
                    zap = requests.post(webhook_url, json=payload)
                    if zap.status_code == 200:
                        st.success("✅ You'll receive your daily routine via email!")
                    else:
                        st.warning("⚠️ Could not register for email reminders.")
                except:
                    st.warning("⚠️ Email sending failed.")

elif nav_option == "🛍️ Shop":
    st.header("🛍️ Shop Recommended Products")
    st.markdown("Coming soon: Affiliate bundles, DIY kits, and luxury skincare collections.")

elif nav_option == "👤 My Account":
    st.header("👤 My Account")
    st.markdown("Feature under development. In future, users can log in, save routines, and manage subscription.")

elif nav_option == "📝 My Routines":
    st.header("📝 Your Recent Routines")
    st.markdown("This feature is only available in the Pro version. Coming soon!")

# Footer
st.markdown("""
<div class='footer'>
    <div class='column'>
        <h5>SIGN UP</h5>
        <p>SHOPPING<br>Offers<br>Gift Cards<br>AfterPay<br>Store Locator<br>Corporate Info<br>Book A Service<br>Scent Finder</p>
    </div>
    <div class='column'>
        <h5>NEED HELP?</h5>
        <p>Returns/Exchanges<br>FAQ<br>Shipping<br>Account Sign-Up / Login<br>Live Chat with Customer Service<br>Live Chat with a Stylist<br>Customer Service: (866) 305 4706</p>
    </div>
    <div class='column'>
        <h5>ABOUT BRAND</h5>
        <p>Our Values<br>Commitments<br>Sustainability<br>Stories<br>Corporate Info<br>Careers<br>Ingredients Glossary</p>
    </div>
    <div class='column'>
        <h5>PRIVACY & TERMS</h5>
        <p>Privacy Policy<br>Do Not Sell or Share My Personal Information / Targeted Ads<br>Limit Use of My Sensitive Personal Information<br>Terms & Conditions<br>Accessibility<br>Supplier Relations<br>Consumer Health Data Privacy Statement</p>
    </div>
</div>
""", unsafe_allow_html=True)
