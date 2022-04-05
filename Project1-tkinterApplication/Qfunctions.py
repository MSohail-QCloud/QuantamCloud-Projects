import datetime
import csv
import sqlite3
from pathlib import Path
from tkinter import simpledialog
from tkinter.filedialog import asksaveasfile, asksaveasfilename
from datetime import datetime

def downloadInventory():
    path = (str(Path.cwd()) + "/sqlitedb.db")
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    cursor.execute("select * from inventory")
    data = [("csv file(*.csv)", "*.csv")]
    #file = asksaveasfilename(filetypes=data, defaultextension='.csv')
    file='/home/linaro/Documents/inventory.csv'
    print(file)
    with open(file, "w", newline='') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=",")
        csv_writer.writerow([i[0] for i in cursor.description])
        csv_writer.writerows(cursor)

def downloadHistory():
    path = (str(Path.cwd()) + "/sqlitedb.db")
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    cursor.execute("select * from History")
    data = [("csv file(*.csv)", "*.csv")]
    #file = asksaveasfilename(filetypes=data, defaultextension='.csv')
    file='/home/linaro/Documents/History.csv'
    # file will have file name provided by user.
    # Now we can use this file name to save file.
    with open(file, "w", newline='') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=",")
        csv_writer.writerow([i[0] for i in cursor.description])
        csv_writer.writerows(cursor)

def resetpassword():
    path = (str(Path.cwd()) + "/sqlitedb.db")
    conn = sqlite3.connect(path)
    s = simpledialog.askstring("Quantam", "please input your new password")
    # print(s)
    sql = ''' UPDATE Login SET enable = 1
                      WHERE id = ?'''
    cur = conn.cursor()
    cur.execute(sql, s)
    conn.commit()


def updateactiveuser(id, con):
    """
        update priority, begin_date, and end date of a task
        :param conn:
        :param task:
        :return: project id
        """
    sql = ''' UPDATE Login SET enable = 1
                  WHERE id = ?'''
    cur = con.cursor()
    cur.execute(sql, id)
    con.commit()


def updateqty(locid, userid, qty, con):
    sql = ''' UPDATE Inventory SET quantity = ?
                      WHERE LocationId = ?'''
    cur = con.cursor()
    cur.execute(sql, (qty, locid))
    con.commit()


def ClearActiveuser(con):
    """
        update priority, begin_date, and end date of a task
        :param conn:
        :param task:
        :return: project id
        """
    sql = ''' UPDATE Login SET enable = 0'''
    cur = con.cursor()
    cur.execute(sql)
    con.commit()


def findActiveUser(con):
    c = con.cursor()
    c.execute('SELECT * from Login WHERE enable=1')
    row = c.fetchone()
    return row[2]


def addadminlog(invid, userid, username, recieveqty, issueqty, con):
    sql = ''' INSERT INTO History VALUES(?, ?, ?, ?, ?) '''
    cur = con.cursor()
    dt = datetime.now().strftime("%B %d, %Y")
    p = (int(invid), dt, username, issueqty, recieveqty)
    cur.execute(sql, p)
    con.commit()
