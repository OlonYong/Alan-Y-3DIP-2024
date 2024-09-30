from tkinter import * # Module for GUI
from tkinter import ttk, messagebox
import customtkinter as ctk # Module for custom tkinter widgets
from PIL import Image, ImageTk # Module for images
from ctypes import windll # Module for DPI awareness
import json # Module for JSON
from datetime import datetime # Module for date and time
import requests # Module for API requests
from cryptography.fernet import Fernet # Module for encryption
from details import session # Module for user details

# class to initialize the program
class Program:
    def __init__(self):
        self.root = Tk()
        self.root.title("RecycleAKL")
        self.root.geometry("1536x864")
        
#       Set DPI awareness
        windll.shcore.SetProcessDpiAwareness(1)
        scaling_factor = self.root.winfo_fpixels('1i') / 72.0
        self.root.tk.call('tk', 'scaling', scaling_factor)
        
        

#       Load custom ttk theme
        self.root.tk.call("source", r"iteration3/assets/Forest-ttk-theme-master\forest-dark.tcl")
        ttk.Style().theme_use(r'forest-dark')

        session = Data()
        Login(self.root)
        
        self.root.mainloop()

# class for login and sign up screen
class Login:
#   initialises the login screen
    def __init__(self, root):
        self.root = root
        self.images = []
        
#       Create UI
        self.content()
        
#       Ensure image loads
        self.root.after(150, self.get_frame_size)

#   Create UI
    def content(self):
#       Create content frames
        self.l_frame = ttk.Frame(self.root)
        self.r_frame = ttk.Frame(self.root)
        self.l_frame.grid(row=0, column=0, sticky="nsew")
        self.r_frame.grid(row=0, column=1, sticky="nsew")
        
#       Configure frames
        self.root.grid_columnconfigure(0, weight=42)
        self.root.grid_columnconfigure(1, weight=58)
        self.root.grid_rowconfigure(0, weight=1)
        self.r_frame.grid_propagate(False)
        self.l_frame.grid_propagate(False)
        self.l_frame.grid_columnconfigure(0, weight=1)
        
        title_frame = ttk.Frame(self.l_frame)
        title_frame.grid(pady=(30, 60))

#       Load logo image
        logo_img = Image.open(r"iteration3/assets/images\logo.png").resize((64, 50))
        logo_img = ImageTk.PhotoImage(logo_img)
        self.images.append(logo_img)
        
        logo = ttk.Label(title_frame, image=self.images[0])
        title_lbl = ttk.Label(title_frame, text="RecycleAKL", font=("Arial", 30, "bold"), foreground="#2EA53A")
        logo.grid(row=0, column=0, padx=(0, 10))
        title_lbl.grid(row=0, column=1, padx=(0, 0))

#       Create Notebook
        self.tabs = ttk.Notebook(self.l_frame)
        self.tabs.grid(row=1)

        self.signup_tab = ttk.Frame(self.tabs)
        self.signin_tab = ttk.Frame(self.tabs)
        self.signup_tab.grid(column=0)
        self.signin_tab.grid(column=2)
        self.tabs.add(self.signin_tab, text="SIGN IN")
        self.tabs.add(self.signup_tab, text="SIGN UP")
        
        self.create_signin_tab()
        self.create_signup_tab()
        
#       Create buttons
        self.error_label = ttk.Label(self.l_frame, text="", font=20)
        self.button_text = StringVar()
        self.action_button = ttk.Button(self.l_frame, textvariable=self.button_text, width=25, command=self.button_clicked, style="Accent.TButton")
        self.anonymous_button = ttk.Button(self.l_frame, text="Continue without signing in", width=25, command=lambda: self.anonymous(), style="Accent.TButton")
        self.error_label.grid(pady=(20, 0))
        self.action_button.grid(pady=(20, 0))
        self.anonymous_button.grid(pady=(20, 0))
        self.button_text.set("Sign In")
        
#       Style buttons
        style = ttk.Style()
        style.configure("Accent.TButton", font=("Arial", 16), padding=10)
        
                
#       Update button text
        self.tabs.bind('<<NotebookTabChanged>>', self.on_tab_change)
        
#   handle anonymous user
    def anonymous(self):
        session.user_details = {
            "username": "Anonymous",
            "password": "Anonymous",
            "address": "Anonymous"
        }
        self.r_frame.grid_propagate(True)
        self.l_frame.grid_propagate(True)
        for widget in self.l_frame.winfo_children():
            widget.destroy()
        for widget in self.r_frame.winfo_children():
            widget.destroy()
        AppManager(self.root)

