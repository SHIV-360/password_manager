from tkinter import *
from tkinter import messagebox
import json
from random import choice, randint, shuffle
import pyperclip

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    numbers = '0123456789'
    symbols = '!#$%&()*+'

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)
    password = "".join(password_list)

    password_entry.delete(0, END)
    password_entry.insert(0, password)
    pyperclip.copy(password)
    messagebox.showinfo(title="Password Generated", message="Password copied to clipboard!")

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = website_entry.get().strip()
    email = email_entry.get().strip()
    password = password_entry.get().strip()

    if not website or not password:
        messagebox.showinfo(title="Oops", message="Please make sure you haven't left any fields empty.")
        return

    new_data = {website.lower(): {"email": email, "password": password}}  # Store website names in lowercase

    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}

    data.update(new_data)

    with open("data.json", "w") as data_file:
        json.dump(data, data_file, indent=4)

    website_entry.delete(0, END)
    password_entry.delete(0, END)

    messagebox.showinfo(title="Success", message="Details saved successfully!")

# ---------------------------- SEARCH PASSWORD (Case-Insensitive) ------------------------------- #
def search_password():
    website = website_entry.get().strip().lower()  # Convert user input to lowercase

    if not website:
        messagebox.showinfo(title="Error", message="Please enter a website name.")
        return

    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
    except (FileNotFoundError, json.JSONDecodeError):
        messagebox.showinfo(title="Error", message="No saved data found!")
        return

    if website in data:
        email = data[website]["email"]
        password = data[website]["password"]
        messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {password}")
    else:
        messagebox.showinfo(title="Not Found", message="No details found for the website.")

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("HOLD-MA-KEES")
window.config(padx=10, pady=10)

canvas = Canvas(height=200, width=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=0, rowspan=5)

# Labels
just_head = Label(text="---- FILL THE FOLLOWING ----")
just_head.grid(row=0, column=2, sticky="e")
website_label = Label(text="WEBSITE:")
website_label.grid(row=1, column=1, sticky="e")
email_label = Label(text="EMAIL/USERNAME:")
email_label.grid(row=2, column=1, sticky="e")
password_label = Label(text="PASSWORD:")
password_label.grid(row=3, column=1, sticky="e")

# Entries
website_entry = Entry(width=21)
website_entry.grid(row=1, column=2, sticky="w")
website_entry.focus()

email_entry = Entry(width=35)
email_entry.grid(row=2, column=2, columnspan=2)
email_entry.insert(0, "shivangd262@gmail.com")

password_entry = Entry(width=20)
password_entry.grid(row=3, column=2)

# Buttons
search_button = Button(text="Search", width=13, command=search_password)
search_button.grid(row=1, column=3)

generate_password_button = Button(text="Generate for me", command=generate_password)
generate_password_button.grid(row=3, column=3)

add_button = Button(text="Add", width=34, command=save)
add_button.grid(row=4, column=2, columnspan=2)

window.mainloop()
