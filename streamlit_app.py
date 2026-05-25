import streamlit as st
import requests
import datetime

# from exception.exceptions import TradingBotException
import sys

BASE_URL = "http://localhost:8000"  # Backend endpoint

st.set_page_config(
    page_title="AI Travel Planner",
    page_icon="✈️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# --- CUSTOM CSS ---
custom_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"]  {
    font-family: 'Outfit', sans-serif;
}

/* Background */
.stApp {
    background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
    background-attachment: fixed;
    color: #e2e8f0;
}

/* Hide default streamlit elements */
#MainMenu {visibility: hidden;}
header {visibility: hidden;}
footer {visibility: hidden;}

/* Custom Title Animation */
@keyframes float {
    0% { transform: translateY(0px); }
    50% { transform: translateY(-10px); }
    100% { transform: translateY(0px); }
}

.title-container {
    text-align: center;
    padding: 2rem 0 1rem 0;
}

.gradient-text {
    background: linear-gradient(to right, #38bdf8, #818cf8, #c084fc);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 3.5rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
    line-height: 1.2;
}

.subtitle {
    color: #94a3b8;
    font-size: 1.2rem;
    font-weight: 300;
    margin-bottom: 2rem;
}

/* Animated Vehicles */
.vehicle-container {
    display: flex;
    justify-content: center;
    gap: 1.5rem;
    margin-bottom: 1rem;
    font-size: 2.5rem;
}
.vehicle {
    display: inline-block;
    animation: float 3s ease-in-out infinite;
    filter: drop-shadow(0 4px 6px rgba(0,0,0,0.3));
}
.vehicle:nth-child(1) { animation-delay: 0.0s; }
.vehicle:nth-child(2) { animation-delay: 0.2s; }
.vehicle:nth-child(3) { animation-delay: 0.4s; }
.vehicle:nth-child(4) { animation-delay: 0.6s; }
.vehicle:nth-child(5) { animation-delay: 0.8s; }

/* Form Styling - Glassmorphism */
div[data-testid="stForm"] {
    background: rgba(30, 41, 59, 0.4) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 20px !important;
    padding: 2rem !important;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3) !important;
    backdrop-filter: blur(12px) !important;
    -webkit-backdrop-filter: blur(12px) !important;
}

/* Input Styling */
div[data-testid="stTextInput"] label p {
    color: #cbd5e1 !important;
    font-size: 1rem !important;
    font-weight: 500 !important;
}

div[data-testid="stTextInput"] > div > div > input {
    background: rgba(15, 23, 42, 0.7) !important;
    border: 2px solid rgba(129, 140, 248, 0.4) !important;
    color: #ffffff !important;
    border-radius: 30px !important;
    padding: 1rem 1.5rem !important;
    font-size: 1.25rem !important;
    letter-spacing: 0.5px !important;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
    box-shadow: 0 8px 16px -4px rgba(0, 0, 0, 0.3), inset 0 2px 4px rgba(255, 255, 255, 0.05) !important;
}

div[data-testid="stTextInput"] > div > div > input::placeholder {
    color: #64748b !important;
    font-style: italic !important;
}

div[data-testid="stTextInput"] > div > div > input:hover {
    border-color: #a855f7 !important;
    box-shadow: 0 8px 20px -4px rgba(168, 85, 247, 0.3) !important;
}

div[data-testid="stTextInput"] > div > div > input:focus {
    border-color: #a855f7 !important;
    box-shadow: 0 0 0 4px rgba(168, 85, 247, 0.2), 0 10px 25px -5px rgba(168, 85, 247, 0.4) !important;
    background: rgba(15, 23, 42, 0.9) !important;
    transform: translateY(-2px) !important;
}

/* Button Styling */
div[data-testid="stFormSubmitButton"] > button {
    background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.6rem 2rem !important;
    font-size: 1.1rem !important;
    font-weight: 600 !important;
    transition: all 0.3s ease !important;
    width: 100% !important;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-top: 1rem !important;
}

div[data-testid="stFormSubmitButton"] > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 10px 20px -10px rgba(168, 85, 247, 0.6) !important;
}
div[data-testid="stFormSubmitButton"] > button:active {
    transform: translateY(0) !important;
}

/* Spinner styling */
div.stSpinner > div > div > div > div > p {
    font-family: 'Outfit', sans-serif;
    color: #818cf8;
    font-size: 1.1rem;
}

