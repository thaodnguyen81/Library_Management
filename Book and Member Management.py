import json

FILE = "library_data.json"

def save_data(data):
    with open(FILE, 'w') as f:
        json.dump(data, f, indent=4)

def initialize_system():
    print("\n--- INITIAL SYSTEM SETUP ---")
    print("Welcome! Please register your 5 books and 5 members.")
    data = {"books": [], "members": []}
    
    # Register 5 Books
    for i in range(1, 6):
        print(f"\n[Book {i}/5]")
        data["books"].append({
            "id": input("ID: "), "title": input("Title: "), 
            "author": input("Author: "), "genre": input("Genre: "), "year": input("Year: ")
        })
    
    # Register 5 Members
    for i in range(1, 6):
        print(f"\n[Member {i}/5]")
        data["members"].append({"id": input("ID: "), "name": input("Name: ")})
    
    save_data(data)
    print("\nSystem initialized successfully!")

def search_data():
    try:
        with open(FILE, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("No data found.")
        return

    term = input("\nEnter ID, Genre, or Name to search: ").lower()
    found = False
    
    for b in data["books"]:
        if term in [b['id'].lower(), b['genre'].lower()]:
            print(f"Found Book: {b['title']} (ID: {b['id']}, Genre: {b['genre']})")
            found = True
            
    for m in data["members"]:
        if term in [m['id'].lower(), m['name'].lower()]:
            print(f"Found Member: {m['name']} (ID: {m['id']})")
            found = True
            
    if not found: print("No results found.")

if __name__ == "__main__":
    # This now runs every time the program starts
    initialize_system()
    
    while True:
        print("\n=== LIBRARY MANAGEMENT MENU ===")
        print("1. Search (ID/Genre/Name)")
        print("2. Exit")
        cmd = input("Choice: ")
        if cmd == '1': search_data()
        elif cmd == '2': break