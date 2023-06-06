import sqlite3
import tkinter
from tkinter import messagebox
from tkinter import ttk

class App(tkinter.Tk):
    def __init__(self):
        super().__init__()

        self.title("Plan and Execute")
        self.geometry("500x500")

        self.label = ttk.Label(self, text="PLAN")
        self.label.pack()

        self.button = ttk.Button(self, text="Execute")
        self.button['command'] = self.button_clicked
        self.button.pack()

    def button_clicked(self):
        print("It works")
            

if __name__ == "__main__":
    main_window = App()
    main_window.mainloop()
