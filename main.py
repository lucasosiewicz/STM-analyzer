import tkinter as tk
from tkinter import ttk, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy.signal import savgol_filter
import pandas as pd
import numpy as np
import spym


def open_file():
    file_path = filedialog.askopenfilename(
        title='Choose file',
        initialdir='/data',
        filetypes=[('SM4', '*.SM4')])
    file = spym.load(file_path)
    file, num_of_curves, didu = create_dataset(file)
    fill_table(file)
    plot_didu(file, ax, num_of_curves, 25)


def plot_didu(file, ax, num_of_curves, w_size):
    x = file['x']
    y = file[file.columns[:num_of_curves]]
    for column in y.columns:
        y_smoothed = savgol_filter(file[column], w_size, 5)
        ax.plot(x, y_smoothed, label=column, linewidth=0.7)
    ax.grid(True)
    ax.set_xlabel('Bias [V]', fontsize=16)
    ax.set_ylabel('Arb. unit', fontsize=16)
    canvas.get_tk_widget().pack(expand=True, fill='both')


def create_dataset(file):
    dIdU = file['dI/dU_']

    # tworzenie obiektu df
    data = pd.DataFrame(dIdU.values, columns=[f'y{x}' for x in range(dIdU.coords['dI/dU__y'].size)])
    data['x'] = dIdU.coords['dI/dU__x']

    # przeszukiwanie metadanych w poszukiwaniu informacji ile krzywych zrobiono w jednym punkcie
    idx = dIdU.attrs['RHK_PRMdata'].find('<1101>')
    curves_per_point = int(dIdU.attrs['RHK_PRMdata'][idx + 28:idx + 29])

    # wyznaczanie ilości krzywych i punktów pomiarowych
    num_of_curves = dIdU.coords['dI/dU__y'].size
    num_of_points = num_of_curves // curves_per_point

    # tworzenie przedziałów punktowych
    intervals = np.linspace(0, num_of_curves, num_of_points + 1, dtype=int)

    # warunek sprawdzający od jakiego kierunku zaczynał się pomiar spektroskopii, OFF = forward, ON = backward
    idx = dIdU.attrs['RHK_PRMdata'].find('<1833>')
    i = -1 if dIdU.attrs['RHK_PRMdata'][idx + 34:idx + 36] == 'ON' else 1

    for idx in range(len(intervals) - 1):
        for fb, name in enumerate(['forward', 'backward'][::i]):
            start = fb + intervals[idx]
            stop = intervals[idx + 1]
            columns = data.columns[start:stop:2]
            data[f'mean_{name}_p{idx + 1}'] = data[columns].mean(axis=1)

    for fb, name in enumerate(['forward', 'backward'][::i]):
        start = fb + num_of_curves + 1
        stop = fb + num_of_curves + 1 + num_of_points * 2
        columns = data.columns[start:stop:2]
        data[f'mean_{name}'] = data[columns].mean(axis=1)

    return data, num_of_curves, dIdU


def fill_table(data):
    # filling table
    table.configure(columns=list(data.columns), show='headings')
    for column in data.columns:
        table.heading(column, text=column)
    for idx in range(data.shape[0]):
        table.insert('', index=idx, values=tuple(data.iloc[idx].values))
    x_scrollbar = ttk.Scrollbar(root, orient="horizontal", command=table.xview)
    y_scrollbar = ttk.Scrollbar(root, orient="vertical", command=table.yview)

    # Konfiguracja suwaków
    table.configure(xscrollcommand=x_scrollbar.set, yscrollcommand=y_scrollbar.set)
    table.grid(row=0, column=0, sticky='news')
    x_scrollbar.grid(row=1, column=0, sticky='we')
    y_scrollbar.grid(row=0, column=1, sticky='ns')

# APLIKACJA


root = tk.Tk()
root.title('Inżynierka')
root.geometry('800x600')


# main menu
main_menu = tk.Menu(master=root)
# file menu
file_menu = tk.Menu(master=main_menu,
                    tearoff=False)
file_menu.add_command(label='Open file',
                      command=open_file)
main_menu.add_cascade(label='File',
                      menu=file_menu)

# tabs
notebook = ttk.Notebook(master=root)
# dataset
dataset = ttk.Frame(master=notebook)
table = ttk.Treeview(master=dataset)
dataset.columnconfigure(0, weight=100)
dataset.columnconfigure(1, weight=1)
dataset.rowconfigure(0, weight=100)
dataset.rowconfigure(1, weight=1)
# plots
plots = ttk.Frame(master=notebook)
fig, ax = plt.subplots()
canvas = FigureCanvasTkAgg(fig, master=plots)



# tworzenie siatki
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# layout
notebook.add(dataset, text='Dataset')
notebook.add(plots, text='Plots')
notebook.grid(row=0, column=0, sticky='news')
root.configure(menu=main_menu)


root.mainloop()