/* Container Hack for Result Card */
div[data-testid="stVerticalBlock"]:has(.result-card-anchor) {
    background: rgba(30, 41, 59, 0.7);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 24px;
    padding: 2.5rem;
    margin-top: 2.5rem;
    box-shadow: 0 20px 40px rgba(0,0,0,0.3);
    backdrop-filter: blur(16px);
    animation: slideUp 0.6s ease-out forwards;
}

@keyframes slideUp {
    0% { opacity: 0; transform: translateY(20px); }
    100% { opacity: 1; transform: translateY(0); }
}

.result-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid rgba(255,255,255,0.1);
    padding-bottom: 1rem;
    margin-bottom: 1.5rem;
}

.result-title {
    background: linear-gradient(to right, #34d399, #3b82f6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 2rem;
    font-weight: 700;
    margin: 0;
}

.result-meta {
    color: #94a3b8;
    font-size: 0.9rem;
    text-align: right;
}

.result-footer {
    margin-top: 2rem;
    padding-top: 1.5rem;
    border-top: 1px dashed rgba(255,255,255,0.1);
    color: #64748b;
    font-size: 0.85rem;
    text-align: center;
    font-style: italic;
}

/* Markdown Content Styling within Result Card */
div[data-testid="stVerticalBlock"]:has(.result-card-anchor) .stMarkdown p,
div[data-testid="stVerticalBlock"]:has(.result-card-anchor) .stMarkdown li {
    color: #e2e8f0;
    font-size: 1.05rem;
    line-height: 1.7;
}

div[data-testid="stVerticalBlock"]:has(.result-card-anchor) .stMarkdown h1,
div[data-testid="stVerticalBlock"]:has(.result-card-anchor) .stMarkdown h2,
div[data-testid="stVerticalBlock"]:has(.result-card-anchor) .stMarkdown h3 {
    color: #f8fafc;
    font-weight: 600;
    margin-top: 1.5rem;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# --- HEADER SECTION ---
header_html = """
<div class="title-container">
    <div class="vehicle-container">
        <span class="vehicle">✈️</span>
        <span class="vehicle">🚆</span>
        <span class="vehicle">🚌</span>
        <span class="vehicle">🚗</span>
        <span class="vehicle">🚢</span>
    </div>
    <div class="gradient-text">AI Travel Planner</div>
    <div class="subtitle">Your personal, intelligent travel concierge</div>
</div>
"""
st.markdown(header_html, unsafe_allow_html=True)


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- MAIN FORM ---
with st.container():
    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
    
    with st.form(key="query_form", clear_on_submit=True):
        st.markdown("<p style='text-align: center; color: #cbd5e1; font-size: 1.2rem; margin-bottom: 1.5rem;'>Where would you like to explore next?</p>", unsafe_allow_html=True)
        user_input = st.text_input("Destination & Details", placeholder="e.g. Plan a 5-day romantic trip to Goa", label_visibility="collapsed")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submit_button = st.form_submit_button("Generate Itinerary 🌟")

# --- RESPONSE SECTION ---
if submit_button and user_input.strip():
    try:
        # Show thinking spinner while backend processes
        with st.spinner("🌍 Crafting your perfect journey..."):
            payload = {"question": user_input}
            response = requests.post(f"{BASE_URL}/query", json=payload)

        if response.status_code == 200:
            answer = response.json().get("answer", "No answer returned.")
            
            # Use a container for the result and inject our anchor class for CSS styling
            result_container = st.container()
            with result_container:
                st.markdown("<div class='result-card-anchor'></div>", unsafe_allow_html=True)
                
                # Render Header
                st.markdown(f"""
                <div class="result-header">
                    <h2 class="result-title">✨ Your Travel Itinerary</h2>
                    <div class="result-meta">
                        Generated: {datetime.datetime.now().strftime('%b %d, %Y at %H:%M')}<br>
                        By Toppo's Travel Agent
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Render Content
                st.markdown(answer)
                
                # Render Footer
                st.markdown("""
                <div class="result-footer">
                    *This travel plan was generated by AI. Please verify all information, especially prices, operating hours, and travel requirements before your trip.*
                </div>
                """, unsafe_allow_html=True)
                
        else:
            st.error(" Bot failed to respond: " + response.text)

    except Exception as e:
        raise Exception(f"The response failed due to {e}")