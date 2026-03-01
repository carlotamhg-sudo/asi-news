import streamlit as st
from google import genai
import feedparser

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="ASI News | Global Pulse", 
    page_icon="🦎", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- MODERN "CUTE GREEN" CSS ---
st.markdown("""
    <style>
    /* Main background */
    .stApp { background-color: #f8fafc; }
    
    /* Hero Banner */
    .hero {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        padding: 40px 20px;
        border-radius: 16px;
        color: white;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 10px 15px -3px rgba(16, 185, 129, 0.2);
    }
    .hero h1 { color: white !important; font-size: 3rem; margin-bottom: 0; padding-bottom: 0;}
    .hero p { font-size: 1.2rem; opacity: 0.9; }
    
    /* News Cards */
    .news-card {
        background-color: white;
        padding: 24px;
        border-radius: 16px;
        border-top: 5px solid #10b981;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    .source-badge {
        background-color: #d1fae5;
        color: #065f46;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        display: inline-block;
        margin-bottom: 10px;
    }
    
    /* Custom Button */
    .stButton>button {
        background-color: #10b981;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #059669;
        box-shadow: 0 4px 6px rgba(16, 185, 129, 0.3);
    }
    </style>
    """, unsafe_allow_html=True)

# --- SETUP GEMINI ---
if "GEMINI_API_KEY" in st.secrets:
    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("⚠️ Missing API Key in Streamlit Secrets!")
    st.stop()

# Using the stable model
MODEL_NAME = "gemini-2.5-flash"

# --- NEWS SOURCES ---
SOURCES = {
    "Reuters": "https://www.reutersagency.com/feed/?best-sectors=world-news",
    "BBC News": "http://feeds.bbci.co.uk/news/world/rss.xml",
    "Al Jazeera": "https://www.aljazeera.com/xml/rss/all.xml",
    "The Guardian": "https://www.theguardian.com/world/rss",
    "The Economist": "https://www.economist.com/international/rss.xml",
    "Financial Times": "https://www.ft.com/?format=rss",
    "Deutsche Welle": "https://rss.dw.com/rdf/rss-en-all"
}

# --- NAVIGATION ---
st.sidebar.image("🦎", width=60)
st.sidebar.title("ASI News")
page = st.sidebar.radio("Navigation", ["📰 Live News Feed", "🦎 About Us"])
st.sidebar.markdown("---")
st.sidebar.caption("Project for Global Business Environment made by Maria Carlota Gonçalves. Any problem please contact 62408@novasbe.pt")

# ==========================================
# PAGE 1: LIVE NEWS FEED
# ==========================================
if page == "📰 Live News Feed":
    
    # Hero Section
    st.markdown("""
        <div class="hero">
            <h1>ASI News</h1>
            <p>Global events, analyzed from every perspective.</p>
        </div>
    """, unsafe_allow_html=True)

    st.subheader("Trending Today")
    
    # Fetch headlines instantly
    for source_name, url in SOURCES.items():
        feed = feedparser.parse(url)
        if feed.entries:
            story = feed.entries[0] # Get the top story
            
            # The UI Card for the story
            with st.container():
                st.markdown(f"""
                    <div class="news-card">
                        <span class="source-badge">{source_name.upper()}</span>
                        <h3 style="margin-top: 5px;">{story.title}</h3>
                        <p style="color: #64748b;">{story.summary[:150]}...</p>
                    </div>
                """, unsafe_allow_html=True)
                
                # The "Analyze" Button - placed right under the card
                if st.button(f"🔍 Analyze Perspectives", key=f"btn_{source_name}"):
                    with st.spinner("AI is synthesizing global viewpoints..."):
                        
                        # THE PROFESSIONAL PROMPT
                        prompt = f"""
                        Act as a professional geopolitical journalist. 
                        Read this news: {story.title} - {story.summary}
                        
                        1. Write a clear, engaging 2-paragraph summary. Use professional but highly accessible language (no heavy jargon).
                        2. Identify 3 distinct international or societal Points of View (e.g., EU Regulators, Developing Nations, Global Markets).
                        3. For each Point of View, provide a Historical Context explaining the root of their stance.
                        
                        Format with bold headers and bullet points.
                        """
                        try:
                            response = client.models.generate_content(model=MODEL_NAME, contents=prompt)
                            st.success("Analysis Complete!")
                            st.markdown(response.text)
                            st.link_button(f"Read full original article on {source_name}", story.link)
                            st.markdown("---")
                        except Exception as e:
                            st.error(f"Error connecting to AI: {e}")
                
                # Add a little space between news items
                st.write("") 

# ==========================================
# PAGE 2: ABOUT US
# ==========================================
elif page == "🦎 About Us":
    st.title("About ASI News")
    st.markdown("---")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### Our Mission
        In today's interconnected world, reading just one news source isn't enough. **ASI News** was built to break filter bubbles and provide a 360-degree view of global events.
        
        ### How It Works
        We aggregate real-time data from the world's leading publications—including Reuters, AP News, Al Jazeera, and The Financial Times. Then, our custom AI engine analyzes the stories to:
        * 📝 Provide clear, bias-free summaries.
        * 🌍 Highlight differing global perspectives.
        * 🕰️ Inject vital historical context so you understand the *why* behind the news.
        
        ### Built For
        This platform was developed as a comprehensive project for the **Global Business Environment** class, demonstrating the intersection of international relations, market economics, and modern AI technology.
        """)
    
    with col2:
        st.info("**Powered By:**")
        st.markdown("""
        * 🐍 Python & Streamlit
        * 🧠 Google Gemini 2.5 AI
        * 📡 Global RSS Feeds
        """)

