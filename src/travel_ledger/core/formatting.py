from travel_ledger.core.schema import COLUMNS
from datetime import datetime

def validate_and_format_values(record: dict):
    """
    Validate and format record in-place.
    :param record:
    :return:
    """
    # --- validation ---
    # Columns with predefined choices
    cols_choices = {col.name: col.choices for col in COLUMNS if col.choices is not None}

    # Validate values in record are among predefined choices
    for col, val in record.items():
        if col in cols_choices:  # This column has predefined choices
            choices = cols_choices[col]
            for choice in choices:  # Match value with choices
                if val.lower() == choice.lower():  # Ignore case difference
                    record[col] = choice  # Use standard case
                    break
            else:  # Value is not matched with any choices
                raise ValueError(f"\nInvalid choice {val} for column {col}!"
                                 f"\nValid choices are: {", ".join(choices)}.")

    # --- formatting ---
    if 'Date' in record and record['Date']:
        val = record['Date']
        # If user entered 6 digits like 251005
        if val.isdigit() and len(val) == 6:
            record['Date'] = f"20{val[:2]}-{val[2:4]}-{val[4:]}"
        else:
            # Validate date format
            try:
                datetime.strptime(val, "%Y-%m-%d")
            except ValueError:
                raise ValueError("\nInvalid date format! Use YYYY-mm-dd or YYmmdd (e.g., 251005).")
    if 'Time' in record and record['Time']:
        val = record['Time']
        # If user entered 4 digits like 1430
        if val.isdigit() and len(val) == 4:
            record['Time'] = f"{val[:2]}:{val[2:]}"
        elif val:
            # Validate time format
            try:
                datetime.strptime(val, "%H:%M")
            except ValueError:
                raise ValueError("\nInvalid time format! Use HH:MM or HHMM (e.g., 1430).")

def get_header_footer() -> tuple[str, str]:
    hor_line = "+-" + "-+-".join(["-" * col.print_width for col in COLUMNS]) + "-+"
    header = "| " + " | ".join([col.name.ljust(col.print_width) for col in COLUMNS]) + " |"
    return hor_line + '\n' + header + '\n' + hor_line, hor_line

def get_formatted_rows(record: list[tuple]) -> str:
    hor_line = "\n+-" + "-+-".join(["-" * col.print_width for col in COLUMNS]) + "-+\n"

    fmt_rows = []
    for row in record:
        fmt_vals = []
        for val, col in zip(row, COLUMNS):
            # Convert numbers to str and trim to fit print width
            val = str(val)[:col.print_width]
            match col.print_align:
                case "left":
                    fmt_val = val.ljust(col.print_width)
                case "center":
                    fmt_val = val.center(col.print_width)
                case "right":
                    fmt_val = val.rjust(col.print_width)
                case _:
                    raise ValueError("\nInvalid column alignment format!")
            fmt_vals.append(fmt_val)
        fmt_row = "| " + " | ".join(fmt_vals) + " |"
        fmt_rows.append(fmt_row)

    return hor_line.join(fmt_rows)

