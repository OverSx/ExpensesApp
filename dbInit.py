import sqlite3

DB_NAME = "expenses.db"

def init_db_expenses():
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

def init_db_weeks():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
                CREATE TABLE IF NOT EXISTS weeks(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    Year INTEGER NOT NULL,
                    Week INTEGER NOT NULL,
                    Date TEXT NOT NULL,
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
    """, (amount, currency, date, time, place, fixed))

    conn.commit()
    conn.close()

def save_new_weeks(year, week, date):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO weeks (Year, Week, Date)
        VALUES (?, ?, ?)
    """, (year, week, date))

    conn.commit()
    conn.close()

def db_last_date_request():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cursor = cur.execute("""SELECT name FROM sqlite_master 
                            WHERE type='table' AND name='weeks';""")

    result = cursor.fetchone()

    if result:
        cursor.execute("SELECT date FROM WEEKS ORDER BY id DESC LIMIT 1")
        last_row = cursor.fetchone()

        if last_row:
            conn.close()
            return last_row[0]
        else:
            conn.close()
            return None

    else:
        conn.close()
        return None