#   Signin tab
    def create_signin_tab(self):
        self.signin_frame = ttk.Frame(self.signin_tab)
        self.signin_frame.pack()

        username_label = ttk.Label(self.signin_tab, text="Username", font=("Calibri", 16), width=30)
        self.signin_username_entry = ttk.Entry(self.signin_tab, font=("Calibri", 16), width=30)
        username_label.pack(pady=(30, 0))
        self.signin_username_entry.pack(pady=(5, 20))

        self.password_images = self.load_password_images()
        password_label = ttk.Label(self.signin_tab, text="Password", font=("Calibri", 16), width=30)
        password_label.pack()
        self.signin_password_frame = ttk.Frame(self.signin_tab)
        self.signin_password_frame.pack()
        self.signin_password_entry = ttk.Entry(self.signin_password_frame, font=("Calibri", 16), width=30, show="*")
        self.show_password = False
        self.signin_show_password_button = Button(self.signin_password_frame, image=self.password_images[0], command=lambda:self.toggle_password(), height=28, width=28, border=0, relief=FLAT)
        self.signin_password_entry.grid(row=0, pady=(5, 20), sticky="ew")
        self.signin_show_password_button.grid(row=0, pady=(5, 20), sticky="e", padx=2)

#   Load hide and show password icons
    def load_password_images(self):
        images = []
        hide_img = Image.open(r"iteration3/assets/images\hide.png").resize((30, 30))
        hide_img = ImageTk.PhotoImage(hide_img)
        images.append(hide_img)
        
        show_img = Image.open(r"iteration3/assets/images\show.png").resize((30, 30))
        show_img = ImageTk.PhotoImage(show_img)
        images.append(show_img)

        return images

#   Toggle password visibility
    def toggle_password(self):
        if self.show_password:
            self.signin_password_entry.config(show="*")
            self.signup_password_entry.config(show="*")
            self.show_password = False
            self.signup_show_password_button.config(image=self.password_images[0])
            self.signin_show_password_button.config(image=self.password_images[0])
        else:
            self.signup_password_entry.config(show="")
            self.signin_password_entry.config(show="")
            self.show_password = True
            self.signin_show_password_button.config(image=self.password_images[1])
            self.signup_show_password_button.config(image=self.password_images[1])


#   Signup Tab
    def create_signup_tab(self):
        self.signup_frame = ttk.Frame(self.signup_tab)
        self.signup_frame.pack()

        username_label = ttk.Label(self.signup_tab, text="Username", font=("Calibri", 16), width=30)
        self.signup_username_entry = ttk.Entry(self.signup_tab, font=("Calibri", 16), width=30)
        username_label.pack(pady=(30, 0))
        self.signup_username_entry.pack(pady=(5, 20))

        password_label = ttk.Label(self.signup_tab, text="Password", font=("Calibri", 16), width=30)
        password_label.pack()
        
        self.signup_password_frame = ttk.Frame(self.signup_tab)
        self.signup_password_frame.pack()
        self.signup_password_entry = ttk.Entry(self.signup_password_frame, font=("Calibri", 16), width=30, show="*")
        self.show_password = False
        self.signup_show_password_button = Button(self.signup_password_frame, image=self.password_images[0], command=lambda:self.toggle_password(), height=28, width=28, border=0, relief=FLAT)
        self.signup_password_entry.grid(row=0, pady=(5, 20), sticky="ew")
        self.signup_show_password_button.grid(row=0, pady=(5, 20), sticky="e", padx=2)
    
        address_label = ttk.Label(self.signup_tab, text="Address", font=("Calibri", 16), width=30)
        self.signup_address_entry = ttk.Entry(self.signup_tab, font=("Calibri", 16), width=30)
        address_label.pack()
        self.signup_address_entry.pack(pady=(5, 20))

#   Update button text
    def on_tab_change(self, event):
        active_tab = self.tabs.index(self.tabs.select())
        if active_tab == 0:
            self.button_text.set("Sign In")
            
        elif active_tab == 1:
            self.button_text.set("Sign Up")

#   Change notebook tabs
    def button_clicked(self):
        active_tab = self.tabs.index(self.tabs.select())
        if active_tab == 0:
            self.check_details()
        elif active_tab == 1:
            self.check_signup()

#   Size image to fit frame
    def get_frame_size(self):
        frame_width = self.r_frame.winfo_width()
        frame_height = self.r_frame.winfo_height()

        bg_img = Image.open(r"iteration3/assets/images\login_background.png").resize((frame_width, frame_height))
        bg_img = ImageTk.PhotoImage(bg_img)
        self.images.append(bg_img)
        bg_img = Label(self.r_frame, image=self.images[1], borderwidth=0)
        bg_img.grid()

