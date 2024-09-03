from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import customtkinter as ctk
from datetime import datetime
import requests

class Collection:
    def __init__(self, root, username, password, address):
        self.username = username
        self.password = password
        self.address = address
        
        self.root = root
        self.images = []
        
        self.sidebar_frame = ttk.Frame(self.root)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.main_frame = Frame(self.root, background="#F2F7FA")
        self.main_frame.grid(row=0, column=1, sticky="nsew")
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=3)
        self.root.grid_rowconfigure(0, weight=1)

        self.main_frame.grid_propagate(False)
        self.sidebar_frame.grid_propagate(False)
        self.sidebar_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.sidebar_frame.grid_columnconfigure(0, weight=1)
        
        icon_img = Image.open(r"assets/iteration3\images\collection_icon.png").resize((50, 50))
        icon_img = ctk.CTkImage(icon_img)
        self.icon_img = icon_img
        
        title_lbl = ctk.CTkLabel(self.main_frame, image=self.icon_img, text="  Next Collection Date", font=("Calibri", 30), bg_color="#F2F7FA", fg_color="#008033", corner_radius=30, compound="left", text_color="white", height=60, width=400)
        title_lbl.grid(column=0, row=0, pady=(50, 40), padx=(0, 400))
        
        self.sidebar = Sidebar(self.sidebar_frame, current="collection")
        if self.address == "Anonymous":
            self.content = GetAddress(self.main_frame)
        else:
            self.content = CollectionContent(self.main_frame, self.address)


class Sidebar:
    def __init__(self, sidebar_frame, current):
        self.sidebar_frame = sidebar_frame
        self.title_frame = ttk.Frame(self.sidebar_frame)
        self.title_frame.grid(row=0, column=0, pady=(25, 50))
        self.sidebar_images = []
        logo_img = Image.open(r"assets/iteration3\images\logo.png").resize((51, 40))
        logo_img = ImageTk.PhotoImage(logo_img)
        self.sidebar_images.append(logo_img)
        
        logo = ttk.Label(self.title_frame, image=self.sidebar_images[0])
        logo.grid()
        title_lbl = ttk.Label(self.title_frame, text="RecycleAKL", font=("Arial", 30, "bold"), foreground="#2EA53A")
        title_lbl.grid(row=0, column=1, padx=(10, 0))
        
        sidebar_buttons = [
            ("collection", "Next collection date", self.show_collection_date, r"assets/iteration3\images\collection_icon.png", 1),
            ("guide", "Recycling Guides", self.show_recycling_guides, r"assets/iteration3\images\guides_icon.png", 2),
            ("profile", "Manage Account", self.show_manage_account, r"assets/iteration3\images\profile_icon.png", 3)
        ]

        for page, text, command, icon, number in sidebar_buttons:
            
            icon_img = Image.open(icon).resize((40, 40))
            #icon_img = ImageTk.PhotoImage(icon_img)
            icon_img = ctk.CTkImage(icon_img)
            self.sidebar_images.append(icon_img)
            
            button = ctk.CTkButton(
                self.sidebar_frame,
                text=f" {text}",
                image=icon_img,
                compound='left',
                command=command,
                fg_color="#313131",
                hover_color="#297430",
                text_color="#f2f7fa",
                font=("Calibri", 25),
                anchor="w",
                border_spacing=15,
                text_color_disabled="#40D24E"
            )
            button.grid(row=number, column=0, sticky="ew")
            if page == current:
                button.configure(fg_color = "#3D3D3D", state="disabled")
            
    def show_collection_date(self):
        pass
    
    def show_recycling_guides(self):
        pass
    
    def show_manage_account(self):
        pass
            

