import re
import customtkinter
import time

class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.current_time = time.time()
        self.past_time = None

    def record(self, start, end):
        print(start, end)
        pass