#   Check if sign in details are valid
    def check_details(self):
        username = self.signin_username_entry.get()
        password = self.signin_password_entry.get()
        if username == "" or password == "":
            self.error_label.config(text="Please fill in all fields.")
            return
        try:
            with open(r"iteration3/assets/accounts-data.json", "r") as file:
                accounts = json.load(file)
            for account in accounts:
                if self.decrypt(account["username"]) == username and self.decrypt(account["password"]) == password:
                    username = self.decrypt(account["username"])
                    password = self.decrypt(account["password"])
                    address = self.decrypt(account["address"])
                    session.user_details = {
                        "username": username,
                        "password": password,
                        "address": address
                    }
                    AppManager(self.root)

            self.error_label.config(text="Invalid username or password.")
        except FileNotFoundError:
            messagebox.showinfo("Error", "No accounts found, please register an account.")
            self.tabs.select(1)
            return
        
#   Write user details into external file
    def save_details(self):
        username = self.signup_username_entry.get()
        password = self.signup_password_entry.get()
        address = self.signup_address_entry.get()
        accounts = self.read_accounts()
        with open(r"iteration3/assets/accounts-data.json", "w") as file:
            data = {"username": self.encrypt(username),
                    "password": self.encrypt(password),
                    "address": self.encrypt(address)}
            accounts.append(data)
            json.dump(accounts, file, indent=4)
        session.user_details = {
            "username": username,
            "password": password,
            "address": address
        }
        AppManager(self.root)

#   Get encryption key
    @classmethod
    def get_key(cls):
        try:
            with open(r"iteration3/assets/key.key", "rb") as file:
                key = file.read()
        except FileNotFoundError:
            key = Fernet.generate_key()
            with open(r"iteration3/assets/key.key", "wb") as file:
                file.write(key)
        return key

#   Encrypt account data
    @classmethod
    def encrypt(cls, data):
        key = cls.get_key()
        cipher = Fernet(key)
        encrypted = cipher.encrypt(data.encode()).decode()
        return encrypted

#   Decrypt account data
    @classmethod
    def decrypt(cls, data):
        key = cls.get_key()
        cipher = Fernet(key)
        decrypted = cipher.decrypt(data.encode()).decode()
        return decrypted

#   Read user details from external file
    @classmethod
    def read_accounts(cls):
        try:
            with open(r"iteration3/assets/accounts-data.json", 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return []
        
#   Check if address is valid
    @classmethod
    def check_address(cls, address):
        url = "http://163.47.222.43:80/api/v1/rr"
        parameters = {'addr': address}
        response = requests.get(url, params=parameters)
        data = response.json()
        if "address" in data:
            return True
        else:
            return False 

#   Check if sign up details are valid
    def check_signup(self):
        if self.signup_username_entry.get() == "" or self.signup_password_entry.get() == "" or self.signup_address_entry.get() == "":
            self.error_label.config(text="Please fill in all fields.")
            return False
        
        valid = self.check_address(self.signup_address_entry.get())
        if valid:
            self.save_details()

        else:
            self.error_label.config(text="Address not found, please try again.")

# class to store session details
class Data:
    user_details = None

# class to manage the app
class AppManager:
    def __init__(self, root):
        self.root = root

        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=3)

        # Sidebar and main content frames
        self.sidebar_frame = Frame(self.root) 
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")

        self.main_frame = Frame(self.root, background="#F2F7FA")
        self.main_frame.grid(row=0, column=1, sticky="nsew")
        
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.sidebar_frame.grid_columnconfigure(0, weight=1)
        self.sidebar_frame.grid_propagate(False)
        self.main_frame.grid_propagate(False)

        self.screens = {}
        self.current_screen = "CollectionScreen"

        self.sidebar = Sidebar(self.sidebar_frame, self.switch_screens, self.current_screen)

#       Create screens
        for screen in [ProfileScreen, GuideScreen, CollectionScreen]:
            self.create_screen(screen)

#   Create screens
    def create_screen(self, screen):
        if screen == ProfileScreen:
            screen_instance = screen(self.main_frame, self, self.root)
        else:
            screen_instance = screen(self.main_frame)
        name = screen.__name__
        self.screens[name] = screen_instance
        screen_instance.grid(row=0, column=0, sticky="nsew")
        
#   Switch between screens
    def switch_screens(self, screen_name):
        self.show_screen(screen_name)

#   Show the selected screen
    def show_screen(self, screen_name):
        if screen_name == "ProfileScreen":
            if session.user_details["username"] == "Anonymous":
                messagebox.showinfo("Error", "Please sign in to access this feature.")
                Login(self.root)
        screen = self.screens[screen_name]
        screen.tkraise()
        self.current_screen = screen_name  # Store the screen name, not the instance
        # Disable the button for the current screen
        for button_name, button in self.sidebar.buttons.items():
            button.configure(state="normal", fg_color="#313131")  # Enable all buttons first
        self.sidebar.buttons[screen_name].configure(state="disabled", fg_color="#3D3D3D")

