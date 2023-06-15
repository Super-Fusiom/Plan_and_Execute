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

        # self.database_print()

        self.add_button = ttk.Button(self, text="+")
        self.add_button["command"] = self.createlst
        self.add_button.pack()

        self.lists_list = [self.add_button]

    def database_add(self):
        con = sqlite3.connect("database.db")
        c = con.cursor()
        c.execute("INSERT INTO lists_list (list) VALUES (?)", self.namelistent)
        self.database_print()

    def database_print(self):
        # Creating list if database doesn't exist
        self.rows = 1
        con = sqlite3.connect("database.db")
        curser_obj = con.cursor()
        curser_obj.execute("create table if not exists lists_list (lists)")
        lists = curser_obj.fetchall()
        # Print List
        for list in lists:
            lis = ttk.Button(self, text=str(list[1])).grid(row=self.rows)
            self.rows += 1
        con.commit()
        con.close()

    # For adding a list into... well a list
    def createlst(self):
        createlst_window = tk.Toplevel(self)
        createlst_window.title("Name List")
        self.namelisttxt = ttk.Label(createlst_window, text="Name of list").grid(
            column=0, row=0
        )
        self.namelistent = ttk.Entry(createlst_window).grid(column=0, row=1)
        self.namelistbtn = ttk.Button(
            createlst_window, text="Add", command=self.database_add
        )


if __name__ == "__main__":
    main_window = Main_app()
    main_window.mainloop()
