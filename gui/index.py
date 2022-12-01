# third party
import tkinter as tk
from tkinter import Menu

# local
from model import Model
from view import View
from controller import Controller

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Multi-Modal-Neural-Interface Demo')
        self.record_options = ('EEG', 'ECG')

        menubar = Menu(self)
        self.config(menu=menubar)
        self.geometry("1080x720+50+50")

        # create a menu
        file_menu = Menu(menubar, tearoff=False)

        # add menu items to the File menu
        file_menu.add_command(label='Open...')
        file_menu.add_separator()

        #add exit menu to menubar
        file_menu.add_command(
            label='Exit',
            command=self.destroy
        )

        # add the File menu to the menubar
        menubar.add_cascade(
            label="File",
            menu=file_menu
        )

        # create a model
        model = Model()

        # create a view and place it on the root window
        view = View(self)
        view.grid(row=0, column=0, padx=10, pady=10)

        # create a controller
        controller = Controller(model, view)

        # set the controller to view
        view.set_controller(controller)


if __name__ == '__main__':
    app = App()
    app.mainloop()