from tkinter import *
from tkinter import messagebox
#from tkinter import OS

def Ok():
    if username_login_entry.get() == "Admin" and password__login_entry.get() == "123":
        messagebox.showinfo("", "Login Success")
        os.system("Project1 mainscreen.py")
        root.destroy()
    else:
        messagebox.showinfo("", "Enter Correct Password")


login_screen=Tk()
login_screen.title("Change Password")
login_screen.geometry("300x250")
Label(login_screen, text="Please Enter Your Credential").pack()
Label(login_screen, text="").pack()
Label(login_screen, text="Username").pack()
username_login_entry = Entry(login_screen, textvariable="username")
username_login_entry.pack()
Label(login_screen, text="").pack()
Label(login_screen, text="Old Password").pack()
password__login_entry = Entry(login_screen, textvariable="password", show= '*')
password__login_entry.pack()
Label(login_screen, text="New Password").pack()
password__login_entryn = Entry(login_screen, textvariable="password", show= '*')
password__login_entryn.pack()
Label(login_screen, text="Confirm Password").pack()
password__login_entryc = Entry(login_screen, textvariable="password", show= '*')
password__login_entryc.pack()
Label(login_screen, text="").pack()
Button(login_screen, text="Login", width=10, height=1,command=Ok).pack()








login_screen.mainloop()
#1200*600