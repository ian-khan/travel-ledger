from dataclasses import dataclass
from typing import Optional


@dataclass
class Column:
    name: str
    sql_type: str
    hint: str
    print_width: int
    print_align: str = "right",
    choices: Optional[tuple[str, ...]] = None

    @property
    def prompt(self):
        prompt = f"{self.name}"
        if self.hint != "":
            prompt = f"{prompt} ({self.hint})"
        return prompt

COLUMNS: list[Column] = [
    Column("ID", "INTEGER PRIMARY KEY AUTOINCREMENT", "Should not set manually", 4),
    Column("Date", "TEXT NOT NULL", "YYYY-MM-DD or YYMMDD", 10),
    Column("Time", "TEXT", "HH:mm or HHmm", 5),
    Column("City", "TEXT", "", 10),
    Column("Place", "TEXT", "", 15),
    Column("Amount", "REAL NOT NULL", "JPY", 8),
    Column("Payer", "TEXT", "", 6, choices=("Ian", "Momo")),
    Column("Method", "TEXT", "", 6, choices=("Cash", "Card", "Wechat", "Alipay")),
    Column("Category", "TEXT", "", 10,
           choices=("Hotel", "Transport", "Meal", "Shopping", "Donation", "Admission")),
    Column("Description", "TEXT", "", 20),
    Column("Note", "TEXT", "", 20),
]