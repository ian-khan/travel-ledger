from .schema import Column
from datetime import datetime

def validate_date_format(value: str) -> str:
    if value.isdigit() and len(value) == 6:
        value = f"20{value[:2]}-{value[2:4]}-{value[4:]}"
    try:
        datetime.strptime(value, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Invalid date format! Please use YYYY-mm-dd or YYmmdd (e.g., 251005).")
    return value

def validate_time_format(value: str) -> str:
    if value.isdigit() and len(value) == 4:
        value = f"{value[:2]}:{value[2:]}"
    try:
        datetime.strptime(value, "%H:%M")
    except ValueError:
        raise ValueError("Invalid time format! Please use HH:MM or HHMM (e.g., 1430).")
    return value

COLUMNS: list[Column] = [
    Column("ID", "INTEGER PRIMARY KEY AUTOINCREMENT", "Should not set manually", 2),
    Column("Date", "TEXT NOT NULL", "YYYY-mm-dd or YYmmdd", 10,
           validate_format=validate_date_format),
    Column("Time", "TEXT", "HH:MM or HHMM", 5,
           validate_format=validate_time_format),
    Column("City", "TEXT", "", 5),
    Column("Place", "TEXT", "", 24),
    Column("Amount", "REAL NOT NULL", "JPY", 7),
    Column("Payer", "TEXT", "", 5, choices=("Person A", "Person B")),
    Column("Method", "TEXT", "", 6, choices=("Cash", "Card")),
    Column("Category", "TEXT", "", 9,
           choices=("Hotel", "Transport", "Meal", "Shopping", "Admission")),
    Column("Items", "TEXT", "", 36, is_counted_items=True),
    Column("Note", "TEXT", "", 4),
]