import streamlit as st
import pandas as pd
import numpy as np

# ==========================================
# PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="Spotify Global Analytics",
    page_icon="🎵",
    layout="wide"
)

# ==========================================
# DATA LOADING & CACHING
# ==========================================
@st.cache_data
def load_data():
    """
    Simulates loading the Spotify dataset.
    Replace with: return pd.read_csv('your_spotify_data.csv') if you have the file.
    """
    np.random.seed(42)
    genres = ['Pop', 'Synth-pop', 'Hip Hop', 'R&B', 'Indie Rock', 'Reggaeton']
    artists = ['The Weeknd', 'Taylor Swift', 'Drake', 'Ed Sheeran', 'Dua Lipa', 'Bad Bunny']
    
    data = {
        'Track_ID': [f"TRK{i:03d}" for i in range(1, 151)],
        'Track_Name': [f"Song {i}" for i in range(1, 151)],
        'Artist': np.random.choice(artists, 150),
        'Genre': np.random.choice(genres, 150),
        'Release_Year': np.random.randint(2015, 2024, 150),
        'Streams_Millions': np.random.uniform(500, 4500, 150).round(1),
        'Chart_Rank': np.random.randint(1, 200, 150),
        'BPM': np.random.randint(60, 200, 150),
        'Duration_Sec': np.random.randint(120, 300, 150)
    }
    return pd.DataFrame(data)

df = load_data()

# ==========================================
# SIDEBAR: FILTERS & NAVIGATION
# ==========================================
st.sidebar.header("🎛️ Dashboard Filters")
st.sidebar.write("Dynamically filter the dataset below:")

# Widget 1: Multiselect for Genre
selected_genres = st.sidebar.multiselect(
    "Select Genres:",
    options=df['Genre'].unique(),
    default=df['Genre'].unique()
)

# Widget 2: Slider for BPM
min_bpm, max_bpm = int(df['BPM'].min()), int(df['BPM'].max())
selected_bpm = st.sidebar.slider(
    "Select BPM Range:",
    min_value=min_bpm, max_value=max_bpm,
    value=(min_bpm, max_bpm)
)

# Widget 3: Selectbox for Artist
all_artists = ["All"] + list(df['Artist'].unique())
selected_artist = st.sidebar.selectbox("Filter by Artist:", options=all_artists)

# Apply Filters
filtered_df = df[
    (df['Genre'].isin(selected_genres)) &
    (df['BPM'] >= selected_bpm[0]) & 
    (df['BPM'] <= selected_bpm[1])
]
if selected_artist != "All":
    filtered_df = filtered_df[filtered_df['Artist'] == selected_artist]

# ==========================================
# MAIN APPLICATION LAYOUT (TABS)
# ==========================================
st.title("🎵 Spotify Global Chart Analytics Dashboard")
st.markdown("Explore patterns, streams, and musical attributes of global chart-topping tracks.")

# Organizing layout using Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "📂 Dataset Overview", 
    "📊 Data Analysis (KPIs)", 
    "📈 Visualizations", 
    "💡 Analytical Insights"
])

# ------------------------------------------
# TAB 1: Dataset Overview (Expanders & Containers)
# ------------------------------------------
with tab1:
    st.header("Dataset Overview")
    st.write("Browse the raw data and understand the structure of the dataset.")
    
    with st.container():
        st.dataframe(filtered_df, use_container_width=True, height=300)
    
    with st.expander("Click here to view Dataset Attributes Description"):
        st.markdown("""
        - **Track_ID / Name**: Unique identifiers for the song.
        - **Artist & Genre**: Categorical classifications of the track.
        - **Streams_Millions**: Total global streams on Spotify (Numerical).
        - **Chart_Rank**: Highest position achieved on the global charts.
        - **BPM**: Beats per minute (Tempo).
        - **Duration_Sec**: Length of the song in seconds.
        """)

# ------------------------------------------
# TAB 2: Data Analysis & KPIs (Columns)
# ------------------------------------------
with tab2:
    st.header("Key Performance Indicators (KPIs)")
    
    # Arranging KPIs side-by-side using Columns
    col1, col2, col3, col4 = st.columns(4)
    
    total_records = len(filtered_df)
    sum_streams = filtered_df['Streams_Millions'].sum()
    avg_streams = filtered_df['Streams_Millions'].mean()
    avg_bpm = filtered_df['BPM'].mean()
    
    col1.metric(label="Total Tracks", value=f"{total_records}")
    col2.metric(label="Total Streams (M)", value=f"{sum_streams:,.1f}")
    col3.metric(label="Avg Streams (M)", value=f"{avg_streams:,.1f}")
    col4.metric(label="Average Tempo (BPM)", value=f"{avg_bpm:.1f}")
    
    st.divider()
    
    # Category-wise record counts using Group By
    st.subheader("Category-wise Track Counts (By Genre)")
    genre_counts = filtered_df.groupby('Genre').size().reset_index(name='Track_Count')
    st.dataframe(genre_counts, use_container_width=True)

# ------------------------------------------
# TAB 3: Visualizations
# ------------------------------------------
with tab3:
    st.header("Data Visualizations")
    
    # 1. BAR CHART: Streams by Artist
    st.subheader("1. Distribution of Streams by Artist (Bar Chart)")
    st.write("Interpretation: Identifies which artists dominate the total stream counts.")
    artist_streams = filtered_df.groupby('Artist')['Streams_Millions'].sum().reset_index()
    st.bar_chart(data=artist_streams, x='Artist', y='Streams_Millions', color="#1DB954")
    
    # 2. LINE CHART: Trend over Time (Release Year)
    st.subheader("2. Streaming Trends Over Time (Line Chart)")
    st.write("Interpretation: Illustrates how total streams vary based on the track's release year.")
    yearly_streams = filtered_df.groupby('Release_Year')['Streams_Millions'].sum().reset_index()
    st.line_chart(data=yearly_streams, x='Release_Year', y='Streams_Millions', color="#FFFFFF")
    
    # 3. SCATTER PLOT: BPM vs Streams
    st.subheader("3. Relationship between Tempo (BPM) and Streams (Scatter Plot)")
    st.write("Interpretation: Examines if faster or slower songs tend to accumulate more streams.")
    st.scatter_chart(data=filtered_df, x='BPM', y='Streams_Millions', color='Genre')

# ------------------------------------------
# TAB 4: Insights
# ------------------------------------------
with tab4:
    st.header("Executive Summary & Insights")
    st.info("Based on the current filtered dataset, the following insights can be drawn:")
    
    st.markdown(f"""
    1. **Volume**: The current view encompasses **{total_records}** tracks, accumulating a massive **{sum_streams:,.1f} Million** global streams.
    2. **Acoustic Preferences**: The average tempo of chart-topping hits in this selection is **{avg_bpm:.1f} BPM**, indicating the general energy level preferred by listeners.
    3. **Genre Dominance**: By analyzing the Data Analysis tab, we can identify which genre produces the highest volume of hits among the selected filters.
    4. **Actionable Decision**: Music labels can utilize the Scatter Plot to determine if a specific tempo (BPM) correlates with higher stream volumes, aiding in future production decisions.
    """)