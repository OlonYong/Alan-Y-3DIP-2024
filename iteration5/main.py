import subprocess # Module for running system commands
import sys # Module for system parameters and functions
import os # Module for dynamic file handling
from tkinter import * # Module for GUI

# Installation of dependencies if needed
try:
    import pip
except ImportError:
    print("Pip is not installed.")
try:
    from tkinter import ttk, messagebox # Additional gui components
    from PIL import Image, ImageTk # Module for image handling
    import customtkinter as ctk # Module for modernized tkinter widgets
    from ctypes import windll # Module for DPI awareness and scaling
    import json # Module for reading and writing JSON formats
    from datetime import datetime, timedelta # Module for handling date and time requests
    import requests # Module for handling HTTP requests and acquisition from APIs
    from cryptography.fernet import Fernet # Module for encryption
    from tkintermapview import TkinterMapView # Module for creating the interactive map
    import google.generativeai as gai # Module for AI resonse generation in guides
    import random # Module for quiz questions
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", os.path.join(os.path.dirname(__file__), "requirements.txt")])

# This class handles the window set up.
class App:
    def __init__(self):
        self.root = Tk()
        self.root.title("RecycleAKL")
        self.root.geometry("1636x864")
        self.root.resizable(False, False)

        global DIRECTORY
        DIRECTORY = os.path.join(os.path.dirname(__file__), "assets")
        
        global IMAGE_PATH
        IMAGE_PATH = os.path.join(os.path.dirname(__file__), "assets", "images")
        
        global DARK_COLOUR
        DARK_COLOUR = "#313131" 

        global LIGHT_COLOUR
        LIGHT_COLOUR = "#F2F7FA"

#       DPI Awareness and Scaling to ensure resolution compatibility
        windll.shcore.SetProcessDpiAwareness(1)
        scaling_factor = self.root.winfo_fpixels('1i') / 72.0 
        self.root.tk.call('tk', 'scaling', scaling_factor)

#       Load custom ttk theme
        self.root.tk.call("source", os.path.join(DIRECTORY, "Forest-ttk-theme-master", "forest-dark.tcl"))
        ttk.Style().theme_use(r'forest-dark')

#       Initialize session details
        global session
        session = Details()

#       Load the sign in/sign out page
        Account(self.root)

#       Run the main loop
        self.root.mainloop()

# class to store the user's details
class Details:
    user_details = None

# class used to store commonly used methods
class Utility:

#   Load image and resize
    @staticmethod
    def load_image(path, resize, tk=True):
        logo_img = Image.open(os.path.join(IMAGE_PATH, path)).resize(resize)
        if tk:
            return ImageTk.PhotoImage(logo_img)
        else:
            return ctk.CTkImage(logo_img) 
        
#   Read user details from external file
    @staticmethod
    def read_accounts():
        try:
            with open(os.path.join(DIRECTORY, "accounts-data.json"), "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return []

#   Check if address is valid
    @staticmethod
    def check_address(address):
        try:
            url = "http://163.47.222.43:80/api/v1/rr"
            parameters = {'addr': address}
            response = requests.get(url, params=parameters)
            data = response.json()
        except:
            return False, False
        if "address" in data:
            return True, data["address"]
        else:
            return False, False

#   Fetch address suggestions
    @staticmethod
    def fetch_address_suggestions(address):
        url = "http://163.47.222.43:80/api/v1/addr"
        parameters = {'addr': address}
        response = requests.get(url, params=parameters)
        if response.status_code == 200:
            data = response.json()
            return [item['Suggestion'] for item in data]
        return []

    # load and resize the background image used in collections
    @staticmethod
    def background_img(parent):
        frame_width = parent.winfo_width()
        frame_height = parent.winfo_height()
        bg_img = Utility.load_image("background.png", (1277, 864))
        bg_img_lbl = Label(parent, image=bg_img, borderwidth=0)
        bg_img_lbl.place(relwidth=1, relheight=1)
        return bg_img
    
#   Update the user's details
    @staticmethod
    def update_file(username):
        encryption = Encryption()
        accounts = Utility.read_accounts()
        for account in accounts:
            if encryption.decrypt(account["username"]) == username:
                account["username"] = encryption.encrypt(session.user_details["username"])
                account["password"] = encryption.encrypt(session.user_details["password"])
                account["address"] = encryption.encrypt(session.user_details["address"])
                account["points"] = session.user_details["points"]
                account["quiz-date"] = session.user_details["quiz_date"]
                account["report-date"] = session.user_details["report_date"]
                account["streak"] = session.user_details["streak"]
        with open(os.path.join(DIRECTORY, "accounts-data.json"), "w") as file:
            json.dump(accounts, file, indent=4)

# class for handling sign in and sign up
class Account:
    def __init__(self, root):
        self.root = root
        self.images = []
        self.encryption = Encryption()
        self.utility = Utility()

        self.create_content()
        self.root.after(150, self.create_background_img)

#   Create UI elements
    def create_content(self):
        self.ui_frame = ttk.Frame(self.root)
        self.ui_frame.grid(row=0, column=0, sticky="nsew")
        self.ui_frame.grid_propagate(False)
        self.ui_frame.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=42)
        self.create_ui(self.ui_frame)
        
#       Create background image
        self.bg_frame = ttk.Frame(self.root)
        self.bg_frame.grid(row=0, column=1, sticky="nsew")
        self.bg_frame.grid_propagate(False)
        self.root.grid_columnconfigure(1, weight=58)
        #self.create_background_img()
        
        self.root.grid_rowconfigure(0, weight=1)

#   Create interface elements
    def create_ui(self, parent):
        title_frame = ttk.Frame(parent)
        title_frame.grid(row=0, pady=(30, 50))

        title_lbl = ttk.Label(title_frame, text="RecycleAKL", font=("Arial", 30, "bold"), foreground="#2EA53A")
        title_lbl.grid(row=0, column=1, padx=(0, 0))

#       Load images
        self.load_images()
        logo = ttk.Label(title_frame, image=self.logo_img)
        logo.grid(row=0, column=0, padx=(0, 10))

#       Create Notebook widget that contains sign in and sign out
        self.tabs = ttk.Notebook(parent)
        self.tabs.grid(row=1)

        self.signin_tab = ttk.Frame(self.tabs)
        self.signin_tab.grid(column=0)
        self.tabs.add(self.signin_tab, text="SIGN IN")

        self.signup_tab = ttk.Frame(self.tabs)
        self.signup_tab.grid(column=1)
        self.tabs.add(self.signup_tab, text="SIGN UP")
        
        self.create_signin_tab()
        self.create_signup_tab()
        
#       Create submit buttons
        self.error_label = ttk.Label(parent, text="", font=20)
        self.error_label.grid(row=2, pady=(15, 0))
        self.signup_button = ttk.Button(parent, text="Don't have an account?", width=25, command=lambda:[self.tabs.select(1), self.signup_button.grid_forget()])

        self.button_text = StringVar()
        self.action_button = ttk.Button(parent, textvariable=self.button_text, width=25, command=self.button_clicked, style="Accent.TButton")
        self.action_button.grid(row=4, pady=(15, 0))
        self.button_text.set("Sign In")

        self.anonymous_button = ttk.Button(parent, text="Continue without signing in", width=25, command=lambda: self.anonymous(), style="Accent.TButton")
        self.anonymous_button.grid(row=5, pady=(15, 0))
        
#       Style buttons
        style = ttk.Style()
        style.configure("Accent.TButton", font=("Arial", 16), padding=10)
        
#       Update button text
        self.tabs.bind('<<NotebookTabChanged>>', self.on_tab_change)
        
        if os.path.exists(os.path.join(DIRECTORY, "accounts-data.json")) == False:
            self.tabs.select(1)
        else:
            self.tabs.select(0)

#   Load images for logo and password visibility
    def load_images(self):
        self.logo_img = self.utility.load_image("logo.png", (64, 50))
        self.hide_img = self.utility.load_image("hide.png", (30, 30))
        self.show_img = self.utility.load_image("show.png", (30, 30))

#   Create sign in tab
    def create_signin_tab(self):
        self.signin_frame = ttk.Frame(self.signin_tab)
        self.signin_frame.pack()

        username_label = ttk.Label(self.signin_tab, text="Username", font=("Calibri light", 16), width=30)
        username_label.pack(pady=(30, 0))

        self.signin_username_entry = ttk.Entry(self.signin_tab, font=("Calibri light", 16), width=30)
        self.signin_username_entry.pack(pady=(5, 15))

        password_label = ttk.Label(self.signin_tab, text="Password", font=("Calibri light", 16), width=30)
        password_label.pack()

        self.signin_password_frame = ttk.Frame(self.signin_tab)
        self.signin_password_frame.pack()

        self.signin_password_entry = ttk.Entry(self.signin_password_frame, font=("Calibri light", 16), width=30, show="*")
        self.signin_password_entry.grid(row=0, pady=(5, 15), sticky="ew")

        self.show_password = False
        self.signin_show_password_button = Button(self.signin_password_frame, image=self.hide_img, command=lambda:self.toggle_password(), height=28, width=28, border=0, relief=FLAT)
        self.signin_show_password_button.grid(row=0, pady=(5, 15), sticky="e", padx=2)

#   Create sign up tab
    def create_signup_tab(self):
        self.signup_frame = ttk.Frame(self.signup_tab)
        self.signup_frame.grid(row=0)

        username_label = ttk.Label(self.signup_tab, text="Username", font=("Calibri light", 16), width=30)
        username_label.grid(row=1, pady=(30, 0))

        self.signup_username_entry = ttk.Entry(self.signup_tab, font=("Calibri light", 16), width=30)
        self.signup_username_entry.grid(row=2, pady=(5, 15))

        password_label = ttk.Label(self.signup_tab, text="Password", font=("Calibri light", 16), width=30)
        password_label.grid(row=3)
        
        self.signup_password_frame = ttk.Frame(self.signup_tab)
        self.signup_password_frame.grid(row=4)

        self.signup_password_entry = ttk.Entry(self.signup_password_frame, font=("Calibri light", 16), width=30, show="*")
        self.signup_password_entry.grid(row=0, pady=(5, 15), sticky="ew")

        self.show_password = False
        self.signup_show_password_button = Button(self.signup_password_frame, image=self.hide_img, command=lambda:self.toggle_password(), height=28, width=28, border=0, relief=FLAT)
        self.signup_show_password_button.grid(row=0, pady=(5, 15), sticky="e", padx=2)
    
        address_label = ttk.Label(self.signup_tab, text="Address", font=("Calibri light", 16), width=30)
        address_label.grid(row=5)

        self.root.after(150, self.create_autocomplete)

