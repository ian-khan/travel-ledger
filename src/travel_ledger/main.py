import os.path as osp
from copy import deepcopy
from travel_ledger.config import COLUMNS, STATE_FILE
from travel_ledger.state import load_last_values, save_last_values
from travel_ledger.transactions import init_db, add_expense

def main_add():
    print("Adding expenses")
    db_path = input("Enter the database path: ").strip()
    # The database to add record into must exist
    assert osp.isfile(db_path), f"File {db_path} does not exist"
    columns = deepcopy(COLUMNS)
    # the 'id' column is set automatically
    columns.pop("id", None)
    kwargs = load_last_values(STATE_FILE)
    print("\nTip: The value in [] is the one used for the last record.",
          "\n     Press Enter to reuse it; or '-' to explicitly clear it.")
    add_more = 'y'
    while add_more == 'y':
        for col, (type_, desc) in columns.items():
            # create prompt with optional default value
            prompt = f"{desc}"
            last_val = kwargs.get(col, None)
            if last_val is not None:
                prompt += f" [{last_val}]"
            prompt += ": "

            val = input(prompt).strip()
            if val == "":
                # reuse the last value, or empty string if it does not exist
                val = last_val if last_val is not None else ""
            elif val == "-":
                # explicitly clear the value
                val = ""
            kwargs.update({col: val})
        add_expense(db_path, **kwargs)
        print("\nExpense added!")
        # save the values of the current record
        save_last_values(STATE_FILE, kwargs)
        while True:
            add_more = input("\nAdd another expanse? [y/N] ").lower()
            if add_more == 'y' or add_more == 'n':
                break

def main_init():
    db_path = input("Enter the database path: ").strip()
    init_db(db_path)
    print("Database initialized")

def main():
    print("Travel Ledger")
    print("1. Initialize database")
    print("2. Add expense")
    choice = input("Enter your choice: ").strip()
    if choice == "1":
        main_init()
    elif choice == "2":
        main_add()
