from tkinter import *

root = Tk()
root.geometry("1000x500")
root.resizable(False, False)

m_frame = Frame(root)
m_frame.grid()
buffer = Label(m_frame, width=18, height=9)
buffer.grid(row=0, column=0)

title = Label(m_frame, text="Welcome!", font=("Helvetica", 40, "bold"), fg="green")
title.grid(row=0, column=2, padx=(0, 0))

reminder = Button(m_frame, width=30, height=15, text="Next collection day")
reminder.grid(column=1, row=1, padx=10, pady=10)
reminder.grid_propagate(False)

guide = Button(m_frame, width=30, height=15, text="Recycling guide")
guide.grid(column=2, row=1, padx=10, pady=10)
guide.grid_propagate(False)

account = Button(m_frame, width=30, height=15, text="Manage Account")
account.grid(column=3, row=1, padx=10, pady=10)
account.grid_propagate(False)

root.mainloop()
