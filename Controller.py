from tkinter import *
from View import View
from Model import Model

class Controller():
    def __init__(self, width, height):
        self.root = Tk()
        self.root.resizable(False, False)
        self.view = View(width, height)
        self.model = Model()
        self.initButtons()

    def initButtons(self):
        pass


    def run(self):
        self.root.mainloop()
