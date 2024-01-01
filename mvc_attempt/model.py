import time

class Model:
    def __init__(self):
        self.data = 0

    def iterate(self):
        for i in range(31):
            self.data = i
            time.sleep(0.5)