class GetAddress:
    def __init__(self, main_frame):
        self.main_frame = main_frame
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)

        self.info_frame = Frame(self.main_frame)
        self.info_frame.grid(row=1, columnspan=2)
        
        address_lbl = ctk.CTkLabel(self.info_frame, text="Please enter your address to view your collection date", font=("Calibri", 25), bg_color="#F2F7FA", fg_color="black", corner_radius=10)
        address_lbl.grid(column=0, row=1)
        
        self.address_entry = ctk.CTkEntry(self.info_frame, font=("Calibri", 25), bg_color="white", fg_color="black", corner_radius=10)
        self.address_entry.grid(column=0, row=2)
        
        submit_button = ctk.CTkButton(self.info_frame, text="Submit", font=("Calibri", 25), bg_color="#008033", fg_color="white", corner_radius=10, command=lambda: [CollectionContent(main_frame, self.address_entry.get()), self.info_frame.destroy()])
        submit_button.grid(column=0, row=3)
    
          
class CollectionContent:
    BIN_TYPES = ["Rubbish", "Foodscraps", "Recycling"]
    
    def __init__(self, main_frame, address):
        self.address = address
        self.images = []
        self.get_collection_date()
        self.load_images()
        self.main_frame = main_frame
        
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)

        self.collections_frame = Frame(self.main_frame, bg="#F2F7FA")
        self.collections_frame.grid(row=1, columnspan=2)
        self.collections_frame.grid_columnconfigure(0, weight=1)
        
        header_lbl = Label(self.collections_frame, text="Your next collection date is on: ", font=("Calibri", 25), bg="#F2F7FA", fg="black")
        header_lbl.grid(pady=(20,0))
        date_lbl = Label(self.collections_frame, text=self.formatted_date, font=("Calibri", 30), bg="#F2F7FA", fg="black")
        date_lbl.grid()
        bins_lbl = Label(self.collections_frame, text="Bins being collected:", font=("Calibri", 25), bg="#F2F7FA", fg="black")
        bins_lbl.grid(pady=(30,0))

        bins_frame = Frame(self.collections_frame, bg="#F2F7FA")
        bins_frame.grid()

        for image in range(len(self.images)):
            img_label = Label(bins_frame, image=self.images[image], width=130, height=160, bg="#F2F7FA")
            img_label.image = self.images[image]
            img_label.grid(row=0, column=(image), padx=40, pady=(20,10))
            bin_name = Label(bins_frame, text=f"{self.BIN_TYPES[image]}", font=("Calibri", 25), bg="#F2F7FA", fg="black")
            bin_name.grid(row=1, column=(image))
            
        note_lbl = Label(self.collections_frame, text="Please put out the bins before 7am", font=("Calibri", 15), bg="#F2F7FA", fg="black")
        note_lbl.grid(pady=(20,0))

#   Get the collection dates from the API
    def get_collection_date(self):
        url = "http://163.47.222.43:80/api/v1/rr"
        parameters = {'addr': self.address}
        response = requests.get(url, params=parameters)
        data = response.json()
        self.rubbish_date = data['rubbish']
        self.recycling_date = data['recycle']
        self.foodscraps_date = data['foodscraps']
        if self.rubbish_date == self.recycling_date:
            self.recycling = True
        else:
            self.recycling = False
        date_object = datetime.strptime(self.rubbish_date, "%Y-%m-%d")
        self.formatted_date = date_object.strftime("%d/%m/%y")

#   Loads the images for the bins
    def load_images(self):
        img_rubbish = Image.open(r"iteration2\images\rubbish.png")
        img_rubbish = img_rubbish.resize((130, 160))
        self.img_rubbish = ImageTk.PhotoImage(img_rubbish)
        self.images.append(self.img_rubbish)

        img_foodscraps = Image.open(r"iteration2\images\foodscraps.png")
        img_foodscraps = img_foodscraps.resize((130, 160))
        self.img_foodscraps = ImageTk.PhotoImage(img_foodscraps)
        self.images.append(self.img_foodscraps)

        if self.recycling:
            img_recycle = Image.open(r"iteration2\images\recycle.png")
            img_recycle = img_recycle.resize((130, 160))
            self.img_recycle = ImageTk.PhotoImage(img_recycle)
            self.images.append(self.img_recycle)
            
    def update_address(self, address):
        self.address = address
        self.get_collection_date()
