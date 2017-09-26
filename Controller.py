from tkinter import *
from View import View
from Model import Model

class Controller():
    def __init__(self, width, height):
        self.root = Tk()
        self.root.resizable(False, False)
        self.width = width
        self.height = height
        self.view = View(width, height)
        self.model = Model()

    def start_sim(self):
        self.model.start_simulation(self.width / 2, self.height / 2)
        self.view.draw_agents(self.model.agents)

    def run_sim(self):
        try:
            iterations = int(self.entry_field.get())
            for i in range(iterations):
                self.model.play()
        except:
            print("Only integers allowed!")

    def run(self):
        self.root.mainloop()
