from dataclasses import dataclass
from typing import Any, Callable, Optional, Sequence, Literal
from wcwidth import wcswidth


@dataclass
class Column:
    name: str
    sql_type: str
    hint: str
    width: int
    align: str = "left"
    choices: Optional[tuple[str, ...]] = None
    validate_format: Optional[Callable] = None
    is_counted_items: bool = False
    as_groups: bool = False

    @property
    def prompt(self):
        prompt = f"{self.name}"
        if self.hint != "":
            prompt = f"{prompt} ({self.hint})"
        return prompt

    def format_printed(self, s: Any) -> str:
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

    def format_printed_label(self) -> str:
        return self.format_printed(self.name)

    def format_printed_value(self, value) -> str:
        return self.format_printed(value)

    def format_counted_items(self, items: Sequence[str], counts: Sequence[int]) -> str:
        assert self.is_counted_items, "This column is not counted items!"
        counted_items = [f"{item} x{count}" for item, count in zip(items, counts)]
        counted_items = ", ".join(counted_items)
        return counted_items

    def validate_choice(self, value: str) -> str:
        assert self.choices is not None, "This column does not have predefined choices!"

        for choice in self.choices:
            if value.lower() == choice.lower():
                return choice
        else:
            raise ValueError(f"Invalid choice! Please choose from {", ".join(self.choices)}.")

    def prompt_and_get_value(self, default_value: Optional[str]=None) -> str:
        """
        Prompt user to enter value for this column and return it.
        For ordinary columns, press Enter to use the default value; press '-' then Enter to clear the field.
        For counted-items columns, press Enter to use the default value; press '-' then Enter when inputting
        item names to stop adding items.
        :param default_value: Default value to return if no value is entered.
        :return: Value for this column.
        """
        # When hint is None or "", omit hint prompt
        hint_prompt = "" if not self.hint else f" ({self.hint})"
        # When default value is absent (None), omit value prompt
        # When it is present, even if it's empty string (""), it is prompted
        value_prompt = "" if default_value is None else f" [{default_value}]"
        default_value = "" if default_value is None else default_value

        # Validate column value's format and choice
        while True:
            try:
                if not self.is_counted_items:
                    prompt = f"{self.name}{hint_prompt}{value_prompt}:\n>> "
                    value = input(prompt).strip()
                    if value == "":
                        value = default_value  # Use the default value or empty string
                    elif value == "-":
                        value = ""  # Explicitly clear the value
                else:
                    prompt = f"{self.name}{hint_prompt}{value_prompt}"
                    print(prompt)

                    items, counts, use_default = [], [], False
                    # Recursively add items and validate item names
                    while True:
                        try:
                            item = input(f"  >> Item : ").strip()
                            if item == "":  # Use the default value or empty string
                                if len(items) == 0:  # Ensure no items have been added
                                    use_default = True
                                    break
                                raise ValueError("To stop adding items, enter '-' (dash) "
                                                 "and press Enter.")
                            elif item == "-":  # Stop adding items
                                break
                            items.append(item)  # Add another item

                            # Validate item counts
                            while True:
                                try:
                                    count = input(f"  >> Count: ").strip()
                                    count = int(count)
                                    counts.append(count)
                                    break
                                except ValueError as e:
                                    print(e)
                                    continue

                        except ValueError as e:
                            print(e)
                            continue

                    value = default_value if use_default else self.format_counted_items(items, counts)

                if self.validate_format is not None:
                    value = self.validate_format(value)
                if self.choices is not None:
                    value = self.validate_choice(value)
                return value

            except ValueError as e:
                print(e)
                continue

try:
    from .columns_private import COLUMNS
except ImportError:
    from .columns_example import COLUMNS