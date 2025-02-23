# Merged Code: Login & Signup + Password Generator & Text Editor

# --- LOGIN & SIGNUP SYSTEM ---
import sqlite3
from tkinter import *
import os
import subprocess
from tkinter import messagebox
from PIL import Image, ImageTk  # For handling images

# Database Setup
conn = sqlite3.connect("users.db")
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        email TEXT PRIMARY KEY, 
        password TEXT
    )
""")
conn.commit()
conn.close()

# Create Main Window
root = Tk()
root.title("Login & Signup System")
root.attributes('-fullscreen', True)  # Fullscreen mode

# Function to exit fullscreen when 'Esc' key is pressed
def exit_fullscreen(event=None):
    root.attributes('-fullscreen', False)

root.bind("<Escape>", exit_fullscreen)  # Bind Esc key to exit fullscreen

# Load and Set Background Image
bg_image = Image.open("700.jpg")  
bg_image = bg_image.resize((root.winfo_screenwidth(), root.winfo_screenheight()), Image.Resampling.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)

# Place Background Image
bg_label = Label(root, image=bg_photo)
bg_label.place(relwidth=1, relheight=1)  # Cover entire screen

# Function to Signup User
def signup():
    email = entry_email_signup.get()
    password = entry_password_signup.get()

    if email == "" or password == "":
        messagebox.showerror("Error", "All fields are required!")
        return

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO users VALUES (?, ?)", (email, password))
        conn.commit()
        messagebox.showinfo("Success", "Account Created Successfully!")
        frame_signup.place_forget()
        frame_login.place(relx=0.5, rely=0.5, anchor="center")
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Email already exists!")
    
    conn.close()

# Function to Login User
import subprocess
import sys

def login():
    email = entry_email_login.get()
    password = entry_password_login.get()

    if email == "" or password == "":
        messagebox.showerror("Error", "All fields are required!")
        return

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
    user = cursor.fetchone()
    
    if user:
        messagebox.showinfo("Success", "Login Successful!")

        # Open PassGen.py without opening a terminal window
        if os.name == 'nt':  # Windows
            subprocess.Popen(["python", "PassGen.py"], shell=True, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, creationflags=subprocess.CREATE_NO_WINDOW)
        else:  # macOS/Linux
            subprocess.Popen(["python3", "PassGen.py"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        root.destroy()  # Close login window after launching PassGen.py
    else:
        messagebox.showerror("Error", "Invalid Email or Password!")

    conn.close()



# Switch to Signup Page
def open_signup():
    frame_login.place_forget()
    frame_signup.place(relx=0.5, rely=0.5, anchor="center")

# Switch to Login Page
def open_login():
    frame_signup.place_forget()
    frame_login.place(relx=0.5, rely=0.5, anchor="center")

# Button Hover Effects
def on_enter(e):
    e.widget.config(bg="#2980b9", fg="white")

def on_leave(e):
    e.widget.config(bg="#3498db", fg="white")

# **Login Frame (Updated Style)**
frame_login = Frame(root, bg="#dfe6e9", padx=40, pady=40, bd=5, relief="ridge", highlightbackground="gray", highlightthickness=5)  
frame_login.place(relx=0.5, rely=0.5, anchor="center")  

Label(frame_login, text="Login", font=("Helvetica", 26, "bold"), bg="#dfe6e9").pack(pady=10)

Label(frame_login, text="Email:", font=("Helvetica", 14), bg="#dfe6e9").pack(anchor="w")
entry_email_login = Entry(frame_login, width=35, font=("Helvetica", 14))
entry_email_login.pack(pady=5)

Label(frame_login, text="Password:", font=("Helvetica", 14), bg="#dfe6e9").pack(anchor="w")
entry_password_login = Entry(frame_login, width=35, font=("Helvetica", 14), show="*")
entry_password_login.pack(pady=5)

btn_login = Button(frame_login, text="Login", command=login, bg="#3498db", fg="white", font=("Helvetica", 14), width=20, height=1)
btn_login.pack(pady=15)
btn_login.bind("<Enter>", on_enter)
btn_login.bind("<Leave>", on_leave)

Button(frame_login, text="Don't have an account? Signup", command=open_signup, fg="blue", bg="#dfe6e9", font=("Helvetica", 12, "bold")).pack()

# **Signup Frame (Updated Style)**
frame_signup = Frame(root, bg="#dfe6e9", padx=40, pady=40, bd=5, relief="ridge", highlightbackground="gray", highlightthickness=5)  

Label(frame_signup, text="Signup", font=("Helvetica", 26, "bold"), bg="#dfe6e9").pack(pady=10)

Label(frame_signup, text="Email:", font=("Helvetica", 14), bg="#dfe6e9").pack(anchor="w")
entry_email_signup = Entry(frame_signup, width=35, font=("Helvetica", 14))
entry_email_signup.pack(pady=5)

Label(frame_signup, text="Password:", font=("Helvetica", 14), bg="#dfe6e9").pack(anchor="w")
entry_password_signup = Entry(frame_signup, width=35, font=("Helvetica", 14), show="*")
entry_password_signup.pack(pady=5)

btn_signup = Button(frame_signup, text="Signup", command=signup, bg="#3498db", fg="white", font=("Helvetica", 14), width=20, height=1)
btn_signup.pack(pady=15)
btn_signup.bind("<Enter>", on_enter)
btn_signup.bind("<Leave>", on_leave)

Button(frame_signup, text="Already have an account? Login", command=open_login, fg="blue", bg="#dfe6e9", font=("Helvetica", 12, "bold")).pack()

# Show Login Page by Default
frame_login.place(relx=0.5, rely=0.5, anchor="center")

def login_success():
    root.destroy()  # Destroy the login window immediately
    open_main_window()  # Call function to open the main application


root.mainloop()


# --- MAIN APPLICATION (Password Generator & Text Editor) ---
import string
import random
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
import pyperclip

# Initialize the root window
root = Tk()
root.title("Password Generator & Text Editor")

# Set full screen
root.geometry("800x600")
root.state('zoomed')

# Get screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Load and resize background image to match the full screen
bg_image = Image.open("700.jpg")
bg_image = bg_image.resize((screen_width, screen_height), Image.Resampling.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)

# Display the resized background image
bg_label = Label(root, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# Frame for password generator and text editor
border_frame = Frame(root, bd=8, relief="ridge", padx=8, pady=15, bg="#f0f0f0", highlightbackground="#7289da", highlightthickness=3)
border_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

# Title label
label_title = Label(border_frame, text="Password Generator & Text Editor", fg='black', bg="#f0f0f0", font=('Arial Rounded MT Bold', 15))
label_title.pack()

# Text Editor
text_area = Text(border_frame, wrap=WORD, font=("Arial", 12), width=50, height=10)
text_area.pack(pady=5)

def open_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        with open(file_path, "r") as file:
            text_area.delete("1.0", END)
            text_area.insert(END, file.read())

def save_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=[("Text files", "*.txt"),
                                                        ("All files", "*.*")])
    if file_path:
        with open(file_path, "w") as file:
            file.write(text_area.get("1.0", END))

def clear_text():
    text_area.delete("1.0", END)

def cut_text():
    text_area.event_generate("<<Cut>>")

def copy_text():
    text_area.event_generate("<<Copy>>")

def paste_text():
    text_area.event_generate("<<Paste>>")

def select_all():
    text_area.tag_add("sel", "1.0", END)

def delete_selected():
    text_area.delete("sel.first", "sel.last")

# Buttons for text editor
button_frame = Frame(border_frame, bg="#f0f0f0")
button_frame.pack()

buttons = [
    ("Open File", open_file, "#7289da"),
    ("Save File", save_file, "#43b581"),
    ("Clear", clear_text, "#ff4747"),
    ("Cut", cut_text, "#ffcc00"),
    ("Copy", copy_text, "#0099ff"),
    ("Paste", paste_text, "#66cc66"),
    ("Select All", select_all, "#9966ff"),
    ("Delete Selected", delete_selected, "#ff6666")
]

for text, command, color in buttons:
    Button(button_frame, text=text, command=command, font=("Arial Rounded MT Bold", 12), bg=color, fg="white", padx=5, pady=5).pack(side=LEFT, padx=2, pady=2)

# Password generator section
choice = IntVar()
Radiobutton(border_frame, text="Weak Password", variable=choice, value=1, bg="#f0f0f0", fg="black", font=('Arial', 12)).pack()
Radiobutton(border_frame, text="Average Password", variable=choice, value=2, bg="#f0f0f0", fg="black", font=('Arial', 12)).pack()
Radiobutton(border_frame, text="Strong Password", variable=choice, value=3, bg="#f0f0f0", fg="black", font=('Arial', 12)).pack()

label_password = Label(border_frame, text="Choose Password Length", bg="#f0f0f0", fg="black", font=('Arial Rounded MT Bold', 13))
label_password.pack()

val = IntVar()
Spinbox(border_frame, from_=4, to_=30, textvariable=val, width=10, font=('Arial', 12)).pack()

def passgen():
    length = val.get()
    if choice.get() == 1:
        chars = string.ascii_lowercase
    elif choice.get() == 2:
        chars = string.ascii_letters + string.digits
    elif choice.get() == 3:
        chars = string.ascii_letters + string.digits + string.punctuation
    else:
        result.config(text="Select Strength!")
        return ""
    password = "".join(random.choice(chars) for _ in range(length))
    return password

def callback():
    generated_password = passgen()
    result.config(text=generated_password, wraplength=200)
    copy_button.config(state=NORMAL)

button_submit = Button(border_frame, text="Generate Password", command=callback, font=("Arial Rounded MT Bold", 12), bg="#7289da", fg="white", padx=10, pady=5)
button_submit.pack(pady=10)

result = Label(border_frame, text="", relief=RAISED, width=25, font=("Arial Rounded MT Bold", 14), bg="white", fg="black", padx=5, pady=5)
result.pack(pady=5)

def copy_to_clipboard():
    password = result.cget("text")
    if password:
        pyperclip.copy(password)

copy_button = Button(border_frame, text="Copy to Clipboard", command=copy_to_clipboard, state=DISABLED, font=("Arial Rounded MT Bold", 12), bg="#43b581", fg="white", padx=10, pady=5)
copy_button.pack(pady=5)

def logout():
    root.destroy()

logout_button = Button(root, text="Logout", command=logout, font=("Arial Rounded MT Bold", 13), bg="Dark Red", fg="white", padx=10, pady=5)
logout_button.place(relx=0.05, rely=0.9)

root.mainloop()

'''
# Ensure proper execution starts from login system
if __name__ == "__main__":
    login_signup_page()  # Ensure this function is correctly defined above'''