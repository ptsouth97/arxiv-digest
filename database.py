import sqlite3
import os

DB_NAME = "papers.db"
print("DATABASE:", os.path.abspath(DB_NAME))

def get_existing_summary(link):

    conn = get_connection()
    cur = conn.cursor()
    
    #Temporary
    print(f"LOOKING UP: {link}")

    cur.execute(
        "SELECT summary FROM papers WHERE link = ?",
        (link,)
    )

    row = cur.fetchone()
    
    #Temporary
    print(f"FOUND: {row is not None}")

    conn.close()

    return row[0] if row else None

def save_paper(
    link,
    title,
    authors,
    published,
    summary,
    teaching_level,
    priority,
    topics,
    research_tags
):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT OR REPLACE INTO papers
        (
            link,
            title,
            authors,
            published,
            summary,
            teaching_level,
            priority,
            topics,
            research_tags
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """,
    (
        link,
        title,
        authors,
        published,
        summary,
        teaching_level,
        priority,
        topics,
        research_tags
    ))

    conn.commit()
    conn.close()
    
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS papers (
        link TEXT PRIMARY KEY,
        title TEXT,
        authors TEXT,
        published TEXT,
        summary TEXT,
        teaching_level TEXT,
        priority TEXT,
        topics TEXT,
        research_tags TEXT
    )
""")

    conn.commit()
    conn.close()
    
def get_connection():
    return sqlite3.connect(DB_NAME)


def initialize_database():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS papers (
            link TEXT PRIMARY KEY,
            title TEXT,
            authors TEXT,
            published TEXT,
            summary TEXT,
            teaching_level TEXT,
            priority TEXT,
            topics TEXT,
            research_tags TEXT
        )
    """)

    conn.commit()
    conn.close()