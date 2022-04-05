#!/usr/bin/env python3


import os
import sqlite3
from pathlib import Path
from tkinter import *
from tkinter import messagebox
import tkinter as tk
from tkinter import ttk
import Qfunctions
# from ttkthemes import themed_tk as tka
from ttkthemes import themed_tk as tkk


def drawKeyboard(parent):
    keyboardFrame = tk.Frame(parent)
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
        sect_frame = tk.Frame(keyboardFrame)
        sect_frame.pack(side='left', expand='yes', fill='both', padx=10, pady=10, ipadx=10, ipady=10)
        for key_group in sect_vals:
            group_frame = tk.Frame(sect_frame)
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


def Ok():
    #try:
    if (username_login_entry.get() == ""):
        messagebox.showinfo("Enter Username")
        return
    if (password__login_entry.get() == ""):
        messagebox.showinfo("Quantam","Enter Password")
        return
    # Connect to database
    # db = sqlite3.connect("D:\\QuantamCloud\\QProject1-tkinterApplication\\sqlitedb.db")
    path = (str(Path.cwd()) + "/sqlitedb.db")
    #messagebox.showinfo("Quantam",str(path))
    db = sqlite3.connect(path)
    Qfunctions.ClearActiveuser(db)
    c = db.cursor()
    parameterlist = [username_login_entry.get(), password__login_entry.get()]
    c.execute('SELECT * from Login WHERE username=? and password=?', parameterlist)
    row = c.fetchone()
    if row is None:
        return
    if len(row) > 0:
        #messagebox.showinfo("Quantam","Successfull")
        userid = (row[0])
        Qfunctions.updateactiveuser((str(userid)), db)
        # messagebox.showinfo("Quantam Cloud", "Login Success "+row[0]+"c"+row[1]+"")
        os.system("python3 myapp.py")
        #exec(open('./myapp.py').read())
        login_screen.destroy()
    else:
        messagebox.showinfo("Quantam", "Enter Correct Password")
#except Exception as e:
    #messagebox.showerror("Q Error", sys.exc_info()[0])


#login_screen = Tk()
login_screen = tkk.ThemedTk(theme="itft1")
login_screen.title("Login")
login_screen.geometry("800x400")
t1 = StringVar()
p1 = StringVar()
ttk.Label(login_screen, font=50, text="Please enter login details").pack()
ttk.Label(login_screen, text="", font=30).pack()
ttk.Label(login_screen, text="Username", font=30).pack()
username_login_entry = ttk.Entry(login_screen, textvariable=t1, width=50, font=30, justify=CENTER)
username_login_entry.pack()
username_login_entry.focus()
ttk.Label(login_screen, text="", font=30).pack()
ttk.Label(login_screen, text="Password", font=30).pack()
password__login_entry = ttk.Entry(login_screen, textvariable=p1, show='*', width=50, font=30, justify=CENTER)
password__login_entry.pack()
ttk.Label(login_screen, text="").pack()

ttk.Button(login_screen, text="Login", width=20, command=Ok).pack()
frame1 = ttk.Frame(login_screen, relief=RIDGE, name='frame1').pack()
drawKeyboard(frame1)


def remember_focus(event):
    global focused_entry
    focused_entry = event.widget


def key_command(event):
    global focused_entry
    if event == "backspace":
        focused_entry.delete(0, "end")
    elif event == "delete":
        focused_entry.delete(0, "end")
    else:
        focused_entry.insert("end", event)
    #focused_entry.insert("end", event)
    # pyautogui.press(event)
    return

username_login_entry.bind('<FocusIn>',remember_focus)
password__login_entry.bind('<FocusIn>',remember_focus)
# END Tab Button Fucntion
#login_screen.bind_class("Entry", "<FocusIn>", remember_focus)
login_screen.title("Quantam - Electronics Application - Login")
#login_screen.iconbitmap(str(Path.cwd()) +'\images\QuantamCloud.ico')
# keyboard end
login_screen.mainloop()
# 1200*600
# format(str(Path.cwd()) + '\plugin'))
