import os.path as osp
from copy import deepcopy

from travel_ledger.config import COLUMNS, STATE_FILE
from travel_ledger.core.state import load_last_values, save_last_values
from travel_ledger.core.validator import validate_and_format_values
from travel_ledger.db.operations import create_table, insert_record, fetch_record_with_id, update_record
from travel_ledger.db.export import export_to_excel

def main_create(db_path: str):
    create_table(db_path)
    print("Database initialized")


def main_insert(db_path: str):
    # The database to add record into must exist
    assert osp.isfile(db_path), f"File {db_path} does not exist, check for typo!"
    columns = deepcopy(COLUMNS)
    # the 'id' column is set automatically
    columns.pop("id", None)
    kwargs = load_last_values(STATE_FILE)
    print("\nTip: The value in [] is the one used for the last record.",
          "\n     Press Enter to reuse it; or '-' to explicitly clear it.")
    add_more = 'y'
    while add_more == 'y':
        print("")
        for col, (type_, desc) in columns.items():
            # create prompt with optional default value
            prompt = f"  {desc}"
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
        try:
            kwargs = validate_and_format_values(**kwargs)
        except ValueError as e:
            print(e)
            input("Press Enter to continue...")
            continue
        insert_record(db_path, **kwargs)
        print("\nExpense added!")
        # save the values of the current record
        save_last_values(STATE_FILE, kwargs)
        while True:
            add_more = input("\nAdd another expanse? [y/N] ").lower()
            if add_more == 'y' or add_more == 'n':
                break


def main_update(db_path: str):
    # The database to add record into must exist
    assert osp.isfile(db_path), f"File {db_path} does not exist, check for typo!"
    columns = deepcopy(COLUMNS)
    # the 'id' column should not be edited
    columns.pop("id", None)
    print("\nTip: The value in [] is the current value.",
          "\n     Press Enter to keep it; or '-' to explicitly clear it.")
    edit_more = 'y'
    while edit_more == 'y':
        try:
            id_ = int(input("\nEnter the id of the expense to edit: ").strip())
        except ValueError:
            print("Invalid ID: please enter a number.")
            continue
        row = fetch_record_with_id(db_path, id_)
        if row is None:
            print(f"\nNo expense with id {id_}.")
            while True:
                abort = input("Abort editing? [y/N] ").lower()
                if abort == 'y':
                    return
                elif abort == 'n':
                    break
            continue
        record = dict(zip(COLUMNS.keys(), row))
        print("Current record:")
        for col, val in record.items():
            print(f"  {col}: {val}")
        print("\nEditing record:")
        kwargs = {}
        for col, (type_, desc) in columns.items():
            prompt = f"  {desc} [{record[col]}]: "
            new_val = input(prompt).strip()
            if new_val == "":
                # column value is kept, skip it in the UPDATE SQL
                continue
            elif new_val == "-":
                new_val = ""
            kwargs.update({col: new_val})
        if not kwargs:
            print(f"\nNo changes made!")
        else:
            try:
                kwargs = validate_and_format_values(**kwargs)
            except ValueError as e:
                print(e)
                input("Press Enter to continue...")
                continue
            update_record(db_path, id_, **kwargs)
            print("\nExpense edited!")
        while True:
            edit_more = input("\nEdit another expense? [y/N] ").lower()
            if edit_more == 'y' or edit_more == 'n':
                break


def main_export(db_path: str):
    assert osp.isfile(db_path), f"File {db_path} does not exist, check for typo!"
    out_path = input("Enter output Excel file path (press Enter to use default): ").strip() or None
    export_to_excel(db_path, out_path)


def main():
    print("Travel Ledger")
    print("1. Create database")
    print("2. Insert records")
    print("3. Update records")
    print("4. Delete records")
    print("5. List records")
    print("9. Export database")
    choice = input("\nEnter your choice: ").strip()

    task_main = None
    match choice:
        case "1":
            print("Creating database...")
            task_main = main_create
        case "2":
            print("Inserting records...")
            task_main = main_insert
        case "3":
            print("Updating records...")
            task_main = main_update
        case "4":
            print("Deleting records...")
            pass
        case "5":
            pass
        case "9":
            task_main = main_export
        case _:
            print("Invalid choice!")
            return

    db_path = input("\nEnter the database path: ").strip()
    task_main(db_path)