#   Create autocomplete address entry
    def create_autocomplete(self):
        self.signup_address_entry = AutoComplete(self.signup_tab, CTK=False).entry

#   Toggle password visibility
    def toggle_password(self):
        if self.show_password:
            self.show_password = False
            self.signin_password_entry.config(show="*")
            self.signup_password_entry.config(show="*")
            self.signup_show_password_button.config(image=self.hide_img)
            self.signin_show_password_button.config(image=self.hide_img)
        else:
            self.show_password = True
            self.signup_password_entry.config(show="")
            self.signin_password_entry.config(show="")
            self.signin_show_password_button.config(image=self.show_img)
            self.signup_show_password_button.config(image=self.show_img)        

#   Update action button text
    def on_tab_change(self, event):
        active_tab = self.tabs.index(self.tabs.select())
        if active_tab == 0:
            self.button_text.set("Sign In")
            self.error_label.config(text="")
            
        elif active_tab == 1:
            self.button_text.set("Sign Up")
            self.error_label.config(text="")
            try:
                self.signup_button.destroy()
            except:
                pass

#   Change notebook tabs
    def button_clicked(self):
        active_tab = self.tabs.index(self.tabs.select())
        if active_tab == 0:
            self.check_details()
        elif active_tab == 1:
            self.check_signup()

#   Size image to fit frame
    def create_background_img(self):
        frame_width = self.bg_frame.winfo_width()
        frame_height = self.bg_frame.winfo_height()
        self.bg_img = self.utility.load_image("login_background.png", (frame_width, frame_height))
        bg_img = Label(self.bg_frame, image=self.bg_img, borderwidth=0)
        bg_img.grid()

#   Check if sign in details are valid
    def check_details(self):
        username = self.signin_username_entry.get()
        password = self.signin_password_entry.get()

        if username == "" or password == "":
            self.error_label.config(text="Please fill in all fields.")
            return
        
        accounts = Utility.read_accounts()
        if accounts != []:
            for account in accounts:
                if self.encryption.decrypt(account["username"]) == username and self.encryption.decrypt(account["password"]) == password:
                    username = self.encryption.decrypt(account["username"])
                    password = self.encryption.decrypt(account["password"])
                    address = self.encryption.decrypt(account["address"])
                    points = account["points"]
                    quiz_date = account["quiz-date"]
                    streak = account["streak"]
                    report_date = account["report-date"]
                    session.user_details = {
                        "username": username,
                        "password": password,
                        "address": address,
                        "points" : points,
                        "quiz_date" : quiz_date,
                        "report_date" : report_date,
                        "streak" : streak
                    }
                    AppManager(self.root)
                    return
            self.error_label.config(text="Invalid username or password.")
            self.signup_button.grid(row=3, pady=(10, 0))
        else:
            messagebox.showinfo("Error", "No accounts found, please register an account.")
            self.tabs.select(1)
            return     
              
#   Check if sign up details are valid
    def check_signup(self):
        if self.signup_username_entry.get() == "" or self.signup_password_entry.get() == "" or self.signup_address_entry.get() == "":
            self.error_label.config(text="Please fill in all fields.")
            return False
        
        valid, address = Utility.check_address(self.signup_address_entry.get())
        if valid:
            self.save_details()

        else:
            self.error_label.config(text="Address not found, please try again.")

#   Write user details into external file
    def save_details(self):
        username = self.signup_username_entry.get()
        password = self.signup_password_entry.get()
        address = self.signup_address_entry.get()
        accounts = Utility.read_accounts()

        with open(os.path.join(DIRECTORY, "accounts-data.json"), "w") as file:
            data = {"username": self.encryption.encrypt(username),
                    "password": self.encryption.encrypt(password),
                    "address": self.encryption.encrypt(address),
                    "points" : 0,
                    "quiz-date" : None,
                    "report-date" : None,
                    "streak" : 0
                    }
            accounts.append(data)
            json.dump(accounts, file, indent=4)

        session.user_details = {
            "username": username,
            "password": password,
            "address": address,
            "points" : 0,
            "quiz_date" : None,
            "report_date" : None,
            "streak" : 0
        }
        AppManager(self.root)

#   Update user details to anonymous
    def anonymous(self):
        session.user_details = {
            "username": "Anonymous",
            "password": "Anonymous",
            "address": "Anonymous",
            "points" : 0,
            "quiz_date" : None,
            "report_date" : None,
            "streak" : 0
        }
        for widget in self.ui_frame.winfo_children():
            widget.destroy()
        for widget in self.bg_frame.winfo_children():
            widget.destroy()
        AppManager(self.root)

# class for handling encryption
class Encryption:
    def __init__(self):
        self.key = self.load_key()

#   Load cipher key
    def load_key(self):
        try:
            keypath = os.path.join(DIRECTORY, "key.key")
            with open(keypath, "rb") as file:
                key = file.read()
        except FileNotFoundError:
            key = Fernet.generate_key()
            with open(keypath, "wb") as file:
                file.write(key)
        return key

#   Encrypt account data
    def encrypt(self, data):
        cipher = Fernet(self.key)
        encrypted = cipher.encrypt(data.encode()).decode()
        return encrypted

#   Decrypt account data
    def decrypt(self, data):
        cipher = Fernet(self.key)
        decrypted = cipher.decrypt(data.encode()).decode()
        return decrypted
    

# class to manage the screens of the program
class AppManager:
    def __init__(self, root):
        self.root = root

        self.root.grid_columnconfigure(0, weight=2)
        self.root.grid_columnconfigure(1, weight=7)

#       Loading screen
        self.loading_screen = Frame(self.root)
        self.loading_screen.grid(row=0, column=0, columnspan=2, sticky="nsew")
        self.loading_screen.grid_rowconfigure(0, weight=1)
        self.loading_screen.grid_columnconfigure(0, weight=1)

        loading_text = Label(self.loading_screen, text="Please wait\n\nLoading...", font=("Arial", 30), bg=DARK_COLOUR, fg="white")
        loading_text.grid(sticky="nsew")

#       Sidebar and main content frames
        self.sidebar_frame = Frame(self.root) 
        self.sidebar_frame.grid_columnconfigure(0, weight=1)
        self.sidebar_frame.grid_propagate(False)

        self.main_frame = Frame(self.root, background=LIGHT_COLOUR)
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_propagate(False)

        self.screens = {}
        self.current_screen = "CollectionScreen"

        self.sidebar = Sidebar(self.sidebar_frame, self.switch_screens, self.current_screen, self)

#       Load screens
        for screen in [ProfileScreen, PointsScreen, QuizScreen, MapScreen, GuideScreen, CollectionScreen]:
            self.create_screen(screen)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.main_frame.grid(row=0, column=1, sticky="nsew")   

#   Create screens
    def create_screen(self, screen):
        if screen == ProfileScreen:
            screen_instance = screen(self.main_frame, self, self.root)
        else:
            if screen in [CollectionScreen, MapScreen]:
                screen_instance = screen(self.main_frame, self.sidebar)
            else:
                screen_instance = screen(self.main_frame)
        name = screen.__name__
        self.screens[name] = screen_instance
        screen_instance.grid(row=0, column=0, sticky="nsew") 

#   Switch between screens
    def switch_screens(self, screen_name):
        if session.user_details["username"] == "Anonymous" and screen_name == "ProfileScreen" or session.user_details["username"] == "Anonymous" and screen_name == "PointsScreen":
            messagebox.showinfo("Error", "Please sign in to access this feature.")
            return
        if screen_name == "PointsScreen":
            self.screens[screen_name].check_update()
        if screen_name not in ["CollectionScreen", "MapScreen"]:
            try:
                self.sidebar.another_button.grid_forget()
            except:
                pass
        else:
            if session.user_details["address"] != "Anonymous":
                self.sidebar.another_button.grid(row=0, column=0, sticky="ew")
        screen = self.screens[screen_name]
        screen.tkraise()
        self.current_screen = screen_name  # Store the screen name, not the instance
        # Disable the button for the current screen
        for button_name, button in self.sidebar.buttons.items():
            button.configure(state="normal", fg_color=DARK_COLOUR)  # Enable all buttons first
        self.sidebar.buttons[screen_name].configure(state="disabled", fg_color="#3D3D3D")


# class for the sidebar
class Sidebar:
    def __init__(self, root, switch_screens, current_screen, app):
        self.root = root
        self.app = app
        self.roots = app.root
        self.switch_screens = switch_screens
        self.current_screen = current_screen

        self.title_frame = Frame(self.root)
        self.title_frame.grid(row=0, column=0, pady=(25, 35))
        
        self.logo_img = Utility.load_image("logo.png", (51, 40))
        logo = Label(self.title_frame, image=self.logo_img)
        logo.grid(row=0, column=0)
        
        title_lbl = Label(self.title_frame, text="RecycleAKL", font=("Arial", 25, "bold"), foreground="#2EA53A")
        title_lbl.grid(row=0, column=1, padx=(10, 0))
        
        self.buttons = self.create_buttons()

