import re
import tkinter as tk
from tkinter import ttk

class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def record(self, start, end):
        print(start, end)
        pass