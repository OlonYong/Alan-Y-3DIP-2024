from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from cryptography.fernet import Fernet
import os
import json

class Login:
#   initialises the login screen
    def __init__(self, root):
        self.root = root
        self.images = []
        self.root.tk.call("source", r"iteration3\Forest-ttk-theme-master\forest-dark.tcl")
        ttk.Style().theme_use(r'forest-dark')


        self.l_frame = ttk.Frame(self.root)
        self.l_frame.grid(row=0, column=0, sticky="nsew")
        self.r_frame = ttk.Frame(self.root)
        self.r_frame.grid(row=0, column=1, sticky="nsew")
        self.root.grid_columnconfigure(0, weight=42)
        self.root.grid_columnconfigure(1, weight=58)
        self.root.grid_rowconfigure(0, weight=1)

        self.r_frame.grid_propagate(False)
        self.l_frame.grid_propagate(False)
        self.l_frame.grid_columnconfigure(0, weight=1)
        title_frame = ttk.Frame(self.l_frame)
        title_frame.grid(pady=30)

        logo_img = Image.open(r"iteration3\images\logo.png").resize((64, 50))
        logo_img = ImageTk.PhotoImage(logo_img)
        self.images.append(logo_img)
        logo = ttk.Label(title_frame, image=self.images[0])
        logo.grid(row=0, column=0, padx=(0, 10))
        title_lbl = ttk.Label(title_frame, text="RecycleAKL", font=("Arial", 30, "bold"), foreground="#2EA53A")
        title_lbl.grid(row=0, column=1)

        self.root.after(150, self.get_frame_size)

        self.tabs = ttk.Notebook(self.l_frame, style="TFrame")
        self.tabs.grid(row=1)


        self.signup_tab = ttk.Frame(self.tabs)
        self.signin_tab = ttk.Frame(self.tabs)
        self.tabs.add(self.signin_tab, text="SIGN IN")
        self.tabs.add(self.signup_tab, text="SIGN UP")
        
        self.create_signin_tab()
        self.create_signup_tab()

        self.error_label = ttk.Label(self.l_frame, text="")
        self.error_label.grid(pady=(20, 0))
        self.button_text = StringVar()
        self.button_text.set("Sign In")
        self.action_button = ttk.Button(self.l_frame, textvariable=self.button_text, command=self.button_clicked)
        self.action_button.grid(pady=(20, 0))
        self.anonnymous_button = ttk.Button(self.l_frame, text="Continue without signing in")
        self.anonnymous_button.grid(pady=(20, 0))

        self.tabs.bind('<<NotebookTabChanged>>', self.on_tab_change)

    def create_signin_tab(self):
        self.signin_frame = ttk.Frame(self.signin_tab)
        self.signin_frame.pack()

        username_label = ttk.Label(self.signin_tab, text="Username")
        username_label.pack(pady=(20, 0))

        self.signin_username_entry = ttk.Entry(self.signin_tab)
        self.signin_username_entry.pack(pady=(5, 15))

        password_label = ttk.Label(self.signin_tab, text="Password")
        password_label.pack()

        self.signin_password_entry = ttk.Entry(self.signin_tab)
        self.signin_password_entry.pack(pady=(5, 15))

    def create_signup_tab(self):
        self.signup_frame = ttk.Frame(self.signup_tab)
        self.signup_frame.pack()

        username_label = ttk.Label(self.signup_tab, text="Username")
        username_label.pack(pady=(20, 0))

        self.signup_username_entry = ttk.Entry(self.signup_tab)
        self.signup_username_entry.pack(pady=(5, 15))

        password_label = ttk.Label(self.signup_tab, text="Password")
        password_label.pack()

        self.signup_password_entry = ttk.Entry(self.signup_tab)
        self.signup_password_entry.pack(pady=(5, 15))

        address_label = ttk.Label(self.signup_tab, text="Address")
        address_label.pack()

        self.address_entry = ttk.Entry(self.signup_tab)
        self.address_entry.pack(pady=(5, 15))

    def on_tab_change(self, event):
        active_tab = self.tabs.index(self.tabs.select())
        if active_tab == 0:
            self.button_text.set("Sign In")
        elif active_tab == 1:
            self.button_text.set("Sign Up")

    def button_clicked(self):
        active_tab = self.tabs.index(self.tabs.select())
        if active_tab == 0:
            self.check_details()
        elif active_tab == 1:
            self.save_details()

    def get_frame_size(self):
        frame_width = self.r_frame.winfo_width()
        frame_height = self.r_frame.winfo_height()

        bg_img = Image.open(r"iteration3\images\login_background.png").resize((frame_width, frame_height))
        bg_img = ImageTk.PhotoImage(bg_img)
        self.images.append(bg_img)
        bg_img = Label(self.r_frame, image=self.images[1])
        bg_img.grid()

    def check_details(self):
        from collection import Collection
        username = self.signin_username_entry.get()
        password = self.signin_password_entry.get()
        if username == "" or password == "":
            self.error_label.config(text="Please fill in all fields.")
            return
        try:
            with open(r"iteration3\accounts-data.json", "r") as file:
                accounts = json.load(file)
            for account in accounts:
                if self.decrypt(account["username"]) == username and self.decrypt(account["password"]) == password:
                    username = self.decrypt(account["username"])
                    password = self.decrypt(account["password"])
                    address = self.decrypt(account["address"])
                    details = Details(self.root, username, password, address)
                    Collection(self.root)
                    

            self.error_label.config(text="Invalid username or password.")
        except FileNotFoundError:
            messagebox.showinfo("Error", "No accounts found, please register an account.")
            self.tabs.select(1)
            return

    def get_key(self):
        try:
            with open(r"iteration3\key.key", "rb") as file:
                key = file.read()
        except FileNotFoundError:
            key = Fernet.generate_key()
            with open(r"iteration3\key.key", "wb") as file:
                file.write(key)
        return key

    def encrypt(self, data):
        key = self.get_key()
        cipher = Fernet(key)
        encrypted = cipher.encrypt(data.encode()).decode()
        return encrypted
    
    def decrypt(self, data):
        key = self.get_key()
        cipher = Fernet(key)
        decrypted = cipher.decrypt(data.encode()).decode()
        return decrypted

    def save_details(self):
        username = self.signup_username_entry.get()
        password = self.signup_password_entry.get()
        address = self.address_entry.get()
        # accounts = self.read_accounts()
        # print(accounts)
        with open(r"iteration3\accounts-data.json", "a") as file:
            data = f'{{"username": {self.encrypt(username)},"password": {self.encrypt(password)},"address": {self.encrypt(address)}}},\n'
            json.dump(data, file, indent=4)

class Details:
    def __init__(self, root, username, password, address):
        self.root = root
        self.username = username
        self.password = password
        self.address = address
        
