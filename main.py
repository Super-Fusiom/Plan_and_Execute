import json
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import pyglet


class Main_app(tk.Tk):
    def __init__(self):
        # The inits... you get the jist.
        super().__init__()
        # Adding font and apply to whole application
        pyglet.font.add_file("assets/IBMPlexMono-Medium.ttf")
        ttk.Style(self).configure(".", font=("IBMPlexMono-Medium", 15))

        self.right_style = ttk.Style(self)
        self.right_style.configure(".TFrame", background="#FEE500")
        self.right_side = ttk.Frame(style=".TFrame")
        self.right_side.grid(column=1, row=0, padx=(20, 0))

        self.list_selected: str = "Please Select a list or make a new one"

        self.title("Plan and Execute")
        self.geometry("540x500")

        self.content_item = ttk.Frame(self.right_side)
        self.content_item.grid(column=1, row=2, rowspan=1000)

        self.add_itemfr = ttk.Frame(self.right_side)
        self.add_itemfr.grid(column=1, row=1)

        self.utils = ttk.Frame(self)
        self.utils.grid(column=0, row=0)

        self.content_list = ttk.Frame(self.utils)
        self.content_list.grid(column=0, row=2, rowspan=1)

        self.print_list("main")

        self.add_listbtn = ttk.Button(self.utils, text="+")
        self.add_listbtn.grid(row=0, column=0, rowspan=1)
        self.add_listbtn["command"] = self.create_list

        self.delete_modebtn = ttk.Button(
            self.utils, text="DEL", command=self.delete_object
        )
        self.delete_modebtn.grid(column=0, row=1, pady=(0, 20), rowspan=1)

        self.list_title = ttk.Label(self.right_side, text=self.list_selected)
        self.list_title.grid(column=1, row=0)

        self.check_selected()

    # Check if the list is selected
    def check_selected(self):
        self.list_title["text"] = self.list_selected
        if self.list_selected != "Please Select a list or make a new one":
            self.add_itembtn = ttk.Button(self.add_itemfr, text="+")
            self.add_itembtn.grid(row=1, column=1)
            self.add_itembtn["command"] = self.create_item

    # Loading JSON file and writing JSON file
    def json_read(self):
        with open("list.json", "r") as f:
            return json.load(f)

    def json_write(self, data: dict[str, str]):
        with open("list.json", "w") as f:
            json.dump(data, f, indent=4)

    # Prints user list
    def print_list(self, window: str):
        if window == "main":
            self.rows = 2
            self.content_list.destroy()
            self.content_list = ttk.Frame(self.utils)
            self.content_list.grid(column=0, row=2, rowspan=1)
            lists = self.json_read()
            # Print List
            for list_name in lists.keys():
                list = ttk.Button(
                    self.content_list,
                    text=str(list_name),
                    command=lambda list_name=list_name: self.print_item(
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
                    command=lambda list_name=list_name: self.remove_object_list(
                        list_name
                    ),
                )
                list.grid(column=0, row=self.rows)
                self.rows += 1

    # The same can go for the items in the list
    def print_item(self, keyname: str, window: str):
        if window == "main":
            self.rows = 0
            self.content_list.destroy()
            self.content_list = ttk.Frame(self.utils)
            self.content_list.grid(column=0, row=2, rowspan=1)
            lists = self.json_read()
            # Print List
            for list_name in lists.keys():
                list = ttk.Button(
                    self.content_list,
                    text=str(list_name),
                    command=lambda list_name=list_name: self.print_item(
                        list_name, "main"
                    ),
                )
                list.grid(column=0, row=self.rows)
                self.rows += 1

            def get_print_item():
                self.rows = 2
                items = self.json_read()
                for item in items[keyname]:
                    ttk.Label(self.content_item, text=str(item)).grid(
                        column=1, row=self.rows
                    )
                    self.rows += 1

            self.content_item.grid_forget()
            self.content_item = ttk.Frame(self.right_side)
            self.content_item.grid(column=1, row=2, rowspan=5)
            self.list_selected = keyname
            self.check_selected()
            e = get_print_item()
            return e
        elif window == "delete":

            def print_item():
                self.rows = 1
                items = self.json_read()
                for index, item in enumerate(items[keyname]):
                    ttk.Button(
                        self.del_items,
                        text=str(item),
                        command=lambda index=index: self.remove_object_item(
                            keyname, index
                        ),
                    ).grid(column=1, row=self.rows)

                    self.rows += 1

            self.del_items.grid_forget()
            self.del_items = ttk.Frame(self.del_object)
            self.del_items.grid(column=1, row=2, rowspan=5)
            e = print_item()
            return e

    # Adding an item and a list
    def add_item(self, keyname: str, nameitem: str):
        checker = self.json_read()
        checker_list = checker[keyname]
        keyname_lth = len(checker_list)
        if len(nameitem) != 0 and keyname_lth <= 6:
            self.createitm_window.destroy()
            data = self.json_read()
            data[keyname].append(nameitem)
            self.json_write(data)
            self.print_item(keyname, "main")
        elif len(nameitem) == 0:
            messagebox.showerror("error", "No item?")
        elif keyname_lth >= 7:
            messagebox.showerror("error", "Max items reached")

    def add_list(self, namelist: str):
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
            command=lambda: self.add_item(
                self.list_selected, str(self.nameitement.get())
            ),
        ).grid(column=0, row=2)

    def delete_object(self):
        if self.list_selected != "Please Select a list or make a new one":
            self.del_object = tk.Toplevel(self)
            self.del_object.geometry("400x400")
            self.del_object.title("Delete object")

            ttk.Label(
                self.del_object, text="Please select which list or item to delete"
            ).grid(column=0, row=0, columnspan=2)

            self.del_items = ttk.Frame(self.del_object)
            self.del_items.grid(column=3, row=0)

            self.print_list("delete")
            self.print_item(self.list_selected, "delete")
        else:
            messagebox.showerror("error", "Please select a list")

    def remove_object_list(self, list: str):
        lists = self.json_read()
        del lists[list]
        self.json_write(lists)
        self.content_list.grid_forget()
        self.content_list = ttk.Frame(self.utils)
        self.content_list.grid(column=0, row=2, rowspan=1000)

        self.add_itemfr.destroy()
        self.add_itemfr = ttk.Frame(self.right_side)
        self.add_itemfr.grid(column=1, row=1)

        self.content_item.destroy()
        self.content_item = ttk.Frame(self.right_side)
        self.content_item.grid(column=1, row=2, rowspan=1000)
        self.list_selected = "Please Select a list or make a new one"
        self.print_list("main")
        self.check_selected()
        self.del_object.destroy()

    def remove_object_item(self, list: str, item: int):
        data = self.json_read()
        list_item_del = data[list]
        del list_item_del[item]

        self.json_write(data)

        self.print_item(list, "main")
        self.del_object.destroy()


if __name__ == "__main__":
    main_window = Main_app()
    main_window.mainloop()
