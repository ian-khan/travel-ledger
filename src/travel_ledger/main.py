import os
import os.path as osp
from copy import deepcopy

from travel_ledger.config import STATE_FILE
from travel_ledger.core.schema import COLUMNS
from travel_ledger.core.state import load_state_file, save_state_file
from travel_ledger.core.formatting import (validate_and_format_values,
                                           format_header_footer,
                                           format_records)
from travel_ledger.db.operations import (create_table,
                                         insert_record, update_record, delete_record,
                                         fetch_one_record, fetch_all_records)
from travel_ledger.db.export import export_to_excel

def main_create(db_path: str):
    create_table(db_path)
    print("Database created!")


def main_insert(db_path: str):
    # The 'ID' field should not be set manually
    columns = deepcopy(COLUMNS)[1:]

    # Load the last inserted record from the state dict
    # last_record should not contain the 'id' field
    state_dict = load_state_file(STATE_FILE)
    last_record = state_dict.get("last_record", {})

    print("\nTip: Press Enter to reuse [values in the last record]"
          "\n     Press '-'   to clear the values")

    # Recursively insert multiple records
    add_more = True
    while add_more:
        print()
        for col in columns:
            # create prompt with optional default value
            prompt = f">> {col.prompt}"
            last_val = last_record.get(col.name, None)
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
            last_record.update({col.name: val})

        try:
            validate_and_format_values(last_record)
        except ValueError as e:
            print(e)
            input("Press Enter to continue...")
            continue

        insert_record(db_path, last_record)
        print("\nRecord inserted!")

        # Save the last record everytime a record is inserted
        state_dict.update({"last_record": last_record})
        save_state_file(STATE_FILE, state_dict)

        # Ask whether to insert another record
        while True:
            choice = input("\nInsert another record? [y/N]: ").lower()
            if choice == 'y' or choice == 'n':
                add_more = True if choice == 'y' else False
                break

def main_update(db_path: str):
    # The 'ID' field should not be set manually
    columns = deepcopy(COLUMNS)[1:]
    col_names = [col.name for col in COLUMNS]

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

        # Fetch the record to update
        record = fetch_one_record(db_path, id_)
        if record is None:
            print(f"\nThere is no record with id {id_}!")
            while True:
                choice = input("Enter another ID? [y/N]: ").lower()
                if choice == 'y':
                    break
                if choice == 'n':
                    return
            continue
        record = dict(zip(col_names, record))

        # Try updating the selected record until succeed
        while True:
            print(f"\nUpdating record id=={id_}")
            # Fields to update for the selected record
            record_patch = {}
            for col in columns:
                prompt = f">> {col.name} [{record[col.name]}]: "
                new_val = input(prompt).strip()
                if new_val == "":
                    # Field value is unchanged; skip this field in the UPDATE SQL
                    continue
                elif new_val == "-":
                    # Field value is set to empty string
                    new_val = ""
                record_patch.update({col.name: new_val})
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
                print("\nRecord updated!")
            break

        # Print the updated record
        updated_record = fetch_one_record(db_path, id_)
        updated_record = dict(zip(col_names, updated_record))
        print("\nUpdated record:")
        for col, val in updated_record.items():
            print(f"<> {col}: {val}")

        # Ask whether to another record
        while True:
            choice = input("\nUpdate another record? [y/N]: ").lower()
            if choice == 'y' or choice == 'n':
                update_more = True if choice == 'y' else False
                break

    if record != updated_record:
        updated_record.pop("ID")
        state_dict = load_state_file(STATE_FILE)
        state_dict.update({"last_record": updated_record})
        save_state_file(STATE_FILE, state_dict)

def main_delete(db_path: str):
    col_names = [col.name for col in COLUMNS]

    # Recursively delete multiple records
    delete_more = True
    while delete_more:
        try:
            id_ = int(input("\nEnter the ID of the record to delete: ").strip())
        except ValueError:
            print("Entered ID is not a number!")
            continue

        # Fetch the record to delete
        record = fetch_one_record(db_path, id_)
        if record is None:
            print(f"\nThere is no record with id {id_}!")
            while True:
                choice = input("\nEnter another ID? [y/N]: ").lower()
                if choice == 'y':
                    break
                if choice == 'n':
                    return
            continue

        # Print the record to delete
        record = dict(zip(col_names, record))
        print("\nRecord to delete:")
        for col, val in record.items():
            print(f"xx {col}: {val}")

        # Ask for final confirmation
        while True:
            choice = input("\nAre you sure to delete this record? [y/N]: ").lower()
            if choice == 'y':
                delete_record(db_path, id_)
                print("\nDeletion complete!")
                break
            if choice == 'n':
                print("\nDeletion cancelled!")
                break

        # Ask whether to delete another record
        while True:
            choice = input("\nDelete another record? [y/N]: ").lower()
            if choice == 'y' or choice == 'n':
                delete_more = True if choice == 'y' else False
                break

def main_print(db_path: str):
    records = fetch_all_records(db_path)
    if records is None:
        print("\nNo records in the database!")
        return

    header, footer = format_header_footer()
    records = format_records(records)
    print(header)
    print(records)
    print(footer)
    return

def main_export(db_path: str):
    out_path = input("Enter output file path or press Enter "
                     "to save beside database: ").strip() or None
    export_to_excel(db_path, out_path)

def get_and_save_db_path() -> str:
    # Load the last database path from state file
    state_dict = load_state_file(STATE_FILE)
    last_path = state_dict.get("db_path", None)

    # Ask user for database path
    if last_path is None:
        prompt = "\nEnter the database path: "
    else:
        prompt = (f"\nLast database path is: [{last_path}]"
                  f"\nEnter the database path or press Enter to use last: ")
    user_input = input(prompt).strip()
    db_path = user_input if user_input else last_path
    db_path = osp.abspath(osp.expanduser(db_path))

    # Save database path if different from last time
    if db_path != last_path:
        state_dict.update({"db_path": db_path})
        save_state_file(STATE_FILE, state_dict)
    return db_path

def main():
    print("\nWelcome to use the Travel Ledger!")
    db_path = get_and_save_db_path()

    print("\nWhat would you like to do?")
    print("0. Create database")
    print("1. Insert records")
    print("2. Update records")
    print("3. Delete records")
    print("4. Print  records")
    print("9. Export database")
    choice = input("\nEnter your choice: ").strip()

    match choice:
        case "0":
            print("Creating database...")
            task_main = main_create
        case "1":
            print("Inserting records...")
            task_main = main_insert
        case "2":
            print("Updating records...")
            task_main = main_update
        case "3":
            print("Deleting records...")
            task_main = main_delete
        case "4":
            print("Printing records...")
            task_main = main_print
        case "9":
            task_main = main_export
        case _:
            print("Invalid choice!")
            return

    # Validate the database path
    db_parent = osp.dirname(db_path)
    is_create_task = task_main is main_create
    if is_create_task and not osp.isdir(db_parent):
        raise FileNotFoundError(f"{db_parent} should be an existing directory!")
    if not is_create_task and not osp.isfile(db_path):
        raise FileNotFoundError(f"{db_path} should be an existing file!")

    task_main(db_path)
