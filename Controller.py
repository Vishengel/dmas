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
        self.dialogue_counter = 0

    def run(self):
        self.view.run_button.config(command=self.execute_step)
        self.root.mainloop()

    def execute_step(self):
        self.model.dialogue_history.append(str(self.dialogue_counter))
        self.view.dialogue_content.set("\n".join(self.model.dialogue_history))
        #self.view.text.insert(INSERT, "\n".join(self.model.dialogue_history))
        self.dialogue_counter += 1        self.model.defendant.get_available_moves()