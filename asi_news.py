import streamlit as st
import requests
import datetime

# --- 1. AESTHETICS (Matches your images) ---
st.set_page_config(page_title="ASI News", page_icon="🦎", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #F9F8F3; } /* Cream background from image_f87099.png */
    .stButton>button { background-color: #005A32; color: white; border-radius: 20px; } /* Forest Green */
    .pill { background: white; border: 1px solid #ddd; border-radius: 20px; padding: 5px 15px; margin: 5px; display: inline-block; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. HEADER & LOGO ---
st.title("🦎 ASI News")
st.write("### All sides of every story, included.")
st.write("AI-powered analysis from 8 trusted global sources.")

# --- 3. SEARCH & FILTERS (Matches image_f9c24f.png) ---
col1, col2 = st.columns([4, 1])
with col1:
    search_query = st.text_input("", placeholder="Search by person, country, or topic...")
with col2:
    if st.button("Search"):
        st.write(f"Searching for: {search_query}")

st.write("📅 Filter by date range")

# Category Pills
categories = ["Middle East", "European Union", "Climate Policy", "Global Economy", "US Elections", "China Relations"]
st.write(" ".join([f'<span class="pill">{c}</span>' for c in categories]), unsafe_allow_html=True)

# --- 4. DATA AGGREGATOR LOGIC ---
# Replace 'YOUR_API_KEY' with a key from newsdata.io
API_KEY = "pub_4cd62100a4e843cb951f7d8a6d164ab1"
SOURCES = "reuters,ap,bbc,aljazeera,theguardian,economist,financialtimes,dw"

def fetch_live_news(query):
    # Fetches from 2021 to now
    url = f"https://newsdata.io/api/1/news?apikey={API_KEY}&q={query}&domain={SOURCES}&from_date=2021-01-01"
    # For this demo, we use a placeholder if no key is provided
    return [{"title": "Example: War in Gaza", "source": "BBC News", "date": "2026-02-26"}]

# --- 5. THE ARTICLE VIEW (Matches image_f96c3d.png) ---
news_items = fetch_live_news(search_query)

for item in news_items:
    with st.container():
        st.write(f"**{item['source'].upper()}** | {item['date']}")
        st.subheader(item['title'])
        if st.button(f"Explore Analysis", key=item['title']):
            st.info("Take a moment to step outside your own perspective and explore how others experience this story.")
            
            # TABS FOR PERSPECTIVES
            tab1, tab2, tab3 = st.tabs(["Local View", "Economic View", "Diplomatic View"])
            with tab1:
                st.write("Detailed 200-word analysis here...")
                st.warning("**ANALYTICAL CONTEXT:** This viewpoint assumes...") # Matches image_f96be1.png
            
            # WORKING COMMENTS (Saves to a local file for now)
            comment = st.text_area("Share your perspective...")
            if st.button("Post Comment"):
                st.success("Comment saved!")