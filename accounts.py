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

        self.anonnymous_button = ttk.Button(self.l_frame, text="Continue without signing in")
        self.anonnymous_button.grid(pady=(20, 0))

    def create_signin_tab(self):
        self.signin_frame = ttk.Frame(self.signin_tab)
        self.signin_frame.pack()

        username_label = ttk.Label(self.signin_tab, text="Username")
        username_label.pack(pady=(20, 0))

        username_entry = ttk.Entry(self.signin_tab)
        username_entry.pack(pady=(5, 15))

        password_label = ttk.Label(self.signin_tab, text="Password")
        password_label.pack()

        password_entry = ttk.Entry(self.signin_tab)
        password_entry.pack(pady=(5, 15))

        login_button = ttk.Button(self.signin_tab, text="Sign In")
        login_button.pack()

    def create_signup_tab(self):
        self.signup_frame = ttk.Frame(self.signup_tab)
        self.signup_frame.pack()

        username_label = ttk.Label(self.signup_tab, text="Username")
        username_label.pack(pady=(20, 0))

        username_entry = ttk.Entry(self.signup_tab)
        username_entry.pack(pady=(5, 15))

        password_label = ttk.Label(self.signup_tab, text="Password")
        password_label.pack()

        password_entry = ttk.Entry(self.signup_tab)
        password_entry.pack(pady=(5, 15))

        address_label = ttk.Label(self.signup_tab, text="Address")
        address_label.pack()

        address_entry = ttk.Entry(self.signup_tab)
        address_entry.pack(pady=(5, 15))

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

