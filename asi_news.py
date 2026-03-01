import streamlit as st
from google import genai
import feedparser

# --- CONFIG ---
st.set_page_config(page_title="ASI News", page_icon="🌍", layout="wide")

# Use the NEW 2026 stable model name
MODEL_NAME = "gemini-2.5-flash" 

# --- STYLING ---
st.markdown("""
    <style>
    .reportview-container { background: #f0f2f5 }
    .news-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        border-bottom: 4px solid #1a73e8;
        margin-bottom: 25px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

# --- SECRETS & CLIENT ---
if "GEMINI_API_KEY" in st.secrets:
    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Please add your GEMINI_API_KEY to Streamlit Secrets!")
    st.stop()

# --- THE NEWS SOURCES ---
SOURCES = {
    "Reuters": "https://www.reutersagency.com/feed/?best-sectors=world-news",
    "BBC": "http://feeds.bbci.co.uk/news/world/rss.xml",
    "Al Jazeera": "https://www.aljazeera.com/xml/rss/all.xml",
    "The Economist": "https://www.economist.com/international/rss.xml",
    "Financial Times": "https://www.ft.com/?format=rss"
}

st.title("🗞️ ASI News: Global Pulse")
st.write("Automatically synthesizing today's global perspectives.")

# --- AUTOMATIC LOADING ---
# This loop runs the moment the page opens
for name, url in SOURCES.items():
    with st.expander(f"📌 Latest from {name}", expanded=True):
        feed = feedparser.parse(url)
        if feed.entries:
            story = feed.entries[0] # Get the very latest story
            
            # Simple Prompt for the "Friendly" and "Historical" requirements
            prompt = f"""
            News: {story.title} - {story.summary}
            1. Summarize in 2 simple paragraphs (easy for a kid to read).
            2. Give 3 Points of View. For each, add 1 sentence of HISTORY explaining why they feel that way.
            """
            
            try:
                response = client.models.generate_content(model=MODEL_NAME, contents=prompt)
                
                st.markdown(f"### {story.title}")
                st.markdown(response.text)
                st.caption(f"[Original Source]({story.link})")
            except Exception as e:
                st.write("AI is currently busy. Click to retry.")
        else:
            st.write("No recent news found for this source.")
