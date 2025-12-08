import os.path as osp
from copy import deepcopy

from travel_ledger.config import COLUMNS, STATE_FILE
from travel_ledger.core.state import load_state_file, save_state_file
from travel_ledger.core.validator import validate_and_format_values
from travel_ledger.db.operations import create_table, insert_record, fetch_record_with_id, update_record
from travel_ledger.db.export import export_to_excel

def main_create(db_path: str):
    create_table(db_path)
    print("Database initialized")


def main_insert(db_path: str):
    assert osp.isfile(db_path), f"Database {db_path} does not exist!"
    columns = deepcopy(COLUMNS)
    # The 'id' field should not be set manually
    columns.pop("id", None)

    # Load the last inserted record
    # last_record should not contain the 'id' field
    last_record = load_state_file(STATE_FILE)

    print("\nTip: Press Enter to reuse [values in the last record]"
          "\n     Press '-'   to clear the values")

    # Recursively insert multiple records
    add_more = True
    while add_more:
        print()
        for col, (type_, desc) in columns.items():
            # create prompt with optional default value
            prompt = f"  {desc}"
            last_val = last_record.get(col, None)
            if last_val is not None:
                prompt += f"[{last_val}]"
            prompt += ": "

            val = input(prompt).strip()
            if val == "":
                # reuse the last value, or empty string if it does not exist
                val = last_val if last_val is not None else ""
            elif val == "-":
                # explicitly clear the value
                val = ""
            last_record.update({col: val})

        try:
            validate_and_format_values(last_record)
        except ValueError as e:
            print(e)
            input("Press Enter to continue...")
            continue

        insert_record(db_path, last_record)
        print("\nRecord inserted!")

        while True:
            choice = input("\nInsert another record? [y/N] ").lower()
            if choice == 'y' or choice == 'n':
                add_more = True if choice == 'y' else False
                break

    # save the last record after all are inserted
    save_state_file(STATE_FILE, last_record)


def main_update(db_path: str):
    # The database to add record into must exist
    assert osp.isfile(db_path), f"Database {db_path} does not exist, check for typo!"
    columns = deepcopy(COLUMNS)
    # The 'id' field should not be set manually
    columns.pop("id", None)

    print("\nTip: Press Enter to reuse [values in the selected record]"
          "\n     Press '-'   to clear the values")

    # Recursively update multiple records
    update_more = True
    while update_more:
        try:
            id_ = int(input("\nEnter the ID of the record to update: ").strip())
        except ValueError:
            print("Entered ID is not a number!")
            continue

        # Fetch
        record = fetch_record_with_id(db_path, id_)
        if record is None:
            print(f"\nThere is no record with id {id_}!")
            while True:
                choice = input("Enter another ID? [y/N] ").lower()
                if choice == 'y':
                    break
                if choice == 'n':
                    return
            continue
        record = dict(zip(COLUMNS.keys(), record))

        # Try updating the selected record until succeed
        while True:
            print(f"\nUpdating record id=={id_}")
            # Fields to update for the selected record
            record_patch = {}
            for col, (type_, desc) in columns.items():
                prompt = f"  {desc} [{record[col]}]: "
                new_val = input(prompt).strip()
                if new_val == "":
                    # Field value is unchanged; skip this field in the UPDATE SQL
                    continue
                elif new_val == "-":
                    # Field value is set to empty string
                    new_val = ""
                record_patch.update({col: new_val})
            # Verify and format the patch for the record
            if not record_patch:
                print(f"\nNo update to be made to the record!")
            else:
                try:
                    validate_and_format_values(record_patch)
                except ValueError as e:
                    print(e)
                    input("Press Enter to update again.")
                    continue
                update_record(db_path, id_, record_patch)
                print("\nRecord edited!")
            break

        # Print the updated record
        record = fetch_record_with_id(db_path, id_)
        record = dict(zip(COLUMNS.keys(), record))
        print("\nUpdated record:")
        for col, val in record.items():
            print(f"  {col}: {val}")

        # Ask for updating another record
        while True:
            choice = input("\nUpdate another record? [y/N] ").lower()
            if choice == 'y' or choice == 'n':
                update_more = True if choice == 'y' else False
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