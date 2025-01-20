import os
import sqlite3
from pathlib import Path

if os.name == "nt":
    db = sqlite3.connect(f"{Path.home()}/Octoffers/ziprecruiter.db")
else:
    db = sqlite3.connect(f"{os.environ['HOME']}/.config/octoffers/ziprecruiter.db")
with db:
    db.execute("""
    CREATE TABLE IF NOT EXISTS jobs (
        id INTEGER PRIMARY KEY,
        job_id VARCHAR(255) UNIQUE,
        role TEXT,
        description TEXT,
        easy_apply BOOLEAN DEFAULT FALSE,
        applied BOOLEAN DEFAULT FALSE,
        applicable BOOLEAN DEFAULT FALSE
    )
    """)    
    db.commit()
