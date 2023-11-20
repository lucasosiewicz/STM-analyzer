import spym
import numpy as np
import pandas as pd
import tkinter as tk
import numdifftools as nd
import matplotlib.pyplot as plt
from tkinter import ttk, filedialog
from matplotlib.figure import Figure
from scipy.signal import savgol_filter
from sklearn.metrics import mean_squared_error
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import train_test_split
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk


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
        self.label1 = ttk.Label(self)
        self.label2 = ttk.Label(self)
        self.label3 = ttk.Label(self)
        self.label4 = ttk.Label(self)
        self.label5 = ttk.Label(self)
        self.label6 = ttk.Label(self)
        self.label7 = ttk.Label(self)

        # Extra Window
        self.extra_window = None

    def load_file(self):
        # function executing while pressing Open Button
        file_path = filedialog.askopenfilename(
            title='Choose file',
            initialdir='/data',
            filetypes=[('SM4', '*.SM4')])
        self.file = spym.load(file_path)

        labels = [self.label1, self.label2, self.label3, self.label4, self.label5, self.label6, self.label7]

        if self.local_visibility:
            for label in labels:
                label.pack_forget()
            self.extra_window.destroy()
        self.local_visibility = True

        # Changing labels' content
        self.label1.configure(text=f"File's name: {self.fetch_filename()}")
        self.label2.configure(text=f"Picture's size (px): {self.fetch_picture_size()[0]}x{self.fetch_picture_size()[1]}")
        self.label3.configure(text=f"Picture's size (nm): {self.fetch_picture_size()[2]}")
        self.label4.configure(text=f"Spectroscopy's first direction: {self.fetch_forward_or_backward()}")
        self.label5.configure(text=f"Spectroscopy's range: {self.fetch_spectroscopy_range()[0]}V - {self.fetch_spectroscopy_range()[1]}V")
        self.label6.configure(text=f"Curves per one point: {self.fetch_curves_per_point()}")
        self.label7.configure(text=f"Number of points: {self.fetch_number_of_points()}")

        # Showing labels
        for label in labels:
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


class Menu(tk.Menu):
    def __init__(self, parent, menu_name, submenu_name, function):
        super().__init__(parent)
        self.create_submenu(menu_name, submenu_name, function)

    def create_submenu(self, menu_name, submenu_name, function):
        submenu = tk.Menu(self, tearoff=False)
        submenu.add_command(label=submenu_name, command=function)
        self.add_cascade(label=menu_name, menu=submenu)


class ExtraWindow(tk.Toplevel):
    def __init__(self, file, curves_per_point, number_of_points, forward_or_backward):
        super().__init__()

        self.title(file['dI/dU_'].attrs['filename'])
        self.geometry('800x700')

        # Tabs
        self.notebook = Notebook(self, file, curves_per_point, number_of_points, forward_or_backward)
        self.notebook.pack(expand=True, fill='both')


class Notebook(ttk.Notebook):
    def __init__(self, parent, file, curves_per_point, number_of_points, forward_or_backward):
        super().__init__(parent)
        # Tabs
        self.dataset = Dataset(self, file, curves_per_point, number_of_points, forward_or_backward)
        self.plots = Plots(self, self.dataset.dataset_dIdU, self.dataset.dataset_current, curves_per_point, number_of_points)

        # Adding Tabs to the Notebook
        self.add(self.dataset, text='Dataset')
        self.add(self.plots, text='Plots')


