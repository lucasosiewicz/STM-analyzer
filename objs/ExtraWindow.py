from objs.Notebook import *
import tkinter as tk


class ExtraWindow(tk.Toplevel):
    def __init__(self, file, curves_per_point, number_of_points, forward_or_backward):
        super().__init__()

        self.title(file['Topography_Forward'].attrs['filename'])
        self.geometry('1200x700')

        # Tabs
        self.notebook = Notebook(self, file, curves_per_point, number_of_points, forward_or_backward)
        self.notebook.pack(expand=True, fill='both')
