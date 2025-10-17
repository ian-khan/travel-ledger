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

PAYERS = ("ian", "momo")
METHODS = ("cash", "wechat", "alipay", "credit card", "others")
CATEGORIES = ("accommodation", "transport", "food and drinks", "admission", "shopping", "others")