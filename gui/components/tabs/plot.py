import matplotlib
import numpy as np
import customtkinter
import tkinter as tk

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk
)

matplotlib.use('TkAgg')

class Plot(customtkinter.CTkFrame):
    def __init__(self, parent, title, x, y, x_data, y_data):
        super().__init__(parent)

         # create a figure
        figure = Figure(figsize=(6, 4), dpi=100)

        # create FigureCanvasTkAgg object
        figure_canvas = FigureCanvasTkAgg(figure, self)

        # create the toolbar
        NavigationToolbar2Tk(figure_canvas, self)

        # create axes
        axes = figure.add_subplot(111)
        axes.plot(x_data, y_data)
        axes.set_title(title)
        axes.set_xlabel(x)
        axes.set_ylabel(y)

        figure_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)