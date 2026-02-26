pip install streamlit requests pandas pysqlite3
import streamlit as st
import requests
import sqlite3
from datetime import datetime

# --- PAGE CONFIG ---
st.set_page_config(page_title="ASI News", page_icon="🦎", layout="wide")

# --- CUSTOM THEME (Matching Screenshots) ---
def local_css():
    st.markdown(f"""
        <style>
        .stApp {{
            background-color: #F9F8F3;
            color: #1A1A1A;
        }}
        .main-header {{
            font-family: 'Serif';
            font-size: 50px;
            font-weight: 800;
            color: #002B1B;
            text-align: center;
        }}
        .stButton>button {{
            background-color: #005A32;
            color: white;
            border-radius: 20px;
            padding: 10px 25px;
        }}
        .news-card {{
            background-color: white;
            padding: 20px;
            border-radius: 15px;
            border: 1px solid #E0E0E0;
            margin-bottom: 20px;
        }}
        .analytical-context {{
            background-color: #FFF9E6;
            border-left: 5px solid #FFC107;
            padding: 15px;
            border-radius: 5px;
            font-style: italic;
        }}
        </style>
    """, unsafe_allow_html=True)

local_css()
def init_db():
    conn = sqlite3.connect('asi_community.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS comments 
                 (article_id TEXT, user_name TEXT, comment TEXT, date TEXT)''')
    conn.commit()
    conn.close()

init_db()
def main():
    # Sidebar Navigation
    st.sidebar.image("https://cdn-icons-png.flaticon.com/512/820/820158.png", width=100) # Placeholder Chameleon
    page = st.sidebar.radio("Navigate", ["Home", "News", "About Us"])

    if page == "Home":
        render_home()
    elif page == "News":
        render_news()
    elif page == "About Us":
        render_about()

def render_home():
    st.markdown('<h1 class="main-header">All sides of every story, included.</h1>', unsafe_allow_html=True)
    
    # Pill-shaped Search
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        query = st.text_input("", placeholder="Search global events...")
        if st.button("Search"):
            st.session_state.search_query = query
            # Logic to switch to news page can go here

    st.write("---")
    st.subheader("Trending Topics")
    cols = st.columns(4)
    topics = ["Middle East", "Climate Policy", "Global Economy", "Tech Ethics"]
    for i, topic in enumerate(topics):
        if cols[i].button(topic):
            st.info(f"Filtering for {topic}...")

def render_news():
    st.title("Latest Analysis")
    
    # Filter Sidebar
    with st.sidebar:
        st.date_input("Filter by Date Range", value=(datetime(2021, 1, 1), datetime.now()))
        sources = st.multiselect("Sources", ["Reuters", "BBC", "AP", "Al Jazeera", "The Guardian"])

    # Mock Data (Replace with requests.get logic using your API Key)
    articles = [
        {"source": "BBC NEWS", "title": "Global Markets React to New Trade Policy", "date": "25/02/2026"},
        {"source": "THE GUARDIAN", "title": "Climate Accord: New Implementation Milestones", "date": "25/02/2026"}
    ]

    for art in articles:
        with st.container():
            st.markdown(f"""
            <div class="news-card">
                <small>{art['source']} • {art['date']}</small>
                <h3>{art['title']}</h3>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Explore Analysis", key=art['title']):
                show_analysis(art)

def show_analysis(article):
    st.divider()
    st.header(article['title'])
    
    # 1. AI Summary
    st.subheader("Event Summary")
    st.write("Generating 3-paragraph summary via AI...") # Here you'd call Gemini/GPT-4
    
    # 2. Deep Dive Perspectives
    p_cols = st.columns(3)
    perspectives = ["Local Residents", "Global Markets", "Environmental Groups"]
    
    for i, p in enumerate(p_cols):
        with p:
            st.markdown(f"**Perspective: {perspectives[i]}**")
            st.markdown('<div class="analytical-context">This viewpoint assumes that economic growth is the primary driver of social stability.</div>', unsafe_allow_html=True)
            st.write("Lorum ipsum... (200+ words of AI generated analysis would appear here)")

    # 3. Community Comments
    st.write("---")
    st.subheader("Community Perspectives")
    with st.form("comment_form"):
        u_name = st.text_input("Name")
        u_comm = st.text_area("Share your perspective")
        if st.form_submit_button("Post"):
            # Insert into SQLite
            st.success("Perspective saved to the community database!")

def render_about():
    st.markdown("<h2 style='text-align: center;'>Our Mission</h2>", unsafe_allow_html=True)
    st.write("To foster empathy and global understanding by providing objective, multi-perspective analysis...")
    
    st.divider()
    st.markdown("<h2 style='text-align: center;'>Our Values</h2>", unsafe_allow_html=True)
    v1, v2, v3, v4 = st.columns(4)
    v1.metric("Objectivity", "All sides")
    v2.metric("Empathy", "Connection")
    v3.metric("Trust", "Reputable")
    v4.metric("Accessibility", "Simple/Clear")

if __name__ == "__main__":
    main()

st.subheader("Trusted Sources Only")
s_cols = st.columns(4)
sources_links = {
    "Reuters": "https://www.reuters.com",
    "AP News": "https://apnews.com",
    "BBC News": "https://www.bbc.com/news",
    "Al Jazeera": "https://www.aljazeera.com"
}

for i, (name, link) in enumerate(sources_links.items()):
    with s_cols[i % 4]:
        st.link_button(f"✅ {name}", link)

st.subheader("Trusted Sources Only")
s_cols = st.columns(4)
sources_links = {
    "Reuters": "https://www.reuters.com",
    "AP News": "https://apnews.com",
    "BBC News": "https://www.bbc.com/news",
    "Al Jazeera": "https://www.aljazeera.com"
}

for i, (name, link) in enumerate(sources_links.items()):
    with s_cols[i % 4]:
        st.link_button(f"✅ {name}", link)

