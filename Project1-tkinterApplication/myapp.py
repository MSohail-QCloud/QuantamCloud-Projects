#!/usr/bin/env python3
import os
import tkinter
from pathlib import Path
from tkinter import *
from tkinter import ttk
from ttkthemes import themed_tk as tk
import sqlite3
import tkinter.font as tkFont
import Qfunctions as qf



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
    global focused_entry
    if event == "backspace":
        focused_entry.delete(0, "end")
    elif event == "delete":
        focused_entry.delete(0, "end")
    else:
        focused_entry.insert("end", event)
    # pyautogui.press(event)
    return



def windowload():
    # Connect to database
    # path = (str(Path.cwd()) + "\sqlitedb.db")
    path = (str(Path.cwd()) + "/sqlitedb.db")
    db = sqlite3.connect(path)
    c = db.cursor()
    c.execute('SELECT * from Login WHERE enable=1')
    row = c.fetchone()
    if row is None:
        exit(0)
    if len(row) > 0:
        global wuser, wuserid, username, ent4, ent5
        wuser.set(str(row[3]))
        wuserid.set(str(row[0]))
        username.set(str(row[1]))
        if wuser.get() == "admin":
            ent4.config(state='disabled')
        elif wuser.get() == "user":
            ent5.config(state='disabled')


def updatetreeview(rows):
    global trv
    trv.delete(*trv.get_children())
    for i in rows:
        trv.insert('', 'end', values=i)


def search():
    global q, updatetreeview
    path = (str(Path.cwd()) + "/sqlitedb.db")
    db = sqlite3.connect(path)
    cur = db.cursor()
    q2 = q.get()
    query = "SELECT LocationId,Itemame,ERPcode,quantity FROM Inventory WHERE Itemame like '%" + q2 + "%' or LocationId like '%" + q2 + "%'"
    cur.execute(query)
    rows = cur.fetchall()
    updatetreeview(rows)


def clear():
    global cur, updatetreeview
    query = "SELECT LocationId,Itemame,ERPcode,quantity FROM Inventory"
    cur.execute(query)
    rows = cur.fetchall()
    updatetreeview(rows)


def getrow(event):
    global trv, t1, t2, t3
    print("get row")
    #messagebox.showinfo("Quantam", "abc")
    rowid = trv.identify_row(event.y)
    item = trv.item(trv.focus())
    t1.set(item['values'][0])
    #t1.set("test")
    #ent1.insert(0,t1)
    t2.set(item['values'][1])
    t3.set(item['values'][3])
    print(t1.get())
    print("get row end")


def update_Qty():
    global t6, t5, t1, wuserid, username, t4, cur, updatetreeview
    if t6.get() == "":
        return
    if wuser.get() == "admin":
        if t5.get() == "":
            return
        qf.addadminlog(t1.get(), wuserid.get(), username.get(), t5.get(),0, conn)
    elif wuser.get() == "user":
        if t4.get() == "":
            return
        qf.addadminlog(t1.get(), wuserid.get(), username.get(), 0, t4.get(), conn)
    qf.updateqty(t1.get(), wuserid.get(), t6.get(), conn)
    query = "SELECT LocationId,Itemame,ERPcode,quantity FROM Inventory"
    cur.execute(query)
    rows = cur.fetchall()
    updatetreeview(rows)
    t4.set('')
    t5.set('')


def callback_Minus(prevQ, issueQ):
    global t4, ent6, t6
    if prevQ.get() == "":
        return
    if issueQ.get() == "":
        return
    if int(issueQ.get())>int(prevQ.get()):
        t4.set(prevQ.get())
    ent6.delete(0, 'end')
    t6.set(str(int(prevQ.get()) - int(issueQ.get())))

def callback_rm(prevQ, issueQ):
    global ent4, ent5, t6, ent6
    ent4.delete(0, 'end')
    ent5.delete(0, 'end')
    t6.set('')
    ent6.delete(0, 'end')


