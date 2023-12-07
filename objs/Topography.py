import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Topography(ttk.Frame):
    def __init__(self, parent, file):
        super().__init__(parent)

        self.tf = file['Topography_Forward']
        self.tb = file['Topography_Backward']
        self.didu_f = file['dI/dU__Forward']
        self.didu_b = file['dI/dU__Backward']

        self.create_topography().pack(expand=True, fill='both')

        self.pack(expand=True, fill='both')

    def create_topography(self):
        frame = ttk.Frame(self)

        fig = Figure()
        for i, dataset, name in zip([1,2], [self.tf, self.tb], ['Forward', 'Backward']):
            ax = fig.add_subplot(2, 2, i)
            x = dataset[f'Topography_{name}_x']
            y = dataset[f'Topography_{name}_y']
            z = dataset.values * 10**9
            im = ax.pcolormesh(x, y, z)
            ax.set_title(name)
            divider = make_axes_locatable(ax)
            cax = divider.append_axes("right", size="5%", pad=0.1)
            colorbar = plt.colorbar(im, cax=cax)

        for i, dataset, name in zip([3,4], [self.didu_f, self.didu_b], ['dI/dU__Forward', 'dI/dU__Backward']):
            ax = fig.add_subplot(2, 2, i)
            x = dataset[f'{name}_x']
            y = dataset[f'{name}_y']
            z = dataset.values
            im = ax.pcolormesh(x, y, z)
            ax.set_title(name)
            divider = make_axes_locatable(ax)
            cax = divider.append_axes("right", size="5%", pad=0.1)
            colorbar = plt.colorbar(im, cax=cax)

        fig.subplots_adjust(hspace=0.5, wspace=0.5)

        canvas = FigureCanvasTkAgg(fig, frame)
        canvas.draw()
        canvas.get_tk_widget().pack(expand=True, fill='both')

        return frame



