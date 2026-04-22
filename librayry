from datetime import date, datetime

# Library's Database
library_db = [
    ["alice_reads", "The Hobbit", "2026-04-10"],
    ["bookworm_99", "1984, Dune", "2026-05-15"],
    ["charlie_b", "Thermodynamics and an Introduction to Thermostatistics 2nd Edition", "2026-01-20"]
]

#Overtime Fee Per Day
daily_fee = 0.50

#Menu Program
while True:
    print("\n--- LIBRARY SYSTEM ---")
    print("1. Show Full List (Sorted by Date)")
    print("2. Warn Overdue Users")
    print("3. Search for User")
    print("4. Register New User")
    print("5. Exit")
    
    choice = input("Select (1-5): ")

    #Error Handling
    if not (choice == "1" or choice == "2" or choice == "3" or choice == "4" or choice == "5"):
        print("Invalid input.")

    if choice == "1":
        # Sort by date (index 2)
        library_db.sort(key=lambda x: x[2])
        print("\nRECORDS (Sorted by Due Date):")
        for user in library_db:
            print(f"User: {user[0]} | Due: {user[2]}")

    elif choice == "2":
            #Checking for overdue status
            print("\n--- OVERDUE WARNINGS ---")
            today = date.today()
            found_any_overdue = False
            
            for user in library_db:
                # Convert the stored string date back into a date object for comparison
                due_date = datetime.strptime(user[2], "%Y-%m-%d").date()
                
                if today > due_date:
                    days_late = (today - due_date).days
                    fee = days_late * daily_fee
                    # Warning the user
                    print(f"\n!!! WARNING: {user[0].upper()} is {days_late} days late!!!")
                    print(f"    Books: {user[1]} | Fee: ${fee}")
                    found_any_overdue = True
            
            if not found_any_overdue:
                print("Great news! No one is overdue today.")

    elif choice == "3":
        # Linear Search
        search_name = input("Enter username: ").lower()
        found = False
        for user in library_db:
            if user[0] == search_name:
                print(f"\nMatch Found! Books: {user[1]}")
                found = True
                break
        if not found:
            print("User not found.")

    elif choice == "4":
        # Add more User into Database
        print("\n--- Register New Member ---")
        new_name = input("Enter Username: ").lower()
        new_books = input("Enter Book Title(s): ")
        new_date = input("Enter Return Date (YYYY-MM-DD): ")
        
        # Add sublist to Database
        new_entry = [new_name, new_books, new_date]
        library_db.append(new_entry)
        print(f"Successfully registered {new_name}!")

    elif choice == "5":
        print("Closing system...")
        break