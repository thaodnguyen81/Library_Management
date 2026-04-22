import os
import json
import tkinter as tk
from tkinter import messagebox

class Book:
    def __init__(self, book_id, title, author, genre, quantity, year):
        # 'self' refers to this specific book instance
        self.book_id   = book_id
        self.title     = title
        self.author    = author
        self.genre     = genre
        self.quantity  = int(quantity)    # total copies owned
        self.available = int(quantity)    # copies not yet borrowed
        self.year      = int(year)

    # Convert a Book object → plain dict so json.dump() can save it
    def to_dict(self):
        return {
            "book_id":   self.book_id,
            "title":     self.title,
            "author":    self.author,
            "genre":     self.genre,
            "quantity":  self.quantity,
            "available": self.available,
            "year":      self.year
        }

    # Create a Book object from a dict loaded from the JSON file
    @staticmethod
    def from_dict(d):
        b = Book(d["book_id"], d["title"], d["author"],
                 d["genre"], d["quantity"], d["year"])
        b.available = d.get("available", d["quantity"])
        return b
    

class Member:
    def __init__(self, member_id, name, email):
        self.member_id = member_id
        self.name      = name
        self.email     = email
        # Collections: a list of dicts, one entry per borrowed book
        # e.g. [{"book_id": "B001", "due_date": "2025-05-01"}, ...]
        self.borrowed  = []

    def to_dict(self):
        return {
            "member_id": self.member_id,
            "name":      self.name,
            "email":     self.email,
            "borrowed":  self.borrowed
        }

    @staticmethod
    def from_dict(d):
        m = Member(d["member_id"], d["name"], d["email"])
        m.borrowed = d.get("borrowed", [])
        return m
    
class Library:
    DATA_FILE = "library_data.json"

    def __init__(self):
        # Collections: two dictionaries — key = id, value = object
        self.books   = {}   # { book_id   : Book   }
        self.members = {}   # { member_id : Member }
        self.load()

    # ── FILE I/O: READ ────────────────────────────────────
    def load(self):
        """Read saved data from the JSON file on startup."""
        # Conditional: only read if the file actually exists
        if not os.path.exists(self.DATA_FILE):
            return
        try:                                   # Error handling
            with open(self.DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Loop through every saved book and rebuild Book objects
            for d in data.get("books", []):
                b = Book.from_dict(d)
                self.books[b.book_id] = b

            # Loop through every saved member and rebuild Member objects
            for d in data.get("members", []):
                m = Member.from_dict(d)
                self.members[m.member_id] = m

        except (json.JSONDecodeError, KeyError) as e:
            messagebox.showerror("Load Error", f"Could not read data:\n{e}")