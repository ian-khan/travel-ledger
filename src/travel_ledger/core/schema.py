from dataclasses import dataclass
from typing import Optional


@dataclass
class Column:
    name: str
    sql_type: str
    hint: str
    print_width: int
    print_align: str = "left"
    choices: Optional[tuple[str, ...]] = None

    @property
    def prompt(self):
        prompt = f"{self.name}"
        if self.hint != "":
            prompt = f"{prompt} ({self.hint})"
        return prompt

COLUMNS: list[Column] = [
    Column("ID", "INTEGER PRIMARY KEY AUTOINCREMENT", "Should not set manually", 3),
    Column("Date", "TEXT NOT NULL", "YYYY-mm-dd or YYmmdd", 10),
    Column("Time", "TEXT", "HH:MM or HHMM", 5),
    Column("City", "TEXT", "", 5),
    Column("Place", "TEXT", "", 15),
    Column("Amount", "REAL NOT NULL", "JPY", 8),
    Column("Payer", "TEXT", "", 5, choices=("Ian", "Momo")),
    Column("Method", "TEXT", "", 6, choices=("Cash", "Card", "Wechat", "Alipay")),
    Column("Category", "TEXT", "", 9,
           choices=("Hotel", "Transport", "Meal", "Shopping", "Donation", "Admission")),
    Column("Description", "TEXT", "", 20),
    Column("Note", "TEXT", "", 15),
]