import customtkinter
import tkinter as tk

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

        # recording button
        self.record_button = customtkinter.CTkButton(
            master=self.options_frame, 
            text=self.rec_state.get(), 
            command=self.record_button_clicked)

        self.record_button.grid(row=8, column=8, padx=15, pady=15, sticky="e")

        self.graph_frame = customtkinter.CTkFrame(parent.tablists.recording_tab)

        # Graphing label
        self.device_has_connection_label = customtkinter.CTkLabel(self.graph_frame, text="Recordings of Graphs", anchor="w")
        self.device_has_connection_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")

        self.options_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        self.graph_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)

    def record_button_clicked(self):
        if self.parent.controller:

            if self.rec_state.get() == "Recording...":
                print("Stopped Recording")
                self.rec_state.set("Record")
                # recording button
                self.record_button.destroy()

                self.record_button = customtkinter.CTkButton(
                master=self.options_frame, 
                text=self.rec_state.get(), 
                command=self.record_button_clicked)
                self.record_button.grid(row=8, column=8, padx=15, pady=15, sticky="e")

            else: 
                print("Started recording...")
                self.rec_state.set("Recording...")
                # recording button
                self.record_button.destroy()

                self.record_button = customtkinter.CTkButton(
                master=self.options_frame, 
                text=self.rec_state.get(), 
                command=self.record_button_clicked,
                bg_color="GREEN")
                self.record_button.grid(row=8, column=8, padx=15, pady=15, sticky="e")
        