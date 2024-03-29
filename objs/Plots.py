from objs.AddingCurvesWindow import *

import tkinter as tk
import ttkbootstrap as ttk
from tkinter import filedialog
from matplotlib.figure import Figure
from scipy.signal import savgol_filter
from ttkbootstrap.dialogs import Messagebox
from ttkbootstrap.scrolled import ScrolledFrame
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Plots(ttk.Frame):
    def __init__(self, parent, dataset_didu, dataset_current, number_of_points):
        super().__init__(parent)

        # Set grid
        self.columnconfigure((0, 1, 2, 3), weight=1, uniform='a')
        self.rowconfigure(0, weight=1, uniform='a')

        # Class variables
        self.dataset_current = dataset_current.iloc[:, -number_of_points-2:-2]
        self.dataset_didu = dataset_didu.iloc[:, -number_of_points-2:-2]
        self.columns = list(dataset_didu.iloc[:, -number_of_points-2:-2].columns)
        self.x = dataset_current['x'].values
        self.number_of_points = number_of_points
        self.colors = []

        # Labels variables
        self.checkbox_vars = [tk.BooleanVar(value=True) for _ in range(self.number_of_points)]
        self.x_range = [tk.StringVar(value=f'{min(self.x)}'), tk.StringVar(value=f'{max(self.x)}')]
        self.savgol_var = tk.IntVar(value=3)

        # Widgets
        self.fig = None
        self.plot_frame = self.create_plot_frame()
        self.navigation_toolbar = self.create_navitagion_toolbar()

        # Layout
        self.plot_frame.grid(row=0, column=0, columnspan=3, sticky='news')
        self.navigation_toolbar.grid(row=0, column=3, sticky='news')
        self.pack(expand=True, fill='both')

    def create_plot_frame(self):
        # Funkcja tworzy obiekt frame z wykresami
        frame = ttk.Frame(self)

        self.fig = Figure(figsize=(8, 7))
        current_plot = self.fig.add_subplot(2, 1, 1)
        didu_plot = self.fig.add_subplot(2, 1, 2)

        self.draw_plot(current_plot, self.dataset_current, 'Current', 'y [A]')

        if len(self.colors) == 0:
            for line in current_plot.get_lines():
                self.colors.append(line.get_color())

        self.draw_plot(didu_plot, self.dataset_didu, 'dI/dU', 'y [arb. unit]', True)

        self.fig.subplots_adjust(hspace=0.5)

        canvas = FigureCanvasTkAgg(self.fig, frame)
        canvas.draw()
        canvas.get_tk_widget().place(relx=0, rely=0, relwidth=1, relheight=1)

        return frame

    def draw_plot(self, plot, y_data, title, yname, first_plot=False):
        plot.clear()

        y_values = y_data.values.T
        xlim_min, xlim_max = self.get_entry_values()

        for y, column, idx in zip(y_values, self.columns, range(len(self.checkbox_vars))):
            if self.checkbox_vars[idx].get() and len(self.colors) == 0:
                y = savgol_filter(y, self.savgol_var.get(), 2)
                plot.plot(self.x, y, label=column, linewidth=0.7)
            elif self.checkbox_vars[idx].get() and len(self.colors) != 0:
                y = savgol_filter(y, self.savgol_var.get(), 2)
                plot.plot(self.x, y, label=column, linewidth=0.7, c=self.colors[idx])

        plot.set_title(title)
        plot.grid(True)
        plot.set_ylabel(yname)
        plot.set_xlim(xlim_min, xlim_max)
        if first_plot:
            plot.set_xlabel('x [V]')

    def create_navitagion_toolbar(self):
        frame = ttk.Frame(self)

        frame.rowconfigure((0, 1, 2, 3, 4, 5, 6), weight=1, uniform='a')
        frame.columnconfigure(0, weight=1, uniform='a')

        self.create_checkboxes(frame).grid(row=0, column=0, rowspan=2, sticky='news', padx=10, pady=10)
        self.create_x_range_entries(frame).grid(row=2, column=0, sticky='news', padx=10, pady=10)
        self.create_savgol_slider(frame).grid(row=3, column=0, sticky='news')
        ttk.Button(frame, text='Add curves', command=self.create_adding_curves_window).grid(row=4, column=0)
        ttk.Button(frame, text='Save plot', command=self.save_plot). grid(row=5, column=0)
        ttk.Button(frame, text='Refresh', command=self.refresh_plot).grid(row=6, column=0)

        return frame

    def create_checkboxes(self, parent):
        frame = ScrolledFrame(parent)
        ttk.Label(frame, text='Display curves:').pack(fill='x')
        for column, idx in zip(self.dataset_current.columns, range(len(self.checkbox_vars))):
            ttk.Checkbutton(frame,
                            text=f'{column}',
                            variable=self.checkbox_vars[idx],
                            onvalue=True,
                            offvalue=False).pack(fill='both')
            canvas = tk.Canvas(frame, width=20, height=20)
            canvas.pack(fill='both')
            canvas.create_rectangle(0, 0, 20, 20, fill=self.colors[idx])

        return frame

    def create_x_range_entries(self, parent):
        frame = ttk.Frame(parent)

        frame.rowconfigure((0, 1), weight=1, uniform='a')
        frame.columnconfigure((0, 1), weight=1, uniform='a')

        ttk.Label(frame, text='Set min X on axis:').grid(row=0, column=0)
        ttk.Label(frame, text='Set max X on axis:').grid(row=1, column=0)
        ttk.Entry(frame, textvariable=self.x_range[0]).grid(row=0, column=1)
        ttk.Entry(frame, textvariable=self.x_range[1]).grid(row=1, column=1)

        return frame

    def create_savgol_slider(self, parent):
        frame = ttk.Frame(parent)

        frame.columnconfigure(0, weight=1, uniform='a')
        frame.rowconfigure((0, 1, 2), weight=1, uniform='a')

        ttk.Label(frame, text='Set level of smoothing plots:').grid(row=0, column=0)
        ttk.Scale(frame, variable=self.savgol_var,
                  from_=3,
                  to=len(self.x) // 5,
                  command=lambda event: self.savgol_var.set(round(int(float(event))))).grid(row=1, column=0)
        ttk.Label(frame, textvariable=self.savgol_var).grid(row=2, column=0)

        return frame

    def create_adding_curves_window(self):
        AddingCurvesWindow(self.dataset_didu, self.x)

    # Event functions
    def refresh_plot(self):
        self.plot_frame.pack_forget()
        self.plot_frame = self.create_plot_frame()
        self.plot_frame.grid(row=0, column=0, columnspan=3, sticky='news')

    def get_entry_values(self):
        try:
            return [float(self.x_range[0].get()), float(self.x_range[1].get())]
        except ValueError:
            Messagebox.show_warning(title='Warning',
                                    message='Provide correct values! Use typical format for float values (x.xxx).')
            self.x_range[0].set(min(self.x))
            self.x_range[1].set(max(self.x))
            return [min(self.x), max(self.x)]

    def save_plot(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                 filetypes=[("PNG files", "*.png")])
        if file_path:
            self.fig.savefig(file_path)
