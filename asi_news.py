import streamlit as st
import requests
from datetime import datetime, timedelta

# --- 1. CONFIG & STYLING ---
st.set_page_config(page_title="ASI News — All Sides Included", layout="wide")

# Apply the Chameleon Aesthetic
st.markdown("""
    <style>
    .stApp { background-color: #F9F8F3; }
    div.stButton > button:first-child { background-color: #005A32; color: white; border-radius: 8px; }
    .news-card { background-color: white; padding: 20px; border-radius: 10px; border-left: 5px solid #005A32; margin-bottom: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
""", unsafe_allow_html=True)

# --- 2. LIVE DATA ENGINE ---
# This pulls the key from Streamlit's secure dashboard settings
API_KEY = st.secrets["news_api_key"] 

def fetch_asi_news(category, search_query=None):
    # Free Tier Limitation: Usually limited to the last 30 days. 
    # For 2021+ data, a 'Business' API plan is required.
    base_url = "https://gnews.io/api/v4/{endpoint}?{parameters}"
    sources = "reuters,associated-press,bbc-news,al-jazeera-english,the-guardian-uk,the-economist,financial-times,deutsche-welle"
    
    params = {
        'apiKey': API_KEY,
        'q': search_query if search_query else category,
        'sources': sources,
        'language': 'en',
        'sortBy': 'publishedAt'
    }
    
    response = requests.get(base_url, params=params)
    return response.json().get("articles", [])

# --- 3. APP INTERFACE ---
page = st.sidebar.radio("Navigation", ["Home", "About Us"])

if page == "Home":
    st.title("🦎 ASI News")
    query = st.text_input("Search archives...", placeholder="e.g. AI Policy")
    
    tabs = st.tabs(["Middle-East", "AI", "USA", "Ukraine", "EU", "Live News"])
    for i, tab in enumerate(tabs):
        cat_name = ["Middle-East", "AI", "USA", "Ukraine", "EU", "General"][i]
        with tab:
            articles = fetch_asi_news(cat_name, query)
            for art in articles[:5]: # Show top 5 for speed
                st.markdown(f"""
                <div class="news-card">
                    <h4>{art['title']}</h4>
                    <p><strong>{art['source']['name']}</strong> | {art['publishedAt'][:10]}</p>
                    <p>{art['description']}</p>
                </div>
                """, unsafe_allow_html=True)
                with st.expander("View Perspectives"):
                    st.write("**Analytical Context:** This report highlights regional shifts...")

elif page == "About Us":
    st.header("Mission: Objectivity through Multi-Perspective Clarity.")
    st.info("The Problem: Echo chambers isolate us. ASI News bridges the gap.")

st.sidebar.markdown("---")
st.sidebar.caption("© 2026 ASI News. Data strictly sourced from AP, Reuters, BBC, and partners.")







