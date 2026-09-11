from summarizer import summarize_paper
import feedparser
import pandas as pd

from database import (
    initialize_database,
    get_existing_summary,
    save_paper
)

# Create database/table if needed
initialize_database()

RSS_URL = "https://rss.arxiv.org/rss/astro-ph.SR"

feed = feedparser.parse(RSS_URL)

papers = []

for i, entry in enumerate(feed.entries):
    existing_summary = None
    '''existing_summary = get_existing_summary(
        entry.link
    )'''
    
    if existing_summary:
        
        print(f"Cached: {entry.title}")
        summary = existing_summary
        
    else:
        
        print(f"Summarizing {i+1}/5: {entry.title}")
        
        result = summarize_paper(
            entry.title,
            entry.summary
        )
        

        if not isinstance(result, dict):
            print(f"Skipping paper due to summary error: {entry.title}")
            continue

        main_result = result["main_result"]

        why_it_matters = result["why_it_matters"]

        summary = f"""
        MAIN RESULT:
        {main_result}

        WHY IT MATTERS:
        {why_it_matters}
        """
    
        save_paper(
            entry.link,
            entry.title,
            getattr(entry, "author", ""),
            getattr(entry, "published", ""),
            summary,
            result["teaching_level"],
            result["priority"],
            ",".join(result["topics"]),
            ",".join(result["research_tags"])
        )
        
    papers.append(
        {
            "title": entry.title,
            "authors": getattr(entry, "author", ""),
            "published":getattr(entry, "published", ""),
            "summary": summary,
            "link": entry.link,
        }
    )

df = pd.DataFrame(papers)
print(df.head())
print(f"Saved {len(df)} papers")