#   Create sidebar buttons
    def create_buttons(self):
        sidebar_buttons = [
            ("CollectionScreen", "Next collection date", "collection_icon.png"),
            ("GuideScreen", "Disposal guides", "guides_icon.png"),
            ("MapScreen", "Interactive map", "map_icon.png"),
            ("QuizScreen", "Recycle quiz", "quiz_icon.png"),
            ("PointsScreen", "EcoPoints", "points_icon.png"),
            ("ProfileScreen", "Manage Account", "profile_icon.png")
        ]
        
        buttons = {}
        self.sidebar_images = []
        row = 1

        for screen, text, icon in sidebar_buttons:
            icon_img = Utility.load_image(icon, (40, 40), False)
            self.sidebar_images.append(icon_img)

            button = ctk.CTkButton(
                self.root,
                text=f" {text}",
                image=icon_img,
                compound='left',
                command=lambda screen=screen: self.switch_screens(screen),
                fg_color=DARK_COLOUR,
                hover_color="#297430",
                text_color=LIGHT_COLOUR,
                font=("Calibri light", 18),
                anchor="ew",
                border_spacing=12,
                text_color_disabled="#40D24E",
            )

#           Disable the button for the current screen
            if self.current_screen == screen:
                button.configure(fg_color = "#3D3D3D", state="disabled")
            
            button.grid(row=row, column=0, sticky="ew")
            row += 1
            buttons[screen] = button
        
        if session.user_details["username"] != "Anonymous":
            signout_btn_text = "Sign Out"
        else:
            signout_btn_text = "Sign In"

        bottom_btn_frame = Frame(self.root)
        bottom_btn_frame.grid(row=row, column=0, sticky="sew")
        self.root.grid_rowconfigure(row, weight=1)
        bottom_btn_frame.grid_columnconfigure(0, weight=1)
        
        self.another_button = ctk.CTkButton(
            bottom_btn_frame,
            text="Change address",
            command=lambda: self.clear_collection(),
            fg_color=DARK_COLOUR,
            hover_color="#297430",
            text_color=LIGHT_COLOUR,
            font=("Calibri light", 18),
            anchor="ew",
            border_spacing=12,
            text_color_disabled="#40D24E"
        )

        signout_button = ctk.CTkButton(
            bottom_btn_frame,
            text=signout_btn_text,
            command=lambda: self.clear_session(),
            fg_color=DARK_COLOUR,
            hover_color="#297430",
            text_color=LIGHT_COLOUR,
            font=("Calibri light", 18),
            anchor="ew",
            border_spacing=12,
            text_color_disabled="#40D24E"
        )
        signout_button.grid(row=1, column=0, sticky="ew")
        return buttons

#   Clear the user's session
    def clear_collection(self):
        session.user_details["address"] = "Anonymous"
        if self.app.current_screen in ["CollectionScreen", "MapScreen"]:
            for widget in self.app.screens[self.app.current_screen].winfo_children():
                widget.destroy()
            self.app.screens[self.app.current_screen].content()

#   Clear current session details
    def clear_session(self):
        session.user_details = None
        self.app.sidebar_frame.destroy()
        self.app.main_frame.destroy()
        Account(self.roots)

# class for handing the bin collection date screen
class CollectionScreen(Frame):
    def __init__(self, parent, sidebar):
        super().__init__(parent, bg=LIGHT_COLOUR)
        user_data = session.user_details
        self.username = user_data["username"]
        self.password = user_data["password"]
        self.address = user_data["address"]
        self.sidebar = sidebar
        self.content()

#   Create the content of the collection screen
    def content(self):

        self.background = Utility.background_img(self)
        
        self.images = []
        title_frame = ctk.CTkFrame(self, bg_color=LIGHT_COLOUR, fg_color="#008033", corner_radius=8)
        title_frame.grid(row=0, column=0, pady=(15, 40), padx=15, sticky="w")
        
        self.icon_img = Utility.load_image("collection_icon.png", (50, 50))
        img_lbl = Label(title_frame, image=self.icon_img, bg="#008033")
        img_lbl.grid(column=0, row=0, rowspan=2, padx=15)
        self.grid_columnconfigure(0, weight=1)
        
        title_lbl = Label(title_frame, text="Next Collection Date", font=("Calibri light", 25), bg="#008033", fg="white")
        title_lbl.grid(column=1, row=0, sticky="sw")

        title_desc_lbl = Label(title_frame, text="View your next kerbside bin collection date", font=("Calibri light", 15), bg="#008033", fg="white")
        title_desc_lbl.grid(column=1, row=1, sticky="nw", pady=(0, 8), padx=(0, 15))
        
#       Check if user is signed in
        if self.address == "Anonymous":
            try:
                self.sidebar.another_button.grid_forget()
            except:
                pass
            self.get_address()
        else:
            self.content = CollectionDate(self, self.address, self.sidebar)

#   class to get the user's address if not logged in
    def get_address(self):

        self.info_frame = ctk.CTkFrame(self, bg_color=LIGHT_COLOUR, fg_color="white", corner_radius=10)
        self.info_frame.grid(row=1, columnspan=2)
        
        address_lbl = ctk.CTkLabel(self.info_frame, text="Please enter your address to view your next kerbside bin collection date", font=("Calibri light", 20), corner_radius=10, text_color="black")
        address_lbl.grid(column=0, row=1, pady=10)
        
        self.address_entry = AutoComplete(self.info_frame).entry

        submit_button = ctk.CTkButton(self.info_frame, text="Submit", font=("Calibri light", 15), corner_radius=10, command=lambda: self.update_address(self.address_entry.get()), text_color="black", fg_color="#40d24e", height=35)
        submit_button.grid(column=0, row=4, pady=10)

#   Update the user's address
    def update_address(self, address):
        valid, address = Utility.check_address(address)
        if valid == True:
            session.user_details["address"] = address
            self.info_frame.destroy()
            CollectionDate(self, address, self.sidebar)
        else:
            messagebox.showinfo("Error", "Address not found, please try again.") 


# class for autocomplete address entry
class AutoComplete:
    def __init__(self, root, CTK=True):
        self.root = root
        if CTK == True:
            self.entry = ctk.CTkEntry(self.root, font=("Calibri light", 15), corner_radius=10, text_color="black", fg_color=LIGHT_COLOUR, width=300, height=35)
            self.row = 2
            self.bg = "white"
            self.text_color = "black"
        else:
            self.entry = ttk.Entry(self.root, font=("Calibri light", 16), width=30)
            self.row = 6
            self.bg = DARK_COLOUR
            self.text_color = "white"
        self.suggestions_frame = ctk.CTkScrollableFrame(self.root, bg_color=self.bg, fg_color=self.bg, corner_radius=10, height=35)
        self.suggestions_frame.grid_columnconfigure(0, weight=1)
        self.create_content()

#   Create the autocomplete entry and suggestions
    def create_content(self):
        self.entry.grid(row=self.row)
        self.suggestions_frame.grid(row=(self.row+1), sticky="ew")  
        self.suggestions_frame.grid_forget() 
        self.entry.bind("<KeyRelease>", self.update_suggestions)
    
#   Update the suggestions based on the user's input
    def update_suggestions(self, event):
        address = self.entry.get()
        if address:
            suggestions = Utility.fetch_address_suggestions(address)
            self.clear_suggestions()
            for suggestion in suggestions:
                btn = ctk.CTkButton(self.suggestions_frame, text=suggestion, command=lambda s=suggestion: self.select_suggestion(s), bg_color=self.bg, text_color=self.text_color, corner_radius=10, fg_color=self.bg, border_width=1)
                btn.grid(column=0, sticky="ew")
            if suggestions:
                self.suggestions_frame.grid(row=(self.row+1), sticky="ew") 
            else:
                self.suggestions_frame.grid_forget()
        else:
            self.clear_suggestions()
    
#   Clear the suggestions when no input
    def clear_suggestions(self):
        for widget in self.suggestions_frame.winfo_children():
            widget.destroy()
        self.suggestions_frame.grid_forget()

#   Select the suggestion and enter into entry when clicked
    def select_suggestion(self, suggestion):
        self.entry.delete(0, END)
        self.entry.insert(0, suggestion)
        self.clear_suggestions()
        self.suggestions_frame.grid_forget() 


# class for the reminder date
class CollectionDate:
    BIN_TYPES = ["Rubbish", "Foodscraps", "Recycling"]
    def __init__(self, parent, address, sidebar):
        self.parent = parent
        self.address = address
        self.sidebar = sidebar
        self.images = []
        self.get_collection_date()
        self.load_images()
        
        self.parent.grid_columnconfigure(0, weight=1)
        self.parent.grid_columnconfigure(1, weight=1)

        self.collections_frame = ctk.CTkFrame(self.parent, bg_color=LIGHT_COLOUR, fg_color="#CDE1CD", corner_radius=20)
        self.collections_frame.grid(row=1, columnspan=2, sticky="ns", pady=20)
        self.collections_frame.grid_columnconfigure(0, weight=1)

        address_lbl = Label(self.collections_frame, text=f"{self.formatted_address}", font=("Calibri light", 20, "underline"), bg="#CDE1CD", fg="black")
        address_lbl.grid(pady=(30,0))

        header_lbl = Label(self.collections_frame, text="Your next collection date is on: ", font=("Calibri light", 20), bg="#CDE1CD", fg="black")
        header_lbl.grid(pady=(20,10))

        date_worded_lbl = Label(self.collections_frame, text=self.worded_date, font=("Calibri light", 25, "bold"), bg="#CDE1CD", fg="black")
        date_worded_lbl.grid()

        date_lbl = Label(self.collections_frame, text=self.formatted_date, font=("Calibri light", 25, "bold"), bg="#CDE1CD", fg="black")
        date_lbl.grid()

        bins_lbl = Label(self.collections_frame, text="Bins being collected:", font=("Calibri light", 20), bg="#CDE1CD", fg="black")
        bins_lbl.grid(pady=(30,0))

        bins_frame = Frame(self.collections_frame, bg="#CDE1CD")
        bins_frame.grid()

