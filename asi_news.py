import streamlit as st
from gnews import GNews
from datetime import datetime

# --- 1. BRANDING & UI ---
st.set_page_config(page_title="ASI News — All Sides Included", layout="wide")

# Chameleon Aesthetic CSS
st.markdown("""
    <style>
    .stApp { background-color: #F9F8F3; }
    div.stButton > button:first-child { 
        background-color: #005A32; 
        color: white; 
        border-radius: 5px; 
    }
    .news-card { 
        background-color: white; 
        padding: 20px; 
        border-radius: 12px; 
        border-left: 6px solid #005A32; 
        margin-bottom: 25px; 
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    .source-tag { color: #005A32; font-weight: bold; font-size: 0.9em; }
    </style>
""", unsafe_allow_html=True)

# --- 2. GNEWS ENGINE ---
def fetch_asi_news(topic_query):
    # Initialize GNews
    # 'period' can be used, but since 2021 we use start_date
    google_news = GNews(language='en', country='US', max_results=15)
    google_news.start_date = (2021, 1, 1) # Start archive from 2021
    
    # Strictly approved sources
    allowed = ["Reuters", "AP", "BBC", "Al Jazeera", "The Guardian", "The Economist", "FT", "DW"]
    
    # Fetch results
    results = google_news.get_news(topic_query)
    
    # Filter logic to ensure only your specific sources are shown
    filtered = []
    for item in results:
        publisher = item.get('publisher', {}).get('title', '')
        if any(source.lower() in publisher.lower() for source in allowed):
            filtered.append(item)
    return filtered

# --- 3. PAGE CONTENT ---
def home():
    st.title("🦎 ASI News")
    st.caption("2021 – 2026 Archive | Strictly Verified Sources")
    
    # Search and Filter Bar
    col1, col2 = st.columns([3, 1])
    with col1:
        search = st.text_input("Global Search", placeholder="Enter keywords...")
    with col2:
        st.write(" ") # Spacer
        if st.button("Refresh Feed"):
            st.rerun()

    # Category Tabs
    tabs = st.tabs(["Middle-East", "AI", "USA", "Ukraine", "EU", "Live News"])
    categories = ["Middle East", "Artificial Intelligence", "USA Politics", "Ukraine War", "European Union", "Breaking News"]

    for i, tab in enumerate(tabs):
        with tab:
            query = f"{categories[i]} {search}".strip()
            articles = fetch_asi_news(query)
            
            if not articles:
                st.info("No matching articles from the 8 approved sources found for this category.")
            
            for art in articles:
                with st.container():
                    st.markdown(f"""
                    <div class="news-card">
                        <span class="source-tag">{art['publisher']['title']}</span>
                        <h3>{art['title']}</h3>
                        <p><strong>Published:</strong> {art['published date']}</p>
                        <p>{art['description']}</p>
                        <a href="{art['url']}" target="_blank">Read Full Perspective →</a>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    with st.expander("Analytical Context & Perspectives"):
                        st.write("**Drivers & Motivations:** Stakeholders are balancing regional stability with economic interests.")
                        st.info("**AI Context:** This event aligns with the 2021-2024 trend of decentralized reporting.")

# --- 4. NAVIGATION & FOOTER ---
page = st.sidebar.radio("Navigation", ["Home", "About Us"])

if page == "Home":
    home()
else:
    st.title("About Us")
    st.markdown("### Mission\nTo foster empathy and global understanding by providing objective, multi-perspective analysis of the world's most important news — because all sides must be included.")
    st.markdown("### The Problem\nWHY WE BUILT ASI NEWS/nIn today's polarized world, news is often presented through a single lens. This creates echo chambers where people only hear views that match their own. We believe that true understanding comes from exploring multiple perspectives. Like a chameleon that adapts and sees the world from many angles, ASI News — All Sides Included — helps you understand why people agree, disagree, or remain uncertain about important events. Our AI-powered analysis presents these viewpoints in a simple, empathetic way — making complex global events accessible to students, professionals, and curious minds of all ages.")
    st.markdown("### Values\n- Objectivity\n- Empathy\n- Trust\n- Accessibility")

st.markdown("---")
st.markdown("<center><i>AI Disclaimer: Summaries and perspectives are AI-generated for analytical context.</i></center>", unsafe_allow_html=True)
st.markdown("<center>© 2026 ASI News — All Sides Included</center>", unsafe_allow_html=True)