# class for the sidebar
class Sidebar:
    def __init__(self, root, switch_screens, current_screen):
        self.root = root
        self.switch_screens = switch_screens
        self.current_screen = current_screen
        self.sidebar_images = []
        self.title_frame = Frame(self.root)
        self.title_frame.grid(row=0, column=0, pady=(25, 50))
        
        logo_img = Image.open(r"iteration3/assets/images\logo.png").resize((51, 40))
        logo_img = ImageTk.PhotoImage(logo_img)
        self.sidebar_images.append(logo_img)
        logo = Label(self.title_frame, image=self.sidebar_images[0])
        logo.grid(row=0, column=0)
        
        title_lbl = Label(self.title_frame, text="RecycleAKL", font=("Arial", 25, "bold"), foreground="#2EA53A")
        title_lbl.grid(row=0, column=1, padx=(10, 0))
        
        self.buttons = self.create_buttons()

#   Create sidebar buttons
    def create_buttons(self):
        sidebar_buttons = [
            ("CollectionScreen", "Next collection date", r"iteration3/assets/images/collection_icon.png"),
            ("GuideScreen", "Disposal guides", r"iteration3/assets/images/guides_icon.png"),
            ("ProfileScreen", "Manage Account", r"iteration3/assets/images/profile_icon.png")
        ]
        
        buttons = {}
        row = 1
        for screen, text, icon in sidebar_buttons:
            icon_img = Image.open(icon).resize((40, 40))
            icon_img = ctk.CTkImage(icon_img)
            self.sidebar_images.append(icon_img)

            button = ctk.CTkButton(
                self.root,
                text=f" {text}",
                image=icon_img,
                compound='left',
                command=lambda p=screen: self.switch_screens(p),
                fg_color="#313131",
                hover_color="#297430",
                text_color="#f2f7fa",
                font=("Calibri", 20),
                anchor="ew",
                border_spacing=15,
                text_color_disabled="#40D24E",
            )

#           Disable the button for the current screen
            if self.current_screen == screen:
                button.configure(fg_color = "#3D3D3D", state="disabled")
            
            button.grid(row=row, column=0, sticky="ew")
            row += 1
            buttons[screen] = button
        return buttons

# class for the collection screen
class CollectionScreen(Frame):
    def __init__(self, root):
        super().__init__(root, bg="#F2F7FA")
        user_data = session.user_details
        self.username = user_data["username"]
        self.password = user_data["password"]
        self.address = user_data["address"]

        self.images = []
        
        icon_img = Image.open(r"iteration3/assets/images\collection_icon.png").resize((50, 50))
        icon_img = ctk.CTkImage(icon_img)
        self.icon_img = icon_img
        self.grid_columnconfigure(0, weight=1)
        
        title_lbl = ctk.CTkButton(self, image=self.icon_img, text=" Next Collection Date ", font=("Calibri", 25), bg_color="#F2F7FA", fg_color="#008033", corner_radius=30, compound="left", text_color="white", anchor="w", border_spacing=5, state="disabled", text_color_disabled="white")
        title_lbl.grid(column=0, row=0, pady=(10, 40), padx=10, sticky="w")
        
#       Check if user is signed in
        if self.address == "Anonymous":
            self.content = GetAddress(self)
        else:
            self.content = CollectionContent(self, self.address)

# class to get the user's address if not logged in
class GetAddress:
    def __init__(self, parent):
        self.parent = parent
        self.parent.grid_columnconfigure(0, weight=1)
        self.parent.grid_columnconfigure(1, weight=1)

        self.info_frame = ctk.CTkFrame(self.parent, bg_color="#F2F7FA", fg_color="white", corner_radius=10)
        self.info_frame.grid(row=1, columnspan=2)
        
        address_lbl = ctk.CTkLabel(self.info_frame, text="Please enter your address to view your next kerbside bin collection date", font=("Calibri", 15), corner_radius=10, text_color="black")
        address_lbl.grid(column=0, row=1, pady=10)
        
        self.address_entry = ctk.CTkEntry(self.info_frame, font=("Calibri", 15), corner_radius=10, text_color="black", fg_color="#F2F7FA", width=300)
        self.address_entry.grid(column=0, row=2)
        
        submit_button = ctk.CTkButton(self.info_frame, text="Submit", font=("Calibri", 15), corner_radius=10, command=lambda: self.update_address(self.address_entry.get()), text_color="black", fg_color="#40d24e")
        submit_button.grid(column=0, row=3, pady=10)
    
#   Update the user's address
    def update_address(self, address):
        if Login.check_address(address) == True:
            session.user_details["address"] = address
            self.info_frame.destroy()
            CollectionContent(self.parent, address)
        else:
            messagebox.showinfo("Error", "Address not found, please try again.")

