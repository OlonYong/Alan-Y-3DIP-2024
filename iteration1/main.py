#Load dependencies
from tkinter import *
from tkinter import ttk, messagebox
import datetime
import openpyxl
from PIL import ImageTk, Image
import os
import webbrowser

# Set up Window
root = Tk()
root.geometry("1000x550")
root.resizable(False, False)

# Set up program variables
loaded_images = []
global user
global passw
user = ""
passw = ""

# Creates the main menu
def main():
    m_frame = Frame(root)
    m_frame.pack()
    buffer = Label(m_frame, height=9)
    buffer.grid(row=0, column=0)

    title = Label(m_frame, text="Welcome!", font=("Helvetica", 40, "bold"), fg="green")
    title.grid(row=0, column=2, padx=(0, 0))

    reminder = Button(m_frame, width=25, height=13, text="Next collection day", command= lambda:[m_frame.destroy(), collection()], font=(15))
    reminder.grid(column=1, row=1, padx=10, pady=10)
    reminder.grid_propagate(False)

    guide = Button(m_frame, width=25, height=13, text="Recycling guide", command= lambda:[m_frame.destroy(), guides()], font=(15))
    guide.grid(column=2, row=1, padx=10, pady=10)
    guide.grid_propagate(False)

    account = Button(m_frame, width=25, height=13, text="Manage Account", command= lambda:[m_frame.destroy(), login()], font=(15))
    account.grid(column=3, row=1, padx=10, pady=10)
    account.grid_propagate(False)

# Creates the collection window
def collection():
    c_frame = Frame(root)
    c_frame.pack()
    if user == "" and passw == "":
        messagebox.showinfo("Important", "Please make an account to save your data.")
    else:
        if os.path.exists("iteration1/assets/dates.txt"):
            with open("iteration1/assets/dates.txt", "r") as file:
                for line in file:
                    dates_data, username = line.strip().split(" : ")
                    year, month, day, is_recycling = dates_data.split("-")
                    
                    if username == user:
                        current_datetime = datetime.datetime.now()
                        target_datetime = datetime.datetime(int(year), int(month), int(day))
                        if current_datetime.date() <= target_datetime.date():
                            c_frame.pack_forget() 
                            reminder(day, month, is_recycling)
                            return
                    

    heading = Label(c_frame, text="Enter your next collection date", font=("Helvetica", 20, "bold"))
    heading.pack()

    date = Frame(c_frame)
    date.pack()

    Label(date, text="Day").grid(row=0, column=0)

    day_var = StringVar()
    day = ttk.Combobox(date, textvariable=day_var, state="readonly")
    day["values"] = tuple(str(i) for i in range(1, 32)) 
    day.grid(row=1, column=0)

    Label(date, text="/").grid(row=1, column=1)

    Label(date, text="Month").grid(row=0, column=2)
    month_var = StringVar()
    month = ttk.Combobox(date, textvariable=month_var, state="readonly")
    month["values"] = tuple(str(i) for i in range(1, 13))
    month.grid(row=1, column=2)
    

    check_recycling = IntVar()
    is_recycling = Checkbutton(c_frame, text="Is there recycling?", variable=check_recycling)
    is_recycling.pack()

    submit = Button(c_frame, text="Submit", command= lambda:calculate_day(day_var.get(), month_var.get(), check_recycling.get(), c_frame))
    submit.pack(pady=5)

    Button(c_frame, command= lambda: webbrowser.open_new("https://www.aucklandcouncil.govt.nz/rubbish-recycling/rubbish-recycling-collections/Pages/rubbish-recycling-collection-days.aspx"), text="Don't know your collection? Check here!").pack(pady=5)

    back = Button(c_frame, text="Back", command= lambda:[c_frame.destroy(), main()])
    back.pack(pady=5)

