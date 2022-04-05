import sqlite3


conn = sqlite3.connect('sqlitedb.db')
c = conn.cursor()


class SqliteDBlib:

    def tables(self):
        c.execute("""CREATE TABLE Login(
        Id int PRIMARY KEY,
        username text,
        password text,
        usertype int,
        enable int
         
        )""")
        c.execute("""CREATE TABLE Inventory (
        InventoryId int PRIMARY KEY,
        LocationId text,
        Itemame text,
        ERPcode text,
        quantity int     
        )""")
        c.execute("""CREATE TABLE History(        
        InventoryId int ,
        current_datetime REAL DEFAULT (datetime('now', 'localtime')),
        issue_by text,
        issue_on text,
        issue_qty int,
        receive_on text,
        receive_qty int,
        enter_by text,
        enter_on text
        )""")

        # c.commit()

    def Insert(query):
        with conn:
            c.execute(query)
            c.commit()


    def Select(query):
        with conn:
            c.execute(query)
            c.commit()

    def treeView(self, str):
        conn = sqlite3.connect("TRIAL.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM profile")
        rows = cur.fetchall()
        return rows
        conn.close()

    def Update(query):
        with conn:
            c.execute(query)
            c.commit()

SqliteDBlib.tables()