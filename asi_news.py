import streamlit as st
from google import genai
import feedparser
import json

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
st.sidebar.caption("Project for the Global Business Environment course made by Maria Carlota Gonçalves. Any problem contact 62408@novasbe.pt")

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
                    
                    # The "Analyze" Button
                if st.button(f"🔍 Analyze Perspectives", key=f"btn_{source_name}"):
                    with st.spinner("AI is synthesizing global viewpoints..."):
                        
                        # THE NEW STRUCTURED PROMPT
                        prompt = f"""
                        Analyze this news: {story.title} - {story.summary}
                        
                        You are a geopolitical analyzer. You must output YOUR ENTIRE RESPONSE as a valid, raw JSON object. 
                        DO NOT include any conversational text like "Here is the summary" or "As a journalist". Start directly with the {{ bracket.
                        
                        Use this EXACT JSON format:
                        {{
                          "summary": [
                            "First bullet point summary (keep it concise).",
                            "Second bullet point summary."
                          ],
                          "perspectives": [
                            {{
                              "title": "Name of Viewpoint 1 (e.g., EU Regulators)",
                              "drivers": "First paragraph about drivers and motivations.\\n\\nSecond paragraph about drivers and motivations.",
                              "context": "Analytical context including the historical background behind this point of view."
                            }},
                            {{
                              "title": "Name of Viewpoint 2",
                              "drivers": "First paragraph...\\n\\nSecond paragraph...",
                              "context": "Analytical context..."
                            }},
                            {{
                              "title": "Name of Viewpoint 3",
                              "drivers": "First paragraph...\\n\\nSecond paragraph...",
                              "context": "Analytical context..."
                            }}
                          ]
                        }}
                        """
                        try:
                            response = client.models.generate_content(model=MODEL_NAME, contents=prompt)
                            
                            # Clean the AI's text just in case it added markdown blocks
                            raw_text = response.text.strip()
                            if raw_text.startswith("```json"):
                                raw_text = raw_text[7:-3].strip()
                            elif raw_text.startswith("```"):
                                raw_text = raw_text[3:-3].strip()
                                
                            # Convert text to a Python Dictionary
                            analysis_data = json.loads(raw_text)
                            
                            # --- 1. RENDER THE SUMMARY ---
                            st.markdown("### 📝 Quick Summary")
                            for bullet in analysis_data["summary"]:
                                st.markdown(f"- {bullet}")
                            
                            st.markdown("---")
                            
                            # --- 2. RENDER THE EMPATHY HEADERS ---
                            st.markdown("<h3 style='color: #065f46;'>Perspectives</h3>", unsafe_allow_html=True)
                            st.markdown("#### Explore How Others Experience This Story")
                            st.caption("Take a moment to step outside your own perspective and explore how others experience this story.")
                            
                            # --- 3. RENDER THE SELECTABLE TABS ---
                            # This creates a list of titles for the tabs
                            tab_titles = [p["title"] for p in analysis_data["perspectives"]]
                            
                            # Create the Streamlit tabs
                            tabs = st.tabs(tab_titles)
                            
                            # Fill each tab with its specific content
                            for i, tab in enumerate(tabs):
                                with tab:
                                    st.markdown(f"<h4 style='color: #10b981; margin-top: 15px;'>{analysis_data['perspectives'][i]['title']}</h4>", unsafe_allow_html=True)
                                    
                                    st.markdown("**DRIVERS & MOTIVATIONS**")
                                    st.write(analysis_data['perspectives'][i]['drivers'])
                                    
                                    st.markdown("**ANALYTICAL CONTEXT**")
                                    st.info(analysis_data['perspectives'][i]['context']) # Puts history in a nice highlighted box!
                            
                            st.divider()
                            st.link_button(f"Read full original article on {source_name}", story.link)
                            st.markdown("---")
                            
                        except Exception as e:
                            st.error(f"Error structuring AI response: {e}")
                            st.info("The AI might have formatted the text incorrectly. Try clicking Analyze again!")

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

        ### Why We Built ASI News
        THE PROBLEM
        In today's polarized world, news is often presented through a single lens. This creates echo chambers where people only hear views that match their own. We believe that true understanding comes from exploring multiple perspectives. Like a chameleon that adapts and sees the world from many angles, ASI News — All Sides Included — helps you understand why people agree, disagree, or remain uncertain about important events. Our AI-powered analysis presents these viewpoints in a simple, empathetic way — making complex global events accessible to students, professionals, and curious minds of all ages.
        
        ### How It Works
        We aggregate real-time data from the world's leading publications—including Reuters, AP News, Al Jazeera, and The Financial Times. Then, our custom AI engine analyzes the stories to:
        📝 Provide clear, bias-free summaries.
        🌍 Highlight differing global perspectives.
        🕰️ Inject vital historical context so you understand the *why* behind the news.
        
        ### Our Values
        🔍 *Objectivity:* We present all sides of a story without bias, allowing readers to form their own informed opinions.
        🤝 *Empathy:* Understanding different perspectives helps us connect with people across cultures and viewpoints.
        🌐 *Trust:* We only source from established, reputable news organizations with proven track records.
        💡 *Accessibility:* Complex global events explained in simple, clear language for everyone to understand.

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
                    <li>🐍 Python & Streamlit</li>
                    <li>🧠 Google Gemini AI</li>
                    <li>📡 Global RSS Feeds</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)










