import tkinter as tk
from tkinter import ttk

# Classes
from objs.Plots import *
from objs.Dataset import *
from objs.Topography import *


class Notebook(ttk.Notebook):
    def __init__(self, parent, file, curves_per_point, number_of_points, forward_or_backward):
        super().__init__(parent)
        # Tabs
        self.dataset = Dataset(self, file, curves_per_point, number_of_points, forward_or_backward)
        self.plots = Plots(self, self.dataset.dataset_dIdU, self.dataset.dataset_current, number_of_points)
        self.topography = Topography(self, file)

        # Adding Tabs to the Notebook
        self.add(self.dataset, text='Dataset')
        self.add(self.plots, text='Plots')
        self.add(self.topography, text='Topography')