# class for the reminder date
class CollectionContent:
    BIN_TYPES = ["Rubbish", "Foodscraps", "Recycling"]
    def __init__(self, parent, address):
        self.parent = parent
        self.address = address
        self.images = []
        self.get_collection_date()
        self.load_images()
        
        self.parent.grid_columnconfigure(0, weight=1)
        self.parent.grid_columnconfigure(1, weight=1)

        self.collections_frame = ctk.CTkFrame(self.parent, bg_color="#F2F7FA", fg_color="#CDE1CD", corner_radius=20)
        self.collections_frame.grid(row=1, columnspan=2, sticky="ns", pady=20)
        self.collections_frame.grid_columnconfigure(0, weight=1)

        address_lbl = Label(self.collections_frame, text=f"{self.formatted_address}", font=("Calibri", 25, "underline"), bg="#CDE1CD", fg="black")
        address_lbl.grid(pady=(30,0))

        header_lbl = Label(self.collections_frame, text="Your next collection date is on: ", font=("Calibri", 20), bg="#CDE1CD", fg="black")
        header_lbl.grid(pady=(20,0))
        date_lbl = Label(self.collections_frame, text=self.formatted_date, font=("Calibri", 30), bg="#CDE1CD", fg="black")
        date_lbl.grid()
        bins_lbl = Label(self.collections_frame, text="Bins being collected:", font=("Calibri", 20), bg="#CDE1CD", fg="black")
        bins_lbl.grid(pady=(30,0))

        bins_frame = Frame(self.collections_frame, bg="#CDE1CD")
        bins_frame.grid()

#       Display the bins
        for image in range(len(self.images)):
            img_label = Label(bins_frame, image=self.images[image], width=130, height=160, bg="#CDE1CD")
            img_label.image = self.images[image]
            img_label.grid(row=0, column=(image), padx=40, pady=(20,10))
            bin_name = Label(bins_frame, text=f"{self.BIN_TYPES[image]}", font=("Calibri", 25), bg="#CDE1CD", fg="black")
            bin_name.grid(row=1, column=(image))
            
        note_lbl = Label(self.collections_frame, text="Please put out the bins before 7am", font=("Calibri", 15), bg="#CDE1CD", fg="black")
        note_lbl.grid(pady=(20,40))

#   Get the collection dates from the API
    def get_collection_date(self):
        url = "http://163.47.222.43:80/api/v1/rr"
        parameters = {'addr': self.address}
        response = requests.get(url, params=parameters)
        data = response.json()
        self.rubbish_date = data['rubbish']
        self.recycling_date = data['recycle']
        self.foodscraps_date = data['foodscraps']
        self.formatted_address = data['address']
        if self.rubbish_date == self.recycling_date:
            self.recycling = True
        else:
            self.recycling = False
        date_object = datetime.strptime(self.rubbish_date, "%Y-%m-%d")
        self.formatted_date = date_object.strftime("%d/%m/%y")

#   Loads the images for the bins
    def load_images(self):
        img_rubbish = Image.open(r"iteration3/assets/images\rubbish.png")
        img_rubbish = img_rubbish.resize((130, 160))
        self.img_rubbish = ImageTk.PhotoImage(img_rubbish)
        self.images.append(self.img_rubbish)

        img_foodscraps = Image.open(r"iteration3/assets/images\foodscraps.png")
        img_foodscraps = img_foodscraps.resize((130, 160))
        self.img_foodscraps = ImageTk.PhotoImage(img_foodscraps)
        self.images.append(self.img_foodscraps)

        if self.recycling:
            img_recycle = Image.open(r"iteration3/assets/images\recycle.png")
            img_recycle = img_recycle.resize((130, 160))
            self.img_recycle = ImageTk.PhotoImage(img_recycle)
            self.images.append(self.img_recycle)
            
#   Update the user's address
    def update_address(self, address):
        self.address = address
        self.get_collection_date()
        
# class for Disposal guide screen
class GuideScreen(Frame):
    def __init__(self, root):   
        super().__init__(root, bg="#F2F7FA")
        icon_img = Image.open(r"iteration3/assets/images/guides_icon.png").resize((50, 50))
        icon_img = ctk.CTkImage(icon_img)
        self.icon_img = icon_img
        self.grid_columnconfigure(0, weight=1)

        title_lbl = ctk.CTkButton(self, image=self.icon_img, text=" Disposal Guides ", font=("Calibri", 25), bg_color="#F2F7FA", fg_color="#008033", corner_radius=30, compound="left", text_color="white", anchor="w", text_color_disabled="white", state="disabled", border_spacing=5)
        title_lbl.grid(column=0, row=0, pady=(10, 20), padx=10, sticky="w")
        
        self.create_buttons(self)

        self.show_guide("overview")

