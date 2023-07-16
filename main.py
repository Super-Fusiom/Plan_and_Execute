import json
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk


class Main_app(tk.Tk):
    def __init__(self):
        # The inits... you get the jist.
        super().__init__()

        self.list_selected = "Please Select a list or make a new one"

        self.title("Plan and Execute")
        self.geometry("500x500")

        self.print_list()

        self.add_listbtn = ttk.Button(self, text="+")
        self.add_listbtn.grid(row=0, column=0)
        self.add_listbtn["command"] = self.create_list

        self.null_list_selected = ttk.Label(self, text=self.list_selected)
        self.null_list_selected.grid(column=1, row=0)

        self.check_selected()

    def check_selected(self):
        self.null_list_selected["text"] = self.list_selected
        if self.list_selected != "Please Select a list or make a new one":
            self.add_itembtn = ttk.Button(self, text="+")
            self.add_itembtn.grid(row=1, column=1)
            self.add_itembtn["command"] = self.create_item

    def json_read(self):
        with open("list.json") as f:
            return json.load(f)

    def json_write(self, data):
        with open("list.json", "w") as f:
            json.dump(data, f, indent=4)

    def print_list(self):
        # Creating list for lists and list of items if database doesn't exist
        self.rows = 1
        lists = self.json_read()

        # Print List
        for list_name in lists.keys():
            self.list = ttk.Button(self, text=str(list_name))
            self.list.grid(column=0, row=self.rows)
            self.list["command"] = lambda: self.get_print_item(list_name)
            self.rows += 1

    def get_print_item(self, keyname: str):
        def print_item():
            self.rows = 2
            items = self.json_read()
            for item in items[keyname]:
                ttk.Label(self, text=str(item)).grid(column=1, row=self.rows)
                self.rows += 1

        self.list_selected = keyname
        self.check_selected()
        return print_item

    def get_add_item(self, keyname: str, nameitem):
        self.createitm_window.destroy()
        data = self.json_read()
        data[keyname].append(nameitem)
        self.json_write(data)

    def add_list(self, namelist):
        self.createlst_window.destroy()
        if namelist:
            data = self.json_read()
            data[namelist] = []
            self.json_write(data)
            self.list_selected = namelist
            self.check_selected()
        else:
            messagebox.showerror("error", "You haven't typed anything!")
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
        self.createitm_window = tk.Toplevel(self)
        self.createitm_window.geometry("200x200")
        self.createitm_window.title("Name Item")
        self.nameitemtxt = ttk.Label(self.createitm_window, text="Name of Item").grid(
            column=0, row=0
        )
        self.nameitement = ttk.Entry(self.createitm_window, text="")
        self.nameitement.grid(column=0, row=1)
        self.nameitembtn = ttk.Button(
            self.createitm_window,
            text="Add",
            command=lambda: self.get_add_item(
                self.list_selected, str(self.nameitement.get())
            ),
        ).grid(column=0, row=2)


if __name__ == "__main__":
    main_window = Main_app()
    main_window.mainloop()
