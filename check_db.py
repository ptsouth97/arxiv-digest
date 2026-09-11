import sqlite3

conn = sqlite3.connect("papers.db")

for row in conn.execute("""
    SELECT
        title,
        research_tags
    FROM papers
    LIMIT 10
"""):
    print(row)

conn.close()