from travel_ledger.config import PAYERS, METHODS, CATEGORIES
from datetime import datetime

def validate_and_format_values(record: dict):
    """
    Validate and format record in-place.
    :param record:
    :return:
    """
    # --- validation ---
    if 'payer' in record:
        for p in PAYERS:
            if p.lower() == record['payer'].lower():
                record['payer'] = p
                break
        else:
            valid = ", ".join(PAYERS)
            raise ValueError(f"\nInvalid payer! Please choose from: {valid}.")
    if 'method' in record:
        for m in METHODS:
            if m.lower() == record['method'].lower():
                record['method'] = m
                break
        else:
            valid = ", ".join(METHODS)
            raise ValueError(f"\nInvalid payment method! Please choose from: {valid}.")
    if 'category' in record:
        for c in CATEGORIES:
            if c.lower() == record['category'].lower():
                record['category'] = c
                break
        else:
            valid = ", ".join(CATEGORIES)
            raise ValueError(f"\nInvalid category! Please choose from: {valid}.")

    # --- formatting ---
    if 'date' in record and record['date']:
        val = record['date']
        # If user entered 6 digits like 251005
        if val.isdigit() and len(val) == 6:
            record['date'] = f"20{val[:2]}-{val[2:4]}-{val[4:]}"
        else:
            # Validate date format
            try:
                datetime.strptime(val, "%Y-%m-%d")
            except ValueError:
                raise ValueError("\nInvalid date format! Use YYYY-MM-DD or YYMMDD (e.g., 251005).")
    if 'time' in record and record['time']:
        val = record['time']
        # If user entered 4 digits like 1430
        if val.isdigit() and len(val) == 4:
            record['time'] = f"{val[:2]}:{val[2:]}"
        elif val:
            # Validate time format
            try:
                datetime.strptime(val, "%H:%M")
            except ValueError:
                raise ValueError("\nInvalid time format! Use HH:MM or HHMM (e.g., 1430).")