class Dataset(ttk.Notebook):
    def __init__(self, parent, file, curves_per_point, number_of_points, forward_or_backward):
        super().__init__(parent)

        # Class variables
        self.file = file                                                                                    # dane z pliku
        self.curves_per_point = curves_per_point                                                            # ilość krzywych na punkt
        self.number_of_points = number_of_points                                                            # ilość punktów
        self.number_of_curves = self.curves_per_point * self.number_of_points                               # liczba krzywych łącznie
        self.forward_or_backward = forward_or_backward                                                      # czy rozpoczęto od forward
        self.intervals = np.linspace(0, self.number_of_curves, self.number_of_points + 1, dtype=int)   # tworzenie przedziałów punktowych

        self.dataset_dIdU = self.create_dataset('dI/dU_')
        self.dataset_current = self.create_dataset('Current_')

        # Widgets
        self.tab_dIdU = self.split_points(self.dataset_dIdU)
        self.tab_current = self.split_points(self.dataset_current)                                           # zakładka dla kanału Current

        # Layout
        self.add(self.tab_dIdU, text='dI/dU')
        self.add(self.tab_current, text='Current')


        self.pack(expand=True, fill='both')

    # Funkcja przetwarza dane i zwraca je w postaci DataFrame
    def create_dataset(self, variable):
        # tworzenie obiektu df
        data = pd.DataFrame(self.file[variable].values,
                            columns=[f'y{x}' for x in range(self.file[variable].coords[f'{variable}_y'].size)])
        data['x'] = self.file[variable].coords[f'{variable}_x']

        # warunek sprawdzający od jakiego kierunku zaczynał się pomiar spektroskopii, OFF = forward, ON = backward
        i = -1 if self.forward_or_backward else 1

        # Liczenie średniej forward i backward dla każdego punktu
        for idx in range(len(self.intervals) - 1):
            for fb, name in enumerate(['forward', 'backward'][::i]):
                start = fb + self.intervals[idx]
                stop = self.intervals[idx + 1]
                columns = data.columns[start:stop:2]
                data[f'mean_{name}_p{idx + 1}'] = data[columns].mean(axis=1)

        for idx in range(len(self.intervals) - 1):
            start = self.intervals[idx]
            stop = self.intervals[idx + 1]
            columns = data.columns[start:stop]
            data[f'mean_p{idx + 1}'] = data[columns].mean(axis=1)

        # Liczenie średniej dla każdego punktu
        for fb, name in enumerate(['forward', 'backward'][::i]):
            start = fb + self.number_of_curves + 1
            stop = fb + self.number_of_curves + (self.number_of_points * 2) + 1
            columns = data.columns[start:stop:2]
            data[f'mean_{name}'] = data[columns].mean(axis=1)

        return data

    # Funkcja tworzy i zasila danymi obiekt treeview
    def create_treeview(self, frame, dataset, interval):
        if interval == self.intervals[-1]:
            new_data = dataset.iloc[:, self.number_of_curves:]
        else:
            new_data = pd.concat([dataset['x'], dataset.iloc[:, interval:interval + self.curves_per_point]], axis=1)

        table = ttk.Treeview(frame)
        table.configure(columns=list(new_data.columns), show='headings')

        for column in new_data.columns:
            table.heading(column, text=column)
            table.column(column, width=170, anchor=tk.CENTER, stretch=False)

        for idx in range(new_data.shape[0]):
            table.insert('', index=idx, values=tuple(new_data.iloc[idx].values))

        table.insert("", "end", text=" ", values=[''] * len(new_data))

        return table

    # Funkcja umieszcza scrollbary w obiekcie treeview
    def place_scrollbar(self, frame):
        scrollbar_x = ttk.Scrollbar(frame, orient='horizontal', command=frame.xview)
        scrollbar_y = ttk.Scrollbar(frame, orient='vertical', command=frame.yview)

        frame.configure(xscrollcommand=scrollbar_x.set, yscrollcommand=scrollbar_y.set)

        scrollbar_x.place(relx=0, rely=0.97, relwidth=1, anchor='nw')
        scrollbar_y.place(relx=1, rely=0, relheight=1, anchor='ne')

    # Funkcja dzieli dataset na poszczególne punkty i pakuje je do obiektu notebook
    def split_points(self, dataset):
        main_frame = ttk.Frame(self)
        notebook_of_points = ttk.Notebook(main_frame)

        for nop, interval in enumerate(self.intervals):
            frame = ttk.Frame(notebook_of_points)
            treeview = self.create_treeview(frame, dataset, interval)
            self.place_scrollbar(treeview)
            treeview.pack(expand=True, fill='both')
            if interval == self.intervals[-1]:
                text = 'Stats'
            else:
                text = f'Point {nop + 1}'
            notebook_of_points.add(frame, text=text)

        notebook_of_points.pack(expand=True, fill='both')

        return main_frame


