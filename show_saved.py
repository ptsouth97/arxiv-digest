import sqlite3

conn = sqlite3.connect("papers.db")

for row in conn.execute("""
    SELECT title
    FROM papers
    WHERE saved = 1
"""):
    print(row[0])

conn.close()