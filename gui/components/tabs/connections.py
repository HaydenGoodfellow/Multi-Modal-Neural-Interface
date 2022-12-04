import customtkinter
import tkinter as tk

class ConnectionsTab(customtkinter.CTkFrame):
    def __init__(self, parent, width, height):
        super().__init__(parent.tablists.connections_tab, width, height)

        self.label1 = customtkinter.CTkLabel(master=self, 
            text="Connect to an available device...", 
            font=("Arial", 12))
        self.label1.grid(row=0, column=0, padx=30, pady=30)

        # bluetooth connect button
        self.connect_button = customtkinter.CTkButton(
            self, 
            text ="Connect", 
            command=None)

        self.connect_button.grid(row=10, columnspan=16, padx=30, pady=30, sticky="e")

        self.pack(padx=15, pady=15)
