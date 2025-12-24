import os.path as osp
from dataclasses import dataclass
from typing import Callable, Optional

from travel_ledger.config import STATE_FILE
from travel_ledger.core.schema import COLUMNS
from travel_ledger.core.state import load_state_file, save_state_file
from travel_ledger.core.formatting import format_header_footer, format_records, format_summary
from travel_ledger.db.operations import (create_table,
                                         insert_record, update_record, delete_record,
                                         fetch_one_record, fetch_all_records,
                                         sum_records_by_group)
from travel_ledger.db.export import export_to_excel

def main_create(db_path: str):
    create_table(db_path)

def main_insert(db_path: str):
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
        new_record = {}
        for col in COLUMNS[1:]:  # The 'ID' field should not be set manually
            last_val = last_record.get(col.name, None)
            val = col.prompt_and_get_value(last_val)
            new_record.update({col.name: val})

        insert_record(db_path, new_record)
        print("\nRecord inserted!")

        # Save the last record everytime a record is inserted
        last_record = new_record
        state_dict.update({"last_record": last_record})
        save_state_file(STATE_FILE, state_dict)

        # Ask whether to insert another record
        while True:
            choice = input("\nInsert another record? [y/N]: ").lower()
            if choice == 'y' or choice == 'n':
                add_more = True if choice == 'y' else False
                break

def main_update(db_path: str):
    col_names = [col.name for col in COLUMNS]

    print("\nTip: Press Enter to reuse [values in the selected record]"
          "\n     Press '-'   to clear the values")

    # Recursively update multiple records
    update_more = True
    while update_more:
        # Ask user for a record ID
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

        # Ask user for new values for the selected record
        print(f"\nUpdating record id={id_}")
        record_patch = {}  # Fields to update for the selected record
        for col in COLUMNS[1:]:  # The 'ID' field should not be set manually
            new_val = col.prompt_and_get_value(record[col.name])
            if new_val != record[col.name]:
                record_patch.update({col.name: new_val})

        if record_patch:
            # Update the record
            update_record(db_path, id_, record_patch)
            print("\nRecord updated!")

            # Print the updated record
            updated_record = fetch_one_record(db_path, id_)
            updated_record = dict(zip(col_names, updated_record))
            print("\nUpdated record:")
            for col, val in updated_record.items():
                print(f"<> {col}: {val}")

            # Update the state file
            updated_record.pop("ID")
            state_dict = load_state_file(STATE_FILE)
            state_dict.update({"last_record": updated_record})
            save_state_file(STATE_FILE, state_dict)
        else:
            print(f"\nNo update to be made to the record!")

        # Ask whether to another record
        while True:
            choice = input("\nUpdate another record? [y/N]: ").lower()
            if choice == 'y' or choice == 'n':
                update_more = True if choice == 'y' else False
                break

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

def main_summarize(db_path: str):
    records = fetch_all_records(db_path)
    if records is None:
        print("\nNo records in the database!")
        return

    for col in COLUMNS:
        if col.as_groups:
            summed_records = sum_records_by_group(db_path, col)
            # Handle the edge case where all values for a column as groups are empty
            if not summed_records:
                print(f"\nNo data for grouping by {col.name}!")
                continue

            summary = format_summary(col.name, summed_records)
            print(summary)
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


@dataclass
class Task:
    key: str
    description: str
    completion: str
    function: Optional[Callable] = None

    @property
    def input_prompt(self):
        return f"{self.key}: {self.description}"

    @property
    def completion_prompt(self):
        return f"{self.completion}!"


TASKS = {
    "0": Task("0", "Create database", "Database created", main_create),
    "1": Task("1", "Insert records", "Insertion complete", main_insert),
    "2": Task("2", "Update records", "Update complete", main_update),
    "3": Task("3", "Delete records", "Deletion complete", main_delete),
    "4": Task("4", "Print  records", "Printing complete", main_print),
    "5": Task("5", "Summarize records", "Summarization complete", main_summarize),
    "9": Task("9", "Export database", "Database exported", main_export),
    "Q": Task("Q", "Quit program", "")
}

def main():
    print("\nWelcome to use the Travel Ledger!")

    # Seamlessly execute multiple tasks
    while True:
        # Ask user for the task to execute
        print()
        for task in TASKS.values():
            print(task.input_prompt)
        choice = input("\nWhat would you like to do? \n>> ").strip().upper()

        # Execute a task
        task = TASKS.get(choice, None)
        if task is None:  # User made an invalid choice
            continue
        elif task.function is None:  # User chose to quit program
            return
        else:  # User chose a non-quitting task
            while True:
                # Prompt user to provide database path and save it to state file
                db_path = get_and_save_db_path()

                # Validate the provided database path
                db_parent = osp.dirname(db_path)
                is_create_task = task.function is main_create
                try:
                    if is_create_task and not osp.isdir(db_parent):
                        raise FileNotFoundError(f"\n{db_parent} should be an existing directory!")
                    if not is_create_task and not osp.isfile(db_path):
                        raise FileNotFoundError(f"\n{db_path} should be an existing file!")
                    break  # Database path validated
                except FileNotFoundError as e:
                    print(e)
                    input("Press Enter to specify another one.")
                    continue

            task.function(db_path)
            print(task.completion_prompt)
