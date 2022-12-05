import numpy as np
import time

class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.frequency = 100
        self.function = None
        self.current_time = time.time()
        self.past_time = None

    def set_func(self, choice):
        if choice == "None":
            self.function = None
        else:
            self.function = choice

    def record(self, freq):
        self.past_time = time.time()
        self.frequency = freq

    def stop_record(self):
        self.current_time = time.time()

        return self.current_time - self.past_time

    # pulls data from that second
    def get_data(self):
        seconds_passed = int(time.time() - self.past_time)

        freq = int(self.frequency.get())

        ratio_freq_remainder = 0
        float_time_passed = 0

        x_data = None
        y_data = None
    
        float_time_passed = time.time() - self.past_time - seconds_passed
        ratio_freq_remainder += int(float_time_passed * freq)


        x_data = np.linspace(0, seconds_passed + float_time_passed, freq * seconds_passed + ratio_freq_remainder)

        if self.function == "Sine":
            y_data = np.sin(x_data)
        elif self.function == "Cosine":
            y_data = np.cos(x_data)
        elif self.function == "Tangent":
            y_data = np.tan(x_data)
        else:
            y_data = np.zeros(freq * seconds_passed + ratio_freq_remainder)


        return (x_data, y_data)

