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

    def run(self):
        self.root.mainloop()

    def draw_dialogue(self):
        return "Test"