class Plots(ttk.Notebook):
    def __init__(self, parent, dataset_didu, dataset_current, curves_per_point, number_of_points):
        super().__init__(parent)

        # Class variables
        self.dataset_dIdU = dataset_didu
        self.dataset_current = dataset_current
        self.curves_per_point = curves_per_point
        self.number_of_points = number_of_points
        self.number_of_curves = curves_per_point * number_of_points
        self.x_dIdU = self.dataset_dIdU['x']
        self.y_dIdU = self.dataset_dIdU[self.dataset_dIdU.columns[-self.number_of_points-2:-2]]
        self.x_current = self.dataset_dIdU['x']
        self.y_current = self.dataset_current[self.dataset_current.columns[-self.number_of_points-2:-2]]
        self.slider_dIdU_var = tk.IntVar(value=6)
        self.slider_current_var = tk.IntVar(value=6)
        self.div_didu_var = tk.BooleanVar(value=False)
        self.div_current_var = tk.BooleanVar(value=False)

        # Widgets
        self.tab_dIdU = ttk.Frame(self)
        self.fig_dIdU = Figure(figsize=(11, 5))
        self.ax_dIdU = self.fig_dIdU.add_subplot(111)
        self.plot_dIdU = FigureCanvasTkAgg(self.fig_dIdU, master=self.tab_dIdU)
        self.toolbar_dIdU = NavigationToolbar2Tk(self.plot_dIdU, self.tab_dIdU, pack_toolbar=False)
        self.button_dIdU = ttk.Button(self.tab_dIdU, text='Refresh',
                                      command=lambda: self.create_plot(self.ax_dIdU, self.plot_dIdU, self.x_dIdU, self.y_dIdU, self.slider_dIdU_var, self.toolbar_dIdU, self.div_didu_var))
        self.slider_dIdU = ttk.Scale(self.tab_dIdU, variable=self.slider_dIdU_var,
                                     orient='horizontal', from_=6, to=35)
        self.slider_dIdU_label = ttk.Label(self.tab_dIdU, textvariable=self.slider_dIdU_var)
        self.checkbox_didu = ttk.Checkbutton(self.tab_dIdU, text='Show derivative', variable=self.div_didu_var, onvalue=True, offvalue=False)

        self.tab_current = ttk.Frame(self)
        self.fig_current = Figure(figsize=(11, 5))
        self.ax_current = self.fig_current.add_subplot(111)
        self.plot_current = FigureCanvasTkAgg(self.fig_current, master=self.tab_current)
        self.toolbar_current = NavigationToolbar2Tk(self.plot_current, self.tab_current, pack_toolbar=False)
        self.button_current = ttk.Button(self.tab_current, text='Refresh',
                                         command=lambda: self.create_plot(self.ax_current, self.plot_current, self.x_current, self.y_current, self.slider_current_var, self.toolbar_current, self.div_current_var))
        self.slider_current = ttk.Scale(self.tab_current, variable=self.slider_current_var,
                                        orient='horizontal', from_=6, to=35)
        self.slider_current_label = ttk.Label(self.tab_current, textvariable=self.slider_current_var)
        self.checkbox_current = ttk.Checkbutton(self.tab_current, text='Show derivative', variable=self.div_current_var, onvalue=True, offvalue=False)


        # Layout
        #self.create_plot_current()
        self.create_plot(self.ax_dIdU, self.plot_dIdU, self.x_dIdU, self.y_dIdU, self.slider_dIdU_var, self.toolbar_dIdU, self.div_didu_var)
        self.create_plot(self.ax_current, self.plot_current, self.x_current, self.y_current, self.slider_current_var, self.toolbar_current, self.div_current_var)

        self.button_dIdU.pack()
        self.button_current.pack()
        self.slider_dIdU.pack()
        self.slider_current.pack()
        self.slider_dIdU_label.pack()
        self.slider_current_label.pack()
        self.checkbox_didu.pack()
        self.checkbox_current.pack()


        self.add(self.tab_dIdU, text='dI/dU')
        self.add(self.tab_current, text='Current')

        self.pack(expand=True, fill='both')

    def create_plot(self, plot, canvas, data_x, data_y, slider_var, toolbar, is_div):
        plot.clear()
        for column in data_y.columns:
            if is_div.get():
                y = self.count_derivative(data_y, column)(data_x)
            else:
                y = data_y[column].values
            y_smoothed = savgol_filter(y, slider_var.get(), 2)
            plot.plot(data_x, y_smoothed, label=column, linewidth=0.7)
        plot.grid(True)
        plot.legend()
        plot.set_xlabel('Bias [V]', fontsize=12)
        plot.set_ylabel('dI/dU [abr. unit]', fontsize=12)

        canvas.draw()
        canvas.get_tk_widget().pack()
        toolbar.pack(anchor='w', fill=tk.X)

    def count_derivative(self, y_data, column):
        return nd.Derivative(np.poly1d(np.polyfit(self.x_dIdU, y_data[column].values, deg=9)))





# Opis osi
# Legenda
# Liczenie pochodnej
app = App()
app.mainloop()
