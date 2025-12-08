from pathlib import Path

STATE_FILE = Path("state_file.json")

COLUMNS = {
    "id": ("INTEGER PRIMARY KEY AUTOINCREMENT",""),
    "date": ("TEXT NOT NULL", "Date (YYYY-MM-DD)"),
    "time": ("TEXT", "Time (HH:MM)"),
    "city": ("TEXT", "City"),
    "place": ("TEXT", "Place"),
    "amount": ("REAL NOT NULL", "Amount (JPY)"),
    "payer": ("TEXT", "Payer"),
    "method": ("TEXT", "Payment Method"),
    "category": ("TEXT", "Category"),
    "description": ("TEXT", "Description"),
    "notes": ("TEXT", "Notes"),
}

PAYERS = ("Ian", "Momo")
METHODS = ("Cash", "Wechat", "Alipay", "Credit Card")
CATEGORIES = ("Accommodation", "Transport", "Food and Drinks", "Admission", "Shopping", "Others")