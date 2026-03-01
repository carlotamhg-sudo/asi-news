import streamlit as st
from google import genai
import feedparser
from datetime import datetime, timedelta

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="ASI News", 
    page_icon="🌍", 
    layout="wide"
)

# --- CSS FOR THE "LOVABLE" LOOK ---
st.markdown("""
    <style>
    .main { background-color: #f0f2f5; }
    .stButton>button { width: 100%; border-radius: 20px; background-color: #000; color: white; }
    .news-card {
        background-color: white;
        padding: 25px;
        border-radius: 12px;
        border-left: 5px solid #1a73e8;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .perspective-box {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #dee2e6;
        margin-top: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SECRETS CHECK ---
if "GEMINI_API_KEY" in st.secrets:
    API_KEY = st.secrets["GEMINI_API_KEY"]
else:
    st.error("Missing API Key! Please add GEMINI_API_KEY to your Streamlit Secrets.")
    st.stop()

client = genai.Client(api_key=API_KEY)

# --- APP LAYOUT ---
st.title("🗞️ ASI News")
st.caption("Bridging Global Perspectives for Business Leaders")

RSS_FEEDS = {
    "Reuters": "https://www.reutersagency.com/feed/?best-sectors=world-news",
    "AP News": "https://apnews.com/hub/international-news.rss",
    "BBC News": "http://feeds.bbci.co.uk/news/world/rss.xml",
    "Al Jazeera": "https://www.aljazeera.com/xml/rss/all.xml",
    "The Guardian": "https://www.theguardian.com/world/rss",
    "The Economist": "https://www.economist.com/international/rss.xml",
    "Financial Times": "https://www.ft.com/?format=rss",
    "Deutsche Welle": "https://rss.dw.com/rdf/rss-en-all"
}

source = st.selectbox("Choose a Global Source:", list(RSS_FEEDS.keys()))

if st.button("Analyze Recent News"):
    with st.spinner("Synthesizing global viewpoints..."):
        feed = feedparser.parse(RSS_FEEDS[source])
        
        if feed.entries:
            # Get the top story
            story = feed.entries[0]
            
            # PROMPT: Explicitly asking for simple language + History
            prompt = f"""
            Summarize this news for a general audience (very simple language). 
            Title: {story.title}
            Description: {story.summary}
            
            Format the response exactly like this:
            ## Summary
            (2 paragraphs maximum)
            
            ## Global Perspectives
            **Point of View 1: [Name]**
            - Current Stance: (Simple sentence)
            - History: (1 sentence explaining the historical background of this group's view)
            
            **Point of View 2: [Name]**
            - Current Stance: (Simple sentence)
            - History: (1 sentence explaining the historical background of this group's view)
            
            **Point of View 3: [Name]**
            - Current Stance: (Simple sentence)
            - History: (1 sentence explaining the historical background of this group's view)
            """
            
            try:
                response = client.models.generate_content(
                    model="gemini-2.0-flash", contents=prompt
                )
                
                # --- DISPLAY ---
                st.markdown(f'<div class="news-card"><h3>{story.title}</h3></div>', unsafe_allow_html=True)
                
                st.markdown(response.text)
                
                st.divider()
                st.link_button(f"Read Original on {source}", story.link)
                
            except Exception as e:
                st.error(f"Gemini AI Error: {e}")
        else:
            st.warning("No news found in the last 3 days for this source.")

