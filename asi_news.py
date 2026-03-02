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

# --- EDITORIAL CSS STYLING ---
st.markdown("""
    <style>
    /* Global Background */
    .stApp { background-color: #fbfbfb; }
    
    /* Typography & Colors */
    .serif-title { font-family: 'Georgia', serif; font-size: 2.8rem; font-weight: bold; color: #1a202c; line-height: 1.2; margin-bottom: 15px;}
    .serif-text { font-family: 'Georgia', serif; font-style: italic; font-size: 1.15rem; color: #334155; line-height: 1.7; margin-bottom: 15px; }
    .grey-caps { color: #64748b; font-size: 0.85rem; font-weight: 600; letter-spacing: 1px; text-transform: uppercase; margin-bottom: 10px; }
    .green-subtitle { color: #065f46; font-size: 1.5rem; font-weight: bold; margin-bottom: 10px; margin-top: 20px;}
    
    /* Article Header Elements */
    .source-badge-grey { background-color: #f1f5f9; color: #475569; padding: 4px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: bold; }
    .date-text { color: #94a3b8; font-size: 0.9rem; float: right; margin-top: 5px; }
    
    /* Cards & Boxes */
    .news-feed-card { background: white; padding: 25px; border-radius: 12px; border: 1px solid #e2e8f0; margin-bottom: 20px; transition: shadow 0.2s; }
    .news-feed-card:hover { box-shadow: 0 10px 15px -3px rgba(0,0,0,0.05); }
    
    .context-box { background-color: #fdf8f3; border: 1px solid #f6e8d9; border-radius: 12px; padding: 25px; margin-top: 20px; }
    .context-icon { color: #d97706; font-size: 1.2rem; font-weight: bold; margin-right: 10px; }
    
    /* Custom Streamlit Overrides for Solid Green Pills */
    div[data-testid="stRadio"] > div { flex-direction: row; flex-wrap: wrap; gap: 10px; }
    div[data-testid="stRadio"] div[role="radio"] { display: none; }
    div[data-testid="stRadio"] label { background-color: white; border: 1px solid #cbd5e1; padding: 10px 20px; border-radius: 30px; cursor: pointer; transition: all 0.2s;}
    div[data-testid="stRadio"] label:hover { border-color: #065f46; }
    div[data-testid="stRadio"] label[data-checked="true"] { background-color: #065f46 !important; border-color: #065f46 !important; }
    div[data-testid="stRadio"] label[data-checked="true"] p { color: white !important; font-weight: bold; }
    
    /* SOBER EDITORIAL LISTS (For About Us Page) */
    .sober-list { list-style-type: none; padding-left: 0; margin-left: 0; }
    .sober-list li { margin-bottom: 12px; padding-left: 1.8em; text-indent: -1.8em; }
    .sober-icon { filter: grayscale(100%) opacity(65%); display: inline-block; width: 1.8em; text-indent: 0; text-align: left; font-style: normal;}
    </style>
    """, unsafe_allow_html=True)

# --- SETUP API ---
if "GEMINI_API_KEY" in st.secrets:
    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("⚠️ Missing API Key in Streamlit Secrets!")
    st.stop()

MODEL_NAME = "gemini-2.5-flash"

# --- STATE MANAGEMENT ---
if "view" not in st.session_state:
    st.session_state.view = "feed"
if "current_story" not in st.session_state:
    st.session_state.current_story = {}
if "ai_analysis" not in st.session_state:
    st.session_state.ai_analysis = None
if "analyzed_url" not in st.session_state:
    st.session_state.analyzed_url = ""

# --- SOURCES ---
SOURCES = {
    "Reuters": "https://www.reutersagency.com/feed/?best-sectors=world-news",
    "AP News": "https://apnews.com/hub/international-news.rss",
    "BBC News": "http://feeds.bbci.co.uk/news/world/rss.xml",
    "Al Jazeera": "https://www.aljazeera.com/xml/rss/all.xml",
    "The Guardian": "https://www.theguardian.com/world/rss",
    "The Economist": "https://www.economist.com/international/rss.xml",
    "Financial Times": "https://www.ft.com/?format=rss",
    "Deutsche Welle": "https://rss.dw.com/rdf/rss-en-all"
}

