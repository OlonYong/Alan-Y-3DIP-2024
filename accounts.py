from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import tkinter.font as tkFont
import customtkinter as ctk

class Login:
    def __init__(self, root):
        self.root = root
        self.ctk = ctk
        self.images = []
        # Import the tcl file
        self.root.tk.call("source", r"iteration3\Forest-ttk-theme-master\forest-dark.tcl")
        ttk.Style().theme_use(r'forest-dark')

        self.l_frame = Frame(self.root, background="blue")
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
        
        self.tabs = ttk.Notebook(self.l_frame)
        self.tabs.grid(row=1, sticky="nsew")


        self.signup_tab = ttk.Frame(self.tabs)
        self.signin_tab = ttk.Frame(self.tabs)
        self.tabs.add(self.signin_tab, text="SIGN IN")
        self.tabs.add(self.signup_tab, text="SIGN UP")
        
        self.create_signin_tab()
        self.create_signup_tab()

    def create_signin_tab(self):
        username_entry = ctk.CTkEntry(self.signin_tab)
        username_entry.pack()

        password_entry = ttk.Entry(self.signin_tab)
        password_entry.pack()

        login_button = ttk.Button(self.signin_tab, text="Login")
        login_button.pack()

    def create_signup_tab(self):
        username_entry = ttk.Entry(self.signup_tab)
        username_entry.pack()

        password_entry = ttk.Entry(self.signup_tab)
        password_entry.pack()

        address_entry = ttk.Entry(self.signup_tab)
        address_entry.pack()

        login_button = ttk.Button(self.signup_tab, text="Sign Up")
        login_button.pack()

    def get_frame_size(self):
        # Now, get the correct width and height of the r_frame
        frame_width = self.r_frame.winfo_width()
        frame_height = self.r_frame.winfo_height()
        print(frame_width, frame_height)

        bg_img = Image.open(r"iteration3\images\login_background.png").resize((frame_width, frame_height))
        bg_img = ImageTk.PhotoImage(bg_img)
        self.images.append(bg_img)
        bg_img = Label(self.r_frame, image=self.images[1])
        bg_img.grid()
