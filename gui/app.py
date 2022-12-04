import customtkinter
from tkinter import Menu

# local
from model import Model
from view import View
from controller import Controller

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        customtkinter.set_default_color_theme("dark-blue")  
        customtkinter.set_appearance_mode("dark")

        self.width = 1080
        self.height = 720

        self.title("Multi-Modal Neural Interface Sample")
        self.minsize(self.width, self.height)

        # create a view and place it on the root window
        view = View(self)
        view.grid(row=0, column=0, padx=10, pady=10)

        model = Model()

        # create a controller
        controller = Controller(model, view)

        # set the controller to view
        view.set_controller(controller)

if __name__ == "__main__":
    app = App()
    app.mainloop()