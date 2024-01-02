import customtkinter

class View(customtkinter.CTk):
    def __init__(self, restart_command):
        super().__init__()
        self.geometry(f"{1100}x{580}")
        self.progressbar = customtkinter.CTkProgressBar(self)
        self.progressbar.pack()
        self.restart_button = customtkinter.CTkButton(self, text="Restart", command=restart_command)
        self.restart_button.pack()
        
        # make a nunber showing generation count
        self.generation_count = customtkinter.CTkLabel(self, text="Generation: 0")
        self.generation_count.pack()

    def update_progressbar(self, value):
        self.progressbar.set(value)
        self.update_idletasks()

    def update_generation_count(self, value):
        self.generation_count.set(f"Generation: {value}")
        self.update_idletasks()