#       Display the bins
        for image in range(len(self.images)):
            img_label = Label(bins_frame, image=self.images[image], width=130, height=160, bg="#CDE1CD")
            img_label.grid(row=0, column=(image), padx=40, pady=(20,10))
            img_label.image = self.images[image]
            bin_name = Label(bins_frame, text=f"{self.BIN_TYPES[image]}", font=("Calibri light", 25), bg="#CDE1CD", fg="black")
            bin_name.grid(row=1, column=(image))
            
        note_lbl = Label(self.collections_frame, text="Please put out the bins before 7am", font=("Calibri light", 15), bg="#CDE1CD", fg="black")
        note_lbl.grid(pady=(20,40))

        if session.user_details["username"] == "Anonymous":
            self.sidebar.another_button.grid(row=0, column=0, sticky="ew")

#   Loads the images for the bins
    def load_images(self):
        self.rubbish_img = Utility.load_image("rubbish.png", (130, 160))
        self.images.append(self.rubbish_img)

        if self.foodscrap:
            self.foodscraps_img = Utility.load_image("foodscraps.png", (130, 160))
            self.images.append(self.foodscraps_img)
        
        if self.recycling:
            self.recycling_img = Utility.load_image("recycle.png", (130, 160))
            self.images.append(self.recycling_img)

#   Get the collection dates from the API
    def get_collection_date(self):
        url = "http://163.47.222.43:80/api/v1/rr"
        parameters = {'addr': self.address}
        response = requests.get(url, params=parameters)
        data = response.json()
        categories = ["rubbish", "recycle", "foodscraps", "address"]
        trys = {}

        for category in categories:
            try:
                trys[category] = data[category]
            except:
                trys[category ] = "NA"

        # Now you can assign the values to your instance variables
        self.rubbish_date = trys.get("rubbish", "NA")
        self.recycling_date = trys.get("recycle", "NA")
        self.foodscraps_date = trys.get("foodscraps", "NA")
        self.formatted_address = trys.get("address", "NA")
        
        if self.rubbish_date == self.recycling_date:
            self.recycling = True
        else:
            self.recycling = False
        if self.foodscraps_date == self.rubbish_date:
            self.foodscrap = True
        else:
            self.foodscrap = False
        self.format_date(self.rubbish_date)

#   Format date to commonly readable format
    def format_date(self, date):
        date_object = datetime.strptime(date, "%Y-%m-%d")
        self.formatted_date = date_object.strftime("%d/%m/%y")

#       Format the date to include weekday and month
        formatted_date = date_object.strftime('%A')  # Gets the full weekday name
        day = date_object.day 

#       Add ordinal suffix to the day
        if 10 <= day % 100 <= 20:
            suffix = 'th'
        else:
            suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(day % 10, 'th')

        self.worded_date = f"{formatted_date} {day}{suffix} {date_object.strftime('%B')}"

# class for handling the disposal guides
class GuideScreen(Frame):
    def __init__(self, parent):   
        super().__init__(parent, bg=LIGHT_COLOUR)

        self.grid_columnconfigure(0, weight=1)
        self.frames = {}

        title_frame = ctk.CTkFrame(self, bg_color=LIGHT_COLOUR, fg_color="#008033", corner_radius=8)
        title_frame.grid(row=0, column=0, pady=(15, 40), padx=15, sticky="w")
        
        self.icon_img = Utility.load_image("guides_icon.png", (50, 50))
        img_lbl = Label(title_frame, image=self.icon_img, bg="#008033")
        img_lbl.grid(column=0, row=0, rowspan=2, padx=15)
        
        title_lbl = Label(title_frame, text="Disposal Guides", font=("Calibri light", 25), bg="#008033", fg="white")
        title_lbl.grid(column=1, row=0, sticky="sw")

        title_desc_lbl = Label(title_frame, text="Learn Auckland Council's waste disposal guidelines", font=("Calibri light", 15), bg="#008033", fg="white")
        title_desc_lbl.grid(column=1, row=1, sticky="nw", pady=(0, 8), padx=(0, 15))
        
        self.create_buttons(self)
        self.create_overview(self)

#       Create the navigation buttons
        for button in self.buttons:
            button_name = button.cget("text").lower()
            if button_name not in ["overview", "custom"]:
                self.create_frames(button_name)
        self.create_overview(self)
        self.create_ai(self)
        self.show_guide("overview")

#   Create buttons for switching between disposal guides
    def create_buttons(self, parent):
        self.data, self.categories = self.load_data()
        buttons_frame = Frame(parent, bg=LIGHT_COLOUR)
        buttons_frame.grid(row=1, column=0)
        self.buttons = []
        
        for i in range(0, len(self.categories)):
            button = ctk.CTkButton(
                buttons_frame,
                text=self.categories[i].capitalize(),
                font=("Calibri light", 15),
                corner_radius=15,
                fg_color="#008033",
                hover_color="#40d24e",
                text_color="white",
                command=lambda page=self.categories[i]: self.show_guide(page),
                width=20,
                text_color_disabled="white"
            )
            button.grid(row=0, column = i, padx=10)
            self.buttons.append(button)

#   Load the disposal guide data from JSON file
    def load_data(self):
        with open(os.path.join(DIRECTORY, "data.json"), "r") as file:
            data = json.load(file)
            categories = list(data.keys())
            return data, categories

#   Show the disposal guide
    def show_guide(self, page):

#       Change the button colours
        for button in self.buttons:
            if button.cget("state").lower() == "disabled":
                button.configure(fg_color = "#008033", state="normal")
            elif button.cget("text").lower() == page:
                button.configure(fg_color = "#004d1e", state="disabled")

#       Show the correct frame
        if page == "overview":
            frame = self.overview_frame
        elif page == "custom":
            frame = self.ai_frame
        else:
            frame = self.frames[page]

        for frames in [self.overview_frame, self.ai_frame] + list(self.frames.values()):
            frames.grid_remove()
        frame.grid(row=2, column=0, sticky="nsew")
    
#   Create the frames for each disposal guide
    def create_frames(self, page):
        self.grid_rowconfigure(2, weight=1)
        content_frame = Frame(self, bg=LIGHT_COLOUR)
        content_frame.grid(row=2, column=0, pady=(20,30), padx=30, sticky="nsew")

#       Configure the grid
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_columnconfigure(1, weight=1)
        content_frame.grid_columnconfigure(2, weight=1)
        content_frame.grid_rowconfigure(0, weight=1)
        
        overview_frame = ctk.CTkFrame(content_frame, bg_color="white", fg_color="white", corner_radius=20)
        overview_frame.grid(row=0, column=0, pady=20, sticky="nsew", padx=20)
        overview_frame.grid_columnconfigure(0, weight=1)
        overview_frame.grid_rowconfigure(1, weight=1)

        overview_lbl = ctk.CTkLabel(overview_frame, text="Overview", font=("Calibri light", 25, "bold", "underline"), corner_radius=10, fg_color="white", text_color="#35353C")
        overview_lbl.grid(row=0, column=0, pady=(10,0))
        
        overview_text = ctk.CTkTextbox(overview_frame, font=("Calibri light", 15), corner_radius=10, fg_color="white", text_color="#35353C", wrap="word")
        overview_text.grid(row=1, column=0, sticky="nsew")
        overview_text.insert("0.0", self.data[page]["overview"])
        overview_text.configure(state="disabled")

        recycle_frame = ctk.CTkFrame(content_frame, bg_color="white", fg_color="white", corner_radius=20)
        recycle_frame.grid(row=0, column=1, pady=20, sticky="nsew")
        recycle_frame.grid_columnconfigure(0, weight=1)
        recycle_frame.grid_rowconfigure(1, weight=1)

        recycle_lbl = ctk.CTkLabel(recycle_frame, text="Recycling Bin", font=("Calibri light", 25, "bold", "underline"), corner_radius=10, fg_color="white", text_color="#D1AC28")
        recycle_lbl.grid(row=0, column=0, pady=(10,0))

        recycle_text = ctk.CTkTextbox(recycle_frame, font=("Calibri light", 15), corner_radius=10, fg_color="white", text_color="#35353C", wrap="word")
        recycle_text.grid(row=1, column=0, sticky="nsew")
        recycle_text.insert("0.0", self.data[page]["recycling"])
        recycle_text.configure(state="disabled")

        rubbish_frame = ctk.CTkFrame(content_frame, bg_color="white", fg_color="white", corner_radius=20)
        rubbish_frame.grid(row=0, column=2, pady=20, sticky="nsew", padx=20)
        rubbish_frame.grid_columnconfigure(0, weight=1)
        rubbish_frame.grid_rowconfigure(1, weight=1)

        rubbish_lbl = ctk.CTkLabel(rubbish_frame, text="Rubbish Bin", font=("Calibri light", 25, "bold", "underline"), corner_radius=10, fg_color="white", text_color="#EA3636")
        rubbish_lbl.grid(row=0, column=0, pady=(10,0))

        rubbish_text = ctk.CTkTextbox(rubbish_frame, font=("Calibri light", 15), corner_radius=10, fg_color="white", text_color="#35353C", wrap="word")
        rubbish_text.grid(row=1, column=0, sticky="nsew")
        rubbish_text.insert("0.0", self.data[page]["rubbish"])
        rubbish_text.configure(state="disabled")

        if page == "organic":
            recycle_lbl.configure(text="Foodscraps Bin", text_color="#40D24E")

        self.frames[page] = content_frame

