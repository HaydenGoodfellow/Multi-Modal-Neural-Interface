import tkinter as tk
from tkinter import ttk
import matplotlib
import pandas as pd
import numpy as np

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk
)

matplotlib.use('TkAgg')


class View(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.tab_parent = ttk.Notebook(self, width=800, height=600)

        self.tab1 = ttk.Frame(self.tab_parent)
        self.main_tab2 = ttk.Frame(self.tab_parent)

        # FIRST TAB
        
        self.first_tab()

        # SECOND TAB

        self.second_tab_scroll_module()

        self.tab1.pack(fill='both', expand=1)
        self.main_tab2.pack(fill='both', expand=1)

        # tab names
        self.tab_parent.add(self.tab1, text="Connections...")
        self.tab_parent.add(self.main_tab2, text="Recording")

        self.tab_parent.pack(expand=1, fill='both')

        # set the controller
        self.controller = None

    def first_tab(self):
        # choose a device label
        self.device_has_connection_label = tk.Label(self.tab1, text="Choose a device...", anchor="w")
        self.device_has_connection_label.grid(row=0, column=0, padx=15, pady=10, sticky="w")

        # bluetooth connect button
        self.connect_button = tk.Button(
            self.tab1, 
            text ="Connect", 
            command=None)

        self.connect_button.grid(row=10, column=16, padx=15, pady=15, sticky="e")

    def second_tab_scroll_module(self):
        self.canvas = tk.Canvas(self.main_tab2)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        # add a scrollbar to canvas

        self.scrollbar = ttk.Scrollbar(self.main_tab2, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # configure the canvas

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # create another frame inside the canvas

        self.tab2 = ttk.Frame(self.canvas)

        # add frame to canvas

        self.canvas.create_window((0, 0), window=self.tab2, anchor="nw")

        self.second_tab()

    def second_tab(self):

        # connection label
        self.device_has_connection_label = tk.Label(self.tab2, text="No devices connected", anchor="w")
        self.device_has_connection_label.grid(row=0, column=0, padx=15, pady=10, sticky="w")

        self.reading_options = tk.Label(self.tab2, text="Select Reading:",  anchor="w")
        self.reading_options.grid(row=1, column=0, padx=15, pady=5, sticky="w")

        # eeg checkbutton
        self.eeg = tk.IntVar()
        self.eeg.set(1)

        self.eeg_button = ttk.Checkbutton(self.tab2,
                        text='EEG',
                        variable=self.eeg,
                        onvalue=1,
                        offvalue=0)

        self.eeg_button.grid(row=2, column=0, padx=30, sticky="w")

        self.ec = tk.IntVar()
        self.ec.set(1)

        self.ec_button = ttk.Checkbutton(self.tab2,
                        text='Electrochemistry',
                        variable=self.ec,
                        onvalue=1,
                        offvalue=0)

        self.ec_button.grid(row=3, column=0, padx=30, sticky="w")

        # start label
        self.start_label = ttk.Label(self.tab2, text='START (seconds):')
        self.start_label.grid(row=4, column=0, padx=30, pady=10, sticky="w")

        self.start = tk.StringVar()
        self.start_entry = ttk.Entry(self.tab2, textvariable=self.start, width=30)
        self.start_entry.grid(row=4, column=1, columnspan=3,sticky=tk.W)

        self.set_start('0')

        # end label
        self.end_label = ttk.Label(self.tab2, text='END (seconds):')
        self.end_label.grid(row=4, column=4, padx=30, pady=10, sticky="w")

        self.end = tk.StringVar()
        self.end_entry = ttk.Entry(self.tab2, textvariable=self.end, width=30)
        self.end_entry.grid(row=4, column=5, columnspan=3,sticky=tk.W)

        self.set_end('5')

        self.eeg_plot = ttk.Frame(self.tab2)


        # frequency label
        self.frequency_label = ttk.Label(self.tab2, text='Frequency (hz): ')
        self.frequency_label.grid(row=5, column=0, padx=30, pady=10, sticky="w")

        self.frequency = tk.StringVar()
        self.frequency_entry = ttk.Entry(self.tab2, textvariable=self.frequency, width=30)
        self.frequency_entry.grid(row=5, column=1, columnspan=3,sticky=tk.W)

        self.set_freq('100')
        self.num_points = self.get_num_points()

        x = np.linspace(self.get_start(), self.get_end(), self.num_points)
        y = np.zeros(self.num_points)

        self.plotting(self.eeg_plot, "EEG Readings", 'Time (seconds)', 'Units', x, y)

        self.eeg_plot.grid(row=6, column=0, columnspan=8, sticky=tk.EW)

        self.ec_plot = ttk.Frame(self.tab2)

        self.plotting(self.ec_plot, "Electrochemical Readings", 'Time (seconds)', 'Units', x, y)

        self.ec_plot.grid(row=7, column=0, columnspan=8, sticky=tk.EW)

        # recording button
        self.record_button = tk.Button(
            self.tab2, 
            text ="Record", 
            command=self.record_button_clicked)

        self.record_button.grid(row=8, column=8, padx=15, pady=15, sticky="e")

    def get_num_points(self):
        return int(self.get_freq() * (self.get_end() - self.get_start()))
    
    def plotting(self, frame, title, x, y, x_data, y_data):

        # create a figure
        figure = Figure(figsize=(6, 4), dpi=100)

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

    def change_plot(self, frame, title, x, y, x_data, y_data):

        for widget in frame.winfo_children():
            widget.destroy()

        # create a figure
        figure = Figure(figsize=(6, 4), dpi=100)

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


    def set_controller(self, controller):
        """
        Set the controller
        :param controller:
        :return:
        """
        self.controller = controller

    def get_start(self):
        return float(self.start.get())

    def set_start(self, val):
        self.start.set(val)

    def get_end(self):
        return float(self.end.get())

    def set_end(self, val):
        self.end.set(val)    
    
    def get_freq(self):
        return float(self.frequency.get())

    def set_freq(self, val):
        self.frequency.set(val) 

    def record_button_clicked(self):
        if self.controller:
            self.controller.record(self.get_start(), self.get_end())

            if(self.eeg.get() == 1):
                self.num_points = self.get_num_points()
                x = np.linspace(self.get_start(), self.get_end(), self.num_points)
                y = np.zeros(self.num_points)
                
                self.change_plot(self.eeg_plot, "EEG Readings", 'Time (seconds)', 'Units', x, y)

            if(self.ec.get() == 1):
                self.num_points = self.get_num_points()
                x = np.linspace(self.get_start(), self.get_end(), self.num_points)
                y = np.zeros(self.num_points)
                
                self.change_plot(self.ec_plot, "EEG Readings", 'Time (seconds)', 'Units', x, y)
            
