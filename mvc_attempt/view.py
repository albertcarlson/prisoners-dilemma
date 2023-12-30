import customtkinter as tk

class View(tk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry(f"{1100}x{580}")
        self.progressbar = tk.CTkProgressBar(self)
        self.progressbar.pack()

    def update_progressbar(self, value):
        self.progressbar.set(value / 100)
        self.update_idletasks()