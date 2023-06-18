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

        self.database_print_list()

        self.add_button = ttk.Button(self, text="+")
        self.add_button.grid(row=0, column=0)
        self.add_button["command"] = self.createlst

        self.lists_list = [self.add_button]

    def database_print_items(self):
        con = sqlite3.connect("database.db")
        c = con.cursor()
        c.execute("SELECT * from item_list")
        con.commit()
        con.close()

    def database_add_list(self, namelist):
        self.createlst_window.destroy()
        con = sqlite3.connect("database.db")
        c = con.cursor()
        c.execute(
            "INSERT INTO lists_list (lists) VALUES (?)",
            [
                namelist,
            ],
        )
        con.commit()
        con.close()
        self.database_print_list()

    def database_print_list(self):
        # Creating list for lists and list of items if database doesn't exist
        self.rows = 1
        con = sqlite3.connect("database.db")
        curser_obj = con.cursor()
        curser_obj.execute(
            "CREATE TABLE IF NOT EXISTS lists_list (id INTEGER PRIMARY KEY AUTOINCREMENT, lists TEXT)"
        )
        curser_obj.execute(
            "CREATE TABLE IF NOT EXISTS item_list (id INTEGER PRIMARY KEY, main_id INTEGER, items TEXT, FOREIGN KEY (main_id) REFERENCES lists_list(id))"
        )
        curser_obj.execute("SELECT * FROM lists_list")
        lists = curser_obj.fetchall()

        # Print List
        for list in lists:
            self.liste = ttk.Button(self, text=str(list[1]))
            self.liste.grid(
                column=0, row=self.rows
            )
            self.liste["command"] = self.database_print_items
            self.rows += 1
        con.commit()
        con.close()

    # For adding a list into... well a list
    def createlst(self):
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
            command=lambda: self.database_add_list(str(self.namelistent.get())),
        ).grid(column=0, row=2)


if __name__ == "__main__":
    main_window = Main_app()
    main_window.mainloop()
