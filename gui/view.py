import customtkinter

import matplotlib
import numpy as np
import tkinter as tk

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk
)

from components.tabmenu import TabMenu
from components.tabs.connections import ConnectionsTab
from components.tabs.recording import RecordingTab

matplotlib.use('TkAgg')

class View(customtkinter.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.width = parent.width
        self.height = parent.height
        
        self.configure(width=self.width, height=self.height)

        self.tablists = TabMenu(self)

        self.connections_frame = ConnectionsTab(self.tablists.connections_tab, width=self.width, height=self.height)

        self.recording_frame = RecordingTab(self.tablists.connections_tab, width=self.width, height=self.height)

        self.tablists.pack(padx=20, pady=20)

        # x = np.linspace(0, 5, 100)
        # y = np.zeros(100)

        # self.eeg_plot = customtkinter.CTkFrame(self)

        # self.plotting(self.eeg_plot, "EEG Readings", 'Time (seconds)', 'Units', x, y)

        # self.eeg_plot.grid(row=0, column=0, columnspan=8, sticky=customtkinter.EW)

    def set_controller(self, controller):
        """
        Set the controller
        :param controller:
        :return:
        """
        self.controller = controller

    def plotting(self, frame, title, x, y, x_data, y_data):

        # create a figure
        figure = Figure(figsize=(6, 4), dpi=200)

        # create FigureCanvasTkAgg object
        figure_canvas = FigureCanvasTkAgg(figure, frame)

        # create the toolbar
        NavigationToolbar2Tk(figure_canvas, frame)

        # create axes
        axes = figure.add_subplot(111)
        axes.plot(x_data, y_data)
        axes.set_title(title)
        axes.set_xlabel(x)
        axes.set_ylabel(y)

        figure_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)