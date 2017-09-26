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
        self.view.run_button.config(command=self.run_game)
        self.root.mainloop()

    def run_game(self):
        print("Hello!!!!")