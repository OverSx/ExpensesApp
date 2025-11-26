import sqlite3

DB_NAME = "expenses.db"

def init_db_expenses(week, year):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    table_name = f"{week}_{year}"
    cur.execute("""
        CREATE TABLE IF NOT EXISTS "{table_name}" (
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

def save_new_expense(expenses_list):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    for expense in expenses_list:
        table_name = f"{expense[0]}_{expense[1]}"
        cur.execute("""
            INSERT INTO "{table_name}" (amount, currency, date, time, place, fixed)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (expense[2], expense[3], expense[4], expense[5], expense[6], expense[7]))

    conn.commit()
    conn.close()

def save_new_weeks(week_list):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    for week in week_list:
        cur.execute("""
            INSERT INTO weeks (Year, Week, Date)
            VALUES (?, ?, ?)
        """, (week[0], week[1], week[2]))

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

def get_week_and_year(date):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
                SELECT Year, Week
                FROM weeks
                WHERE Date = ?
                """, (date,))

    row = cur.fetchone()

    conn.close()
    return row