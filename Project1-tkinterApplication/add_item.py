from pathlib import Path
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from tkinter.filedialog import asksaveasfile, asksaveasfilename
import csv
import os
import tkinter as tt
from ttkthemes import themed_tk as tk
# from pynput.keyboard import Key, Controller
import sqlite3


def drawKeyboard(parent):
    keyboardFrame = ttk.Frame(parent)
    keyboardFrame.pack()
    keys = [
        [("Alpha Keys"),
         [('q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p'),
          (' ', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l'),
          ('capslock', 'z', 'x', 'c', 'v', 'b', 'n', 'm'),
          ('delete', 'backspace', 'home', 'end')
          ]
         ],
        [("Numeric Keys"),
         [('7', '8', '9'),
          ('4', '5', '6'),
          ('1', '2', '3'),
          (' ', '0', ' ')
          ]
         ]
    ]

    for key_section in keys:
        sect_vals = key_section[1]
        sect_frame = ttk.Frame(keyboardFrame)
        sect_frame.pack(side='left', expand='yes', fill='both', padx=10, pady=10, ipadx=10, ipady=10)
        for key_group in sect_vals:
            group_frame = ttk.Frame(sect_frame)
            group_frame.pack(side='top', expand='yes', fill='both')
            for key in key_group:
                key = key.capitalize()
                if len(key) <= 1:
                    key_button = ttk.Button(group_frame, text=key, width=4)
                else:
                    key_button = ttk.Button(group_frame, text=key.center(5, ' '))
                if ' ' in key:
                    key_button['state'] = 'disable'
                key_button['command'] = lambda q=key.lower(): key_command(q)
                key_button.pack(side='left', fill='both', expand='yes')


def remember_focus(event):
    global focused_entry
    focused_entry = event.widget


def key_command(event):
    if event == "backspace":
        focused_entry.delete(0, "end")
    else:
        focused_entry.insert("end", event)
        
    # pyautogui.press(event)
    return


def Update():
    rack_get = rack_entry.get()
    erp_get = erp_entry.get()
    des_get = des_entry.get()
    if rack_get=="":
        messagebox.showinfo("Quantam info","Rack Number cannot be empty.")
    if rack_get.isdigit():
        conn = sqlite3.connect(path)
        curr = conn.cursor()
        query = '''update 'Inventory' set itemame = ?,ERPCode = ? where InventoryId = ?'''
        data = (des_get, erp_get, rack_get)
        curr.execute(query, data)
        conn.commit()
        messagebox.showinfo("Quantam Info","Successful")
    else:
        messagebox.showerror("Quantam Error", "Rack Number is not digit.")



def Insert():
    rack_get = rack_entry.get()
    erp_get = erp_entry.get()
    des_get = des_entry.get()
    if rack_get=="":
        messagebox.showinfo("Quantam Infor", "Rack Number cannot be empty.")
        return
    if rack_get.isdigit():
        path = (str(Path.cwd()) + "/sqlitedb.db")
        conn = sqlite3.connect(path)
        curr = conn.cursor()
        query = '''insert into 'Inventory'('InventoryId','LocationId','Itemame','ERPcode','quantity')
             values (?, ?, ?, ?, ?)'''
        data = (rack_get, rack_get, des_get, erp_get, 0)
        curr.execute(query, data)
        conn.commit()
        messagebox.showinfo("Quantam Info","Successful")
    else:
        messagebox.showerror("Quantam Alert","Rack Number is not digit.")

def callback():
    q2 = sv.get()
    conn = sqlite3.connect(path)
    curr = conn.cursor()
    query = "SELECT LocationId,Itemame,ERPcode,quantity FROM Inventory WHERE  LocationId = '" + q2 + "'"
    curr.execute(query)
    rows = curr.fetchone()
    if rows is None:
        global b_insert, b_update
        # b_insert = Button(window,state = NORMAL)
        # b_update = Button(window,state = DISABLED)
        b_insert["state"] = NORMAL
        b_update["state"] = DISABLED
    else:
        b_insert["state"] = DISABLED
        b_update["state"] = NORMAL
        erp_entry.delete(0,'end')
        des_entry.delete(0,'end')
        erptxt.set(rows[2])
        destxt.set(rows[1])
        #erp_entry.insert(0, rows[2])
        #des_entry.insert(0, rows[1])
    return True


'''def open_keyboard(self):
    # print("keyboard")
    os.system('wmic process where name="TabTip.exe" delete')
    os.system("C:\\PROGRA~1\\COMMON~1\\MICROS~1\\ink\\tabtip.exe")'''

path = (str(Path.cwd()) + "/sqlitedb.db")
conn = sqlite3.connect(path)
curr = conn.cursor()
window = tk.ThemedTk(theme="itft1")
sv = StringVar()
erptxt=StringVar()
destxt=StringVar()

mydata = []
# window.get_themes()
# window.set_theme("Blue")
frame = ttk.Frame(window)
kbFrame = ttk.Frame(window)
frame.place(x=0, y=0, width=1024, height=350)
kbFrame.place(x=70, y=350)
frame.config(relief=RIDGE)
kbFrame.config(height=300, width=1024, relief=RIDGE)

ttk.Label(frame, text='ITEM ADDITION', font=("KABEL", 23)).place(x=450, y=0)
ttk.Label(frame, text='Rack No.', font=("KABEL", 15)).place(x=100, y=50)
ttk.Label(frame, text='ERP Code', font=("KABEL", 15)).place(x=100, y=100)
ttk.Label(frame, text='Description', font=("KABEL", 15)).place(x=100, y=150)

rack_entry = Entry(frame, font=20, textvariable=sv, validate="focusout", validatecommand=callback)
rack_entry.place(x=220, y=50, width=200)
erp_entry = Entry(frame,font=20, textvariable=erptxt)
erp_entry.place(x=220, y=100, width=200)
des_entry = Entry(frame, font=20, textvariable=destxt)
des_entry.place(x=220, y=150, width=200)


# download_btn = ttk.Button(frame, text="DOWNLOAD", command=SaveFile).place(x=-75, y=70, width=150, height=75)


b_insert = ttk.Button(frame, text="INSERT", command=Insert)
b_insert.place(x=350, y=250, width=150, height=75)
b_update = ttk.Button(frame, text="UPDATE", command=Update, state=NORMAL)
b_update.place(x=550, y=250, width=150, height=75)
close_btn = ttk.Button(frame, text="CLOSE", command=window.destroy).place(x=750, y=250, width=150, height=75)

drawKeyboard(kbFrame)

# rack_entry.bind("<KeyRelease>",binds)
rack_entry.delete(0, END)
erp_entry.delete(0, END)
des_entry.delete(0, END)
# q2 = sv.get()
# rack_entry.bind("<KeyRelease>",q2)
# ent5.bind('<FocusIn>',remember_focus)
rack_entry.focus()
window.bind_class("Entry", "<FocusIn>", remember_focus)
window.title("Quantam - Electronics Application - Add/Update Items")
# window.iconbitmap('images/QuantamCloud.ico')
window.maxsize(1024, 600)
window.minsize(1024, 600)
conn.close()
window.mainloop()
