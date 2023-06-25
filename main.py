import sqlite3
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk


class Main_app(tk.Tk):
    def __init__(self):
        # The inits... you get the jist.
        super().__init__()

        self.title("Plan and Execute")
        self.geometry("500x500")

        self.print_list()

        self.add_list = ttk.Button(self, text="+")
        self.add_list.grid(row=0, column=0)
        self.add_list["command"] = self.create_list

        self.add_item = ttk.Button(self, text="+")
        self.add_item.grid(row=0, column=1)
        self.add_item["command"] = self.add_item



    def print_items(self):
        self.rows = 1
        con = sqlite3.connect("database.db")
        c = con.cursor()
        c.execute("SELECT item_name, complete FROM {} ORDER BY completed, item_list")
        items = c.fetchall()
        for item in items:
            self.item = ttk.Label(self, text=str(item[2]))
            self.item.grid(column=1, row=self.rows)
            self.rows += 1

        con.close()

    def print_list(self):
        # Creating list for lists and list of items if database doesn't exist
        self.rows = 1
        con = sqlite3.connect("database.db")
        curser_obj = con.cursor()
        curser_obj.execute(
            "CREATE TABLE IF NOT EXISTS lists_list (list_name TEXT PRIMARY KEY)"
        )
        curser_obj.execute(
            "CREATE TABLE IF NOT EXISTS item_list (list name TEXT, item_name TEXT, completed INTERGER"
        )
        curser_obj.execute("SELECT * FROM lists_list")
        lists = curser_obj.fetchall()

        # Print List
        for list in lists:
            self.list = ttk.Button(self, text=str(list[1]))
            self.list.grid(
                column=0, row=self.rows
            )
            self.list["command"] = self.print_items
            self.rows += 1
        con.commit()
        con.close()

    def add_item(self):
        self.createitem_window.destroy()
        con = sqlite3.connect('database.db')
        c = con.cursor()

        c.execute("INSERT INTO {} VALUES (?, 0)".format())

    def add_list(self, namelist):
        self.createlst_window.destroy()
        if namelist:
            con = sqlite3.connect("database.db")
            c = con.cursor()
            c.execute(
                "INSERT INTO lists_list (list_name) VALUES (?)",
                [
                    namelist,
                ],
            )
            c.execute("CREATE TABLE IF NOT EXISTS {} (task_name TEXT, completed INTERGER)".format(namelist))
            con.commit()
            con.close()
        else: messagebox.showerror("error", "You haven't typed anything!")
        self.print_list()


    # For adding a list into... well a list
    def create_list(self):
        self.createlst_window = tk.Toplevel(self)
        self.createlst_window.geometry("200x200")
        self.createlst_window.title("Name List")
        self.namelisttxt = ttk.Label(self.createlst_window, text="Name of list").grid(
            column=0, row=0
        )
        self.namelistent = ttk.Entry(self.createlst_window, text="")
        self.namelistent.grid(column=0, row=1)
        self.namelistbtn = ttk.Button(
            self.createlst_window,
            text="Add",
            command=lambda: self.add_list(str(self.namelistent.get())),
        ).grid(column=0, row=2)

    def create_item(self):
        self.createitem_window = tk.Toplevel(self)
        self.createitem_window.geometry("200x200")
        self.createitem_window.title("Name item")
        self.createitemlbl = ttk.Label(self.createitem_window, text="Name of item").grid(column=0, row=0)
        self.createitement = ttk.Entry(self.createitem_window, text="")
        self.createitement.grid(column=0, row=1)
        self.createitembtn = ttk.Button(self.createitem_window, text="Add", command=lambda: self.add_item(str(self.createitement.get())))


if __name__ == "__main__":
    main_window = Main_app()
    main_window.mainloop()
