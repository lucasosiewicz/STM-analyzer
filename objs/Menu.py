import tkinter as tk


class Menu(tk.Menu):
    def __init__(self, parent, menu_name, submenu_name, function):
        super().__init__(parent)
        self.create_submenu(menu_name, submenu_name, function)

    def create_submenu(self, menu_name, submenu_name, function):
        submenu = tk.Menu(self, tearoff=False)
        for name, func in zip(submenu_name, function):
            submenu.add_command(label=name, command=func)
        self.add_cascade(label=menu_name, menu=submenu)
