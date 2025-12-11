from dataclasses import dataclass
from typing import Optional, Any
from wcwidth import wcswidth


@dataclass
class Column:
    name: str
    sql_type: str
    hint: str
    width: int
    align: str = "left"
    choices: Optional[tuple[str, ...]] = None

    @property
    def prompt(self):
        prompt = f"{self.name}"
        if self.hint != "":
            prompt = f"{prompt} ({self.hint})"
        return prompt

    def format(self, s: Any) -> str:
        """
        Format any object according to the column display width and alignment.
        :param s: any object, typically strings and numbers
        :return: formatted string
        """
        s = str(s)  # Handle non-str values
        s = s[:self.width]  # Number of characters is at most self.print_width

        # Compare display width with limit, incrementally truncate until fits
        while wcswidth(s) > self.width:
            s = s[:-1]

        # Pad and align
        pad = self.width - wcswidth(s)
        if pad > 0:
            if self.align == "left":
                s = s + " " * pad
            elif self.align == "right":
                s = " " * pad + s
            elif self.align == "center":
                l_pad = pad // 2
                r_pad = pad - l_pad
                s = " " * l_pad + s + " " * r_pad
            else:
                raise ValueError("Invalid alignment!")
        return s

    def format_label(self) -> str:
        return self.format(self.name)

    def format_value(self, value) -> str:
        return self.format(value)

COLUMNS: list[Column] = [
    Column("ID", "INTEGER PRIMARY KEY AUTOINCREMENT", "Should not set manually", 3),
    Column("Date", "TEXT NOT NULL", "YYYY-mm-dd or YYmmdd", 10),
    Column("Time", "TEXT", "HH:MM or HHMM", 5),
    Column("City", "TEXT", "", 5),
    Column("Place", "TEXT", "", 30),
    Column("Amount", "REAL NOT NULL", "JPY", 8),
    Column("Payer", "TEXT", "", 5, choices=("Ian", "Momo")),
    Column("Method", "TEXT", "", 6, choices=("Cash", "Card", "Wechat", "Alipay")),
    Column("Category", "TEXT", "", 9,
           choices=("Hotel", "Transport", "Meal", "Shopping", "Donation", "Admission")),
    Column("Description", "TEXT", "", 20),
    Column("Note", "TEXT", "", 10),
]