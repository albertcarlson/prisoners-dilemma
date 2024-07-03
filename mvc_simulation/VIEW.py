import customtkinter

class View(customtkinter.CTk):
    def __init__(self, next_generation_cmd):
        super().__init__()
        self.geometry(f"{350}x{580}")
        self.progressbar = customtkinter.CTkProgressBar(self)
        self.progressbar.pack()
        self.progressbar.set(0)
        self.next_generation_button = customtkinter.CTkButton(self, text="Restart", command=next_generation_cmd)
        self.next_generation_button.pack()
        
        # make a nunber showing generation count
        self.generation_count = customtkinter.CTkLabel(self, text="Generation: 0")
        self.generation_count.pack()

        # leaderboard showing population counts
        self.population_title = customtkinter.CTkLabel(self, text="Populations", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.population_title.pack()
        self.population_counts = customtkinter.CTkLabel(self)
        self.population_counts.pack()

    def update_progressbar(self, value):
        self.progressbar.set(value)
        self.update_idletasks()

    def update_generation_count(self, value):
        self.generation_count.configure(text=f"Generation: {value}")
        self.update_idletasks()

    def update_population_counts(self, value: dict[str, int]):
        stringified = "\n".join([f"{species_name}: {count}" for species_name, count in value.items()])
        self.population_counts.configure(text=f"{stringified}")
        self.update_idletasks()