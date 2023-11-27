import pandas as pd
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt

# Classes
from objs.Plots import *


class AddingCurvesWindow(tk.Toplevel):
    def __init__(self, data, x):
        super().__init__()
        self.title('Adding curves')
        self.geometry('600x300')

        # Inicjalizacja danych
        self.x = x
        self.data = data
        self.left_data = list(self.data.columns)
        self.right_data = []

        # Ramka do przechowywania widoków TreeView
        frame = tk.Frame(self)
        frame.pack(padx=10, pady=10)

        # TreeView po lewej stronie
        self.left_tree = ttk.Treeview(frame, columns=('Data',), show='headings')
        self.left_tree.heading('Data', text='Curves:')
        self.left_tree.pack(side=tk.LEFT, padx=10)

        # Wypełnij TreeView po lewej stronie danymi
        for data in self.left_data:
            self.left_tree.insert("", "end", values=(data,))

        button_frame = ttk.Frame(frame)
        # Dodaj pasek przewijania dla TreeView po lewej stronie
        left_scroll = ttk.Scrollbar(frame, orient="vertical", command=self.left_tree.yview)
        left_scroll.pack(side=tk.LEFT, fill="y")
        self.left_tree.configure(yscrollcommand=left_scroll.set)

        # Przycisk do przenoszenia danych z lewej do prawej
        move_right_button = tk.Button(button_frame, text="-->", command=self.move_right)
        move_right_button.pack(expand=True, fill='both')

        # Przycisk do przenoszenia danych z prawej do lewej
        move_left_button = tk.Button(button_frame, text="<--", command=self.move_left)
        move_left_button.pack(expand=True, fill='both')
        button_frame.pack(side=tk.LEFT, padx=20)

        # TreeView po prawej stronie
        self.right_tree = ttk.Treeview(frame, columns=('Data',), show='headings')
        self.right_tree.heading('Data', text='Curves to add:')
        self.right_tree.pack(side=tk.RIGHT, padx=10)

        # Dodaj pasek przewijania dla TreeView po prawej stronie
        right_scroll = ttk.Scrollbar(frame, orient="vertical", command=self.right_tree.yview)
        right_scroll.pack(side=tk.LEFT, fill="y")
        self.right_tree.configure(yscrollcommand=right_scroll.set)

        # Przycisk Ok
        self.button_ok = ttk.Button(self, text='Ok', command=self.return_curves).pack(expand=True)

    def move_right(self):
        # Pobierz zaznaczone dane z lewej strony
        selected_items = self.left_tree.selection()
        for item in selected_items:
            data = self.left_tree.item(item, 'values')[0]
            # Przenieś dane z lewej do prawej
            self.right_data.append(data)
            self.right_tree.insert("", "end", values=(data,))
            # Usuń dane z lewej
            self.left_tree.delete(item)

    def move_left(self):
        # Pobierz zaznaczone dane z prawej strony
        selected_items = self.right_tree.selection()
        for item in selected_items:
            data = self.right_tree.item(item, 'values')[0]
            # Przenieś dane z prawej do lewej
            self.left_data.append(data)
            self.left_tree.insert("", "end", values=((data,)))
            # Usuń dane z prawej
            self.right_tree.delete(item)

    def return_curves(self):
        new_data = self.data[self.right_data].mean(axis=1)
        plt.plot(self.x, new_data.values)
        plt.xlabel('x [V]')
        plt.ylabel('y [arb. units]')
        plt.grid(True)
        plt.show()