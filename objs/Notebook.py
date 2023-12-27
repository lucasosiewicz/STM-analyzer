from objs.Plots import *
from objs.Dataset import *
from objs.Topography import *
from ttkbootstrap import ttk
from ttkbootstrap.dialogs import Messagebox


class Notebook(ttk.Notebook):
    def __init__(self, parent, file, curves_per_point, number_of_points, forward_or_backward):
        super().__init__(parent)
        # Tabs
        try:
            # Initializing Tabs
            self.dataset = Dataset(self, file, curves_per_point, number_of_points, forward_or_backward)
            self.plots = Plots(self, self.dataset.dataset_dIdU, self.dataset.dataset_current, number_of_points)

            # Adding these Tabs to the Notebook
            self.add(self.dataset, text='Dataset')
            self.add(self.plots, text='Plots')
        except KeyError:
            Messagebox.show_warning("Spectroscopy hasn't made in this file.", title='Warning')
        finally:
            self.topography = Topography(self, file)
            self.add(self.topography, text='Topography')
