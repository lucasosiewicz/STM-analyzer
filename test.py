import tkinter as tk
from tkinter import ttk

class MoveDataApp:
    def __init__(self, master):
        self.master = master
        master.title("Move Data App")

        # Inicjalizacja danych
        self.left_data = ["Tekst 1", "Tekst 2", "Tekst 3"]
        self.right_data = []

        # Ramka do przechowywania widoków TreeView
        frame = tk.Frame(master)
        frame.pack(padx=10, pady=10)

        # TreeView po lewej stronie
        self.left_tree = ttk.Treeview(frame, columns=('Data',), show='headings')
        self.left_tree.heading('Data', text='Left Data')
        self.left_tree.pack(side=tk.LEFT, padx=10)

        # Wypełnij TreeView po lewej stronie danymi
        for data in self.left_data:
            self.left_tree.insert("", "end", values=(data,))

        # Dodaj pasek przewijania dla TreeView po lewej stronie
        left_scroll = ttk.Scrollbar(frame, orient="vertical", command=self.left_tree.yview)
        left_scroll.pack(side=tk.LEFT, fill="y")
        self.left_tree.configure(yscrollcommand=left_scroll.set)

        # Przycisk do przenoszenia danych z lewej do prawej
        move_right_button = tk.Button(frame, text="Move Right", command=self.move_right)
        move_right_button.pack(side=tk.LEFT, padx=10)

        # Przycisk do przenoszenia danych z prawej do lewej
        move_left_button = tk.Button(frame, text="Move Left", command=self.move_left)
        move_left_button.pack(side=tk.LEFT, padx=10)

        # TreeView po prawej stronie
        self.right_tree = ttk.Treeview(frame, columns=('Data',), show='headings')
        self.right_tree.heading('Data', text='Right Data')
        self.right_tree.pack(side=tk.LEFT, padx=10)

        # Dodaj pasek przewijania dla TreeView po prawej stronie
        right_scroll = ttk.Scrollbar(frame, orient="vertical", command=self.right_tree.yview)
        right_scroll.pack(side=tk.LEFT, fill="y")
        self.right_tree.configure(yscrollcommand=right_scroll.set)

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
            self.left_tree.insert("", "end", values=(data,))
            # Usuń dane z prawej
            self.right_tree.delete(item)

if __name__ == "__main__":
    root = tk.Tk()
    app = MoveDataApp(root)
    root.mainloop()
