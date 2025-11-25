import dbInit

import re
import sqlite3

from PySide6.QtWidgets import QMessageBox

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
            operation.append(text_blocks[i][2])

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
            operation.append(None)

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