#   Create buttons for switching between disposal guides
    def create_buttons(self, parent):
        self.data, self.categories = self.load_data()
        self.categories.insert(0, "overview")
        buttons_frame = Frame(parent, bg="#F2F7FA")
        buttons_frame.grid(row=1, column=0)
        self.buttons = []
        
        for i in range(0, len(self.categories)):
            button = ctk.CTkButton(
                buttons_frame,
                text=self.categories[i].capitalize(),
                font=("Calibri", 15),
                corner_radius=15,
                fg_color="#008033",
                hover_color="#40d24e",
                text_color="white",
                command=lambda p=self.categories[i]: self.show_guide(p),
                width=20,
                text_color_disabled="white"
            )
            button.grid(row=0, column = i, padx=10)
            self.buttons.append(button)
        
#   Load data from JSON file
    def load_data(self):
        with open(r"iteration3/assets/data.json", "r") as file:
            data = json.load(file)
            categories = list(data.keys())
            return data, categories

#   Create the overview section
    def create_overview(self, parent):
        self.content_frame = ctk.CTkFrame(parent, bg_color="white", fg_color="white", corner_radius=20)
        self.content_frame.grid(row=2, column=0, pady=(20,30), padx=30, sticky="nsew")
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        overview_lbl = ctk.CTkLabel(self.content_frame, text="Overview", font=("Calibri", 25, "bold", "underline"), corner_radius=10, fg_color="white", text_color="#35353C")
        overview_lbl.grid(row=0, column=0, pady=(10,0))
        self.content_frame.grid_rowconfigure(1, weight=1)
        overview_text = ctk.CTkScrollableFrame(self.content_frame, bg_color="white", fg_color="white", corner_radius=20)
        overview_text.grid(row=1, column=0, sticky="nsew")
        overview_text.grid_columnconfigure(0, weight=1)
        
        overview_content = "Utilizing Auckland Council's kerbside collection service effectively can significantly reduce household waste, promote responsible recycling, and contribute to a cleaner environment. Understanding what can and cannot be recycled, along with following the correct disposal methods, ensures that materials are processed properly, minimizing landfill use and supporting sustainability efforts.\n\nAuckland households have access to three types of bins for kerbside collection: the red rubbish bin, the yellow recycling bin, and the green food scraps bin.\n\n- Red rubbish bin: This is for general waste that goes to the landfill and is collected weekly\n\n- Yellow recycling bin: Used for recyclable materials, this bin is collected every two weeks\n\n- Green food scraps bin: Designed for all organic food waste, this bin is also collected weekly\n\nTo ensure timely collection, bins should be placed at the kerbside by 7:00 a.m. on collection day, with the handles facing the street. The food scraps bin should have its handle facing upwards and be positioned slightly away from the other bins. By following these guidelines, residents can help streamline the collection process and support a cleaner, more sustainable Auckland."
        overview_lbl = ctk.CTkLabel(overview_text, font=("Calibri", 15), text=overview_content, corner_radius=10, fg_color="white", text_color="#35353C", wraplength=650, justify="left") 
        overview_lbl.grid(row=0, column=0, pady=(0, 20), sticky="nsew")
        self.example_img = Image.open(r"iteration3/assets/images/example.jpg").resize((650, 290))
        self.example_img = ImageTk.PhotoImage(self.example_img)
        self.example_img_lbl = Label(overview_text, image=self.example_img)
        self.example_img_lbl.grid(row=1, column=0, pady=(20, 0))
        

#   Show the disposal guide
    def show_guide(self, page):
#       Destroy the current content frame
        try:
            self.content_frame.destroy()
        except AttributeError:
            pass
#       Change the button colours
        for button in self.buttons:
            if button.cget("text").lower() == page:
                button.configure(fg_color = "#004d1e", state="disabled")
            else:
                button.configure(fg_color = "#008033", state="normal")
        if page == "overview":
            self.create_overview(self)
            return
        self.grid_rowconfigure(2, weight=1)
        self.content_frame = Frame(self, bg="#F2F7FA")
        self.content_frame.grid(row=2, column=0, sticky="nsew")

