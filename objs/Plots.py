import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from scipy.signal import savgol_filter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

# Classes
from objs.Dataset import *
from objs.Notebook import *
from objs.AddingCurvesWindow import *


class Plots(ttk.Frame):
    def __init__(self, parent, dataset_didu, dataset_current, number_of_points):
        super().__init__(parent)

        # Class variables
        self.dataset_current = dataset_current.iloc[:, -number_of_points-2:-2]
        self.dataset_didu = dataset_didu.iloc[:, -number_of_points-2:-2]
        self.columns = list(dataset_didu.iloc[:, -number_of_points-2:-2].columns)
        self.x = dataset_current['x'].values
        self.number_of_points = number_of_points

        # Labels variables
        self.checkbox_vars = [tk.BooleanVar(value=True) for _ in range(self.number_of_points)]
        self.x_range = [tk.StringVar(value=f'{min(self.x)}'), tk.StringVar(value=f'{max(self.x)}')]

        # Widgets
        self.plot_frame = self.create_plot_frame()
        self.navigation_toolbar = self.create_navitagion_toolbar()



        # Layout
        self.plot_frame.place(relx=0, rely=0, anchor='nw', relwidth=0.66, relheight=1)
        self.navigation_toolbar.place(relx=0.8, rely=0, anchor='nw', relwidth=0.9, relheight=0.5)
        self.pack(expand=True, fill='both')

    def create_plot_frame(self):
        # Funkcja tworzy obiekt frame z wykresami
        frame = ttk.Frame(self)

        fig = Figure()
        current_plot = fig.add_subplot(2, 1, 1)
        didu_plot = fig.add_subplot(2, 1, 2)

        self.draw_plot(current_plot, self.dataset_current, 'Current', 'y [A]')
        self.draw_plot(didu_plot, self.dataset_didu, 'dI/dU', 'y [arb. unit]', True)

        fig.subplots_adjust(hspace=0.5)

        canvas = FigureCanvasTkAgg(fig, frame)
        canvas.draw()
        canvas.get_tk_widget().pack(expand=True, fill='both')

        return frame

    def draw_plot(self, plot, y_data, title, yname, first_plot=False):
        plot.clear()

        y_values = y_data.values.T


        for y, column, idx in zip(y_values, self.columns, range(len(self.checkbox_vars))):
            if self.checkbox_vars[idx].get():
                y = savgol_filter(y, 35, 2)
                plot.plot(self.x, y, label=column, linewidth=0.7)

        plot.set_title(title)
        plot.grid(True)
        plot.set_ylabel(yname)
        if first_plot:
            plot.set_xlabel('x [V]')
        else:
            plot.legend()

    def create_navitagion_toolbar(self):
        frame = ttk.Frame(self)

        self.create_checkboxes(frame).pack(fill='both')
        self.create_x_range_entries(frame).pack(fill='both')
        ttk.Button(frame, text='Refresh', command=self.refresh_plot).pack(fill='both')
        ttk.Button(frame, text='Add curves', command=self.create_adding_curves_window).pack(fill='both')

        return frame

    def create_checkboxes(self, parent):
        frame = ttk.Frame(parent)
        ttk.Label(frame, text='Display curves:').pack(expand=True, fill='both')
        for column, idx in zip(self.dataset_current.columns, range(len(self.checkbox_vars))):
            ttk.Checkbutton(frame,
                            text=f'{column}',
                            variable=self.checkbox_vars[idx],
                            onvalue=True,
                            offvalue=False).pack(expand=True, fill='both')
        return frame

    def create_x_range_entries(self, parent):
        frame = ttk.Frame(parent)

        ttk.Entry(frame, textvariable=self.x_range[0]).pack(fill='both')
        ttk.Entry(frame, textvariable=self.x_range[1]).pack(fill='both')

        return frame

    def create_adding_curves_window(self):
        AddingCurvesWindow(self.dataset_didu, self.x)


    # Event functions
    def refresh_plot(self):
        self.plot_frame.pack_forget()
        self.plot_frame = self.create_plot_frame()
        self.plot_frame.place(relx=0, rely=0, anchor='nw', relwidth=0.66, relheight=1)

    def get_entry_values(self):
        try:
            return [float(self.x_range[0].get()), float(self.x_range[1].get())]
        except TypeError:
            print('Not a digit in entry')
            return [min(self.x), max(self.x)]

