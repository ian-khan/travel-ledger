import os.path as osp
from copy import deepcopy
from travel_ledger.config import COLUMNS
from travel_ledger.transactions import init_db, add_expense

def main_add():
    print("Adding expenses")
    db_path = input("Enter the database path: ").strip()
    # The database to add record into must exist
    assert osp.isfile(db_path), f"File {db_path} does not exist"

    columns = deepcopy(COLUMNS)
    columns.pop("id", None)
    kwargs = dict()

    add_more = 'y'
    while add_more == 'y':
        for col, (type_, desc) in columns.items():
            last_val = kwargs.get(col, "")
            val = input(f"{desc} [{last_val}]: ").strip()
            kwargs.update({col: val})
        add_expense(db_path, **kwargs)
        print("Expense added")
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