# --- NAVIGATION ---
st.sidebar.image("https://img.icons8.com/color/96/chameleon.png", width=60)
st.sidebar.title("ASI News")
page = st.sidebar.radio("Navigation", ["📰 Live News Feed", "🦎 About Us"], label_visibility="collapsed")
st.sidebar.markdown("---")

# ==========================================
# PAGE 1: LIVE NEWS FEED & ARTICLE VIEW
# ==========================================
if page == "📰 Live News Feed":
    
    if st.session_state.view == "feed":
        head_col, btn_col = st.columns([4, 1])
        with head_col:
            st.markdown("<h1 style='color: #065f46; font-family: Georgia, serif; margin-bottom: 0;'>ASI News Dashboard</h1>", unsafe_allow_html=True)
            st.markdown("<p style='color: #64748b; font-size: 1.1rem; margin-top: 5px;'>Select an article below to analyze global perspectives.</p>", unsafe_allow_html=True)
        with btn_col:
            st.markdown("<br>", unsafe_allow_html=True) 
            if st.button("🔄 Refresh Live Feed", use_container_width=True):
                st.rerun()
                
        st.markdown("---")
        
        for source_name, url in SOURCES.items():
            feed = feedparser.parse(url)
            if len(feed.entries) >= 2:
                for i in range(2):
                    story = feed.entries[i]
                    
                    st.markdown(f"""
                        <div class="news-feed-card">
                            <span class="source-badge-grey">{source_name.upper()}</span>
                            <h3 style="margin-top: 15px; color: #1e293b; font-family: Georgia, serif;">{story.title}</h3>
                            <p style="color: #64748b; font-family: Georgia, serif; font-style: italic;">{story.summary[:150]}...</p>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button("Read & Analyze ➔", key=f"read_{source_name}_{i}"):
                        st.session_state.current_story = {
                            "source": source_name,
                            "title": story.title,
                            "summary": story.summary,
                            "link": story.link
                        }
                        st.session_state.view = "article"
                        st.rerun()

    elif st.session_state.view == "article":
        story = st.session_state.current_story
        
        if st.button("← Back to all stories"):
            st.session_state.view = "feed"
            st.rerun()
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown(f"""
            <div>
                <span class="source-badge-grey">{story['source'].upper()}</span>
                <span class="date-text">Latest News Update</span>
                <div class="serif-title" style="margin-top: 20px;">{story['title']}</div>
                <p style="font-size: 1.2rem; color: #64748b; line-height: 1.6; font-family: Georgia, serif;">{story['summary']}</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.link_button("Read original article ↗", story['link'])
        st.markdown("---")
        
        if st.session_state.analyzed_url != story['link']:
            with st.spinner("Generating AI perspectives..."):
                prompt = f"""
                Analyze this news: {story['title']} - {story['summary']}
                
                Output strictly as JSON. 
                Write clear, informative, yet concise explanations. Each bullet point MUST be exactly 1 to 2 well-crafted sentences. Do not clutter the mobile screen.
                
                Format exactly like this, using ONLY arrays of strings for the content:
                {{
                  "summary": ["Concise summary bullet 1...", "Concise summary bullet 2..."],
                  "perspectives": [
                    {{
                      "title": "Name of Viewpoint 1",
                      "drivers": ["Concise motivation explanation 1...", "Concise motivation explanation 2..."],
                      "context": ["Concise historical context 1...", "Concise historical context 2..."]
                    }},
                    {{
                      "title": "Name of Viewpoint 2",
                      "drivers": ["Concise motivation explanation 1...", "Concise motivation explanation 2..."],
                      "context": ["Concise historical context 1...", "Concise historical context 2..."]
                    }}
                  ]
                }}
                """
                try:
                    response = client.models.generate_content(model=MODEL_NAME, contents=prompt)
                    raw_text = response.text.strip()
                    if raw_text.startswith("```json"): raw_text = raw_text[7:-3].strip()
                    elif raw_text.startswith("```"): raw_text = raw_text[3:-3].strip()
                        
                    st.session_state.ai_analysis = json.loads(raw_text)
                    st.session_state.analyzed_url = story['link']
                except Exception as e:
                    st.error(f"Error parsing AI analysis: {e}")
                    if st.button("Retry Analysis"):
                        st.session_state.analyzed_url = "" 
                        st.rerun()
                        
        if st.session_state.ai_analysis:
            data = st.session_state.ai_analysis
            
            # QUICK SUMMARY (Emoji removed)
            st.markdown("<h3 style='color: #334155; font-family: Georgia, serif;'>Quick Summary</h3>", unsafe_allow_html=True)
            for bullet in data["summary"]:
                st.markdown(f"<li style='color: #475569; margin-bottom: 12px; line-height: 1.6; font-family: Georgia, serif;'>{bullet}</li>", unsafe_allow_html=True)
            
            st.markdown("<hr style='margin: 30px 0;'>", unsafe_allow_html=True)
            
            # PERSPECTIVES
            st.markdown("<div class='grey-caps' style='color: #065f46;'>PERSPECTIVES</div>", unsafe_allow_html=True)
            st.markdown("<div class='serif-title' style='font-size: 2.2rem;'>Explore How Others Experience This Story</div>", unsafe_allow_html=True)
            st.markdown("<p style='color: #64748b; font-size: 1.1rem; margin-bottom: 25px;'>Take a moment to step outside your own perspective and explore how others experience this story.</p>", unsafe_allow_html=True)

            perspective_titles = [p["title"] for p in data["perspectives"]]
            selected_tab = st.radio("Select a viewpoint:", perspective_titles, label_visibility="collapsed")
            active_data = next(item for item in data["perspectives"] if item["title"] == selected_tab)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            st.markdown(f"<div class='grey-caps'>{active_data['title']}</div>", unsafe_allow_html=True)
            st.markdown("<div class='grey-caps'>DRIVERS & MOTIVATIONS</div>", unsafe_allow_html=True)
            for driver in active_data['drivers']:
                st.markdown(f"<div class='serif-text'>• {driver}</div>", unsafe_allow_html=True)
            
            # BULLETED CONTEXT BOX (Unified HTML block)
            context_html = """
                <div class="context-box">
                    <div class="grey-caps" style="color: #b45309; margin-bottom: 15px;"><span class="context-icon">!</span> ANALYTICAL CONTEXT</div>
                    <ul style="color: #334155; font-family: 'Georgia', serif; font-size: 1.1rem; line-height: 1.6; padding-left: 20px; margin-bottom: 0;">
            """
            for ctx in active_data['context']:
                context_html += f"<li style='margin-bottom: 12px;'>{ctx}</li>"
            
            context_html += "</ul></div><br><br>"
            
            st.markdown(context_html, unsafe_allow_html=True)

# ==========================================
# PAGE 2: ABOUT US
# ==========================================
elif page == "🦎 About Us":
    st.session_state.view = "feed" 
    
    st.markdown("<div class='serif-title' style='font-size: 2.8rem;'>About ASI News</div>", unsafe_allow_html=True)
    st.markdown("---")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("<div class='green-subtitle'>Our Mission</div>", unsafe_allow_html=True)
        st.markdown("<div class='serif-text'>To foster empathy and global understanding by providing objective, multi-perspective analysis of the world's most important news — because all sides must be included.</div>", unsafe_allow_html=True)

        st.markdown("<div class='green-subtitle'>Why We Built ASI News</div>", unsafe_allow_html=True)
        st.markdown("<div class='grey-caps'>THE PROBLEM</div>", unsafe_allow_html=True)
        st.markdown("<div class='serif-text'>In today's polarized world, news is often presented through a single lens. This creates echo chambers where people only hear views that match their own. We believe that true understanding comes from exploring multiple perspectives. Like a chameleon that adapts and sees the world from many angles, ASI News — All Sides Included — helps you understand why people agree, disagree, or remain uncertain about important events. Our AI-powered analysis presents these viewpoints in a simple, empathetic way — making complex global events accessible to students, professionals, and curious minds of all ages.</div>", unsafe_allow_html=True)
        
        st.markdown("<div class='green-subtitle'>How It Works</div>", unsafe_allow_html=True)
        st.markdown("<div class='serif-text'>We aggregate real-time data from the world's leading publications—including Reuters, AP News, Al Jazeera, and The Financial Times. Then, our custom AI engine analyzes the stories to:</div>", unsafe_allow_html=True)
        st.markdown("""
        <ul class='sober-list serif-text'>
            <li><span class='sober-icon'>📝</span> <span>Provide clear, bias-free summaries.</span></li>
            <li><span class='sober-icon'>🌍</span> <span>Highlight differing global perspectives.</span></li>
            <li><span class='sober-icon'>🕰️</span> <span>Inject vital historical context so you understand the <em>why</em> behind the news.</span></li>
        </ul>
        """, unsafe_allow_html=True)
        
        st.markdown("<div class='green-subtitle'>Our Values</div>", unsafe_allow_html=True)
        st.markdown("""
        <ul class='sober-list serif-text'>
            <li><span class='sober-icon'>🔍</span> <span><strong>Objectivity:</strong> We present all sides of a story without bias, allowing readers to form their own informed opinions.</span></li>
            <li><span class='sober-icon'>🤝</span> <span><strong>Empathy:</strong> Understanding different perspectives helps us connect with people across cultures and viewpoints.</span></li>
            <li><span class='sober-icon'>🌐</span> <span><strong>Trust:</strong> We only source from established, reputable news organizations with proven track records.</span></li>
            <li><span class='sober-icon'>💡</span> <span><strong>Accessibility:</strong> Complex global events explained in simple, clear language for everyone to understand.</span></li>
        </ul>
        """, unsafe_allow_html=True)

        st.markdown("<div class='green-subtitle'>Trusted Sources Only</div>", unsafe_allow_html=True)
        st.markdown("<div class='serif-text'>We exclusively source our news from globally recognized, reputable news organizations known for their journalistic integrity and fact-based reporting.</div>", unsafe_allow_html=True)
        
        s_col1, s_col2 = st.columns(2)
        with s_col1:
            st.markdown("""
            <ul class='sober-list serif-text'>
                <li><span class='sober-icon'>📰</span> <span>Al Jazeera</span></li>
                <li><span class='sober-icon'>📰</span> <span>AP News</span></li>
                <li><span class='sober-icon'>📰</span> <span>BBC News</span></li>
                <li><span class='sober-icon'>📰</span> <span>Deutsche Welle</span></li>
            </ul>
            """, unsafe_allow_html=True)
        with s_col2:
            st.markdown("""
            <ul class='sober-list serif-text'>
                <li><span class='sober-icon'>📰</span> <span>Financial Times</span></li>
                <li><span class='sober-icon'>📰</span> <span>Reuters</span></li>
                <li><span class='sober-icon'>📰</span> <span>The Economist</span></li>
                <li><span class='sober-icon'>📰</span> <span>The Guardian</span></li>
            </ul>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background-color: #f8fafc; padding: 25px; border-radius: 8px; border: 1px solid #e2e8f0; border-top: 4px solid #64748b; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); position: sticky; top: 20px;">
            <div class='grey-caps' style="color: #475569; margin-top: 0; margin-bottom: 15px;"><span class='sober-icon'>⚡</span> Powered By</div>
            <ul class='sober-list serif-text' style="color: #334155; font-size: 1.05rem; line-height: 1.8; margin-bottom: 0;">
                <li><span class='sober-icon'>🐍</span> <span>Python & Streamlit</span></li>
                <li><span class='sober-icon'>🧠</span> <span>Google Gemini 2.5 AI</span></li>
                <li><span class='sober-icon'>📡</span> <span>Global RSS Feeds</span></li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
