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

        self.connections_frame = ConnectionsTab(self, width=self.width, height=self.height)

        self.recording_frame = RecordingTab(self, width=self.width, height=self.height)

        self.tablists.pack(padx=20, pady=20)

    def set_controller(self, controller):
        """
        Set the controller
        :param controller:
        :return:
        """
        self.controller = controller