#   Create the overview section
    def create_overview(self, parent):
        content_frame = ctk.CTkFrame(parent, bg_color=LIGHT_COLOUR, fg_color="white", corner_radius=20)
        content_frame.grid(row=2, column=0, pady=(20,30), padx=30, sticky="nsew")
        content_frame.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        overview_lbl = ctk.CTkLabel(content_frame, text="Overview", font=("Calibri light", 25, "bold", "underline"), corner_radius=10, fg_color="white", text_color="#35353C")
        overview_lbl.grid(row=0, column=0, pady=(10,0))
        content_frame.grid_rowconfigure(1, weight=1)
        overview_text = ctk.CTkScrollableFrame(content_frame, bg_color="white", fg_color="white", corner_radius=20)
        overview_text.grid(row=1, column=0, sticky="nsew", pady=20, padx=20)
        overview_text.grid_columnconfigure(0, weight=1)
        
        overview_content = "Utilizing Auckland Council's kerbside collection service effectively can significantly reduce household waste, promote responsible recycling, and contribute to a cleaner environment. Understanding what can and cannot be recycled, along with following the correct disposal methods, ensures that materials are processed properly, minimizing landfill use and supporting sustainability efforts.\n\nAuckland households have access to three types of bins for kerbside collection: the red rubbish bin, the yellow recycling bin, and the green food scraps bin.\n\n- Red rubbish bin: This is for general waste that goes to the landfill and is collected weekly\n\n- Yellow recycling bin: Used for recyclable materials, this bin is collected every two weeks\n\n- Green food scraps bin: Designed for all organic food waste, this bin is also collected weekly\n\nTo ensure timely collection, bins should be placed at the kerbside by 7:00 a.m. on collection day, with the handles facing the street. The food scraps bin should have its handle facing upwards and be positioned slightly away from the other bins. By following these guidelines, residents can help streamline the collection process and support a cleaner, more sustainable Auckland."
        overview_lbl = ctk.CTkLabel(overview_text, font=("Calibri light", 15), text=overview_content, corner_radius=10, fg_color="white", text_color="#35353C", wraplength=650, justify="left") 
        overview_lbl.grid(row=0, column=0, pady=(0, 20), sticky="nsew")
        self.example_img = Utility.load_image("example.jpg", (650, 245))
        self.example_img_lbl = Label(overview_text, image=self.example_img)
        self.example_img_lbl.grid(row=1, column=0, pady=(20, 0))

        self.overview_frame = content_frame

#   Create the AI section     
    def create_ai(self, parent):
        content_frame = ctk.CTkFrame(parent, bg_color=LIGHT_COLOUR, fg_color=LIGHT_COLOUR, corner_radius=20)
        content_frame.grid(row=2, column=0, pady=(20,30), padx=30, sticky="nsew")
        content_frame.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_rowconfigure(1, weight=1)
        
        input_frame = ctk.CTkFrame(content_frame, bg_color="white", fg_color="white", corner_radius=20)
        input_frame.grid(row=0, column=0, padx=40, sticky="nsew")
        input_frame.grid_columnconfigure(0, weight=1)
        intro_lbl = ctk.CTkLabel(input_frame, text="AI response:", font=("Calibri light", 20), corner_radius=10, text_color="black")
        intro_lbl.grid(column=0, row=0, pady=(10,5))
        desc_lbl = ctk.CTkLabel(input_frame, text="Enter any item you want to recycle and Gemini AI will attempt to give you a detailed disposal guide. Please note that responses may be inaccurate", font=("Calibri light", 15), corner_radius=10, text_color="black", wraplength=500)
        desc_lbl.grid(column=0, row=1)
        input_lbl = ctk.CTkLabel(input_frame, text="Enter your item", font=("Calibri light", 15), corner_radius=10, text_color="black")
        input_lbl.grid(column=0, row=2, pady=(5,10))
        
        self.item_entry = ctk.CTkEntry(input_frame, font=("Calibri light", 10), corner_radius=10, text_color="black", fg_color=LIGHT_COLOUR, width=300)
        self.item_entry.grid(column=0, row=4)
        
        submit_button = ctk.CTkButton(input_frame, text="Submit", font=("Calibri light", 15), corner_radius=10, command=lambda: self.get_response(self.item_entry.get()), text_color="black", fg_color="#40d24e")
        submit_button.grid(column=0, row=5, pady=10)
        
        output_frame = ctk.CTkFrame(content_frame, bg_color="white", fg_color="white", corner_radius=20)
        output_frame.grid(row=1, column=0, padx=40, sticky="nsew")
        output_frame.grid_columnconfigure(0, weight=1)
        output_frame.grid_rowconfigure(0, weight=1)
        self.outputlbl = ctk.CTkTextbox(output_frame, font=("Calibri light", 15), corner_radius=10, fg_color="white", text_color="#35353C", wrap="word")
        self.outputlbl.grid(row=0, column=0, pady=(0, 20), sticky="nsew")
        self.outputlbl.configure(state="disabled")

        self.ai_frame = content_frame

#   Get the response from the AI
    def get_response(self, item):
        GOOGLE_API_KEY = "AIzaSyCSvHr9B3427DTTLQ1ZfW1resmHEanGb9g"
        gai.configure(api_key=GOOGLE_API_KEY)
        model = gai.GenerativeModel('gemini-1.5-pro')
        response = model.generate_content(f"{self.data["custom"]["prompt"]} the item is {item}")
        self.outputlbl.configure(state="normal")
        self.outputlbl.delete("0.0", "end")
        self.outputlbl.insert("0.0", response.text)
        self.outputlbl.configure(state="disabled")
        

# class for the map screen
class MapScreen(Frame):
    def __init__(self, parent, sidebar):
        super().__init__(parent, bg=LIGHT_COLOUR)
        self.grid_columnconfigure(0, weight=1)
        self.parent = parent
        self.sidebar = sidebar
        self.radius = 2000  # 2 km radius for searching
        self.content()

#   Create the content of the map screen
    def content(self):
        title_frame = ctk.CTkFrame(self, bg_color=LIGHT_COLOUR, fg_color="#008033", corner_radius=8)
        title_frame.grid(row=0, column=0, pady=(15, 40), padx=15, sticky="w")

        self.icon_img = Utility.load_image("map_icon.png", (50, 50))
        img_lbl = Label(title_frame, image=self.icon_img, bg="#008033")
        img_lbl.grid(column=0, row=0, rowspan=2, padx=15)

        title_lbl = Label(title_frame, text="Interactive map", font=("Calibri light", 25), bg="#008033", fg="white")
        title_lbl.grid(column=1, row=0, sticky="sw")

        title_desc_lbl = Label(title_frame, text="Find nearby recycling centers", font=("Calibri light", 15), bg="#008033", fg="white")
        title_desc_lbl.grid(column=1, row=1, sticky="nw", pady=(0, 8), padx=(0, 15))
  
        if session.user_details["username"] == "Anonymous":
            try:
                self.sidebar.another_button.grid_forget()
            except:
                pass
            self.get_address()
        else:
            self.create_content()

#   Get address info and create the map
    def create_content(self):
        self.content_frame = ctk.CTkFrame(self, bg_color=LIGHT_COLOUR, fg_color=LIGHT_COLOUR, corner_radius=20)
        self.content_frame.grid(row=1, column=0, pady=(10,20), padx=20, sticky="nsew")
        self.content_frame.grid_columnconfigure(1, weight=1)
        self.map_frame = ctk.CTkFrame(self.content_frame, bg_color="white", fg_color="white", corner_radius=20, width=700, height=600)
        self.map_frame.grid(row=0, column=0, padx=(20,0), sticky="nsew")
        
        self.list_frame = ctk.CTkScrollableFrame(self.content_frame, bg_color="white", fg_color="white", corner_radius=20)
        self.list_frame.grid(row=0, column=1, padx=(0,20), sticky="nsew")
        
        self.create_map()
        self.geocode_address()
        self.places_list()

#   Get the user's address if not logged in    
    def get_address(self):
        self.address_frame = ctk.CTkFrame(self, bg_color="white", fg_color="white", corner_radius=20)
        self.address_frame.grid(row=2, column=0, columnspan=2)
        self.address_frame.grid_columnconfigure(0, weight=1)
        address_lbl = ctk.CTkLabel(self.address_frame, text="Please enter your address to view nearby recycling centers", font=("Calibri light", 20), corner_radius=10, text_color="black")
        address_lbl.grid(column=0, row=1, pady=10)
        
        self.address_entry  = AutoComplete(self.address_frame).entry
        
        submit_button = ctk.CTkButton(self.address_frame, text="Submit", font=("Calibri light", 15), corner_radius=10, command=lambda: self.update_address(self.address_entry.get()), text_color="black", fg_color="#40d24e", height=35)
        submit_button.grid(column=0, row=4, pady=10)

#   Update the user's address when entered
    def update_address(self, address):
        valid, address = Utility.check_address(address)
        if valid == True:
            session.user_details["address"] = address
            self.loading_screen = LoadingScreen(self.parent)
            self.loading_screen.grid(row=0, column=0, sticky="nsew")
            self.address_frame.destroy()
            self.create_content() 
            self.sidebar.another_button.grid(row=0, column=0, sticky="ew")
            self.loading_screen.destroy()
        else:
            messagebox.showinfo("Error", "Address not found, please try again.")

#   Create the map
    def create_map(self):
        self.map = TkinterMapView(self.map_frame, width=700, height=600)
        self.map.grid(row=0, column=0, sticky="nsew")

        self.places = []

#   Geocode the user's address and set a marker on the map
    def geocode_address(self):
        api_key = "AIzaSyBytlVveIZV4hPPZu6u4bgeIkQ_O-5kukU"
        geocode_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={session.user_details["address"]}&key={api_key}"
        response = requests.get(geocode_url)
        data = response.json()

        location = data['results'][0]['geometry']['location']
        self.lat, self.lng = location['lat'], location['lng']
        self.map.set_position(self.lat, self.lng)
        self.map.set_zoom(14)
        self.map.set_marker(self.lat, self.lng, session.user_details["address"])
        self.fetch_recycling_centers(self.lat, self.lng)

#   Fetch the recycling centers near the user's address
    def fetch_recycling_centers(self, lat, lng):
        api_key = "AIzaSyBytlVveIZV4hPPZu6u4bgeIkQ_O-5kukU"
        places_url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lng}&radius={self.radius}&keyword=recycling&key={api_key}"
        response = requests.get(places_url)
        places = response.json().get('results', [])
        self.map.set_marker(lat, lng, session.user_details["address"])

        for place in places:
            self.name = place['name']
            lat = place['geometry']['location']['lat']
            lng = place['geometry']['location']['lng']
            self.places.append((place))

            self.place_details(place)
            self.map.set_marker(lat, lng, self.name, command=lambda marker, names=place: self.open_list(names))

