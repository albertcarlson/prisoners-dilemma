from mvc_simulation.MODEL import MODEL_Simulation as Model
from mvc_simulation.VIEW import View
import threading
# from multiprocessing import Process

class Controller:
    def __init__(self):
        self.model = Model()
        self.view = View(self.run_generation)
        self.view.after(2000, self.update_view)  # schedule the first update

    def run(self):
        #threading.Thread(target=self.model.iterate).start()  # Try with Process(...) instead of threading.Thread(...)
        self.run_generation()
        self.view.mainloop()

    def run_generation(self):
        self.running_gen_thread = threading.Thread(target=self.model.do_generation)
        self.running_gen_thread.start()

    def update_view(self):
        self.view.update_progressbar(self.model.progress)
        self.view.update_generation_count(self.model.generation)
        self.view.update_population_counts(self.model.species_counts)
        self.view.after(100, self.update_view)  # schedule the next update
        #print(self.model.data)
        if self.running_gen_thread.is_alive():
            self.view.next_generation_button.configure(state="disabled")
        else:
            self.view.next_generation_button.configure(state="normal")

