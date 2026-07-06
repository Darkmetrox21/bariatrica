import sqlite3

DB_NAME = "bariatrica.db"


def connect():
    return sqlite3.connect(DB_NAME)


def create_tables():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            time TEXT NOT NULL,
            note TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    """)

    conn.commit()
    conn.close()


def add_pill(name, time, note):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO pills (name, time, note) VALUES (?, ?, ?)",
        (name, time, note)
    )

    conn.commit()
    conn.close()


def get_pills():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("SELECT id, name, time, note FROM pills ORDER BY time ASC")
    rows = cursor.fetchall()

    conn.close()
    return rows


def delete_pill(pill_id):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM pills WHERE id = ?", (pill_id,))

    conn.commit()
    conn.close()


def save_setting(key, value):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR REPLACE INTO settings (key, value)
        VALUES (?, ?)
    """, (key, value))

    conn.commit()
    conn.close()


def get_setting(key, default=None):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("SELECT value FROM settings WHERE key = ?", (key,))
    row = cursor.fetchone()

    conn.close()

    if row:
        return row[0]

    return default
