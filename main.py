import sqlite3
from tkinter import *
from tkinter import messagebox
from tkinter import ttk

class Window:
    def __init__(self, window):
        self.window = window


main_window = Window("edger")

print(main_window.window)
