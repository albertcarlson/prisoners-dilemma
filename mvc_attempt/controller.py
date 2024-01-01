from model import Model
from view import View
import threading
# from multiprocessing import Process

class Controller:
    def __init__(self):
        self.model = Model()
        self.view = View(self.restart_iteration)
        self.view.after(500, self.update_view)  # schedule the first update

    def run(self):
        #threading.Thread(target=self.model.iterate).start()  # Try with Process(...) instead of threading.Thread(...)
        self.restart_iteration()
        self.view.mainloop()

    def restart_iteration(self):
        self.iteration_thread = threading.Thread(target=self.model.iterate)
        self.iteration_thread.start()

    def update_view(self):
        self.view.update_progressbar(self.model.data)
        self.view.after(500, self.update_view)  # schedule the next update
        #print(self.model.data)
        if self.iteration_thread.is_alive():
            self.view.restart_button.configure(state="disabled")
        else:
            self.view.restart_button.configure(state="normal")

