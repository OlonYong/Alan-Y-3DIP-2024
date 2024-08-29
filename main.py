from tkinter import *
from tkinter import ttk, PhotoImage
import datetime
import openpyxl
from PIL import ImageTk, Image


root = Tk()
root.geometry("1000x550")
root.resizable(False, False)

loaded_images = []

def main():
    m_frame = Frame(root)
    m_frame.grid()
    buffer = Label(m_frame, width=18, height=9)
    buffer.grid(row=0, column=0)

    title = Label(m_frame, text="Welcome!", font=("Helvetica", 40, "bold"), fg="green")
    title.grid(row=0, column=2, padx=(0, 0))

    reminder = Button(m_frame, width=30, height=15, text="Next collection day", command= lambda:[m_frame.destroy(), collection()])
    reminder.grid(column=1, row=1, padx=10, pady=10)
    reminder.grid_propagate(False)

    guide = Button(m_frame, width=30, height=15, text="Recycling guide", command= lambda:[m_frame.destroy(), guides()])
    guide.grid(column=2, row=1, padx=10, pady=10)
    guide.grid_propagate(False)

    account = Button(m_frame, width=30, height=15, text="Manage Account")
    account.grid(column=3, row=1, padx=10, pady=10)
    account.grid_propagate(False)

def collection():
    c_frame = Frame(root)
    c_frame.pack()

    heading = Label(c_frame, text="Enter your next collection date")
    heading.pack()

    date = Frame(c_frame)
    date.pack()

    day_var = StringVar()
    day = ttk.Combobox(date, textvariable=day_var)
    day["values"] = tuple(str(i) for i in range(1, 31)) 
    day.grid(row=0, column=0)

    Label(date, text="/").grid(row=0, column=1)

    month_var = StringVar()
    month = ttk.Combobox(date, textvariable=month_var)
    month["values"] = ("January", "February", "March", "April", "June", "July", "August", "September", "October", "November", "December")
    month.grid(row=0, column=2)
    check_recycling = IntVar()
    is_recycling = Checkbutton(c_frame, text="Recycling?", variable=check_recycling)
    is_recycling.pack()

    calculate_day(day_var, month_var, check_recycling)

    submit = Button(c_frame, text="Submit", command= lambda:[c_frame.destroy(), reminder()])
    submit.pack()

def calculate_day():
    datetime.datetime.now()

def reminder():
    r_frame = Frame(root)
    r_frame.pack()

    Label(r_frame, text="Your next collection day is:").pack()





    day = 5
    month = "March"
    Label(r_frame, text=f"{day} {month}").pack()


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
        frame.append(Button(catalogue,text=f"{data[i][0]}", width=40, height=10, command= lambda i=i: [load_panels(infopanels[i]), g_frame.destroy()]))
        frame[i].grid(row=i-((i)%2), column=((i)%2))

def load_data():
    guide_data = []
    path = "testdatabase.xlsx"
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

def info_panels(data):
    info_panels = []
    for i in range(0, len(data)):
        frame = Frame(root)
        print(data[i][2])
        Label(frame, text=data[i][0], font=("Helvetica", 40, "bold")).pack()
        Label(frame, image=data[i][2]).pack()
        Label(frame, text=data[i][1], wraplength=500, pady=10).pack()
        info_panels.append(frame)
    return info_panels

def load_panels(panel):
    panel.pack()
    back = Button(panel, text="Back", command= lambda:[panel.destroy(), guides()])
    back.pack()


main()
root.mainloop()
