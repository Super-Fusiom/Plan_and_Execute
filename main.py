import json
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import pyglet


class Main_app(tk.Tk):
    def __init__(self):
        # The inits... you get the jist.
        super().__init__()

        # Adding font
        pyglet.font.add_file("assets/IBMPlexMono-Medium.ttf")
        ttk.Style(self).configure(".", font=("IBMPlexMono-Medium", 15))

        self.list_selected = "Please Select a list or make a new one"

        self.title("Plan and Execute")
        self.geometry("500x500")

        self.print_list("main")

        self.content_item = ttk.Frame()
        self.content_item.grid(column=1, row=2)

        self.add_listbtn = ttk.Button(self, text="+")
        self.add_listbtn.grid(row=0, column=0)
        self.add_listbtn["command"] = self.create_list

        self.delete_modebtn = ttk.Button(self, text="DEL", command=self.delete_object)
        self.delete_modebtn.grid(column=0, row=1, pady=(0, 20))

        self.list_title = ttk.Label(self, text=self.list_selected)
        self.list_title.grid(column=1, row=0)

        self.check_selected()

    # Check if the list is selected
    def check_selected(self):
        self.list_title["text"] = self.list_selected
        if self.list_selected != "Please Select a list or make a new one":
            self.add_itembtn = ttk.Button(self, text="+")
            self.add_itembtn.grid(row=1, column=1)
            self.add_itembtn["command"] = self.create_item

    # Loading JSON file
    def json_read(self):
        with open("list.json", "r") as f:
            return json.load(f)

    def json_write(self, data):
        with open("list.json", "w") as f:
            json.dump(data, f, indent=4)

    def print_list(self, window: str):
        if window == "main":
            self.rows = 2
            lists = self.json_read()
            # Print List
            for list_name in lists.keys():
                list = ttk.Button(
                    self,
                    text=str(list_name),
                    command=lambda list_name=list_name: self.get_print_item(
                        list_name, "main"
                    ),
                )
                list.grid(column=0, row=self.rows)
                self.rows += 1
        elif window == "delete":
            self.rows = 2
            lists = self.json_read()
            # Print List
            for list_name in lists.keys():
                list = ttk.Button(
                    self.del_object,
                    text=str(list_name),
                    command=lambda list_name=list_name: self.get_print_item(
                        list_name, "delete"
                    ),
                )
                list.grid(column=0, row=self.rows)
                self.rows += 1

    def get_print_item(self, keyname: str, window: str):
        if window == "main":
            self.rows = 2
            lists = self.json_read()
            # Print List
            for list_name in lists.keys():
                list = ttk.Button(
                    self,
                    text=str(list_name),
                    command=lambda list_name=list_name: self.get_print_item(
                        list_name, "main"
                    ),
                )
                list.grid(column=0, row=self.rows)
                self.rows += 1

            def print_item():
                self.rows = 2
                items = self.json_read()
                for item in items[keyname]:
                    ttk.Label(self.content_item, text=str(item)).grid(
                        column=1, row=self.rows
                    )
                    self.rows += 1

            self.content_item.grid_forget()
            self.content_item = ttk.Frame()
            self.content_item.grid(column=1, row=2, rowspan=5)
            self.list_selected = keyname
            self.check_selected()
            e = print_item()
            return e
        elif window == "delete":

            def print_item():
                self.rows = 1
                items = self.json_read()
                for item in items[keyname]:
                    ttk.Button(
                        self.del_items, text=str(item), command=self.remove_object
                    )

                    self.rows += 1

            self.del_items.grid_forget()
            self.del_items = ttk.Frame(self.del_object)
            self.del_items.grid(column=1, row=2, rowspan=5)
            e = print_item()
            return e

    def get_add_item(self, keyname: str, nameitem):
        self.createitm_window.destroy()
        data = self.json_read()
        data[keyname].append(nameitem)
        self.json_write(data)
        self.get_print_item(keyname, "main")

    def add_list(self, namelist):
        self.createlst_window.destroy()
        data = self.json_read()
        if len(data) <= 4:
            if namelist:
                data = self.json_read()
                data[namelist] = []
                self.json_write(data)
                self.list_selected = namelist
                self.check_selected()
            else:
                messagebox.showerror("error", "You haven't typed anything!")
            self.print_list("main")
        else:
            messagebox.showerror("error", "you have more then 5 lists")

    # For adding a list into... well a list
    def create_list(self):
        self.createlst_window = tk.Toplevel(self)
        self.createlst_window.geometry("200x200")
        self.createlst_window.title("Name List")
        self.namelisttxt = ttk.Label(self.createlst_window, text="Name of list").grid(
            column=0, row=0
        )
        self.namelistent = ttk.Entry(self.createlst_window)
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
        self.nameitement = ttk.Entry(self.createitm_window)
        self.nameitement.grid(column=0, row=1)
        self.nameitembtn = ttk.Button(
            self.createitm_window,
            text="Add",
            command=lambda: self.get_add_item(
                self.list_selected, str(self.nameitement.get())
            ),
        ).grid(column=0, row=2)

    def delete_object(self):
        self.del_object = tk.Toplevel(self)
        self.del_object.geometry("300x300")
        self.del_object.title("Delete object")

        ttk.Label(
            self.del_object, text="Please select which list or item to delete"
        ).grid(column=0, row=0)

        self.del_items = ttk.Frame(self.del_object)
        self.del_items.grid(column=3, row=0)

        self.print_list("delete")

    def remove_object(self):
        print(2)


if __name__ == "__main__":
    main_window = Main_app()
    main_window.mainloop()
