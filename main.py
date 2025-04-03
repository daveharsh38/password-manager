from random import randint, choice, shuffle
from tkinter import *
from tkinter import messagebox
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
#Password Generator Project
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

def generate_password():
    password_entry.delete(0,END)
    password_list = [choice(letters) for _ in range(randint(8, 10))]
    password_list += [choice(symbols) for _ in range(randint(2, 4))]
    password_list += [choice(numbers) for _ in range(randint(2, 4))]
    shuffle(password_list)

    # password = ""
    # for char in password_list:
    #   password += char
    password = "".join(password_list)
    password_entry.insert(0,password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_password():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
    website : {
        "email": email,
        "password": password,
        }
    }

    if len(website) == 0 or len(password) ==0:
        messagebox.showinfo(title="Opps", message="Please make sure you haven't left any fields empty.")

    else:
        try:
            with open("data.json",'r') as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            with open("data.json",'w') as data_file:
                json.dump(new_data, data_file, indent=4)
                messagebox.showinfo(title="Success", message="Password added successfully.\nYou can directly paste it.")
        else:
            if website in data:
                messagebox.showinfo(title=f"Password Found for {website}", message=f"Email: {data[website]['email']}\n"
                                                                                   f"Password: {data[website]['password']}"
                                                                                   f"\n You can directily paste it.")
                pyperclip.copy(data[website]['password'])
                return
            else:
                data.update(new_data)
                with open("data.json", "w") as data_file:
                    json.dump(data, data_file, indent=4)
                    messagebox.showinfo(title="Success", message="Password added successfully.\nYou can directly paste it. ")
        finally:
            website_entry.delete(0,END)
            password_entry.delete(0,END)


# ---------------------------- Find password ------------------------------- #
def find_password():
    if len(website_entry.get()) == 0:
        messagebox.showinfo(title="Value error", message="Please add website")

    else:
        website = website_entry.get()
        try:
            with open("data.json") as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            messagebox.showinfo(title="Error", message="No Data File Found.")
        else:
            if website in data:
                messagebox.showinfo(title=website,message=f"Email: {data[website]['email']}\nPassword: {data[website]['password']}"
                                                          f"\nYou can directly paste it")
                pyperclip.copy(data[website]['password'])
            else:
                messagebox.showinfo(title="Error",message=f"No details for website: {website} exists.")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50,pady=50)
window.maxsize(500,400)

canvas = Canvas(width=200,height=200)
password_logo = PhotoImage(file="logo.png")
canvas.create_image(100,100,image=password_logo)
canvas.grid(column=1, row=0)

#Labels
website_label = Label(text="Website:")
website_label.grid(row=1, column=0)
email_label = Label(text="Email/Username:")
email_label.grid(row=2, column=0)
password_label = Label(text="Password:")
password_label.grid(row=3, column=0)

#Entries
website_entry = Entry(width=30)
website_entry.grid(row=1, column=1)
website_entry.focus()

email_entry = Entry(width=49)
email_entry.grid(row=2, column=1,columnspan=2)
email_entry.insert(0,"daveharsh38@gmail.com")

password_entry = Entry(width=30)
password_entry.grid(row=3, column=1)

# Buttons
generate_password_button = Button(text="Generate Password",command=generate_password,width=15)
generate_password_button.grid(row=3, column=2)
add_button = Button(text="Add", command=save_password,width=35)
add_button.grid(row=4, column=1,columnspan=3)
search_button = Button(text="Search",command=find_password,width=15)
search_button.grid(row=1,column=2)

window.mainloop()
