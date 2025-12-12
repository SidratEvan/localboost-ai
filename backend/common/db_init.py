import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "localboost.db"
SQL_SCHEMA = Path(__file__).parent / "models.sql"


def init_db():
    print(f"Initializing database at: {DB_PATH}")

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    with open(SQL_SCHEMA, "r") as f:
        sql_script = f.read()

    cur.executescript(sql_script)
    conn.commit()
    conn.close()

    print("Database initialized successfully.")


if __name__ == "__main__":
    init_db()