def callback_Add(prevQ, recievQ):
    global ent6,t6
    ent6.delete(0, 'end')
    if prevQ.get() == "":
        return
    if recievQ.get() == "":
        return
    ent6.delete(0, 'end')
    t6.set(str(int(prevQ.get()) + int(recievQ.get())))

def OpenAdditem():
    #exec(open('add_item.py').read())
    os.system("python3 add_item.py")


        
#conn = sqlite3.connect("sqlitedb.db")
#cur = conn.cursor()
window = tk.ThemedTk(theme="itft1")
q = StringVar()
t1 = StringVar()
t2 = StringVar()
t3 = StringVar()
t4 = StringVar()
t5 = StringVar()
t6 = StringVar()
wuser = StringVar()
wuserid = StringVar()
username = StringVar(window, '')


frame1 = ttk.Frame(window, relief=RIDGE, width=100, height=200)
frame2 = ttk.Frame(window, relief=RIDGE, width=100)  # search
kbframe = ttk.Frame(window, relief=RIDGE)

frame1.place(x=0, y=0)
frame2.place(x=610, y=0)
kbframe.place(x=70, y=350)

wrapper2 = ttk.LabelFrame(frame2, text="Search")
wrapper1 = ttk.LabelFrame(frame1)
wrapper3 = ttk.LabelFrame(frame2)



MenuFont = tkFont.Font(family="KABEL", size=15)
Fontlbl = tkFont.Font(family="KABEL", size=15)
BtnFont = tkFont.Font(family="KABEL", size=20)
TreeviewFont = tkFont.Font(family="KABEL", size=20)
EntryFont = tkFont.Font(family="KABEL", size=15)

# *********************************Menu Start*********************************
mymenu = Menu(window, font=MenuFont)
window.config(menu=mymenu)
# Menu item
filemenu = Menu(mymenu, font=MenuFont)
mymenu.add_cascade(font=MenuFont, label="File", menu=filemenu)
filemenu.add_command(font=MenuFont, label="Add/Update Inventory", command=OpenAdditem)
filemenu.add_separator()
filemenu.add_command(font=MenuFont, label="Exit", command=window.quit)
filemenu.add_separator()
# Edit menu
EditMenu = Menu(mymenu, font=MenuFont)
mymenu.add_cascade(label="Edit", font=MenuFont, menu=EditMenu)
EditMenu.add_command(label="Reset Password", font=MenuFont, command=qf.resetpassword)
EditMenu.add_separator()
# download menu
downloadMenu = Menu(mymenu, font=MenuFont)
mymenu.add_cascade(label="Download", menu=downloadMenu, font=MenuFont)
downloadMenu.add_command(label="Download Item list", font=MenuFont, command=qf.downloadInventory)
downloadMenu.add_separator()
downloadMenu.add_command(label="Download History", font=MenuFont, command=qf.downloadHistory)
downloadMenu.add_separator()

# *********************Frame Start**************************************

wrapper2.pack(side=TOP)
wrapper1.pack(side=TOP)
wrapper3.pack(side=LEFT)

trv = ttk.Treeview(wrapper1, columns=("1", "2", "3", "4"), show="headings",height=15)
trv.pack()

'''# Constructing vertical scrollbar
# with treeview
verscrlbar = ttk.Scrollbar(window,
                           orient="vertical",
                           command=trv.xview)

# Calling pack method w.r.to vertical
# scrollbar
verscrlbar.pack(side='right', fill='x')

# Configuring treeview
trv.configure(xscrollcommand=verscrlbar.set)'''

trv.column("# 1", anchor=CENTER, stretch=NO, width=100)
trv.column("# 2", anchor=CENTER, stretch=NO, width=250)
trv.column("# 3", anchor=CENTER, stretch=NO, width=150)
trv.column("# 4", anchor=CENTER, stretch=NO, width=100)

trv.heading(1, text="Location Id")
trv.heading(2, text="Item Detail")
trv.heading(3, text="ERP Code")
trv.heading(4, text="Quantity")


path = (str(Path.cwd()) + "/sqlitedb.db")
db = sqlite3.connect(path)
cur = db.cursor()
query = "SELECT LocationId,Itemame,ERPcode,quantity FROM Inventory"
cur.execute(query)
rows = cur.fetchall()
#print("main form lin 255")
updatetreeview(rows)
#print ("after main")
# search section

