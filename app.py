import sys
import subprocess
import pandas as pd
import streamlit as st
import sqlite3

st.title("🌞 astro-ph.SR Daily Digest")

# Sidebar filters
priority = st.sidebar.selectbox(
    "Priority",
    ["All", "High", "Medium", "Low"]
)

level = st.sidebar.selectbox(
    "Teaching Level",
    [
        "All",
        "Intro Astronomy",
        "Undergraduate",
        "Advanced Undergraduate",
        "Graduate",
        "Research"
    ]
)

if st.button("Refresh Papers"):
    subprocess.run([sys.executable, "fetch.py"])
    st.success("Paper list updated")

# Load data
conn = sqlite3.connect("papers.db")

df = pd.read_sql_query(
    """
    SELECT *
    FROM papers
    """,
    conn
)

conn.close()

RESEARCH_INTERESTS = {
    "Cataclysmic Variables": 10,
    "Dwarf Novae": 10,
    "Novae": 9,
    "Accretion Disks": 9,
    "Variable Stars": 8,
    "White Dwarfs": 7,
    "Binary Stars": 7,
    "Time Domain Astronomy": 6,
    "TESS": 5,
    "Gaia": 4
}

def calculate_relevance(tag_string):

    if pd.isna(tag_string):
        return 0

    score = 0

    tags = tag_string.split(",")

    for tag in tags:

        tag = tag.strip()

        score += RESEARCH_INTERESTS.get(
            tag,
            0
        )

    return score
    
df["relevance_score"] = df[
    "research_tags"
].apply(calculate_relevance)

recommended_df = df.sort_values(
    "relevance_score",
    ascending=False
)

cv_df = df[
    df["research_tags"].str.contains(
        "Cataclysmic Variables|Dwarf Novae|Novae",
        na=False
    )
]

# Apply filters
if priority != "All":
    df = df[df["priority"] == priority]
    
if level != "All":
    df = df[df["teaching_level"] == level]

# Search box
search = st.text_input("Search papers")

if search:
    df = df[
        df["title"].str.contains(search, case=False, na=False)
        |
        df["summary"].str.contains(search, case=False, na=False)
    ]

st.dataframe(
    df[
        [
            "title",
            "research_tags",
            "relevance_score"
        ]
    ].head(10)
)

st.subheader("🚨 CV Watchlist")

if len(cv_df) == 0:

    st.write("No cataclysmic variable papers found.")

else:

    cv_display = cv_df.sort_values(
        "relevance_score",
        ascending=False
    )

    for _, row in cv_display.iterrows():

        st.markdown(
            f"**{row['title']}** "
            f"(Score: {row['relevance_score']})"
        )

        if row["research_tags"]:

            st.caption(
                f"Tags: {row['research_tags']}"
            )
            
st.subheader("🎯 Recommended for Blake")

top_papers = recommended_df.head(5)

for _, row in top_papers.iterrows():

    st.markdown(
        f"**{row['title']}** "
        f"(Score: {row['relevance_score']})"
    )

    if row["research_tags"]:
        st.caption(
            f"Tags: {row['research_tags']}"
        )
        
st.write(f"{len(df)} papers found")

for _, row in df.iterrows():

    with st.expander(row["title"]):

        st.markdown(f"**Authors:** {row['authors']}")
        st.markdown(f"**Published:** {row['published']}")

        st.markdown("### Abstract")
        st.markdown(row["summary"])

        st.link_button(
            "Open on arXiv",
            row["link"]
        )