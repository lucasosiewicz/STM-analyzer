import numpy as np
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
        try:
            self.didu_f = file['dI/dU__Forward']
            self.didu_b = file['dI/dU__Backward']
            self.rows = 2
        except KeyError:
            self.rows = 1

        self.maps = self.draw_plot()

        self.maps.pack(expand=True, fill='both')
        self.pack(expand=True, fill='both')

    def create_topography(self, fig, idx, data, titles):

        for i, dataset, name in zip(idx, data, titles):
            ax = fig.add_subplot(self.rows, 3, i)
            z = dataset
            im = ax.pcolormesh(self.x, self.y, z)
            ax.set_title(name)
            ax.set_xlabel('X [m]')
            ax.set_ylabel('Y [m]')
            divider = make_axes_locatable(ax)
            cax = divider.append_axes("right", size="5%", pad=0.1)
            plt.colorbar(im, cax=cax, label='Z [m]')

    def draw_plot(self):
        frame = ttk.Frame(self)
        fig = Figure(figsize=(12, 7))

        self.create_topography(fig, idx=[1,2], data=[self.tf, self.tb], titles=['Forward', 'Backward'])
        optimal_shift = self.find_optimal_shift([self.tf, self.tb])
        z = self.create_mean_topography_data(optimum=optimal_shift, data=[self.tf, self.tb])
        self.create_topography(fig, idx=[3], data=[z], titles=[f'Mean {optimal_shift}px'])

        try:
            self.create_topography(fig, idx=[4,5], data=[self.didu_f, self.didu_b], titles=['dI/dU Forward', 'dI/dU Backward'])
            z = self.create_mean_topography_data(optimum=optimal_shift, data=[self.didu_f, self.didu_b])
            self.create_topography(fig, idx=[6], data=[z], titles=[f'Mean {optimal_shift}px'])
        except AttributeError:
            pass

        fig.subplots_adjust(hspace=0.7, wspace=0.7)
        canvas = FigureCanvasTkAgg(fig, frame)
        canvas.draw()
        canvas.get_tk_widget().place(relx=0, rely=0, relwidth=1, relheight=1)

        plt.close(fig)

        return frame

    def find_optimal_shift(self, data):
        results = np.array([])

        for threshold in range(-10, 11):
            if threshold < 0:
                sub = np.sum(np.abs(data[0].values[:, -threshold:] - data[1].values[:, :threshold]))
            elif threshold > 0:
                sub = np.sum(np.abs(data[0].values[:, threshold:] - data[1].values[:, :-threshold]))
            else:
                sub = np.sum(np.abs(data[0].values - data[1].values))
            results = np.append(results, sub)

        return results.argmin() - 10

    def create_mean_topography_data(self, optimum, data):
        if optimum < 0:
            z = (data[0].values[:, -optimum:] + data[1].values[:, :optimum]) / 2
            z = np.c_[z, data[1].values[:, optimum:]]
        elif optimum > 0:
            z = (data[0].values[:, optimum:] + data[1].values[:, :-optimum]) / 2
            z = np.c_[data[0].values[:, :optimum], z]
        else:
            z = (data[0].values + data[1].values) / 2

        return z

