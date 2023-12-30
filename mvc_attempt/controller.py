from model import Model
from view import View
import threading
import time

class Controller:
    def __init__(self):
        self.model = Model()
        self.view = View()
        self.view.after(500, self.update_view)  # schedule the first update

    def run(self):
        threading.Thread(target=self.model.iterate).start()
        self.view.mainloop()

    def update_view(self):
        self.view.update_progressbar(self.model.data)
        self.view.after(500, self.update_view)  # schedule the next update
        print(self.model.data)