#       Configure the grid
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(1, weight=1)
        self.content_frame.grid_columnconfigure(2, weight=1)
        self.content_frame.grid_rowconfigure(0, weight=1)
        
        overview_frame = ctk.CTkFrame(self.content_frame, bg_color="white", fg_color="white", corner_radius=20)
        overview_frame.grid(row=0, column=0, pady=20, sticky="nsew", padx=20)
        overview_frame.grid_columnconfigure(0, weight=1)
        overview_frame.grid_rowconfigure(1, weight=1)

        overview_lbl = ctk.CTkLabel(overview_frame, text="Overview", font=("Calibri", 25, "bold", "underline"), corner_radius=10, fg_color="white", text_color="#35353C")
        overview_lbl.grid(row=0, column=0, pady=(10,0))
        
        overview_text = ctk.CTkTextbox(overview_frame, font=("Calibri", 15), corner_radius=10, fg_color="white", text_color="#35353C", wrap="word")
        overview_text.grid(row=1, column=0, sticky="nsew")
        overview_text.insert("0.0", self.data[page]["overview"])
        overview_text.configure(state="disabled")

        recycle_frame = ctk.CTkFrame(self.content_frame, bg_color="white", fg_color="white", corner_radius=20)
        recycle_frame.grid(row=0, column=1, pady=20, sticky="nsew")
        recycle_frame.grid_columnconfigure(0, weight=1)
        recycle_frame.grid_rowconfigure(1, weight=1)

        recycle_lbl = ctk.CTkLabel(recycle_frame, text="Recycling Bin", font=("Calibri", 25, "bold", "underline"), corner_radius=10, fg_color="white", text_color="#D1AC28")
        recycle_lbl.grid(row=0, column=0, pady=(20, 10))

        recycle_text = ctk.CTkTextbox(recycle_frame, font=("Calibri", 15), corner_radius=10, fg_color="white", text_color="#35353C", wrap="word")
        recycle_text.grid(row=1, column=0, sticky="nsew")
        recycle_text.insert("0.0", self.data[page]["recycling"])
        recycle_text.configure(state="disabled")

        rubbish_frame = ctk.CTkFrame(self.content_frame, bg_color="white", fg_color="white", corner_radius=20)
        rubbish_frame.grid(row=0, column=2, pady=20, sticky="nsew", padx=20)
        rubbish_frame.grid_columnconfigure(0, weight=1)
        rubbish_frame.grid_rowconfigure(1, weight=1)

        rubbish_lbl = ctk.CTkLabel(rubbish_frame, text="Rubbish Bin", font=("Calibri", 25, "bold", "underline"), corner_radius=10, fg_color="white", text_color="#EA3636")
        rubbish_lbl.grid(row=0, column=0, pady=(20, 10))

        rubbish_text = ctk.CTkTextbox(rubbish_frame, font=("Calibri", 15), corner_radius=10, fg_color="white", text_color="#35353C", wrap="word")
        rubbish_text.grid(row=1, column=0, sticky="nsew")
        rubbish_text.insert("0.0", self.data[page]["rubbish"])
        rubbish_text.configure(state="disabled")

        if page == "organic":
            recycle_lbl.configure(text="Foodscraps Bin", text_color="#40D24E")

# class for the profile screen
class ProfileScreen(Frame):
    def __init__(self, parent, app, root):
        super().__init__(parent, bg="#F2F7FA")
        self.parent = parent
        self.root = root
        self.app = app
        self.load_account()
        self.grid_columnconfigure(0, weight=1)
        icon_img = Image.open(r"iteration3/assets/images\profile_icon.png").resize((50, 50))
        icon_img = ctk.CTkImage(icon_img)
        self.icon_img = icon_img
        
        title_lbl = ctk.CTkButton(self, image=self.icon_img, text=" Manage Account ", font=("Calibri", 25), bg_color="#F2F7FA", fg_color="#008033", corner_radius=30, compound="left", text_color="white", anchor="w", border_spacing=5, text_color_disabled="white", state="disabled")
        title_lbl.grid(column=0, row=0, pady=(10, 40), padx=10, sticky="w")

        self.content_frame = Frame(self, bg="#F2F7FA")
        self.content_frame.grid(row=1, column=0)

        self.content()

