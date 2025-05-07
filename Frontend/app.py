import streamlit as st
import requests as r
import pandas as pd

FASTAPI_URL = "http://anime_backend:8000"

# Page configuration with expanded layout
st.set_page_config(
    page_title="🌟 Anime Recommender System", 
    page_icon="🎌",
    layout="wide"  # Use wide layout for more space
)

# Custom CSS with improved styling
custom_css = """
<style>
    /* Main container styling */
    .main-container {
        background-color: #f8f9fa;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 30px;
    }
    
    /* Header styling */
    .main-title {
        color: #2c3e50;
        font-size: 42px;
        font-weight: 700;
        text-align: center;
        margin-bottom: 10px;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }
    
    .subheader {
        font-size: 28px;
        color: #3498db;
        margin-top: 20px;
        margin-bottom: 20px;
        padding-bottom: 10px;
        border-bottom: 2px solid #3498db;
    }
    
    /* Anime card styling */
    .anime-card {
        background-color: white;
        border-radius: 12px;
        padding: 15px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        height: 100%;
        display: flex;
        flex-direction: column;
    }
    
    .anime-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 12px 20px rgba(0, 0, 0, 0.15);
    }
    
    .anime-image {
        border-radius: 8px;
        width: 100%;
        margin-bottom: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    .anime-title {
        font-size: 18px;
        font-weight: 600;
        text-align: center;
        color: #2c3e50;
        margin: 10px 0;
        height: 50px;
        overflow: hidden;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
    }
    
    /* Button styling */
    .custom-button {
        background-color: #3498db;
        color: white;
        text-decoration: none;
        padding: 10px 20px;
        border-radius: 30px;
        font-weight: 600;
        display: inline-block;
        text-align: center;
        cursor: pointer;
        transition: all 0.3s ease;
        border: none;
        width: 100%;
        margin-top: auto;
    }
    
    .custom-button:hover {
        background-color: #e74c3c;
        transform: scale(1.05);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    
    .recommend-button {
        background-color: #2ecc71;
        color: white;
        border-radius: 30px;
        padding: 10px 20px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .recommend-button:hover {
        background-color: #27ae60;
        transform: scale(1.05);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    
    /* Form styling */
    .form-container {
        background-color: white;
        padding: 25px;
        border-radius: 12px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
    }
    
    /* Divider styling */
    .divider {
        margin: 30px 0;
        border-top: 1px solid #e0e0e0;
    }
    
    /* Footer styling */
    .footer {
        text-align: center;
        color: #7f8c8d;
        margin-top: 40px;
        font-size: 14px;
    }
    
    /* Loading animation */
    .loading-spinner {
        display: flex;
        justify-content: center;
        margin: 20px 0;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# Main title with enhanced styling
st.markdown("<h1 class='main-title'>🌟 Anime Recommender System</h1>", unsafe_allow_html=True)

# Cache data loading function
@st.cache_data
def load_anime_data():
    response = r.get(f"{FASTAPI_URL}/get_anime_list")
    if response.status_code == 200:
        return pd.DataFrame(response.json())
    else:
        st.error("🚨 Failed to fetch anime data from API!")
        return pd.DataFrame()

animes = load_anime_data()

# Recommendation section
st.markdown("<div class='main-container'>", unsafe_allow_html=True)
st.markdown("<h2 class='subheader'>🎬 Find Similar Anime</h2>", unsafe_allow_html=True)

# Improved selectbox
s_anime = st.selectbox(
    "🔍 Search for an anime you like to get recommendations:", 
    animes['English'].values if not animes.empty else [],
    index=0 if not animes.empty else None,
    help="Select an anime from the dropdown to get similar recommendations"
)

# Styled button
if st.button('🎯 Show Recommendations', key='recommend_btn', use_container_width=True):
    with st.spinner('Finding the perfect anime matches for you...'):
        response = r.get(f"{FASTAPI_URL}/recommend_anime/{s_anime}")
        
        if response.status_code == 200:
            recommendations = response.json()["recommendations"]
            
            if recommendations:
                # Use container width instead of fixed columns
                recommendations_container = st.container()
                
                with recommendations_container:
                    cols = st.columns(3)
                    
                    for i in range(min(3, len(recommendations))):
                        with cols[i]:
                            st.markdown("<div class='anime-card'>", unsafe_allow_html=True)
                            
                            # Image with better styling
                            st.image(
                                recommendations[i]["image"], 
                                use_column_width=True,
                                output_format="JPEG",
                                caption=None
                            )
                            
                            # Anime title
                            st.markdown(
                                f"<p class='anime-title'>{recommendations[i]['name']}</p>", 
                                unsafe_allow_html=True
                            )
                            
                            # Button with improved styling
                            link = recommendations[i]['link']
                            st.markdown(
                                f"<a href='{link}' target='_blank' class='custom-button'>"
                                f"<i class='fas fa-info-circle'></i> View Details</a>", 
                                unsafe_allow_html=True
                            )
                            
                            st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.info("No similar anime found. Try another title!")
        else:
            st.error("🚨 No recommendations found or API error!")

st.markdown("</div>", unsafe_allow_html=True)

# Divider
st.markdown("<hr class='divider'>", unsafe_allow_html=True)

# Add New Anime section with improved styling
st.markdown("<div class='main-container'>", unsafe_allow_html=True)
st.markdown("<h2 class='subheader'>📝 Add New Anime</h2>", unsafe_allow_html=True)

st.markdown("<div class='form-container'>", unsafe_allow_html=True)
with st.form("add_anime_form"):
    # Form layout with columns for better organization
    col1, col2 = st.columns(2)
    
    with col1:
        ID = st.number_input("🔢 Anime ID", min_value=1, help="Unique identifier for the anime")
        title = st.text_input("📌 Original Title", help="Original title in Japanese or other language")
        english = st.text_input("🇬🇧 English Title", help="English translation of the title")
        anime_type = st.selectbox(
            "🎥 Type", 
            ["TV", "Movie", "OVA", "ONA", "Special"],
            help="Format of the anime"
        )
        premiered = st.text_input("📅 Premiered", placeholder="Fall 2023", help="Season and year of release")
        producers = st.text_input("🏭 Producers", help="Companies that produced the anime")
    
    with col2:
        studios = st.text_input("🎬 Studios", help="Animation studios")
        source = st.text_input("📖 Source", help="Original material (Manga, Light Novel, etc.)")
        genres = st.text_input("🎭 Genres", placeholder="Action, Romance, Comedy", help="Comma separated genres")
        themes = st.text_input("🎨 Themes", placeholder="School, Magic, Military", help="Comma separated themes")
        demographics = st.text_input("👥 Demographics", help="Target audience (Shounen, Seinen, etc.)")
        rating = st.text_input("⭐ Rating", placeholder="PG-13", help="Content rating")
        score = st.text_input("📊 Score", placeholder="8.75", help="Average user score")
    
    # Full width for synopsis
    synopsis = st.text_area(
        "📜 Synopsis", 
        height=150,
        help="Brief description of the anime plot"
    )

    # Submit button with improved styling
    submitted = st.form_submit_button(
        "➕ Add Anime", 
        use_container_width=True,
        type="primary"
    )
    
    if submitted:
        with st.spinner('Adding new anime to database...'):
            anime_data = {
                "ID": ID,
                "Title": title,
                "English": english,
                "Type": anime_type,
                "Premiered": premiered,
                "Producers": producers,
                "Studios": studios,
                "Source": source,
                "Genres": genres,
                "Themes": themes,
                "Demographics": demographics,
                "Rating": rating,
                "Score": score,
                "Synopsis": synopsis
            }
            
            response = r.post(f"{FASTAPI_URL}/add_anime/", json=anime_data)
            if response.status_code == 200:
                st.success(response.json().get("message", "✅ Anime added successfully!"))
                st.balloons()  # Add a fun element on success
            else:
                st.error("🚨 Failed to add anime!")

st.markdown("</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("<div class='footer'>", unsafe_allow_html=True)
st.markdown("© 2025 Anime Recommender System | Powered by Streamlit", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)