#   Get the details of the recycling center
    def place_details(self, place):
        api_key = "AIzaSyBytlVveIZV4hPPZu6u4bgeIkQ_O-5kukU"  # Replace with your Google API Key
        details_url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place['place_id']}&key={api_key}"
        response = requests.get(details_url)
        self.phone = response.json().get("result", "N/A").get("formatted_phone_number")
        self.details = response.json().get("result", {})
        
#   Open the tab of individual recycling centers to see additional info
    def open_list(self, name):
        for key, value in self.detail_places.items():
            if name["name"] == key:
                value.after(10, self.list_frame._parent_canvas.yview_moveto, (value.winfo_y() / self.list_frame._parent_canvas.winfo_height()))
                self.show_place_info(value)

#   List the recycling centers
    def places_list(self):
        self.detail_places = {}
        if not self.places and self.radius == 2000:
            self.radius = 4000
            self.fetch_recycling_centers(self.lat, self.lng)
        elif not self.places and self.radius == 4000:
            messagebox.showinfo("No Results", "No recycling centers found in the vicinity.")
            return
        for place in self.places:
            self.place_details(place)
            place_frame = ctk.CTkFrame(self.list_frame, bg_color="white", fg_color="white", border_width=1, corner_radius=10)
            place_frame.grid(row=self.places.index(place), column=0, sticky="ew", padx=(0,20), pady=5)
            place_btn = ctk.CTkButton(place_frame, text=place["name"], font=("Calibri light", 15), corner_radius=5, fg_color="white", hover_color="#eaeaea", text_color=DARK_COLOUR, command=lambda p=place_frame: self.show_place_info(p), anchor="w")
            place_btn.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
            formatted_hours = "\n".join([entry.replace('\u202f', ' ').replace('\u2009', ' ').replace('\u2013', '-') for entry in self.details.get('opening_hours', {}).get('weekday_text', [])])
            place_details = f"Name: {self.details["name"]}\n\nAddress: {self.details["formatted_address"]}\n\nPhone Number: {self.phone}\n\nRating: {place["rating"]}\n\nOpening hours:\n{formatted_hours}"
            place_details_lbl = ctk.CTkLabel(
                place_frame,
                text=place_details,
                font=("Calibri light", 12),
                fg_color="white",
                text_color="#35353C",
                wraplength=200,
                anchor="w",
                justify="left"
            )
            place_frame.place_details_lbl = place_details_lbl
            self.detail_places[place["name"]] = place_frame
            
#   Show the details of the recycling center
    def show_place_info(self, frame):
        if frame.place_details_lbl.winfo_ismapped():
            frame.place_details_lbl.grid_forget()
        else:
            frame.place_details_lbl.grid(row=1, column=0, padx=(5,15), pady=(0,5), sticky="w")


# class for loading screen when fetching recycling center data
class LoadingScreen(Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=DARK_COLOUR)
        loading_label = Label(self, text="Please wait\n\nLoading...", font=("Arial", 30), bg=DARK_COLOUR, fg="white")
        loading_label.pack(expand=True)


# class for the quiz screen
class QuizScreen(Frame):
    def __init__(self, root):
        super().__init__(root, bg=LIGHT_COLOUR)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        title_frame = ctk.CTkFrame(self, bg_color=LIGHT_COLOUR, fg_color="#008033", corner_radius=8)
        title_frame.grid(row=0, column=0, pady=(15, 40), padx=15, sticky="w")
        
        self.icon_img = Utility.load_image("quiz_icon.png", (50, 50))
        img_lbl = Label(title_frame, image=self.icon_img, bg="#008033")
        img_lbl.grid(column=0, row=0, rowspan=2, padx=15)

        title_lbl = Label(title_frame, text="Recycling quiz", font=("Calibri light", 25), bg="#008033", fg="white")
        title_lbl.grid(column=1, row=0, sticky="sw")

        title_desc_lbl = Label(title_frame, text="Test your knowledge of Auckland Council's disposal guidelines!", font=("Calibri light", 15), bg="#008033", fg="white")
        title_desc_lbl.grid(column=1, row=1, sticky="nw", pady=(0, 8), padx=(0, 15))

        self.content_frame = ctk.CTkFrame(self, bg_color=LIGHT_COLOUR, fg_color=LIGHT_COLOUR, corner_radius=20)
        self.content_frame.grid(row=1, column=0, pady=(10,40), padx=40, sticky="nsew")
        self.content_frame.grid_columnconfigure(0, weight=1)

        self.start_quiz()

#   Start the quiz
    def start_quiz(self):
        self.start_frame = ctk.CTkFrame(self.content_frame, bg_color=LIGHT_COLOUR, fg_color="white", corner_radius=20)
        self.start_frame.grid(row=0, column=0)
        self.start_frame.grid_columnconfigure(0, weight=1)
        self.message_lbl = Label(self.start_frame, text="", font=("Calibri light", 20), bg="white", fg="#35353C", wraplength=600, justify="center")
        self.message_lbl.grid(row=0, column=0, pady=20, sticky="nsew", padx=20)
        played = self.check_played()
        if played:
            return
        self.start_btn = ctk.CTkButton(self.start_frame, text="Start Quiz", font=("Calibri light", 20), corner_radius=10, fg_color="#217346", hover_color="#247f4c", text_color="white", command=self.start_questions, height=45, width=200)
        self.start_btn.grid(row=2, column=0, pady=20)
    
#   Check if the user has already played the quiz
    def check_played(self):
        if str(datetime.now().date()) == session.user_details["quiz_date"]:
            self.message_lbl.configure(text="You have already played the quiz today. Come back tomorrow to play again!")
            return True
        else:
            if session.user_details["username"] == "Anonymous":
                self.message_lbl.configure(text="Welcome to the recycling quiz! \nClick the button below to start the quiz.")
                self.anon_message_lbl = Label(self.start_frame, text="You are currently not signed in, so you will not gain any points.", font=("Calibri light", 15), bg="white", fg="#35353C", wraplength=600, justify="center")
                self.anon_message_lbl.grid(row=1, column=0, pady=20, padx=20, sticky="nsew")
            else:
                self.message_lbl.configure(text="Welcome to the recycling quiz! \nClick the button below to start the quiz.")

#   Start the quiz questions
    def start_questions(self):
        self.start_frame.grid_forget()
        self.start_btn.grid_forget()
        self.quiz_frame = Frame(self.content_frame, bg="white")
        self.quiz_frame.grid(row=0, column=0, padx=(20,0), sticky="new")
        self.quiz_frame.grid_columnconfigure(0, weight=1)
        self.questions = self.load_questions()

        self.correct_answers = 0
        self.question_number = 0
        self.quiz()

#   Load the questions from the JSON file
    def load_questions(self):
        with open(os.path.join(DIRECTORY, "questions.json"), "r") as file:
            questions = json.load(file)
            return questions
        
#   Start the quiz
    def quiz(self):
        self.selected_questions = []
        for i in range(5):
            question = random.choice(list(self.questions.keys()))
            if question not in self.selected_questions:
                self.selected_questions.append(self.questions[question])
        self.create_question()

#   Create the question
    def create_question(self):
        if self.question_number <= 4:
            question_lbl = Label(self.quiz_frame, text=f"Question {self.question_number+1}/5\n\n{self.selected_questions[self.question_number]["question"]}", font=("Calibri light", 18), bg="white", fg="#35353C", wraplength=600, justify="center")
            question_lbl.grid(row=0, column=0, pady=(20, 10), sticky="nsew")
            answers_frame = Frame(self.quiz_frame, bg="white")
            answers_frame.grid(row=1, column=0, pady=(10, 0), sticky="nsew")
            answers_frame.grid_columnconfigure(0, weight=1)
            count = 0
            self.buttons = {}
            for answer in ("a", "b", "c", "d"):
                answer_btn = ctk.CTkButton(answers_frame, text=self.selected_questions[self.question_number][answer], font=("Calibri light", 18), corner_radius=10, fg_color="white", hover_color="#247f4c", text_color="#35353c", text_color_disabled="#35353c", border_width=1, command=lambda a=answer: self.check_answer(a), height=45, width=200)
                answer_btn.grid(row=count, column=0, pady=(5, 0), sticky="ew")
                count += 1
                self.buttons[answer] = answer_btn
                
            self.correct_answer_lbl = Label(self.quiz_frame, text="", font=("Calibri light", 20), bg="white", fg="#35353C")
        else:
            self.quiz_end()

#   Check the answer
    def check_answer(self, answer):
        if answer == self.selected_questions[self.question_number]["answer"]:
            self.correct_answers += 1
            self.correct_answer_lbl.configure(text="Correct!")
            self.correct_answer_lbl.grid(row=2, column=0, pady=(20, 10), sticky="nsew")
            self.buttons[answer].configure(fg_color="#40d24e")
            for button in self.buttons:
                self.buttons[button].configure(state="disabled")
        else:
            self.correct_answer_lbl.configure(text=f"Incorrect!")
            self.correct_answer_lbl.grid(row=2, column=0, pady=(20, 10), sticky="nsew")
            self.buttons[self.selected_questions[self.question_number]["answer"]].configure(fg_color="#40d24e")
            self.buttons[answer].configure(fg_color="#ea3636")
            for button in self.buttons:
                self.buttons[button].configure(state="disabled")
        next_btn = ctk.CTkButton(self.quiz_frame, text="Next", font=("Calibri light", 20), corner_radius=10, fg_color="#217346", hover_color="#247f4c", text_color="white", command=lambda:self.next_question(), height=45, width=200)
        next_btn.grid(row=3, column=0, pady=(10,0))

#   Move to the next question
    def next_question(self):
        self.question_number += 1
        for widget in self.quiz_frame.winfo_children():
            widget.destroy()
        self.quiz()

