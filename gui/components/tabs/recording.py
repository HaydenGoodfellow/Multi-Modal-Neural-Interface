import customtkinter
import tkinter as tk
from tkinter import ttk
import numpy as np
from components.tabs.plot import Plot

# Initial Graph Data
x = np.linspace(0, 5, 100)
y = np.zeros(100)

class RecordingTab(customtkinter.CTkFrame):
    def __init__(self, parent, width, height):
        super().__init__(parent.tablists.recording_tab, width, height)

        self.parent = parent
        self.options_frame = customtkinter.CTkFrame(parent.tablists.recording_tab)

        # connection label
        self.device_has_connection_label = customtkinter.CTkLabel(self.options_frame, text="No devices connected", anchor="w")
        self.device_has_connection_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.reading_options = customtkinter.CTkLabel(self.options_frame, text="Select Reading:", anchor="w")
        self.reading_options.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        # EEG checkbox
        self.eeg_check = tk.IntVar()
        self.eeg_check.set(1)
        self.eeg_checkbox = customtkinter.CTkCheckBox(master=self.options_frame, text="EEG", command=None,
                                     variable=self.eeg_check, onvalue=1, offvalue=0)

        self.eeg_checkbox.grid(row=2, column=0, padx=30, pady=7, sticky="w")

        # Electrochemical checkbox
        self.ec_check = tk.IntVar()
        self.ec_check.set(1)
        self.ec_checkbox = customtkinter.CTkCheckBox(master=self.options_frame, text="Electrochemical", command=None,
                                     variable=self.ec_check, onvalue=1, offvalue=0)

        self.ec_checkbox.grid(row=3, column=0, padx=30, pady=7, sticky="w")

        # Frequency label
        self.device_has_connection_label = customtkinter.CTkLabel(self.options_frame, text="Frequency (Hz)", anchor="w")
        self.device_has_connection_label.grid(row=4, column=0, padx=10, pady=10, sticky="w")

        self.frequency = tk.StringVar()
        self.frequency.set("100")

        # Frequency Input
        self.freq_entry = customtkinter.CTkEntry(self.options_frame, textvariable=self.frequency)
        self.freq_entry.grid(row=4, column=1, columnspan=3,sticky=tk.W)

        self.rec_state = tk.StringVar()
        self.rec_state.set("Record")

        # function label
        self.functions_device = customtkinter.CTkLabel(self.options_frame, text="Functions that can be used without a device:", anchor="w")
        self.functions_device.grid(row=8, column=0, padx=10, pady=10, sticky="w")

        self.func_options = customtkinter.CTkOptionMenu(master=self.options_frame,
                                       values=["None", "Sine", "Cosine", "Tangent"],
                                       command=self.set_func)

        self.func_options.grid(row=9, column=0, padx=15, pady=15, sticky="e")
        self.func_options.set("None")

        # recording button
        self.record_button = customtkinter.CTkButton(
            master=self.options_frame, 
            text=self.rec_state.get(), 
            command=self.record_button_clicked)

        self.record_button.grid(row=10, column=8, padx=15, pady=15, sticky="e")

        # Beginning of graphing frame

        self.graph_frame = customtkinter.CTkFrame(parent.tablists.recording_tab)

        # Scrollbar

        self.canvas = tk.Canvas(self.graph_frame)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        self.scrollbar = ttk.Scrollbar(self.graph_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # create another frame inside the canvas

        self.graphs = ttk.Frame(self.canvas)

        # add frame to canvas

        self.canvas.create_window((0, 0), window=self.graphs, anchor="nw")

        self.eeg_graph = Plot( self.graphs, "EEG Readings", "Time (seconds)", "Units", x, y)

        self.eeg_graph.grid(row=1, column=0, padx=15, pady=15, sticky="e")

        self.ec_graph = Plot( self.graphs, "Electrochemical Readings", "Time (seconds)", "Units", x, y)

        self.ec_graph.grid(row=2, column=0, padx=15, pady=15, sticky="e")

        # Two sides packed into the window
        self.options_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        self.graph_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)
    
    def update_graphs(self):
        if self.rec_state.get() == "Recording...":
            data = self.parent.controller.get_data()
            x = data[0]
            y = data[1]

            if self.eeg_check.get():

                self.update_plot(self.eeg_graph.figure_canvas, self.eeg_graph.axes, "EEG Readings", "Time (seconds)", "Units", x, y)

            if self.ec_check.get():

                self.update_plot(self.ec_graph.figure_canvas, self.ec_graph.axes, "Electrochemical Readings", "Time (seconds)", "Units", x, y)

            self.graphs.after(1, self.update_graphs)

    def set_func(self, choice):
        self.parent.controller.set_func(choice)

    def update_plot(self, canvas, axes, title, x, y, x_data, y_data):
        axes.clear()
        axes.plot(x_data, y_data)
        axes.set_title(title)
        axes.set_xlabel(x)
        axes.set_ylabel(y)
        canvas.draw()

    def record_button_clicked(self):
        if self.parent.controller:

            if self.rec_state.get() == "Recording...":
                time_passed = self.parent.controller.stop_record()

                data = self.parent.controller.get_data()
                data_x = data[0]
                data_y = data[1]
                self.rec_state.set("Record")
                # recording button
                self.record_button.destroy()

                self.record_button = customtkinter.CTkButton(
                master=self.options_frame, 
                text=self.rec_state.get(), 
                command=self.record_button_clicked)
                self.record_button.grid(row=10, column=8, padx=15, pady=15, sticky="e")

                if self.eeg_check.get():
                    self.update_plot(self.eeg_graph.figure_canvas, self.eeg_graph.axes, "EEG Readings", "Time (seconds)", "Units", data_x, data_y)


                if self.ec_check.get():
                    self.update_plot(self.ec_graph.figure_canvas, self.ec_graph.axes, "Electrochemical Readings", "Time (seconds)", "Units", data_x, data_y)

            else: 
                self.parent.controller.record(self.frequency)
                self.rec_state.set("Recording...")
                # recording button
                self.record_button.destroy()

                self.record_button = customtkinter.CTkButton(
                master=self.options_frame, 
                text=self.rec_state.get(), 
                command=self.record_button_clicked,
                bg_color="GREEN")
                self.record_button.grid(row=10, column=8, padx=15, pady=15, sticky="e")

                self.update_graphs()
        