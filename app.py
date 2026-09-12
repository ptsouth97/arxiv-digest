import sys
import subprocess
import pandas as pd
import streamlit as st
import sqlite3
import re
from database import (
    mark_saved,
    mark_unsaved
)

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

saved_only = st.sidebar.checkbox(
    "Saved Papers Only"
)

saved_count = len(
    df[df["saved"] == 1]
)

st.sidebar.write(
    f"⭐ Saved Papers: {saved_count}"
)

if st.button("Refresh Papers"):
    subprocess.run([sys.executable, "fetch.py"])
    st.success("Paper list updated")



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

def clean_title(title):

    if pd.isna(title):
        return title

    # Remove inline LaTeX expressions
    title = re.sub(r"\$.*?\$", "", title)

    # Remove common LaTeX commands
    title = re.sub(r"\\[A-Za-z]+", "", title)

    # Remove leftover braces
    title = title.replace("{", "")
    title = title.replace("}", "")

    # Compress extra spaces
    title = " ".join(title.split())

    return title
    
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

def explain_relevance(tag_string):

    if pd.isna(tag_string):
        return []

    explanations = {

        "Cataclysmic Variables":
            "Directly related to your primary research area.",

        "Dwarf Novae":
            "Relevant subtype of cataclysmic variables.",

        "Novae":
            "Connected to interacting white dwarf binaries.",

        "Variable Stars":
            "Relevant to variable star behavior and evolution.",

        "White Dwarfs":
            "Important for CV evolution and compact binaries.",

        "Binary Stars":
            "Many CVs originate from close binary systems.",

        "Accretion Disks":
            "Accretion physics is fundamental to CV research.",

        "Time Domain Astronomy":
            "Useful for variability and outburst studies.",

        "TESS":
            "Provides light curves useful for CV discoveries.",

        "Gaia":
            "Useful for distances, populations, and binaries."
    }

    reasons = []

    for tag in tag_string.split(","):

        tag = tag.strip()

        if tag in explanations:

            reasons.append(
                explanations[tag]
            )

    return reasons
    
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
    
if saved_only:
    df = df[df["saved"] == 1]

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
    
must_read = cv_display[
    cv_display["research_priority"]
    == "Must Read"
]

worth_reading = cv_display[
    cv_display["research_priority"]
    == "Worth Reading"
]

background_reading = cv_display[
    cv_display["research_priority"]
    == "Background Reading"
]

st.markdown("## 🔥 Must Read")

for _, row in must_read.iterrows():

    st.markdown(
        f"**{clean_title(row["title"])}** "
        f"(Score: {row['relevance_score']})"
    )
    
    if row["saved"] == 0:

        if st.button(
            "⭐ Save",
            key=f"save_{row['link']}"
        ):
            mark_saved(row["link"])
            st.rerun()

    else:

        if st.button(
            "✅ Saved",
            key=f"unsave_{row['link']}"
        ):
            mark_unsaved(row["link"])
            st.rerun()
        if row["research_tags"]:

            st.caption(
            f"Tags: {row['research_tags']}"
        )

if row["why_blake_should_read_this"]:

    st.markdown(
        "**Why Blake should read this:**"
    )

    st.info(
        row["why_blake_should_read_this"]
    )
        
st.subheader("🎯 Recommended for Blake")

top_papers = recommended_df.head(5)

for _, row in top_papers.iterrows():

    st.markdown(
        f"**{clean_title(row["title"])}** "
        f"(Score: {row['relevance_score']})"
    )

    if row["research_tags"]:
        st.caption(
            f"Tags: {row['research_tags']}"
        )
        
st.write(f"{len(df)} papers found")

for _, row in df.iterrows():

    with st.expander(clean_title(clean_title(row["title"]))):

        st.markdown(f"**Authors:** {row['authors']}")
        st.markdown(f"**Published:** {row['published']}")

        st.markdown("### Abstract")
        st.markdown(row["summary"])

        st.link_button(
            "Open on arXiv",
            row["link"]
        )
        