#   End the quiz
    def quiz_end(self):
        self.start_frame.grid(row=0, column=0)
        try:
            last_quiz_date = datetime.strptime(session.user_details["quiz_date"], "%Y-%m-%d")
        except:
            # If the quiz_date is invalid, initialize it to a date that ensures a reset
            last_quiz_date = datetime.now() - timedelta(days=2)
        if last_quiz_date.date() == (datetime.now() - timedelta(days=1)).date():
            session.user_details["streak"] += 1
        else:
            session.user_details["streak"] = 1

        session.user_details["quiz_date"] = str(datetime.now().date())
        session.user_details["points"] += self.correct_answers
        if session.user_details["username"] == "Anonymous":
            self.message_lbl.configure(text=f"Quiz complete! You scored {self.correct_answers} out of 5!")
        else:
            self.message_lbl.configure(text=f"Quiz complete! You scored {self.correct_answers} out of 5!\n\nYou have gained {self.correct_answers} EcoPoints.\n\n You have a total of {session.user_details["points"]} EcoPoints\n\nCome back tomorrow to play again.")
        self.quiz_frame.grid_forget()
        Utility.update_file(session.user_details["username"])

#   class to view user's points and milestones
class PointsScreen(Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=LIGHT_COLOUR)
        self.parent = parent
        self.initialize_points()
        self.images = []

        title_frame = ctk.CTkFrame(self, bg_color=LIGHT_COLOUR, fg_color="#008033", corner_radius=8)
        title_frame.grid(row=0, column=0, pady=(15, 40), padx=15, sticky="w")
        
        self.icon_img = Utility.load_image("collection_icon.png", (50, 50))
        img_lbl = Label(title_frame, image=self.icon_img, bg="#008033")
        img_lbl.grid(column=0, row=0, rowspan=2, padx=15)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        #self.grid_rowconfigure(1, weight=1)
        
        title_lbl = Label(title_frame, text="EcoPoints", font=("Calibri light", 25), bg="#008033", fg="white")
        title_lbl.grid(column=1, row=0, sticky="sw")

        title_desc_lbl = Label(title_frame, text="Get EcoPoints to unlocked badges", font=("Calibri light", 15), bg="#008033", fg="white")
        title_desc_lbl.grid(column=1, row=1, sticky="nw", pady=(0, 8), padx=(0, 15))
        
        self.levels_frame = ctk.CTkFrame(self, bg_color=LIGHT_COLOUR, fg_color=LIGHT_COLOUR, corner_radius=20)
        self.levels_frame.grid(row=1, column=0, pady=(10,40), padx=40, sticky="nsew")
        self.levels_frame.grid_columnconfigure(0, weight=1)

        self.report_frame = ctk.CTkFrame(self, bg_color=LIGHT_COLOUR, fg_color=LIGHT_COLOUR, corner_radius=20)
        self.report_frame.grid(row=1, column=1, pady=(20,40), padx=40, sticky="nsew")
        self.report_frame.grid_columnconfigure(0, weight=1)

        self.create_levels(self.levels_frame)
        self.create_report()
    
#   Initialize the user's points and streak
    def initialize_points(self):
        self.user_data = session.user_details
        self.user = session.user_details["username"]
        self.points = session.user_details["points"]
        self.streak = session.user_details["streak"]
        self.date = session.user_details["report_date"]

#   Check if the user's points have been updated
    def check_update(self):
        if self.user != session.user_details["username"] or self.points != session.user_details["points"] or self.streak != session.user_details["streak"]:
            self.update_points()

#   Update the user's points and streak
    def update_points(self):
        self.user_data = session.user_details
        self.user = session.user_details["username"]
        self.points = session.user_details["points"]
        self.streak = session.user_details["streak"]
        self.date = session.user_details["report_date"]
        for widget in self.levels_frame.winfo_children():
            widget.destroy()
        self.create_levels(self.levels_frame)

#   Create the levels section to show points related information
    def create_levels(self, parent):
        line_lbl = ctk.CTkLabel(parent, text="____________________________________________________", font=("Calibri light", 15), corner_radius=10, fg_color=LIGHT_COLOUR, text_color="#35353C")
        line_lbl.grid(row=0, column=0, sticky="w")

        level_lbl = ctk.CTkLabel(parent, text=session.user_details["username"], font=("Calibri light", 25, "bold"), corner_radius=10, fg_color=LIGHT_COLOUR, text_color="#35353C")
        level_lbl.grid(row=0, column=0, pady=(0,20), padx=20, sticky="w")
        award_frame = Frame(parent, bg=LIGHT_COLOUR)
        award_frame.grid(row=0, column=0, sticky="w", pady=(69,0))

        badge, medal = self.get_awards()
        if badge is not None:
            self.badge_img = Utility.load_image(badge, (50, 50))
            badge_lbl = Label(award_frame, image=self.badge_img, background=LIGHT_COLOUR)
            badge_lbl.grid(row=0, column=0, padx=10)
        if medal is not None:
            self.medal_img = Utility.load_image(medal, (50, 50))
            medal_lbl = Label(award_frame, image=self.medal_img, background=LIGHT_COLOUR)
            medal_lbl.grid(row=0, column=1, padx=10)

        self.find_level()

        self.level_lbl = ctk.CTkLabel(parent, text=f"Level {int(self.level)}", font=("Calibri light", 25), corner_radius=10, fg_color=LIGHT_COLOUR, text_color="#35353C")
        self.level_lbl.grid(row=3, column=0, pady=(30,0), sticky="w", padx=90)

        self.progress = ctk.CTkProgressBar(parent, fg_color="#40d24e", bg_color="#CDE1CD", corner_radius=8, height=20, width=250)
        self.progress.set(self.progress_pts/100)
        self.progress.grid(row=4, column=0, pady=5, sticky="w", padx=10)

        points_lbl = ctk.CTkLabel(parent, text=f"Points: {int(session.user_details["points"])}", font=("Calibri light", 20), corner_radius=10, fg_color=LIGHT_COLOUR, text_color="#35353C")
        points_lbl.grid(row=5, column=0, pady=(5,20), sticky="w")

        streak_lbl = ctk.CTkLabel(parent, text=f"Streak: {session.user_details["streak"]}", font=("Calibri light", 20), corner_radius=10, fg_color=LIGHT_COLOUR, text_color="#35353C")
        streak_lbl.grid(row=6, column=0, pady=(5,20), sticky="w")

#   Get the awards based on the user's points and streak
    def get_awards(self):
        if self.points >= 100 and self.points < 200:
            badge = "badge_bronze.png"
        elif self.points >= 200 and self.points < 300:
            badge = "badge_silver.png"
        elif self.points >= 300:
            badge = "badge_gold.png"
        else:
            badge = None
        if self.streak >= 5 and self.streak < 10:
            medal = "medal_bronze.png"
        elif self.streak >= 10 and self.streak < 100:
            medal = "medal_silver.png"
        elif self.streak >= 100:
            medal = "medal_gold.png"
        else:
            medal = None
        return badge, medal

#   Find the user's level based on their points
    def find_level(self):
        self.total_points = session.user_details["points"]
        if  self.total_points <= 300:
            self.level = self.total_points // 100
        elif self.total_points != 0:
            self.level = 3
        self.progress_pts = self.total_points % 100

#   Create the report section for the user to submit their weekly recycling reflection
    def create_report(self):
        report_lbl = ctk.CTkLabel(self.report_frame, text="Recycling Reflection", font=("Calibri light", 20, "bold"), corner_radius=10, text_color="black")
        report_lbl.grid(row=0, column=0, pady=(10,5))
        note_lbl = ctk.CTkLabel(self.report_frame, text="Complete your weekly recycling reflection for EcoPoints!", font=("Calibri light", 20), corner_radius=10, text_color="black")
        note_lbl.grid(row=1, column=0, pady=(5,10))

        report_frame = ctk.CTkFrame(self.report_frame, bg_color=LIGHT_COLOUR, fg_color=LIGHT_COLOUR, corner_radius=20)
        report_frame.grid(row=2, column=0, pady=(10,0), padx=20, sticky="nsew")
        report_frame.grid_columnconfigure(0, weight=1)

        self.check_date()
        
#       Question 1: Did you recycle this week? (Yes/No)
        question1_lbl = ctk.CTkLabel(report_frame, text="Did you recycle this week?", font=("Calibri light", 20), corner_radius=10, text_color="black")
        question1_lbl.grid(row=0, column=0, pady=(10, 5), padx=20, sticky="w")

        question1_combo = ctk.CTkComboBox(report_frame, font=("Calibri light", 15), text_color="#35353C", width=700, height=45, values= ["Yes", "No"], bg_color="white", fg_color=LIGHT_COLOUR, border_width=1, state="readonly")
        question1_combo.grid(row=1, column=0, pady=(5, 10), padx=20, sticky="w")
        question1_combo.set("Pick an option")

#       Question 2: How many items did you recycle this week?
        question2_lbl = ctk.CTkLabel(report_frame, text="How many items did you recycle this week?", font=("Calibri light", 20), corner_radius=10, text_color="black")
        question2_lbl.grid(row=2, column=0, pady=(10, 5), padx=20, sticky="w")

        question2_combo = ctk.CTkComboBox(report_frame, font=("Calibri light", 15), text_color="#35353C", width=700, height=45, values=["0-5", "6-10", "11-20", "more than 20"], bg_color="white", fg_color=LIGHT_COLOUR, border_width=1, state="readonly")
        question2_combo.grid(row=3, column=0, pady=(5, 10), padx=20, sticky="w")
        question2_combo.set("Pick an option")

#        Question 3: Rate your recycling this week (1-10)
        question3_lbl = ctk.CTkLabel(report_frame, text="How well do you think you recycled this week?", font=("Calibri light", 20), corner_radius=10, text_color="black")
        question3_lbl.grid(row=4, column=0, pady=(10, 5), padx=20, sticky="w")

        self.slider_lbl = ctk.CTkLabel(report_frame, text="Rating: 5", font=("Calibri light", 15), corner_radius=10, text_color="black")
        self.slider_lbl.grid(row=6, column=0, pady=(5, 10), padx=20, sticky="w")

        self.question3_slider = ctk.CTkSlider(report_frame, width=700, border_width=0, height=45, from_=1, to=10, command=self.update_slider)
        self.question3_slider.grid(row=5, column=0, pady=(5, 0), padx=20, sticky="w")

        submit_btn = ctk.CTkButton(report_frame, text="Submit", font=("Calibri light", 15), corner_radius=10, fg_color="#217346", hover_color="#247f4c", text_color="white", height=45, width=200, command=lambda: self.submit_report(question1_combo.get(), question2_combo.get(), int(self.question3_slider.get())))
        submit_btn.grid(row=7, column=0, pady=(10, 0), padx=20)

