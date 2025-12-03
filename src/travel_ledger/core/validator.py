from travel_ledger.config import PAYERS, METHODS, CATEGORIES
from datetime import datetime

def validate_and_format_values(**kwargs):
    # --- validation ---
    if 'payer' in kwargs:
        for p in PAYERS:
            if p.lower() == kwargs['payer'].lower():
                kwargs['payer'] = p
                break
        else:
            valid = ", ".join(PAYERS)
            raise ValueError(f"\nInvalid payer! Please choose from: {valid}.")
    if 'method' in kwargs:
        for m in METHODS:
            if m.lower() == kwargs['method'].lower():
                kwargs['method'] = m
                break
        else:
            valid = ", ".join(METHODS)
            raise ValueError(f"\nInvalid payment method! Please choose from: {valid}.")
    if 'category' in kwargs:
        for c in CATEGORIES:
            if c.lower() == kwargs['category'].lower():
                kwargs['category'] = c
                break
        else:
            valid = ", ".join(CATEGORIES)
            raise ValueError(f"\nInvalid category! Please choose from: {valid}.")

    # --- formatting ---
    if 'date' in kwargs and kwargs['date']:
        val = kwargs['date']
        # If user entered 6 digits like 251005
        if val.isdigit() and len(val) == 6:
            kwargs['date'] = f"20{val[:2]}-{val[2:4]}-{val[4:]}"
        else:
            # Validate date format
            try:
                datetime.strptime(val, "%Y-%m-%d")
            except ValueError:
                raise ValueError("\nInvalid date format! Use YYYY-MM-DD or YYMMDD (e.g., 251005).")
    if 'time' in kwargs and kwargs['time']:
        val = kwargs['time']
        # If user entered 4 digits like 1430
        if val.isdigit() and len(val) == 4:
            kwargs['time'] = f"{val[:2]}:{val[2:]}"
        elif val:
            # Validate time format
            try:
                datetime.strptime(val, "%H:%M")
            except ValueError:
                raise ValueError("\nInvalid time format! Use HH:MM or HHMM (e.g., 1430).")

    return kwargs