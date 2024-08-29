# load dependencies
from tkinter import *
from PIL import Image, ImageTk
from ctypes import windll #DPI awareness
import requests #Web scraping
from tkinter import messagebox
from datetime import datetime
import json

class Program():
    banner_image = []

#   Create the main window 
    def __init__(self):
        self.root = Tk()
        self.root.title("Register Account")
        self.root.geometry("1150x600")
        self.root.state("zoomed")
        self.root.config(bg="white")
        windll.shcore.SetProcessDpiAwareness(1)
        scaling_factor = self.root.winfo_fpixels('1i') / 72.0
        self.root.tk.call('tk', 'scaling', scaling_factor)

#       Load the banner image
        banner_img = Image.open(r"iteration2/images/banner.png")
        banner_img = ImageTk.PhotoImage(banner_img)
        self.banner_image.append(banner_img)

        back_img = Image.open(r"iteration2/images/back.png")
        back_img = ImageTk.PhotoImage(back_img)
        self.banner_image.append(back_img)

        self.banner(self.root)
        MainMenu(self.root)
        self.root.mainloop()

#   Create the banner at the top of the page
    @classmethod
    def banner(cls, frame):
        cls.banner_frame = Frame(frame)
        cls.banner_frame.pack(side=TOP, fill=X)
        cls.banner_frame.grid_columnconfigure(0, weight=1)

        Label(cls.banner_frame, image=cls.banner_image[0]).grid(row=0,column=0)
        cls.heading = Label(cls.banner_frame, text="", font=("Calibri", 40, "bold"), fg="green", bg="white")
        cls.heading.grid(row=0,column=0)

        cls.back_button = Button(cls.banner_frame, image=cls.banner_image[1], font=("Calibri", 15))

#   Return to the previous page
    @classmethod
    def back(cls, frame):
        frame.destroy()
        MainMenu(cls.banner_frame.master)

#   Update the banner title and back button
    @classmethod
    def update_banner(cls, title, frame):
        if title == "Main menu":
            cls.back_button.grid_forget()
        else:
            cls.back_button.grid(row=0,column=0, padx=10, pady=10, sticky="nw")

        cls.heading.config(text=title)
        cls.back_button.config(command=lambda:cls.back(frame))

#   Save the account details
    @classmethod
    def details(cls, username, password, address):
        global logged_in
        cls.username = username
        cls.password = password
        cls.address = address
        logged_in = True


#   Create the main menu page
class MainMenu():
    def __init__(self, master):
        self.master = master
        self.master.title("Main Menu")
        self.main()

#   Main page content
    def main(self):
        self.main_menu_frame = Frame(self.master, bg="white")
        self.main_menu_frame.pack()
        Program.update_banner(title = "Main menu", frame=self.main_menu_frame)

        title = Label(self.main_menu_frame, text="Welcome!", font=("Helvetica", 40, "bold"), fg="green", bg="white")
        title.pack(pady=40)

        content_frame = Frame(self.main_menu_frame, bg="white")
        content_frame.pack(expand=True)

        reminder = Button(content_frame, width=30, height=15, text="Next collection day", font=("Calibri", 20, "bold"), fg="Green", command= lambda:[self.main_menu_frame.forget(), self.check_logged_in()])
        reminder.grid(column=1, row=1, padx=10, pady=10)
        reminder.grid_propagate(False)

        guide = Button(content_frame, width=30, height=15, text="Recycling guide", font=("Calibri", 20, "bold"), fg="Green", command= lambda:[self.main_menu_frame.forget(), Guide(self.master)])
        guide.grid(column=2, row=1, padx=10, pady=10)
        guide.grid_propagate(False)

        if logged_in == True:
            acc = "Manage Account"
            func = lambda:[self.main_menu_frame.forget(), Profile(self.master)]
        else:
            acc = "Log in"
            func = lambda:[self.main_menu_frame.forget(), Login(self.master)]

        self.account = Button(content_frame, width=30, height=15, text=acc, command= func, font=("Calibri", 20, "bold"), fg="Green")
        self.account.grid(column=3, row=1, padx=10, pady=10)
        self.account.grid_propagate(False)
        self.check_account_status()

#   Adjusts the profile button in the main menu
    def check_account_status(self):
        if logged_in:
            self.account.config(text="Manage Account")
        else:
            self.account.config(text="Log in")

#   Checks if the user is logged in before accessing collections
    def check_logged_in(self):
        if logged_in:
            Collection(self.master)
        else:
            messagebox.showinfo("Error", "Please log in to access this feature.")
            Login(self.master)


#   Create the register page
class Register():
    def __init__(self, master):
        self.master = master
        self.master.title("Register Account")
        self.main()

