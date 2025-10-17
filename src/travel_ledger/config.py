COLUMNS = {
    "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
    "date": "TEXT NOT NULL",
    "time": "TEXT",
    "city": "TEXT",
    "place": "TEXT",
    "amount": "REAL NOT NULL",
    "payer": "TEXT",
    "method": "TEXT",
    "category": "TEXT",
    "description": "TEXT",
    "notes": "TEXT"
}

PAYERS = ("ian", "momo")
METHODS = ("cash", "wechat", "alipay", "credit card", "others")
CATEGORIES = ("accommodation", "transport", "food and drinks", "admission", "shopping", "others")