# lbl = ttk.Label(wrapper2, text="Search", font=Fontlbl)
# lbl.pack(side=tkinter.LEFT, padx=1)
ent = ttk.Entry(wrapper2, textvariable=q, font=EntryFont)
ent.pack(side=tkinter.LEFT, padx=2)
btn = ttk.Button(wrapper2, text="Search", command=search)
btn.pack(side=tkinter.LEFT, padx=2)
# btn['font'] = BtnFont
cbtn = ttk.Button(wrapper2, text="Clear", command=clear)
cbtn.pack(side=tkinter.LEFT, padx=2)
# cbtn['font'] = BtnFont

# user data section
lbl1 = ttk.Label(wrapper3, text="Location ID", font=Fontlbl)
lbl1.grid(row=0, column=0, padx=5, pady=3)
ent1 =ttk.Entry(wrapper3, textvariable=t1, state=DISABLED, font=EntryFont)
ent1.grid(row=0, column=1, padx=5, pady=3)

lbl2 = ttk.Label(wrapper3, text="Detail", font=Fontlbl)
lbl2.grid(row=1, column=0, padx=5, pady=3)
ent2 = ttk.Entry(wrapper3, textvariable=t2, state=DISABLED, font=EntryFont)
ent2.grid(row=1, column=1, padx=5, pady=3)
t3.trace("w", lambda name, index, mode, sv=t3: callback_rm(t3, t4))

lbl3 = ttk.Label(wrapper3, text="Qty", font=Fontlbl)
lbl3.grid(row=2, column=0, padx=5, pady=3)
ent3 = ttk.Entry(wrapper3, textvariable=t3, state=DISABLED)
ent3.grid(row=2, column=1, padx=5, pady=3)

t4.trace("w", lambda name, index, mode, sv=t4: callback_Minus(t3, t4))
lbl4 = ttk.Label(wrapper3, text="Issue Qty", font=Fontlbl)
lbl4.grid(row=3, column=0, padx=5, pady=3)
ent4 = ttk.Entry(wrapper3, textvariable=t4, font=EntryFont)
ent4.grid(row=3, column=1, padx=5, pady=3)

t5.trace("w", lambda name, index, mode, sv=t5: callback_Add(t3, t5))
lbl5 = ttk.Label(wrapper3, text="Received Qty", font=Fontlbl)
lbl5.grid(row=4, column=0, padx=5, pady=3)
ent5 = ttk.Entry(wrapper3, textvariable=t5, font=EntryFont)
ent5.grid(row=4, column=1, padx=5, pady=3)

lbl6 = ttk.Label(wrapper3, text="Remaining Qty", font=Fontlbl)
lbl6.grid(row=5, column=0, padx=5, pady=3)
ent6 = ttk.Entry(wrapper3, textvariable=t6, state='disabled', font=EntryFont)
ent6.grid(row=5, column=1, padx=5, pady=3)

upd_btn = ttk.Button(wrapper3, text="Update", command=update_Qty)
upd_btn.grid(row=6, column=1, padx=5, pady=3)
# upd_btn['font'] = BtnFont
ent.bind('<FocusIn>', remember_focus)
ent4.bind('<FocusIn>',remember_focus)
ent5.bind('<FocusIn>',remember_focus)

#t3.trace_add('write',callback_rm(t3,t4))
#t4.trace_add('write',callback_Minus(t3, t4))
#t5.trace_add('write',callback_Add(t3, t5))
window.bind('<Visibility>', windowload())
drawKeyboard(kbframe)
# *************************************
trv.bind('<Double 1>', getrow)
window.bind_class("Entry", "<FocusIn>", remember_focus)
window.title("Quantam - Electronics Application - Main")
#window.iconbitmap('images/QuantamCloud.ico')
window.minsize(1024,600)
window.maxsize(1024, 600)

#window.attributes('-fullscreen', True)
#window.state('zoomed')
window.mainloop()