#   Load the user's account details
    def content(self):

        edit_img = Image.open(r"iteration3/assets/images\edit.png").resize((22, 22))
        edit_img = ImageTk.PhotoImage(edit_img)
        self.edit_img = edit_img

        username_lbl = ctk.CTkLabel(self.content_frame, text=f"Username: ", font=("Calibri", 15), corner_radius=10, text_color="#35353C")
        username_lbl.grid(row=0, column=0, sticky="w")
        self.username_entry = ctk.CTkEntry(self.content_frame, font=("Calibri", 15), corner_radius=20, fg_color="#CDE1CD", text_color="#35353C", width=700, border_width=0, height=45)
        self.username_entry.grid(row=1, column=0)
        self.username_entry.insert(0, self.username)
        self.username_entry.configure(state="disabled")
        username_edit_btn = Button(self.content_frame, image=self.edit_img, command=lambda: [self.username_entry.configure(state="normal"), self.username_entry.focus()], height=22, width=22, border=0, relief=FLAT, bg="#CDE1CD")
        username_edit_btn.grid(row=1, column=0, sticky="nse", padx=(0, 15), pady=3)

        password_lbl = ctk.CTkLabel(self.content_frame, text=f"Password: ", font=("Calibri", 15), corner_radius=10, text_color="#35353C")
        password_lbl.grid(row=2, column=0, sticky="w", pady=(25,0))
        self.password_entry = ctk.CTkEntry(self.content_frame, font=("Calibri", 15), corner_radius=20, fg_color="#CDE1CD", text_color="#35353C", width=700, border_width=0, height=45)
        self.password_entry.grid(row=3, column=0)
        self.password_entry.insert(0, self.password)
        self.password_entry.configure(state="disabled")
        password_edit_btn = Button(self.content_frame, image=self.edit_img, command=lambda: [self.password_entry.configure(state="normal"), self.password_entry.focus()], height=22, width=22, border=0, relief=FLAT, bg="#CDE1CD")
        password_edit_btn.grid(row=3, column=0, sticky="e", padx=(0, 15), pady=3)

        address_lbl = ctk.CTkLabel(self.content_frame, text=f"Address: ", font=("Calibri", 15), corner_radius=10, text_color="#35353C")
        address_lbl.grid(row=4, column=0, sticky="w", pady=(25,0))
        self.address_entry = ctk.CTkEntry(self.content_frame, font=("Calibri", 15), corner_radius=20, fg_color="#CDE1CD", text_color="#35353C", width=700, border_width=0, height=45)
        self.address_entry.grid(row=5, column=0)
        self.address_entry.insert(0, self.address)
        self.address_entry.configure(state="disabled")
        address_edit_btn = Button(self.content_frame, image=self.edit_img, command=lambda: [self.address_entry.configure(state="normal"), self.address_entry.focus()], height=22, width=22, border=0, relief=FLAT, bg="#CDE1CD")
        address_edit_btn.grid(row=5, column=0, sticky="e", pady=3, padx=(0, 15))

        btn_frame = ctk.CTkFrame(self.content_frame, bg_color="#F2F7FA", fg_color="#F2F7FA", corner_radius=20)
        btn_frame.grid(row=6, column=0, pady=(20, 0))

        update_btn = ctk.CTkButton(btn_frame, text="Change details", font=("Calibri", 20), corner_radius=10, fg_color="#217346", hover_color="#247f4c", text_color="white", command=lambda: self.update_account(self.username_entry.get(), self.password_entry.get(), self.address_entry.get()), height=45, width=450)
        update_btn.grid(row=0, column=0, pady=(20,0), columnspan=2)

        signout_btn = ctk.CTkButton(btn_frame, text="Sign Out", font=("Calibri", 20), corner_radius=10, fg_color="#217346", hover_color="#247f4c", text_color="white", command=self.sign_out, height=45, width=200)
        signout_btn.grid(row=1, column=0, pady=(5,0), sticky="e", padx=(0, 5))

        delete_btn = ctk.CTkButton(btn_frame, text="Delete Account", font=("Calibri", 20), corner_radius=10, fg_color="#217346", hover_color="#247f4c", text_color="white", command=self.delete_account, height=45, width=200)
        delete_btn.grid(row=1, column=1, pady=(5,0), sticky="w", padx=(5, 0))

#   Update the user's account details
    def update_account(self, username, password, address):
        if session.user_details["username"] != username or session.user_details["password"] != password or session.user_details["address"] != address:
            if username == "" or password == "" or address == "":
                messagebox.showinfo("Error", "Please fill in all fields.")
                return
            self.original_username = session.user_details["username"]
            if Login.check_address(address) == False:
                messagebox.showinfo("Error", "Address not found, please try again.")
                return
            session.user_details = {
                "username": username,
                "password": password,
                "address": address
            }
            self.update_file()
            messagebox.showinfo("Success", "Account updated successfully")
        else:
            messagebox.showinfo("Error", "No changes were made")
            self.disable_entry()
            
#   Update the account details in the external file
    def update_file(self):
        accounts = Login.read_accounts()
        for account in accounts:
            if Login.decrypt(account["username"]) == self.original_username:
                account["username"] = Login.encrypt(session.user_details["username"])
                account["password"] = Login.encrypt(session.user_details["password"])
                account["address"] = Login.encrypt(session.user_details["address"])
        with open(r"iteration3/assets/accounts-data.json", "w") as file:
            json.dump(accounts, file, indent=4)
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
        accounts = Login.read_accounts()
        updated_accounts = []

        # Filter out the account that matches the username in the session
        for account in accounts:
            if Login.decrypt(account["username"]) != session.user_details["username"]:
                updated_accounts.append(account)

        # Write the updated accounts list back to the JSON file
        with open(r"iteration3/assets/accounts-data.json", "w") as file:
            json.dump(updated_accounts, file, indent=4)
        self.clear_session()

#   Clear the session details
    def clear_session(self):
        session.user_details = None
        self.app.sidebar_frame.destroy()
        self.app.main_frame.destroy()
        Login(self.root)

#   Load the user's account details
    def load_account(self):
        user_data = session.user_details
        self.username = user_data["username"]
        self.password = user_data["password"]
        self.address = user_data["address"]
 
if __name__ == "__main__":
    Program()