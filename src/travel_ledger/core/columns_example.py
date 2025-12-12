from .schema import Column

COLUMNS: list[Column] = [
    Column("ID", "INTEGER PRIMARY KEY AUTOINCREMENT", "Should not set manually", 2),
    Column("Date", "TEXT NOT NULL", "YYYY-mm-dd or YYmmdd", 10),
    Column("Time", "TEXT", "HH:MM or HHMM", 5),
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