import spym
import tkinter as tk
from tkinter import ttk, filedialog

# Classes
from objs.Menu import *
from objs.ExtraWindow import *


class App(tk.Tk):
    # Main class
    def __init__(self):
        super().__init__()
        self.title('Praca inżynierska')
        self.geometry('300x150')

        # global variables
        self.file = ''
        self.curves_per_point = 0
        self.number_of_points = 0
        self.forward_or_backward = None
        self.local_visibility = False

        # Menu
        self.menu = Menu(self, 'File', 'Open file', self.load_file)
        self.configure(menu=self.menu)

        # Widgets
        self.labels = [ttk.Label(self) for _ in range(7)]

        # Extra Window
        self.extra_window = None

    def load_file(self):
        # function executing while pressing Open Button
        file_path = filedialog.askopenfilename(
            title='Choose file',
            initialdir='/data',
            filetypes=[('SM4', '*.SM4')])
        self.file = spym.load(file_path)

        if self.local_visibility:
            for label in self.labels:
                label.pack_forget()
            self.extra_window.destroy()
        self.local_visibility = True

        functions = [f"File's name: {self.fetch_filename()}",
                     f"Picture's size (px): {self.fetch_picture_size()[0]}x{self.fetch_picture_size()[1]}",
                     f"Picture's size (nm): {self.fetch_picture_size()[2]}",
                     f"Spectroscopy's first direction: {self.fetch_forward_or_backward()}",
                     f"Spectroscopy's range: {self.fetch_spectroscopy_range()[0]}V - {self.fetch_spectroscopy_range()[1]}V",
                     f"Curves per one point: {self.fetch_curves_per_point()}",
                     f"Number of points: {self.fetch_number_of_points()}"]

        labels_functions = {label:value for (label, value) in zip(self.labels, functions)}

        for (label, text) in labels_functions.items():
            label.configure(text=text)
            label.pack(expand=True)

        # Showing extra window
        self.extra_window = ExtraWindow(self.file, self.curves_per_point, self.number_of_points, self.forward_or_backward)

    def fetch_filename(self):
        # Fetching filename
        return self.file['dI/dU_'].attrs['filename']

    def fetch_picture_size(self):
        # Fetching picture size from metadata

        # Pixel size
        idx_x = self.file['dI/dU_'].attrs['RHK_PRMdata'].find('<1986>')
        x_size = self.file['dI/dU_'].attrs['RHK_PRMdata'][idx_x+21:idx_x+24]

        idx_y = self.file['dI/dU_'].attrs['RHK_PRMdata'].find('<1987>')
        y_size = self.file['dI/dU_'].attrs['RHK_PRMdata'][idx_y+21:idx_y+24]

        # Nanometers size
        idx = self.file['dI/dU_'].attrs['RHK_PRMdata'].find('<1322>')
        start = self.file['dI/dU_'].attrs['RHK_PRMdata'][idx:].find('::') + idx + 2
        stop = self.file['dI/dU_'].attrs['RHK_PRMdata'][idx:].find('\r') + idx
        nm_size = self.file['dI/dU_'].attrs['RHK_PRMdata'][start:stop]

        return x_size, y_size, nm_size

    def fetch_forward_or_backward(self):
        # Fetching first spectroscopy's direction
        # If value is OFF that means microscope started with Forward
        # Else means Backward

        idx = self.file['dI/dU_'].attrs['RHK_PRMdata'].find('<1833>')
        start = self.file['dI/dU_'].attrs['RHK_PRMdata'][idx:].find('::') + idx + 2
        stop = self.file['dI/dU_'].attrs['RHK_PRMdata'][idx:].find('\r') + idx
        f_or_b = self.file['dI/dU_'].attrs['RHK_PRMdata'][start:stop]

        self.forward_or_backward = True if f_or_b == 'OFF' else False
        return 'Forward' if f_or_b == 'OFF' else 'Backward'

    def fetch_spectroscopy_range(self):
        # Fetching spectroscopy's range by taking min and max values
        values = self.file['dI/dU_'].coords['dI/dU__x'].values
        return round(min(values), 5), round(max(values), 5)

    def fetch_curves_per_point(self):
        # Fetching how many measurements has taken in one point
        idx = self.file['dI/dU_'].attrs['RHK_PRMdata'].find('<1101>')
        curves_per_point = int(self.file['dI/dU_'].attrs['RHK_PRMdata'][idx + 28:idx + 29])
        self.curves_per_point = curves_per_point
        return curves_per_point

    def fetch_number_of_points(self):
        num_of_curves = self.file['dI/dU_'].coords['dI/dU__y'].size
        number_of_points = num_of_curves // self.curves_per_point
        self.number_of_points = number_of_points
        return number_of_points