#   Update the slider value
    def update_slider(self, value):
        self.slider_lbl.configure(text=f"Rating: {int(value)}")

#   Check if the user has already submitted their report for the week
    def check_date(self):
        try:
            year1, week1, _ = datetime.strptime(session.user_details["report_date"], "%Y-%m-%d").isocalendar()
        except:
            year1, week1, _ = (datetime.now()-timedelta(days=7)).isocalendar()
        year2, week2, _ = datetime.now().isocalendar()

        if year1 == year2 and week1 == week2:
            self.message_lbl = ctk.CTkLabel(self.report_frame, text="You have already submitted your report for this week.\nCome back next week!", font=("Calibri light", 18), corner_radius=10, text_color="black")
            self.message_lbl.grid(row=2, column=0, pady=(10,0), padx=20, sticky="nsew")
            return

#   Submit the user's report and calculate the points gained
    def submit_report(self, q1, q2, q3):
        if q1 == "Pick an option" or q2 == "Pick an option" or q3 == "":
            messagebox.showinfo("Error", "Please answer all questions.")
            return
        else:
            gained_points = 0
            if q1 == "Yes":
                gained_points += 5
            if q2 == "0-5":
                gained_points += 5  
            elif q2 == "6-10":
                gained_points += 10
            elif q2 == "11-20":
                gained_points += 15
            else:
                gained_points += 20
            gained_points += q3

            session.user_details["points"] += gained_points
            session.user_details["report_date"] = str(datetime.now().date())
            Utility.update_file(session.user_details["username"])
            messagebox.showinfo("Success", f"Report submitted! You have gained {gained_points} EcoPoints.")
            for widget in self.levels_frame.winfo_children():
                widget.destroy()
            for widget in self.report_frame.winfo_children():
                widget.destroy()
            self.create_levels(self.levels_frame)
            self.create_report()


#  class to view user profile      
class ProfileScreen(Frame):
    def __init__(self, parent, app, root):
        super().__init__(parent, bg=LIGHT_COLOUR)
        self.parent = parent
        self.root = root
        self.app = app

        self.load_account()
        self.grid_columnconfigure(0, weight=1)

        title_frame = ctk.CTkFrame(self, bg_color=LIGHT_COLOUR, fg_color="#008033", corner_radius=8)
        title_frame.grid(row=0, column=0, pady=(15, 40), padx=15, sticky="w")
        
        self.icon_img = Utility.load_image("profile_icon.png", (50, 50))
        img_lbl = Label(title_frame, image=self.icon_img, bg="#008033")
        img_lbl.grid(column=0, row=0, rowspan=2, padx=15)
        
        title_lbl = Label(title_frame, text="Account", font=("Calibri light", 25), bg="#008033", fg="white")
        title_lbl.grid(column=1, row=0, sticky="sw")
        title_desc_lbl = Label(title_frame, text="Manage your account", font=("Calibri light", 15), bg="#008033", fg="white")
        title_desc_lbl.grid(column=1, row=1, sticky="nw", pady=(0, 8), padx=(0, 15))

        self.content_frame = Frame(self, bg=LIGHT_COLOUR)
        self.content_frame.grid(row=1, column=0)

        self.content()

#   Load the user's account details
    def content(self):
        username_lbl = ctk.CTkLabel(self.content_frame, text=f"Username: ", font=("Calibri light", 15), corner_radius=10, text_color="#35353C")
        username_lbl.grid(row=0, column=0, sticky="w")
        
        self.username_entry = ctk.CTkEntry(self.content_frame, font=("Calibri light", 15), corner_radius=20, fg_color="#CDE1CD", text_color="#35353C", width=700, border_width=0, height=45)
        self.username_entry.grid(row=1, column=0)
        self.username_entry.insert(0, self.username)
        self.username_entry.configure(state="disabled")
        
        self.edit_img = Utility.load_image("edit.png", (22, 22))
        username_edit_btn = Button(self.content_frame, image=self.edit_img, command=lambda: [self.username_entry.configure(state="normal"), self.username_entry.focus()], height=22, width=22, border=0, relief=FLAT, bg="#CDE1CD")
        username_edit_btn.grid(row=1, column=0, sticky="nse", padx=(0, 15), pady=3)

        password_lbl = ctk.CTkLabel(self.content_frame, text=f"Password: ", font=("Calibri light", 15), corner_radius=10, text_color="#35353C")
        password_lbl.grid(row=2, column=0, sticky="w", pady=(25,0))
        
        self.password_entry = ctk.CTkEntry(self.content_frame, font=("Calibri light", 15), corner_radius=20, fg_color="#CDE1CD", text_color="#35353C", width=700, border_width=0, height=45)
        self.password_entry.grid(row=3, column=0)
        self.password_entry.insert(0, self.password)
        self.password_entry.configure(state="disabled")
        
        password_edit_btn = Button(self.content_frame, image=self.edit_img, command=lambda: [self.password_entry.configure(state="normal"), self.password_entry.focus()], height=22, width=22, border=0, relief=FLAT, bg="#CDE1CD")
        password_edit_btn.grid(row=3, column=0, sticky="e", padx=(0, 15), pady=3)

        address_lbl = ctk.CTkLabel(self.content_frame, text=f"Address: ", font=("Calibri light", 15), corner_radius=10, text_color="#35353C")
        address_lbl.grid(row=4, column=0, sticky="w", pady=(25,0))
        
        self.address_entry = ctk.CTkEntry(self.content_frame, font=("Calibri light", 15), corner_radius=20, fg_color="#CDE1CD", text_color="#35353C", width=700, border_width=0, height=45)
        self.address_entry.grid(row=5, column=0)
        self.address_entry.insert(0, self.address)
        self.address_entry.configure(state="disabled")
        
        address_edit_btn = Button(self.content_frame, image=self.edit_img, command=lambda: [self.address_entry.configure(state="normal"), self.address_entry.focus()], height=22, width=22, border=0, relief=FLAT, bg="#CDE1CD")
        address_edit_btn.grid(row=5, column=0, sticky="e", pady=3, padx=(0, 15))

        btn_frame = ctk.CTkFrame(self.content_frame, bg_color=LIGHT_COLOUR, fg_color=LIGHT_COLOUR, corner_radius=20)
        btn_frame.grid(row=6, column=0, pady=(20, 0))

        update_btn = ctk.CTkButton(btn_frame, text="Change details", font=("Calibri light", 20), corner_radius=10, fg_color="#217346", hover_color="#247f4c", text_color="white", command=lambda: self.update_account(self.username_entry.get(), self.password_entry.get(), self.address_entry.get()), height=45, width=450)
        update_btn.grid(row=0, column=0, pady=(20,0), columnspan=2)

        signout_btn = ctk.CTkButton(btn_frame, text="Sign Out", font=("Calibri light", 20), corner_radius=10, fg_color="#217346", hover_color="#247f4c", text_color="white", command=self.sign_out, height=45, width=200)
        signout_btn.grid(row=1, column=0, pady=(5,0), sticky="e", padx=(0, 5))

        delete_btn = ctk.CTkButton(btn_frame, text="Delete Account", font=("Calibri light", 20), corner_radius=10, fg_color="#217346", hover_color="#247f4c", text_color="white", command=self.delete_account, height=45, width=200)
        delete_btn.grid(row=1, column=1, pady=(5,0), sticky="w", padx=(5, 0))

#   Update the user's account details
    def update_account(self, username, password, address):
        if (session.user_details["username"] != username and username != ""
            or session.user_details["password"] != password and password != ""
            or session.user_details["address"] != address and address != ""):
            self.original_username = session.user_details["username"]

            valid, addresses = Utility.check_address(address)
            if valid == False:
                messagebox.showinfo("Error", "Address not found, please try again.")
                return
            
            session.user_details = {
                "username": username,
                "password": password,
                "address": address,
                "points": session.user_details["points"],
                "quiz_date": session.user_details["quiz_date"],
                "report_date": session.user_details["report_date"],
                "streak": session.user_details["streak"]
            }
            Utility.update_file(self.original_username)
            self.disable_entry()
            messagebox.showinfo("Success", "Account updated successfully")

        else:
            messagebox.showinfo("Error", "No changes were made")
            for widget in self.content_frame.winfo_children():
                widget.destroy()
            self.content()
            self.disable_entry()

#   Disable the entry fields
    def disable_entry(self):
        self.username_entry.configure(state="disabled")
        self.password_entry.configure(state="disabled")
        self.address_entry.configure(state="disabled")

#   Sign out of the account
    def sign_out(self):
        self.clear_session()

#   Delete the user's account
    def delete_account(self):
        accounts = Utility.read_accounts()
        updated_accounts = []

        # Filter out the account that matches the username in the session
        for account in accounts:
            if Encryption.decrypt(account["username"]) != session.user_details["username"]:
                updated_accounts.append(account)

        # Write the updated accounts list back to the JSON file
        with open(os.path.join(DIRECTORY, "accounts-data.json"), "w") as file:
            json.dump(updated_accounts, file, indent=4)
        self.clear_session()

#   Clear the session details
    def clear_session(self):
        session.user_details = None
        self.app.sidebar_frame.destroy()
        self.app.main_frame.destroy()
        Account(self.root)

#   Load the user's account details
    def load_account(self):
        user_data = session.user_details
        self.username = user_data["username"]
        self.password = user_data["password"]
        self.address = user_data["address"]

if __name__ == "__main__":
    App()