import json
import sqlite3
from datetime import datetime

from carbonation.utils import get_newscatcher_headlines


def fetch_store(hours=1, max_page=10, use_sources=False):
    now = datetime.now().strftime("%m-%d-%Y_%H:%M:%S")

    urls = None
    if use_sources:
        with open("carbonation/resources/sources/sources.txt", "r") as f:
            urls = f.readlines()

    # Get news with urls as sources
    news = get_newscatcher_headlines(hours, sources=urls, max_page=max_page)

    # Write and return news
    # Connect to or create the database
    conn = sqlite3.connect("carbonation/resources/carbonaton.db")

    # Create a table (if it doesn't already exist)
    conn.execute(
        """CREATE TABLE IF NOT EXISTS models
                (id text primary key, news json)"""
    )

    table_name = f"{hours}hr_{now}"
    # Insert data into the table
    conn.execute(
        "INSERT INTO mytable (id, news) VALUES (?, ?)", (table_name, json.dumps(news))
    )

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

    return news
