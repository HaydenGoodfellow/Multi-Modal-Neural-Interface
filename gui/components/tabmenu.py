import customtkinter

class TabMenu(customtkinter.CTkTabview):
    def __init__(self, parent):
        super().__init__(parent, parent.width, parent.height)

        self.width = parent.width
        self.height = parent.height

        conn_string = "  Connections  "
        rec_string = "  Recording  "

        self.file_tab = self.add("     File     ")
        self.configurations_tab = self.add(" Configuration ") 
        self.connections_tab = self.add(conn_string) 
        self.recording_tab = self.add(rec_string) 
        self.help_tab = self.add("   Help  ")

        self.set(rec_string)  # set currently visible tab
