import random
import sqlite3
from tkinter import *
from tkinter import messagebox

DB_PATH = "database/users.db"

# Ensure DB and table exist
def initialize_db():
    with sqlite3.connect(DB_PATH) as db:
        cursor = db.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users(
                Username TEXT NOT NULL UNIQUE, 
                GeneratedPassword TEXT NOT NULL
            );
        """)
        db.commit()

# Insert a new user-password pair
def save_user(username, password):
    with sqlite3.connect(DB_PATH) as db:
        cursor = db.cursor()
        try:
            cursor.execute("INSERT INTO users(Username, GeneratedPassword) VALUES (?, ?)", (username, password))
            db.commit()
            return True
        except sqlite3.IntegrityError:
            return False

# GUI Class
class PasswordGeneratorGUI:
    def __init__(self, master):
        self.master = master
        master.title("Password Generator")
        master.geometry("660x500")
        master.resizable(False, False)

        self.username = StringVar()
        self.password_length = IntVar()
        self.generated_password = StringVar()

        # Header
        Label(master, text="Password Generator", fg='darkblue', font='arial 20 bold underline').grid(row=0, column=1, pady=10)

        # Username input
        Label(master, text="Enter username:", font='times 15').grid(row=1, column=0, padx=20, sticky=E)
        self.username_entry = Entry(master, textvariable=self.username, font='times 15', bd=6)
        self.username_entry.grid(row=1, column=1)

        # Password length input
        Label(master, text="Enter password length:", font='times 15').grid(row=2, column=0, padx=20, sticky=E)
        self.length_entry = Entry(master, textvariable=self.password_length, font='times 15', bd=6)
        self.length_entry.grid(row=2, column=1)

        # Generated password
        Label(master, text="Generated password:", font='times 15').grid(row=3, column=0, padx=20, sticky=E)
        self.password_entry = Entry(master, textvariable=self.generated_password, font='times 15', bd=6, fg='darkgreen')
        self.password_entry.grid(row=3, column=1)

        # Buttons
        Button(master, text="Generate Password", command=self.generate_password, font='forte 15', bg='darkblue', fg='white').grid(row=4, column=1, pady=10)
        Button(master, text="Save", command=self.save_password, font='forte 15', bg='green', fg='white').grid(row=5, column=1, pady=5)
        Button(master, text="Reset", command=self.reset_fields, font='forte 15', bg='gray', fg='white').grid(row=6, column=1, pady=5)

    def generate_password(self):
        name = self.username.get().strip()
        try:
            length = int(self.password_length.get())
        except ValueError:
            messagebox.showerror("Invalid input", "Password length must be a number")
            return

        if not name:
            messagebox.showerror("Input Error", "Username cannot be empty")
            return
        if not name.isalpha():
            messagebox.showerror("Input Error", "Username must contain only letters")
            return
        if length < 6:
            messagebox.showerror("Input Error", "Password must be at least 6 characters long")
            return

        upper = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        lower = list("abcdefghijklmnopqrstuvwxyz")
        chars = list("@#%&()\"?!")
        numbers = list("1234567890")

        u = random.randint(1, length - 3)
        l = random.randint(1, length - 2 - u)
        c = random.randint(1, length - 1 - u - l)
        n = length - u - l - c

        password = random.sample(upper, u) + random.sample(lower, l) + random.sample(chars, c) + random.sample(numbers, n)
        random.shuffle(password)
        final_password = ''.join(password)

        self.generated_password.set(final_password)

    def save_password(self):
        name = self.username.get().strip()
        password = self.generated_password.get().strip()

        if not name or not password:
            messagebox.showerror("Input Error", "Username and password cannot be empty")
            return

        if save_user(name, password):
            messagebox.showinfo("Success", "Password saved successfully!")
        else:
            messagebox.showerror("Duplicate", "Username already exists. Use a different one.")

    def reset_fields(self):
        self.username.set("")
        self.password_length.set(0)
        self.generated_password.set("")

# Run GUI
if __name__ == "__main__":
    initialize_db()
    root = Tk()
    app = PasswordGeneratorGUI(root)
    root.mainloop()