# Main page content 
    def main(self):
        self.register_frame = Frame(self.master, bg="white")
        self.register_frame.pack()
        Program.update_banner(title = "Register", frame=self.register_frame)

        Label(self.register_frame, text="Register your account", font=("Calibri", 20), bg="white").pack(pady=(60,20))
        self.credentials_frame = Frame(self.register_frame, bg="white")
        self.credentials_frame.pack()

        self.label_username = Label(self.credentials_frame, text="Username:", font=("Calibri", 15), bg="white")
        self.label_username.grid(row=0, column=0, pady=(0,3), padx=(0,10))
        
        self.entry_username = Entry(self.credentials_frame, width=25, font=("Calibri", 15), bg="white")
        self.entry_username.grid(row=0, column=1)

        self.label_password = Label(self.credentials_frame, text="Password:", font=("Calibri", 15), bg="white")
        self.label_password.grid(row=1, column=0, pady=(0,3), padx=(0,10))

        self.entry_password = Entry(self.credentials_frame, show="*", width=25, font=("Calibri", 15), bg="white")
        self.entry_password.grid(row=1, column=1, pady=(10))

        self.label_address = Label(self.credentials_frame, text="Address:", font=("Calibri", 15), bg="white")
        self.label_address.grid(row=2, column=0, pady=(0,3), padx=(0,4))
        
        self.entry_address = Entry(self.credentials_frame, width=25, font=("Calibri", 15), bg="white")
        self.entry_address.grid(row=2, column=1)
        
        self.error_label = Label(self.register_frame, text="", font=("Calibri", 10), bg="white")
        self.error_label.pack(pady=(10,0))

        submit = Button(self.register_frame, text="Register", command=lambda:self.check_details(), font=("Calibri", 15), width=35)
        submit.pack(pady=15)

        login = Button(self.register_frame, text="Login", command=lambda:[Login(self.master), self.register_frame.forget()], font=("Calibri", 15), width=35)
        login.pack()

#   Check if the details are correct before creating the account
    def check_details(self):
        if self.entry_username.get() == "" or self.entry_password.get() == "" or self.entry_address.get() == "":
            self.error_label.config(text="Please fill in all fields.")
            return False
        
        valid = self.check_address(self.entry_address.get())
        if valid:
            self.create_account()

        else:
            self.error_label.config(text="Address not found, please try again.")
    
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

