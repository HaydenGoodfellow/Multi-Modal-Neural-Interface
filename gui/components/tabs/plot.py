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
        self.figure = Figure(figsize=(6, 4), dpi=100)

        # create FigureCanvasTkAgg object
        self.figure_canvas = FigureCanvasTkAgg(self.figure, self)

        # create the toolbar
        NavigationToolbar2Tk(self.figure_canvas, self)

        # create axes
        self.axes = self.figure.add_subplot(111)
        self.axes.plot(x_data, y_data)
        self.axes.set_title(title)
        self.axes.set_xlabel(x)
        self.axes.set_ylabel(y)

        self.figure_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)