import dbInit

import requests
from datetime import date, timedelta, datetime

def text_parser(text):
    lines = text.splitlines()
    text_blocks = []
    block = []
    for i in range(0, len(lines)):
        line_parts = lines[i].split()
        if not line_parts:
            continue

        if line_parts[0] in ("Payment:", "Conversion:", "Money", "Deposit"):
            if block:
                text_blocks.append(block.copy())
                block = []
                block.append(lines[i])
            else:
                block.append(lines[i])
        elif line_parts[0].replace(".", "", 1).isdigit():
            if not block:
                block.append(lines[i])
            elif len(block) < 4:
                block.append(lines[i])
            else:
                text_blocks.append(block.copy())
                block = []
                block.append(lines[i])

        else:
            block.append(lines[i])

    text_blocks.append(block.copy())
    return text_blocks

def blocks_parser(text_blocks):
    parsed_data = []
    operation = []

    income_key = ("Deposit", "Conversion")
    for i in range(0, len(text_blocks)):
        if any(keyword in item for item in text_blocks[i] for keyword in income_key):
            continue
        elif any("Payment" in item for item in text_blocks[i]):

            #add amount and currency
            text_parts = text_blocks[i][1].split()
            operation.append(text_parts[0])
            operation.append(text_parts[1])

            #add date and time
            text_parts = text_blocks[i][4].split()
            operation.append(text_parts[2])
            operation.append(text_parts[3])

            #add place
            operation.append(f"Оплата {text_blocks[i][2]}")

            #add fixed param
            operation.append(0)

        elif any("Money" in item for item in text_blocks[i]):

            #add amount and currency
            text_parts = text_blocks[i][1].split()
            operation.append(text_parts[0])
            operation.append(text_parts[1])

            #add date and time
            text_parts = text_blocks[i][3].split()
            operation.append(text_parts[0])
            operation.append(None)

            #add place
            operation.append("Перевод")

            #add fixed param
            operation.append(0)

        else:

            #add amount and currency
            text_parts = text_blocks[i][0].split()
            operation.append(text_parts[0])
            operation.append(text_parts[1])

            #add date and time
            text_parts = text_blocks[i][2].split()
            operation.append(text_parts[-2])
            operation.append(text_parts[-1])

            #add place
            place = " ".join(text_parts[:-2])
            operation.append(place)

            #add fixed param
            operation.append(1)

        parsed_data.append(operation)
        operation = []

    return parsed_data

def year_generator(starting_year):
    weeks = []
    week = []

    d = dbInit.db_last_date_request()
    if not d:
        d = date(starting_year, 1, 1)
        while d.weekday() != 5:
            d += timedelta(days=1)

    if isinstance(d, date):
        current_date = d
    else:
        current_date = datetime.strptime(d, "%d/%m/%Y").date()
        current_date += timedelta(days=1)

    for i in range(1, 53):
        for day in range(1, 8):
            week.append(current_date.year)
            week.append(i)
            week.append(current_date.strftime("%d/%m/%Y"))
            weeks.append(week.copy())
            week = []

            current_date += timedelta(days=1)

    dbInit.init_db_weeks()
    dbInit.save_new_weeks(weeks)

def expense_distributor(date):
    return dbInit.get_week_and_year(date)

def add_expense(expenses_list):
    dbInit.init_db_expenses()
    dbInit.save_new_expense(expenses_list)

def get_full_week(date):
    cur_date = date.strftime("%d/%m/%Y")
    year, week = dbInit.get_week_and_year(cur_date)
    dates_list = dbInit.get_dates_for_week(year, week)

    temp_str = f"{dates_list[0][0]} - {dates_list[-1][0]}"
    return week, year, temp_str

def get_rate(base, target):
    url = f"https://open.er-api.com/v6/latest/{base}"
    data = requests.get(url).json()

    return data["rates"][target]

def get_expense_amount(year, week, fix, EUR_rate, USD_rate, RUB_rate):
    p = dbInit.get_expenses_value(year, week, fix)
    sum = 0

    for each in p:
        if each[1] == 'RUB':
            sum += each[0] / float(RUB_rate)
        elif each[1] == 'USD':
            sum += each[0] * float(USD_rate)
        elif each[1] == 'EUR':
            sum += each[0] * float(EUR_rate)
        else:
            sum += each[0]


    return sum

