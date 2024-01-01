import customtkinter

class View(customtkinter.CTk):
    def __init__(self, restart_command):
        super().__init__()
        self.geometry(f"{1100}x{580}")
        self.progressbar = customtkinter.CTkProgressBar(self)
        self.progressbar.pack()
        self.restart_button = customtkinter.CTkButton(self, text="Restart", command=restart_command)
        self.restart_button.pack()

    def update_progressbar(self, value):
        self.progressbar.set(value / 30)
        self.update_idletasks()

