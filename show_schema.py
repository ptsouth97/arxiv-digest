import sqlite3
import os

db_path = os.path.abspath("papers.db")

print("DATABASE:", db_path)

conn = sqlite3.connect("papers.db")

for row in conn.execute(
    "PRAGMA table_info(papers)"
):
    print(row)

conn.close()