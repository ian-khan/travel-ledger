from travel_ledger.transactions import init_db, add_expense

def main():
    print("Travel Ledger")
    print("1. Initialize database")
    print("2. Add expense")
    choice = input("Enter your choice: ").strip()

    if choice == "1":
        db_path = input("Enter the database path: ").strip()
        init_db(db_path)
        print("Database initialized")
    elif choice == "2":
        db_path = input("Enter the database path: ").strip()
        date = input("Date (YYYY-MM-DD): ")
        time = input("Time (HH:MM): ")
        city = input("City: ")
        place = input("Place: ")
        amount = float(input("Amount (JPY): "))
        payer = input("Payer: ")
        method = input("Method: ")
        category = input("Category: ")
        description = input("Description: ")
        notes = input("Notes: ")
        add_expense(db_path,
                    date=date, time=time, city=city, place=place,
                    amount=amount, payer=payer, method=method,
                    category=category, description=description, notes=notes)
        print("Expense added.")
