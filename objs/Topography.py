from ttkbootstrap import ttk
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Topography(ttk.Frame):
    def __init__(self, parent, file):
        super().__init__(parent)

        self.tf = file['Topography_Forward']
        self.tb = file['Topography_Backward']
        self.x = self.y = self.tf['Topography_Forward_x']
        self.didu_f = file['dI/dU__Forward']
        self.didu_b = file['dI/dU__Backward']

        self.create_topography().pack(expand=True, fill='both')

        self.pack(expand=True, fill='both')

    def create_topography(self):
        frame = ttk.Frame(self)

        fig = Figure()
        for i, dataset, name in zip([1, 2], [self.tf, self.tb], ['Forward', 'Backward']):
            ax = fig.add_subplot(2, 3, i)
            z = dataset.values * 10**9
            im = ax.pcolormesh(self.x, self.y, z)
            ax.set_title(name)
            divider = make_axes_locatable(ax)
            cax = divider.append_axes("right", size="5%", pad=0.1)
            plt.colorbar(im, cax=cax)

        for i, dataset, name in zip([4, 5], [self.didu_f, self.didu_b], ['dI/dU Forward', 'dI/dU Backward']):
            ax = fig.add_subplot(2, 3, i)
            z = dataset.values
            im = ax.pcolormesh(self.x, self.y, z)
            ax.set_title(name)
            divider = make_axes_locatable(ax)
            cax = divider.append_axes("right", size="5%", pad=0.1)
            plt.colorbar(im, cax=cax)

        mean_topology = (self.tf.values + self.tb.values) / 2
        mean_didu = (self.didu_f.values + self.didu_b.values) / 2

        for i, z, name in zip([3, 6], [mean_topology, mean_didu], ['Mean', 'dI/dU mean']):
            ax = fig.add_subplot(2, 3, i)
            im = ax.pcolormesh(self.x, self.y, z)
            ax.set_title(name)
            divider = make_axes_locatable(ax)
            cax = divider.append_axes("right", size="5%", pad=0.1)
            plt.colorbar(im, cax=cax)

        fig.subplots_adjust(hspace=0.5, wspace=0.5)

        canvas = FigureCanvasTkAgg(fig, frame)
        canvas.draw()
        canvas.get_tk_widget().pack(expand=True, fill='both')

        return frame
