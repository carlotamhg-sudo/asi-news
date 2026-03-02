import streamlit as st
from google import genai
import feedparser

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="ASI News | All Sides Included", 
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
    "Deutsche Welle": "https://rss.dw.com/rdf/rss-en-all",
    "AP News": "https://rsshub.app/apnews/topics/ap-top-news"
}

# --- NAVIGATION ---
st.sidebar.image("https://img.icons8.com/color/96/chameleon.png", width=60)
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

    # --- THE MAGIC REFRESH BUTTON ---
    col1, col2 = st.columns([4, 1])
    with col1:
        st.subheader("Trending Today")
    with col2:
        if st.button("🔄 Refresh Live Feed", use_container_width=True):
            st.rerun() # This forces the app to wake up and fetch new data immediately!

    # Fetch headlines
    for source_name, url in SOURCES.items():
        feed = feedparser.parse(url)
        
        # Check if the feed has at least 2 stories
        if len(feed.entries) >= 2:
            # We will loop through the top 2 newest stories instead of just 1!
            for i in range(2): 
                story = feed.entries[i]
                
                # The UI Card for the story
                with st.container():
                    st.markdown(f"""
                        <div class="news-card">
                            <span class="source-badge">{source_name.upper()}</span>
                            <h3 style="margin-top: 5px;">{story.title}</h3>
                            <p style="color: #64748b;">{story.summary[:150]}...</p>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # Create a unique key for the button so Streamlit doesn't get confused
                    btn_key = f"btn_{source_name}_{i}"
                    
                    if st.button(f"🔍 Analyze Perspectives", key=btn_key):
                        with st.spinner("AI is synthesizing global viewpoints..."):
                            
                            prompt = f"""
                            Act as a professional geopolitical journalist. 
                            Read this news: {story.title} - {story.summary}
                            
                            1. Write a clear, engaging 2-paragraph summary. Use professional but highly accessible language (no heavy jargon).
                            2. Identify 3 distinct international or societal Points of View (e.g., EU Regulators, Developing Nations, Global Markets).
                            3. For each Point of View, provide exactly 1 sentence of Historical Context explaining the root of their stance.
                            
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
                    
                    st.write("") # Little space between cards

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
        To foster empathy and global understanding by providing objective, multi-perspective analysis of the world's most important news — because all sides must be included.

        THE PROBLEM
        ### Why We Built ASI News
        In today's polarized world, news is often presented through a single lens. This creates echo chambers where people only hear views that match their own. We believe that true understanding comes from exploring multiple perspectives. Like a chameleon that adapts and sees the world from many angles, ASI News — All Sides Included — helps you understand why people agree, disagree, or remain uncertain about important events. Our AI-powered analysis presents these viewpoints in a simple, empathetic way — making complex global events accessible to students, professionals, and curious minds of all ages.
        
        ### How It Works
        We aggregate real-time data from the world's leading publications—including Reuters, AP News, Al Jazeera, and The Financial Times. Then, our custom AI engine analyzes the stories to:
        📝 Provide clear, bias-free summaries.
        🌍 Highlight differing global perspectives.
        🕰️ Inject vital historical context so you understand the *why* behind the news.
        
        ### Our Values
        🔍 Objectivity: We present all sides of a story without bias, allowing readers to form their own informed opinions.
        🤝 Empathy: Understanding different perspectives helps us connect with people across cultures and viewpoints.
        🌐 Trust: We only source from established, reputable news organizations with proven track records.
        💡 Accessibility: Complex global events explained in simple, clear language for everyone to understand.

        ### Trusted Sources Only
        We exclusively source our news from globally recognized, reputable news organizations known for their journalistic integrity and fact-based reporting.
        📰 Al Jazeera    
        📰 AP News 
        📰 BBC News
        📰 Deutsche Welle
        📰 Financial Times
        📰 Reuters
        📰 The Economist
        📰 The Guardian
        """)
    
    with col2:
            st.markdown("""
            <div style="background-color: #d1fae5; padding: 20px; border-radius: 16px; border-left: 5px solid #10b981; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);">
                <h4 style="color: #065f46; margin-top: 0;">⚡ Powered By:</h4>
                <ul style="color: #334155; font-size: 0.95rem; line-height: 1.8;">
                    🐍 Python & Streamlit
                    🧠 Google Gemini AI
                    📡 Global RSS Feeds
                </ul>
            </div>
            """, unsafe_allow_html=True)




