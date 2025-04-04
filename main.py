from random import randint, choice, shuffle
from tkinter import *
from tkinter import messagebox, ttk
import pyperclip
import json
from cryptography.fernet import Fernet

# ---------------------------- CONSTANTS ------------------------------- #
DATA_FILE = 'password.dat'
KEY_FILE = 'secret.key'
DEFAULT_EMAIL = 'daveharsh38@gmail.com'

letters = list('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
numbers = list('0123456789')
symbols = list('!#$%&()*+')

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    """Generate a secure random password and copy it to clipboard."""
    password_entry.delete(0, END)
    password_list = [
        choice(letters) for _ in range(randint(8, 10))
    ] + [
        choice(symbols) for _ in range(randint(2, 4))
    ] + [
        choice(numbers) for _ in range(randint(2, 4))
    ]
    shuffle(password_list)
    password = "".join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)

# ---------------------------- ENCRYPTION / DECRYPTION ------------------------------- #
def load_key():
    """Load the encryption key from the secret.key file."""
    with open(KEY_FILE, "rb") as key_file:
        return key_file.read()

def encrypt_password(new_data, filename, secret_key):
    """Encrypt and store new or updated password data."""
    fernet = Fernet(secret_key)
    try:
        with open(filename, "rb") as file:
            decrypted_data = fernet.decrypt(file.read())
            data = json.loads(decrypted_data.decode())
            data.update(new_data)
    except FileNotFoundError:
        data = new_data

    with open(filename, "wb") as file:
        encrypted = fernet.encrypt(json.dumps(data).encode())
        file.write(encrypted)

def decrypt_password(filename, secret_key):
    """Decrypt password data and return it as a dictionary."""
    fernet = Fernet(secret_key)
    with open(filename, "rb") as file:
        decrypted = fernet.decrypt(file.read())
    return json.loads(decrypted.decode())

# ---------------------------- PASSWORD ACTIONS ------------------------------- #
def save_password():
    """Validate and save a new password entry securely."""
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {website: {"email": email, "password": password}}

    if not website or not password:
        messagebox.showinfo(title="Oops", message="Please don't leave any fields empty.")
        return

    try:
        secret_key = load_key()
    except FileNotFoundError:
        secret_key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as key_file:
            key_file.write(secret_key)

    encrypt_password(new_data, DATA_FILE, secret_key)
    clear_fields()
    messagebox.showinfo(title="Success", message="Password saved successfully!")
    update_dropdown()

def update_password():
    """Update password for an existing website entry."""
    website = website_entry.get()
    password = password_entry.get()
    email = email_entry.get()

    if not website:
        messagebox.showinfo(title="Value Error", message="Please enter website")
        return
    if not password:
        messagebox.showinfo(title="Missing Password", message="Please generate or type a new password")
        return

    try:
        fernet = Fernet(load_key())
        with open(DATA_FILE, 'rb') as file:
            data = json.loads(fernet.decrypt(file.read()).decode())

        if website in data:
            data[website] = {"email": email, "password": password}
            with open(DATA_FILE, 'wb') as file:
                file.write(fernet.encrypt(json.dumps(data).encode()))
            pyperclip.copy(password)
            messagebox.showinfo(title="Updated", message="Password updated and copied to clipboard.")
        else:
            messagebox.showinfo(title="Not Found", message=f"No password found for {website}.")

    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No password file found. Save one first!")

def find_password():
    """Retrieve and show login info for a given website."""
    website = website_entry.get()

    if not website:
        messagebox.showinfo(title="Value Error", message="Please enter website")
        return

    try:
        fernet = Fernet(load_key())
        with open(DATA_FILE, 'rb') as file:
            data = json.loads(fernet.decrypt(file.read()).decode())

        if website in data:
            email, password = data[website]['email'], data[website]['password']
            email_entry.delete(0, END)
            email_entry.insert(0, email)
            password_entry.delete(0, END)
            password_entry.insert(0, password)
            pyperclip.copy(password)
            messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {password}")
        else:
            messagebox.showinfo(title="Not Found", message=f"No details for {website} exist.")

    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="Password file not found.")

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager Securevault")
window.config(padx=50, pady=50)
window.maxsize(600, 600)

canvas = Canvas(width=200, height=200)
logo = PhotoImage(file="Images/logo.png")
canvas.create_image(100, 100, image=logo)
canvas.grid(row=0, column=1)

Label(text="Website:").grid(row=1, column=0)
Label(text="Email/Username:").grid(row=2, column=0)
Label(text="Password:").grid(row=3, column=0)

website_entry = Entry(width=28)
website_entry.grid(row=1, column=1)
website_entry.focus()

email_entry = Entry(width=28)
email_entry.grid(row=2, column=1)
email_entry.insert(0, DEFAULT_EMAIL)

password_entry = Entry(width=28, show="*")
password_entry.grid(row=3, column=1)

# ---------------------------- PASSWORD VISIBILITY TOGGLE ------------------------------- #
show_var = IntVar()

def toggle_password():
    """Toggle visibility of password field."""
    is_shown = show_var.get()
    password_entry.config(show="" if is_shown else "*")
    show_checkbox.config(text="🙈 Hide" if is_shown else "👁 Show")

show_checkbox = Checkbutton(text="👁 Show", variable=show_var, command=toggle_password)
show_checkbox.grid(row=3, column=2, sticky="w")

# ---------------------------- BUTTONS ------------------------------- #
Button(text="Add", command=save_password, width=22).grid(row=4, column=1, pady=(10, 0))
Button(text="Update", command=update_password, width=22).grid(row=4, column=2, pady=(10, 0))
Button(text="Generate", command=generate_password, width=22).grid(row=2, column=2, pady=(10, 0))
Button(text="🧹 Clear All", command=lambda: clear_fields(), width=50).grid(row=6, column=1, columnspan=2, pady=(15, 0))

# ---------------------------- DROPDOWN FOR SEARCH ------------------------------- #
search_dropdown = ttk.Combobox(window, width=27)
search_dropdown.grid(row=1, column=2, columnspan=2, pady=(10, 0))

def handle_dropdown(event):
    """Handle website selection from dropdown."""
    selected = search_dropdown.get()
    website_entry.delete(0, END)
    website_entry.insert(0, selected)
    find_password()

search_dropdown.bind("<<ComboboxSelected>>", handle_dropdown)

# ---------------------------- FIELD UTILITIES ------------------------------- #
def clear_fields():
    """Clear all input fields and reset to defaults."""
    website_entry.delete(0, END)
    email_entry.delete(0, END)
    email_entry.insert(0, DEFAULT_EMAIL)
    password_entry.delete(0, END)
    search_dropdown.set("")

def update_dropdown():
    """Update website dropdown with saved sites."""
    try:
        fernet = Fernet(load_key())
        with open(DATA_FILE, 'rb') as file:
            websites = json.loads(fernet.decrypt(file.read()).decode())
            search_dropdown['values'] = list(websites.keys())
    except:
        search_dropdown['values'] = []

update_dropdown()

window.mainloop()
