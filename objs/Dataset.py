import numpy as np
import pandas as pd
import tkinter as tk
from ttkbootstrap import ttk


class Dataset(ttk.Notebook):
    def __init__(self, parent, file, curves_per_point, number_of_points, forward_or_backward):
        super().__init__(parent)

        # Class variables
        self.file = file
        self.curves_per_point = curves_per_point
        self.number_of_points = number_of_points
        self.number_of_curves = self.curves_per_point * self.number_of_points
        self.forward_or_backward = forward_or_backward
        self.intervals = np.linspace(0, self.number_of_curves, self.number_of_points + 1, dtype=int)

        self.dataset_dIdU = self.create_dataset('dI/dU_')
        self.dataset_current = self.create_dataset('Current_')

        # Widgets
        self.tab_dIdU = self.split_points(self.dataset_dIdU)
        self.tab_current = self.split_points(self.dataset_current)

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

        # warunek sprawdzający, od jakiego kierunku zaczynał się pomiar spektroskopii, OFF = forward, ON = backward
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
