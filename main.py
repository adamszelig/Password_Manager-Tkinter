from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_button():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_list = []

    # for char in range(nr_letters):
    #   password_list.append(random.choice(letters))
    # for char in range(nr_symbols):
    #   password_list += random.choice(symbols)
    # for char in range(nr_numbers):
    #   password_list += random.choice(numbers)

    password_list += [random.choice(letters) for _ in range(nr_letters)]
    password_list += [random.choice(numbers) for _ in range(nr_numbers)]
    password_list += [random.choice(symbols) for _ in range(nr_symbols)]

    random.shuffle(password_list)

    # gen_password = ""
    # for char in password_list:
    #   gen_password += char

    gen_password = "".join(password_list)

    pass_input.delete(0, END)
    pass_input.insert(END, gen_password)

    pyperclip.copy(gen_password)

    # print(f"Your password is: {gen_password}")

# ---------------------------- SAVE PASSWORD ------------------------------- #
def add_button():
    website = site_input.get()
    email = user_input.get()
    password = pass_input.get()

    new_data = {
        website: {
            "email": email,
            "password": password
        }
    }

    if not website or not password:
        messagebox.showinfo(title="Oops", message="Please don't leave any fields empty")
    else:
        try:
            with open("data.json", mode="r") as file:
                # Reading old json data
                data = json.load(file)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            with open("data.json", mode="w") as file:
                json.dump(new_data, file, indent=4)
        else:
            # Updating old json data with new data
            data.update(new_data)

            with open("data.json", mode="w") as file:
                # Saving updated data
                json.dump(data, file, indent=4)
        finally:
            site_input.delete(0, END)
            pass_input.delete(0, END)

# ---------------------------- SEARCH PASSWORDS ------------------------------- #
def search_button():
    website = site_input.get()
    if len(website) > 0:
        try:
            with open("data.json", mode="r") as file:
                data = json.load(file)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            messagebox.showinfo(title="Empty Password List", message="There are no saved passwords")
        else:
            if website in data:
                search = data[website]
                email = search["email"]
                password = search["password"]
                messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {password}")
            else:
                messagebox.showinfo(title="Error", message=f"Searched website is not in list")
    else:
        messagebox.showinfo(title="Empty search field", message="Website entry is empty")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Passsword Manager")
window.config(padx=20, pady=20)

# Create canvas
canvas = Canvas(width=200, height=200)
password_img = PhotoImage(file="./logo.png")
canvas.create_image(100, 100, image=password_img)
canvas.grid(column=1, row=0)

# Labels
w_label = Label(text="Website:")
w_label.grid(column=0, row=1)

e_label = Label(text="Email/Username:")
e_label.grid(column=0, row=2)

p_label = Label(text="Password:")
p_label.grid(column=0, row=3)

# Entry
site_input = Entry(width=45)
site_input.grid(column=1, row=1, sticky="ew")
site_input.focus()

user_input = Entry(width=45)
user_input.insert(END, "dummy@gmail.com")
user_input.grid(column=1, row=2, columnspan=2, sticky="ew")

pass_input = Entry(width=21)
pass_input.grid(column=1, row=3, sticky="ew")

# Buttons
gen_button = Button(text="Generate password", command=generate_button)
gen_button.grid(column=2, row=3, sticky="ew")

add_button = Button(text="Add", command=add_button, width=36)
add_button.grid(column=1, row=4, columnspan=2, sticky="ew")

search_button = Button(text="Search", command=search_button)
search_button.grid(column=2, row=1, sticky="ew")


window.mainloop()