# Calculates the next collection day
def calculate_day(day, month, is_recycling, c_frame):
    collection_day = int(day)
    collection_month = int(month)
    recycling = is_recycling
    year = False
    
    try:
        next_date = datetime.datetime(datetime.datetime.now().year, collection_month, collection_day )
        if next_date.month == 12 and next_date.day >= 24:
            year = True
        next_date += datetime.timedelta(days=7)
    except ValueError:
        messagebox.showinfo("Important", "Please enter a valid date")
        return
    
    if recycling:
        recycling = False
    elif recycling == False:
        recycling = True

    if user != "" and passw != "":
        
        with open("iteration1/assets/dates.txt", "w") as file:
            file.write(f"{str(next_date.date())+"-"+str(recycling)} : {user}")
    
    while datetime.datetime.now() > next_date:
        next_date += datetime.timedelta(days=7)
        if next_date.month == 12 and next_date.day >= 24:
            year = True
            break
            
    
    collection_day = next_date.day
    collection_month = next_date.month
    if c_frame != None:
        c_frame.forget()
    reminder(collection_day, collection_month, recycling, year)
    
# Creates the reminder window
def reminder(day, month, is_recycling, years=False):
    c_frame = None
    r_frame = Frame(root)
    r_frame.pack()
    year = datetime.date.today().year
    if years:
        year += 1
    if user != "":
        with open("iteration1/assets/dates.txt", "r") as file:
            for line in file:
                year, month, day, is_recycling = line.split("-")
            if datetime.datetime.now() > datetime.datetime(int(year), int(month), int(day)):
                r_frame.forget()
                calculate_day(day, month, is_recycling, c_frame)
                

    Label(r_frame, text="Your next collection day is:", font=(15)).pack(pady=5)
    Label(r_frame, text=f"{day}/{month}/{year}", font=(20)).pack()
    if is_recycling == True:
        Label(r_frame, text="Recycling: Yes", font=(20)).pack(pady=5)
    else:
        Label(r_frame, text="Recycling: No", font=(20)).pack()

    back = Button(r_frame, text="Back", command= lambda:[r_frame.destroy(), main()])
    back.pack()

# Creates the recycling guide window
def guides():
    data = load_data()
    g_frame = Frame(root)
    g_frame.pack()
    title = Label(g_frame, text="Recycling Guides", font=("Helvetica", 20, "bold"))
    title.pack()
    catalogue = Frame(g_frame)
    catalogue.pack()
    frame = []
    infopanels = info_panels(data)
    for i in range(6):
        frame.append(Button(catalogue, text=f"{data[i][0]}", width=40, height=10, command= lambda i=i: [load_panels(infopanels[i]), g_frame.destroy()]))
        frame[i].grid(row=i-((i)%2), column=((i)%2))

    back = Button(g_frame, text="Back", command= lambda:[g_frame.destroy(), main()])
    back.pack()

# Loads the data from the excel file
def load_data():
    guide_data = []
    path = r"iteration1/assets/data.xlsx"
    workbook = openpyxl.load_workbook(path)
    sheet = workbook.active
    for row in sheet.iter_rows(min_row=0, max_col=3, max_row=6, values_only=True):
        row = list(row)
        image = Image.open(f"{row[2]}")
        image = ImageTk.PhotoImage(image)
        loaded_images.append(image)
        row[2] = image
        
        guide_data.append(row)
    return guide_data

# Creates the information panels for the recycling guide
def info_panels(data):
    info_panels = []
    for i in range(0, len(data)):
        frame = Frame(root)
        Label(frame, text=data[i][0], font=("Helvetica", 40, "bold")).pack()
        Label(frame, image=data[i][2]).pack()
        Label(frame, text=data[i][1], wraplength=500, pady=10).pack()
        info_panels.append(frame)
    return info_panels

# Loads the information panels
def load_panels(panel):
    panel.pack()
    back = Button(panel, text="Back", command= lambda:[panel.destroy(), guides()])
    back.pack()

# Creates the profile window
def profile():
    p_frame = Frame(root)
    p_frame.pack()

    Label(p_frame, text="Profile", font=("Helvetica", 20, "bold")).grid(row=0, columnspan=2)

    Label(p_frame, text="Username:").grid(row=1, column=0)

    username = Label(p_frame, text=user)
    username.grid(row=1, column=1)

    Label(p_frame, text="Password:").grid(row=2, column=0)

    password = Label(p_frame, text=passw)
    password.grid(row=2, column=1)

    back = Button(p_frame, text="Back", command= lambda:[p_frame.destroy(), main()])
    back.grid(row=4, columnspan=2)

    Button(p_frame, text="Log Out", command= lambda:[log_out(), p_frame.destroy()]).grid(row=3, columnspan=2, pady=5)

    delete = Button(p_frame, text="Delete Account", command= lambda:[delete_account(), p_frame.destroy()])
    delete.grid(row=5, columnspan=2)

