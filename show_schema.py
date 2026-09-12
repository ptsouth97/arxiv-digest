import sqlite3
import os

print("DATABASE:", os.path.abspath("papers.db"))

conn = sqlite3.connect("papers.db")

tables = conn.execute("""
SELECT name
FROM sqlite_master
WHERE type='table'
""").fetchall()

print("TABLES:", tables)

for row in conn.execute(
    "PRAGMA table_info(papers)"
):
    print(row)

conn.close()