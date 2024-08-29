from tkinter import *
from tkinter import ttk
import datetime
import openpyxl
from PIL import ImageTk, Image
import os
import webbrowser


root = Tk()
	@@ -13,8 +15,8 @@

def main():
    m_frame = Frame(root)
    m_frame.pack()
    buffer = Label(m_frame, height=9)
    buffer.grid(row=0, column=0)

    title = Label(m_frame, text="Welcome!", font=("Helvetica", 40, "bold"), fg="green")
	@@ -28,57 +30,92 @@ def main():
    guide.grid(column=2, row=1, padx=10, pady=10)
    guide.grid_propagate(False)

    account = Button(m_frame, width=30, height=15, text="Manage Account", command= lambda:[m_frame.destroy(), login()])
    account.grid(column=3, row=1, padx=10, pady=10)
    account.grid_propagate(False)

def collection():
    c_frame = Frame(root)
    c_frame.pack()

    if os.path.exists("dates.txt"):
        with open("dates.txt", "r") as file:
            for line in file:
                year, month, day, is_recycling = line.split("-")
            if datetime.datetime.now() < datetime.datetime(int(year), int(month), int(day)):
                reminder()
                return

    heading = Label(c_frame, text="Enter your next collection date", font=("Helvetica", 20, "bold"))
    heading.pack()

    date = Frame(c_frame)
    date.pack()

    Label(date, text="Day").grid(row=0, column=0)

    day_var = StringVar()
    day = ttk.Combobox(date, textvariable=day_var)
    day["values"] = tuple(str(i) for i in range(1, 32)) 
    day.grid(row=1, column=0)

    Label(date, text="/").grid(row=1, column=1)

    Label(date, text="Month").grid(row=0, column=2)
    month_var = StringVar()
    month = ttk.Combobox(date, textvariable=month_var)
    month["values"] = tuple(str(i) for i in range(1, 13))
    month.grid(row=1, column=2)


    check_recycling = IntVar()
    is_recycling = Checkbutton(c_frame, text="Is there recycling?", variable=check_recycling)
    is_recycling.pack()

    Button(c_frame, command= lambda: webbrowser.open_new("https://www.aucklandcouncil.govt.nz/rubbish-recycling/rubbish-recycling-collections/Pages/rubbish-recycling-collection-days.aspx"), text="Don't know your collection? Check here!").pack(pady=5)

    submit = Button(c_frame, text="Submit", command= lambda:[calculate_day(day_var.get(), month_var.get(), check_recycling.get()), c_frame.destroy(), reminder()])
    submit.pack()

    back = Button(c_frame, text="Back", command= lambda:[c_frame.destroy(), main()])
    back.pack()


def calculate_day(day, month, is_recycling):
    collection_day = int(day)
    collection_month = int(month)
    recycling = is_recycling
    next_date = datetime.datetime(datetime.datetime.now().year, collection_month, collection_day )
    next_date += datetime.timedelta(days=7)
    if recycling:
        recycling = False
    elif recycling == False:
        recycling = True

    with open("dates.txt", "w") as file:
        file.write(str(next_date.date())+"-"+str(recycling))

    return collection_day, collection_month, recycling

def reminder():
    r_frame = Frame(root)
    r_frame.pack()

    with open("dates.txt", "r") as file:
        for line in file:
            year, month, day, is_recycling = line.split("-")
        if datetime.datetime.now() > datetime.datetime(int(year), int(month), int(day)):
            calculate_day(day, month, is_recycling)

    Label(r_frame, text="Your next collection day is:").pack()
    Label(r_frame, text=f"{day}/{month}/{year}").pack()
    if is_recycling == True:
        Label(r_frame, text="Recycling: Yes").pack()
    else:
        Label(r_frame, text="Recycling: No").pack()

    back = Button(r_frame, text="Back", command= lambda:[r_frame.destroy(), main()])
    back.pack()

def guides():
    data = load_data()
	@@ -91,9 +128,12 @@ def guides():
    frame = []
    infopanels = info_panels(data)
    for i in range(6):
        frame.append(Button(catalogue, text=f"{data[i][0]}", width=40, height=10, command= lambda i=i: [load_panels(infopanels[i]), g_frame.destroy()]))
        frame[i].grid(row=i-((i)%2), column=((i)%2))

    back = Button(g_frame, text="Back", command= lambda:[g_frame.destroy(), main()])
    back.pack()

def load_data():
    guide_data = []
    path = "testdatabase.xlsx"
	@@ -113,7 +153,6 @@ def info_panels(data):
    info_panels = []
    for i in range(0, len(data)):
        frame = Frame(root)
        Label(frame, text=data[i][0], font=("Helvetica", 40, "bold")).pack()
        Label(frame, image=data[i][2]).pack()
        Label(frame, text=data[i][1], wraplength=500, pady=10).pack()
	@@ -125,6 +164,136 @@ def load_panels(panel):
    back = Button(panel, text="Back", command= lambda:[panel.destroy(), guides()])
    back.pack()

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

    delete = Button(p_frame, text="Delete Account", command= lambda:[delete_account(), p_frame.destroy()])
    delete.grid(row=5, columnspan=2)

def delete_account():
    d_frame = Frame(root)
    d_frame.pack()

    Label(d_frame, text="Are you sure you want to delete your account?").pack()

    confirm = Button(d_frame, text="Yes", command= lambda:[d_frame.destroy(), main(), os.remove("info.txt")])
    confirm.pack()

    back = Button(d_frame, text="No", command= lambda:[d_frame.destroy(), profile()])
    back.pack()


def login():
    try:
        f = open('info.txt', 'r')
        f.close()
    except FileNotFoundError:
        register_account()
        return

    global user
    global passw
    user = ""
    passw = ""

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

def check_login(username, password, l_frame):
    with open("info.txt", "r") as file:
        for line in file:
            info = line.strip().split(" : ")
            user = username.get()
            passw = password.get()
            if info[0] == user and info[1] == passw:
                l_frame.destroy()
                profile()

                return
    info_message = Label(l_frame, text="Incorrect username or password")
    info_message.grid(row=4, columnspan=2, pady=5)

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

def create_account(username, password, error_message, r_frame):
    if username == "" or password == "":
        error_message.config(text="Please enter a username and password", wraplength=140, pady=5)
        return
    r_frame.destroy()
    with open("info.txt", "a") as file:
        file.write(f"{username} : {(password)}\n")
    main()

main()
root.mainloop()
