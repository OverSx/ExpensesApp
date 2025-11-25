import sqlite3

DB_NAME = "expenses.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL,
            currency TEXT NOT NULL,
            date TEXT NOT NULL,
            time TEXT,
            place TEXT,
            fixed INTEGER DEFAULT 1
        )
    """)

    conn.commit()
    conn.close()

def save_new_expense(amount, currency, date, time, place, fixed):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO expenses (amount, currency, date, time, place, fixed)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (amount, currency. date, time. place, fixed))

    conn.commit()
    conn.close()
