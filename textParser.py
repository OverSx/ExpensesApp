import re

from PySide6.QtWidgets import QMessageBox

def text_parser(parent, text):
    lines = text.splitlines()
    parsed_data = []
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


