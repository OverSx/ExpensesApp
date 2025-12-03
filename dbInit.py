import sqlite3

DB_NAME = "expenses.db"

def init_db_expenses():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            year INTEGER NOT NULL,
            week INTEGER NOT NULL,
            amount REAL,
            currency TEXT NOT NULL,
            eur_amount REAL,
            date TEXT NOT NULL,
            time TEXT,
            place TEXT,
            fixed INTEGER DEFAULT 1
        );
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
                Month INTEGER NOT NULL,
                Week INTEGER NOT NULL,
                Date TEXT NOT NULL
                );
                """)

    conn.commit()
    conn.close()

def init_db_useful_data():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
                CREATE TABLE IF NOT EXISTS useful_data(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                Rent_amount REAL NOT NULL,
                Rent_currency TEXT NOT NULL,
                Debt_amount REAL NOT NULL
                );
                """)

    conn.commit()
    conn.close()

def save_new_expense(expenses_list):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    for expense in expenses_list:
        cur.execute("""
            INSERT INTO expenses (year, week, amount, currency, eur_amount, date, time, place, fixed)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (expense[0], expense[1], expense[2], expense[3], expense[4], expense[5], expense[6], expense[7], expense[8]))

    conn.commit()
    conn.close()

def save_new_weeks(week_list):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    for week in week_list:
        cur.execute("""
            INSERT INTO weeks (Year, Month, Week, Date)
            VALUES (?, ?, ?, ?)
        """, (week[0], week[1], week[2], week[3]))

    conn.commit()
    conn.close()

def save_new_useful_data(rent_amount, rent_currency, debt_amount):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("DELETE FROM useful_data")


    cur.execute("""
                INSERT INTO useful_data (Rent_amount, Rent_currency, Debt_amount)
                VALUES (?, ?, ?)
                """, (rent_amount, rent_currency, debt_amount))

    conn.commit()
    conn.close()

def db_debt_and_rent_request():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cursor = cursor = cur.execute("""SELECT name FROM sqlite_master 
                            WHERE type='table' AND name='useful_data';""")

    result = cursor.fetchone()

    if result:
        cursor.execute("""SELECT Rent_amount, Rent_currency, Debt_amount
                        FROM useful_data 
                        ORDER BY id DESC LIMIT 1
                       """)

        last_row = cursor.fetchone()

        if last_row:
            conn.close()
            return last_row
        else:
            conn.close()
            return None

    else:
        conn.close()
        return None

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

def get_dates_for_week(year, week_index):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
                SELECT Date
                FROM weeks
                WHERE Year = ? AND Week = ?
                """, (year, week_index,))

    dates = cur.fetchall()

    conn.close()
    return dates

def get_dates_from_month(year, month_index):
    month_str = f"{month_index:02}"

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
                SELECT Date
                FROM weeks
                WHERE substr(Date, 7, 4) = ? AND substr(Date, 4, 2) = ?
                """, (year, month_str,))

    dates = cur.fetchall()

    conn.close()
    return dates

def get_expenses_value(year, week_index, fix):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
                SELECT eur_amount
                FROM expenses
                WHERE year = ? AND week = ? AND fixed = ?
                """, (year, week_index, fix))

    expenses = cur.fetchall()
    conn.close()
    return expenses

def get_month_expenses_value(year, month_index, fix):
    month_str = f"{month_index:02}"

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
                SELECT eur_amount
                FROM expenses
                WHERE year = ? AND substr(date, 4, 2) = ? AND fixed = ?
                """, (year, month_str, fix))

    expenses = cur.fetchall()
    conn.close()

    return expenses

def get_weeks_db_unique_years():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
                SELECT DISTINCT Year
                FROM weeks
                """)

    year_list = cur.fetchall()

    conn.close()

    return year_list

def get_weeks_for_month(year, month_index):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
                SELECT DISTINCT Week
                FROM weeks
                WHERE Year = ? AND Month = ?
                """, (year, month_index,))

    weeks_list = cur.fetchall()

    return weeks_list

def get_month_from_week_and_year(year, week):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
                SELECT Month
                FROM weeks
                WHERE Year = ? AND Week = ?
                """, (year, week,))

    month = cur.fetchone()

    conn.close()

    return month[0]