#   Save account details to external file
    def create_account(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        address = self.entry_address.get()
        with open(r"iteration2\details.txt", "a") as file:
            file.write(f"{username[::-1]},{password[::-1]},{address[::-1]}\n")
        Program.details(username, password, address)
        MainMenu(self.master)
        self.register_frame.forget()


#   Create log in page
class Login:
    def __init__(self, master):
        self.master = master
        self.master.title("Log in")
        self.main()

# Main page content
    def main(self):
        self.login_frame = Frame(self.master, bg="white")
        self.login_frame.pack()
        Program.update_banner(title = "Log in", frame=self.login_frame)

        Label(self.login_frame, text="Log in to your account:", font=("Calibri", 20), bg="white").pack(pady=(60,20))
        self.frame_credentials = Frame(self.login_frame, bg="white")
        self.frame_credentials.pack()

        self.label_username = Label(self.frame_credentials, text="Username:", font=("Calibri", 15), bg="white")
        self.label_username.grid(row=0, column=0, pady=(0,3), padx=(0,10))
        
        self.entry_username = Entry(self.frame_credentials, width=25, font=("Calibri", 15), bg="white")
        self.entry_username.grid(row=0, column=1)

        self.label_password = Label(self.frame_credentials, text="Password:", font=("Calibri", 15), bg="white")
        self.label_password.grid(row=1, column=0, pady=(0,3), padx=(0,10))

        self.entry_password = Entry(self.frame_credentials, show="*", width=25, font=("Calibri", 15), bg="white")
        self.entry_password.grid(row=1, column=1, pady=(10))

        self.error_label = Label(self.login_frame, text="", font=("Calibri", 10), bg="white")
        self.error_label.pack(pady=(10,0))

        submit = Button(self.login_frame, text="Login", command=self.check_details, font=("Calibri", 15), width=35)
        submit.pack(pady=15)

        login = Button(self.login_frame, text="Register", command=lambda:[Register(self.master), self.login_frame.forget()], font=("Calibri", 15), width=35)
        login.pack()

#   Check if the details are correct before logging in
    def check_details(self):
        if self.entry_username.get() == "" or self.entry_password.get() == "":
            self.error_label.config(text="Please fill in all fields.")
            return
        try:
            with open(r"iteration2\details.txt", "r") as file:
                for line in file:
                    username, password, address = line.replace("\n","").split(",")
                    if username[::-1] == self.entry_username.get() and password[::-1] == self.entry_password.get():
                        self.username = username[::-1]
                        self.password = password[::-1]
                        self.address = address[::-1]
                        Program.details(self.username, self.password, self.address)
                        MainMenu(self.master)
                        self.login_frame.forget()
                        return
            self.error_label.config(text="Invalid username or password.")
        except FileNotFoundError:
            messagebox.showinfo("Error", "No accounts found, please register an account.")
            Register(self.master)
            self.login_frame.forget()


#   Create the collection page
class Collection():
    def __init__(self, master):
        self.master = master
        self.master.title("Collection")

        self.master.config(cursor="watch")
        self.master.update_idletasks()
        
        self.loading = Label(self.master, text="Loading... Please wait.", font=("Calibri", 25))
        self.loading.pack(pady=(20,0), expand=True, fill=BOTH)

        self.images = []
        self.get_collection_date()
        self.load_images()

        self.master.config(cursor="")
        self.master.update_idletasks()

        self.main()

#   Main page content
    def main(self):
        self.loading.forget()
        collections_frame = Frame(self.master, bg="white")
        collections_frame.pack()
        Program.update_banner(title = "Collection", frame=collections_frame)
        Label(collections_frame, text="Your next collection date is on: ", font=("Calibri", 25), bg="white").pack(pady=(20,0))
        Label(collections_frame, text=self.formatted_date, font=("Calibri", 30), bg="white").pack()
        Label(collections_frame, text="Bins being collected:", font=("Calibri", 25), bg="white").pack(pady=(30,0))

        bins = Frame(collections_frame, bg="white")
        bins.pack()

        name = ["Rubbish", "Foodscraps", "Recycling"]

        for image in range(len(self.images)):
            img_label = Label(bins, image=self.images[image], width=130, height=160, bg="white")
            img_label.image = self.images[image]
            img_label.grid(row=0, column=(image), padx=40, pady=(20,10))
            Label(bins, text=f"{name[image]}", font=("Calibri", 25), bg="white").grid(row=1, column=(image))
            
        Label(collections_frame, text="Please put out the bins before 7am", font=("Calibri", 15), bg="white").pack(pady=(20,0))

#   Get the collection dates from the API
    def get_collection_date(self):
        url = "http://163.47.222.43:80/api/v1/rr"
        parameters = {'addr': Program.address}
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

#   Create the profile page
class Profile:
    def __init__(self, master):
        self.master = master
        self.master.title("Collection")
        
        self.main()

#   Main page content
    def main(self):
        self.profile_frame = Frame(self.master, bg="white")
        self.profile_frame.pack()
        Program.update_banner(title = "Profile", frame=self.profile_frame)

        Label(self.profile_frame, text="Profile", font=("Calibri", 20), bg="white").pack(pady=(60,20))
        self.credentials_frame = Frame(self.profile_frame, bg="white")
        self.credentials_frame.pack()

        self.username_label = Label(self.credentials_frame, text="Username", font=("Calibri", 15), bg="white")
        self.username_label.grid(row=0, column=0, pady=(0,3), sticky="w")

        self.username_entry = Entry(self.credentials_frame, width=25, font=("Calibri", 15), bg="white")
        self.username_entry.insert(0, Program.username)
        self.username_entry.config(state=DISABLED)
        self.username_entry.grid(row=1, column=0, pady=(0,10))

        self.password_label = Label(self.credentials_frame, text="Password", font=("Calibri", 15), bg="white")
        self.password_label.grid(row=2, column=0, pady=(0,3), sticky="w")
        self.password_btn = Button(self.credentials_frame, text="Edit", command=lambda:[self.password_entry.config(state=NORMAL), self.password_entry.focus(), self.password_entry.delete(0, END)])
        self.password_btn.grid(row=3, column=1, padx=(20,0))
        self.password_entry = Entry(self.credentials_frame, show="*", width=25, font=("Calibri", 15), bg="white")
        self.password_entry.insert(0, Program.password)
        self.password_entry.config(state=DISABLED)
        self.password_entry.grid(row=3, column=0, pady=(0,10))

        self.address_label = Label(self.credentials_frame, text="Address", font=("Calibri", 15), bg="white")
        self.address_label.grid(row=4, column=0, pady=(0,3), sticky="w")
        self.address_btn = Button(self.credentials_frame, text="Edit", command=lambda:[self.address_entry.config(state=NORMAL), self.address_entry.focus(), self.address_entry.delete(0, END)])
        self.address_btn.grid(row=5, column=1, padx=(20,0))
        self.address_entry = Entry(self.credentials_frame, width=25, font=("Calibri", 15), bg="white")
        self.address_entry.insert(0, Program.address)
        self.address_entry.config(state=DISABLED)
        self.address_entry.grid(row=5, column=0)
        
        submit = Button(self.profile_frame, text="Save changes", command=lambda:self.save_changes(), font=("Calibri", 15), width=35)
        submit.pack(pady=15)

        login = Button(self.profile_frame, text="Log out", command=lambda:self.log_out(), font=("Calibri", 15), width=35)
        login.pack()

#   Save the changes made to the account
    def save_changes(self):
        if self.password_entry.get() == Program.password and self.address_entry.get() == Program.address:
            messagebox.showinfo("Error", "No changes were made.")
            return
        if self.address_entry.get() != Program.address:
            valid = Register.check_address(self.address_entry.get())
            if not valid:
                messagebox.showinfo("Error", "Address not found, please try again.")
                return

        with open(r"iteration2\details.txt", "r") as file:
            data = file.readlines()
        with open(r"iteration2\details.txt", "w") as file:
            for line in data:
                if Program.username in line[::-1]:
                    line = f"{Program.username[::-1]},{self.password_entry.get()[::-1]},{self.address_entry.get()[::-1]}\n"
                file.write(line)
        messagebox.showinfo("Success", "Changes saved.")
        Program.details(Program.username, self.password_entry.get(), self.address_entry.get())
        self.profile_frame.update()

#   Log out of the account
    def log_out(self):
        global logged_in
        logged_in = False
        self.profile_frame.forget()
        MainMenu(self.master)

#   Create the recycling guide page
class Guide:
    def __init__(self, master):
        self.master = master
        self.master.title("Recycling Guide")
        self.main()
        
#   Main page content
    def main(self):
        self.guide_frame = Frame(self.master, bg="white")
        self.guide_frame.pack()
        Program.update_banner(title = "Disposal Guide", frame=self.guide_frame)

        buttons_frame = Frame(self.guide_frame, bg="white")
        buttons_frame.pack()
        buttons = []
        data, categories = self.load_data()

        for i in range(len(data)):

            btn = Button(buttons_frame, text=categories[i].capitalize(), font=("Calibri", 20), width=45, height=6, command=lambda i=i: [Info(self.master, i, data, categories), self.guide_frame.forget()])
            btn.grid(row=i-((i)%2), column=((i)%2), pady=10, padx=10)

            buttons.append(btn)

#   Load the data from the external file
    def load_data(self):
        with open(r"iteration2\data.json", "r") as file:
            data = json.load(file)
            categories = list(data.keys())
            return data, categories
        
#   Create the information page
class Info:
    def __init__(self, master, number, data, category):
        self.master = master
        self.master.title("Recycling Guide")
        self.data = data
        self.category = category[number]
        self.main()

#   Main page content
    def main(self):
        self.info_frame = Frame(self.master, bg="white")
        self.info_frame.pack(fill=BOTH, expand=True)
        Program.update_banner(title = self.category.capitalize(), frame=self.info_frame)

        frame1 = Frame(self.info_frame, bg="white")
        frame1.grid(row=0, column=0, sticky="nw", padx=20, pady=20)

        frame2 = Frame(self.info_frame, bg="white")
        frame2.grid(row=0, column=1, sticky="new")

        frame3 = Frame(self.info_frame, bg="white")
        frame3.grid(row=0, column=2, sticky="ne", padx=20)

        self.info_frame.grid_columnconfigure(0, weight=1)
        self.info_frame.grid_columnconfigure(1, weight=1)
        self.info_frame.grid_columnconfigure(2, weight=1)
        self.info_frame.grid_rowconfigure(0, weight=1)

        Label(frame1, text=f"Types of {self.category}", font=("Calibri", 30), fg="brown", bg="white").pack()
        Message(frame1, text=self.data[self.category]["type"], font=("Calibri", 18), bg="white").pack()

        Label(frame2, text="Yellow recycling bin", font=("Calibri", 30), fg="#d5c400", bg="white").pack()
        Message(frame2, text=self.data[self.category]["recycle"], font=("Calibri", 18), bg="white").pack()

        Label(frame2, text="Red rubbish bin", font=("Calibri", 30), fg="red", bg="white").pack(pady=(80,0))
        Message(frame2, text=self.data[self.category]["rubbish"], font=("Calibri", 18), bg="white").pack()

        Label(frame3, text="Tips", font=("Calibri", 30), fg="green", bg="white").pack()
        Message(frame3, text=self.data[self.category]["tips"], font=("Calibri", 18), bg="white").pack()

if __name__ == "__main__":
    logged_in = False
    Program()
