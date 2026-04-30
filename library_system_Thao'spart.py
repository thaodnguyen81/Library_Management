import json
from datetime import datetime, timedelta

FILE = "library_data.json"

# Save/load data

def save_data(data):
    with open(FILE, 'w') as f:
        json.dump(data, f, indent=4)

def load_data():
    try:
        with open(FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"books": [], "members": [], "loans": []}  

data = load_data()

# find item by id

def find_by_id(lst, id_value):
    for item in lst:
        if item["id"] == id_value:
            return item
    return None


# Late Fee - Recursive
# Each call adds $0.50 and counts down one day.

def late_fee(days):
    if days <= 0: 
        return 0.0
    return 0.50 + late_fee(days - 1)

def ask_date(prompt):
    while True:
        raw = input(f"{prompt} (YYYY-MM-DD): ").strip()
        try:
            return datetime.strptime(raw, "%Y-%m-%d")
        except ValueError:
            print("  Invalid format. Please use YYYY-MM-DD, e.g. 2025-04-27")

# 5. Borrow a book

def borrow(data):
    print("\n--- BORROW A BOOK ---")

    member_id = input("Member ID: ").strip()
    member = find_by_id(data["members"], member_id)
    if not member:
        print("  Member not found.")
        return

    book_id = input("Book ID:   ").strip()
    book = find_by_id(data["books"], book_id)
    if not book:
        print("  Book not found.")
        return

    if book["available"] == False:
        print(f"  '{book['title']}' is already on loan.")
        return

    borrow_date = ask_date("  Borrow date ")
    due_date    = borrow_date + timedelta(days=14)

    loan = {
        "member_id":   member_id,
        "book_id":     book_id,
        "borrow_date": borrow_date.strftime("%Y-%m-%d"),
        "due_date":    due_date.strftime("%Y-%m-%d"),
        "returned":    False,
        "return_date": None
    }

    data["loans"].append(loan)
    book["available"] = False
    save_data(data)

    print(f"\n  '{book['title']}' borrowed by {member['name']}.")
    print(f"  Borrow date  : {loan['borrow_date']}")
    print(f"  Due date     : {loan['due_date']}  (14 days)")


# 6. Return a book

def return_book(data):
    print("\n--- RETURN A BOOK ---")

    book_id = input("Book ID: ").strip()

    loan = None
    for l in data["loans"]:
        if l["book_id"] == book_id and l["returned"] == False:
            loan = l

    if loan is None:
        print("  No active loan found for that book.")
        return

    book   = find_by_id(data["books"],   book_id)
    member = find_by_id(data["members"], loan["member_id"])

    return_date  = ask_date("  Return date ")          
    due_date     = datetime.strptime(loan["due_date"], "%Y-%m-%d")
    days_overdue = (return_date - due_date).days        
    fee          = late_fee(days_overdue)

    loan["returned"]    = True
    loan["return_date"] = return_date.strftime("%Y-%m-%d")  
    book["available"]   = True
    save_data(data)

    print(f"\n  '{book['title']}' returned by {member['name']}.")
    print(f"  Due date     : {loan['due_date']}")
    print(f"  Return date  : {loan['return_date']}")

    if days_overdue > 0:
        print(f"  Days overdue : {days_overdue}")
        print(f"  Late fee     : ${fee:.2f}  ($0.50 x {days_overdue} days)")
    else:
        print("  On time — no late fee!")


# 7. View active loans

def view_loans(data):
    print("\n--- ACTIVE LOANS ---")

    active = []
    for l in data["loans"]:
        if l["returned"] == False:
            active.append(l)

    if len(active) == 0:
        print("  No books currently on loan.")
        return

    check_date = ask_date("  Check as of date")       #Control the 'today' date

    for l in active:
        book   = find_by_id(data["books"],   l["book_id"])
        member = find_by_id(data["members"], l["member_id"])

        book_title  = book["title"]  if book   else l["book_id"]
        member_name = member["name"] if member else l["member_id"]

        due_date     = datetime.strptime(l["due_date"], "%Y-%m-%d")
        days_overdue = (check_date - due_date).days    
        
        if days_overdue > 0:
            fee    = late_fee(days_overdue)
            status = f"OVERDUE by {days_overdue} day(s) — fee so far: ${fee:.2f}"
        else:
            status = f"Due: {l['due_date']}"

        print(f"  {book_title} -> {member_name} | {status}")

# Main loop or Menu Program 

while True:
    print("""
=== LIBRARY MANAGEMENT MENU ===
5. Borrow a book
6. Return a book
7. View active loans 
8. Exit""")

    choice = input("Choice: ").strip()
    if choice == "5": borrow(data)
    elif choice == "6": return_book(data)
    elif choice == "7": view_loans(data)
    elif choice == "8":
        print("Exiting Program.")
        break
    else:
        print("Please enter 1-8.")
