from dataclasses import dataclass
from typing import Optional, Any, Sequence, Literal
from wcwidth import wcswidth


@dataclass
class Column:
    name: str
    sql_type: str
    hint: str
    width: int
    align: str = "left"
    choices: Optional[tuple[str, ...]] = None
    is_counted_items: bool = False

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

    def format_counted_items(self, items: Sequence[str], counts: Sequence[int]) -> str:
        if not self.is_counted_items:
            raise ValueError("This column is not counted items!")
        counted_items = [f"{item} x{count}" for item, count in zip(items, counts)]
        counted_items = ", ".join(counted_items)
        return counted_items

    def prompt_and_get_value(self, default_value: Optional[str]=None) -> str:
        """
        Prompt user to enter value for this column.
        :param default_value: Default value to return if no value is entered.
        :return: Value for this column.
        """
        default_value = "" if default_value is None else default_value
        hint_prompt = "" if self.hint == "" else f" ({self.hint})"
        value_prompt = "" if default_value == "" else f" [{default_value}]"
        prompt = f">> {self.name}{hint_prompt}{value_prompt}: "

        if not self.is_counted_items:
            value = input(prompt).strip()
            if value == "":
                value = default_value  # Use the default value or empty string
            elif value == "-":
                value = ""  # Explicitly clear the value
        else:
            print(prompt)

            use_default, items, counts, i = False, [], [], 1
            while True:
                item = input(f">>>> Item  {i}: ").strip()
                if item == "":  # Use the default value or empty string
                    if i != 1:
                        raise ValueError("To use the default value, press Enter when prompted to "
                                         "enter the first item. To stop adding items, press '-'.")
                    use_default = True
                    break
                if item == "-":
                    break  # Stop adding item
                while True:
                    count = input(f">>>> Count {i}: ").strip()
                    if count == "":
                        print("Count should not be empty!")
                        continue
                    try:
                        count = int(count)
                        break
                    except ValueError:
                        print("Count should be an integer!")
                items.append(item)
                counts.append(count)
                i = i + 1
            value = default_value if use_default else self.format_counted_items(items, counts)
        return value


try:
    from .columns_private import COLUMNS
except ImportError:
    from .columns_example import COLUMNS