# Logs out the user
def log_out():
    global user
    global passw
    user = ""
    passw = ""
    main()

# Deletes the user account
def delete_account():
    d_frame = Frame(root)
    d_frame.pack()

    Label(d_frame, text="Are you sure you want to delete your account?").pack()

    confirm = Button(d_frame, text="Yes", command= lambda user = "", passw = "":[d_frame.destroy(), main(), os.remove("iteration1/assets/info.txt")])
    confirm.pack()

    back = Button(d_frame, text="No", command= lambda:[d_frame.destroy(), profile()])
    back.pack()
        
# Creates the login window
def login():
    try:
        f = open('iteration1/assets/info.txt', 'r')
        f.close()
    except FileNotFoundError:
        register_account()
        return
    
    global user
    global passw

    if user != "" and passw != "":
        profile()
        return

    l_frame = Frame(root)
    l_frame.pack()

    Label(l_frame, text="Login", font=("Helvetica", 20, "bold")).grid(row=0, columnspan=2)
    
    Label(l_frame, text="Username").grid(row=1, column=0)

    username = Entry(l_frame)
    username.grid(row=2, column=0)

    Label(l_frame, text="Password").grid(row=1, column=1)

    password = Entry(l_frame, show="*")
    password.grid(row=2, column=1)

    submit = Button(l_frame, text="Submit", command= lambda:check_login(username, password, l_frame))
    submit.grid(row=3, columnspan=2)

    infomessage = Label(l_frame, text="")
    infomessage.grid(row=4, columnspan=2)

    Label(l_frame, text="Don't have an account?").grid(row=5, columnspan=2)
    register = Button(l_frame, text="Register", command= lambda:[register_account(), l_frame.destroy()])
    register.grid(row=6, columnspan=2)

    back = Button(l_frame, text="Back", command= lambda:[l_frame.destroy(), main()])
    back.grid(row=7, columnspan=2, pady=(10,0))

# Checks the login details
def check_login(username, password, l_frame):
    with open("iteration1/assets/info.txt", "r") as file:
        for line in file:
            info = line.strip().split(" : ")
            usern = username.get()
            pas = password.get()
            if info[0] == usern and info[1] == pas:
                l_frame.destroy()
                main()
                global user
                global passw
                user = usern
                passw = pas
                return
    info_message = Label(l_frame, text="Incorrect username or password")
    info_message.grid(row=4, columnspan=2, pady=5)

# Creates the register account window
def register_account():
    r_frame = Frame(root)
    r_frame.pack()

    Label(r_frame, text="Register", font=("Helvetica", 20, "bold")).grid(row=0, columnspan=2)
    
    Label(r_frame, text="Username").grid(row=1, column=0)

    username = Entry(r_frame)
    username.grid(row=1, column=1)
    
    Label(r_frame, text="Password").grid(row=2, column=0)
    
    password = Entry(r_frame, show="*")
    password.grid(row=2, column=1)

    submit = Button(r_frame, text="Submit", command= lambda:[create_account(username.get(), password.get(), error_message, r_frame)])
    submit.grid(row=3, columnspan=2)

    error_message = Label(r_frame, text="")
    error_message.grid(row=4, columnspan=2)

    back = Button(r_frame, text="Back", command= lambda:[r_frame.destroy(), main()])
    back.grid(row=5, columnspan=2)
    
    Label(r_frame, text="Already have an account?").grid(row=6, columnspan=2, pady=(10,0))
    Button(r_frame, text="Login", command= lambda:[login(), r_frame.destroy()]).grid(row=7, columnspan=2)

# Creates the account
def create_account(username, password, error_message, r_frame):
    if username == "" or password == "" or " : " in username or " : " in password:
        error_message.config(text="Please enter a valid username and password", wraplength=140, pady=5)
        return
    r_frame.destroy()
    with open("iteration1/assets/info.txt", "a") as file:
        file.write(f"{username} : {(password)}\n")
    global user
    global passw
    user = username
    passw = password
    main()

main()
root.mainloop()
