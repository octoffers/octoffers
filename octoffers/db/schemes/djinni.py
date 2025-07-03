import os
import sqlite3
from pathlib import Path

if os.name == "nt":
    try:
        db = sqlite3.connect(f"{Path.home()}/Octoffers/djinni.db")
    except sqlite3.OperationalError as e:
        if "unable to open database file" in str(e):
            os.makedirs(f"{Path.home()}/Octoffers", exist_ok=True)
            db = sqlite3.connect(f"{Path.home()}/Octoffers/djinni.db")
        else:
            raise e
else:
    db = sqlite3.connect(f"{os.environ['HOME']}/.config/octoffers/djinni.db")
with db:
    db.execute(
        """
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY,
            job_id TEXT,
            role TEXT,
            link TEXT,
            category TEXT,
            source TEXT,
            description TEXT,
            salary INT,
            matches BOOLEAN DEFAULT FALSE,
            cv_sent BOOLEAN DEFAULT FALSE
        )
    """
    )
    db.commit()
