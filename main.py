from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v',
               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
               'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]
    password_list = password_numbers + password_symbols + password_letters
    shuffle(password_list)

    password = "".join(password_list)

    password_input.delete(0, END)
    password_input.insert(0, password)
    pyperclip.copy(password)
    messagebox.showinfo(title='Password Generated', message=f"New password is set.\ncopied to clipboard")


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_password():
    website = web_input.get()
    username = user_input.get()
    password = password_input.get()
    new_data = {website: {"username": username,
                          "password": password}}
    if len(website) == 0 or len(username) == 0 or len(password) == 0:
        messagebox.showinfo(title='Oops', message='Fields are empty.\n'
                                                  'Fill all fields before saving')
    else:
        is_ok = messagebox.askokcancel(title=website, message=f'Username: {username}\n'
                                                              f'Password: {password}\n'
                                                              f'Are you sure you want to save it?')
        if is_ok:
            # Save password to a file
            try:
                with open('data.json', 'r') as file:
                    # reading old data
                    data = json.load(file)
            except FileNotFoundError:
                with open('data.json', 'w') as file:
                    json.dump(new_data, file, indent=4)
            else:
                # updating old data with new data
                data.update(new_data)
                with open('data.json', 'w') as file:
                    json.dump(data, file, indent=4)
            finally:
                # Reset UI fields
                web_input.delete(0, END)
                user_input.delete(0, END)
                user_input.insert(0, 'eitan9994@gmail.com')
                password_input.delete(0, END)


# -------------------------- SEARCH PASSWORD-----------------------------#
def search():
    web_name = web_input.get()
    if len(web_name) == 0:
        messagebox.showerror(message='Please insert website')
    else:
        try:
            with open('data.json', 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            messagebox.showerror(message='No Data File Found.')
        else:
            if web_name in data:
                username = data[web_name]['username']
                password = data[web_name]['password']
                messagebox.showinfo(web_name, f'User: {username}\n'
                                              f'pass: {password}')
            else:
                messagebox.showerror(message=f'No password saved for website: {web_name}')


# ---------------------------- UI SETUP ------------------------------- #
FONT = ('Ariel', 10)

window = Tk()
window.title('Password Manager')
window.config(padx=20, pady=20)

canvas = Canvas(width=200, height=200)
logo_img = PhotoImage(file='logo.png')
canvas.create_image(110, 100, image=logo_img)
canvas.grid(row=0, column=1)

# Labels
web_label = Label(text='Website:', font=FONT)
web_label.grid(row=1, column=0)

user_label = Label(text='Email/Username:', font=FONT)
user_label.grid(row=2, column=0)

password_label = Label(text='Password:', font=FONT)
password_label.grid(row=3, column=0)

# Entries
web_input = Entry(width=21)
web_input.focus()
web_input.grid(row=1, column=1)

user_input = Entry(width=40)
user_input.insert(0, 'Your Username')
user_input.grid(row=2, column=1, columnspan=2)

password_input = Entry(width=21)
password_input.grid(row=3, column=1)

# Buttons
search_button = Button(text='Search', font=FONT, width=16, command=search)
search_button.grid(row=1, column=2)

pass_generator_button = Button(text='Generate Password', font=FONT, command=generate_password)
pass_generator_button.grid(row=3, column=2)

add_button = Button(text='Add', width=37, font=FONT, command=save_password)
add_button.grid(row=4, column=1, columnspan=2)

window.mainloop()
