from tkinter import *
from View import View
from Model import Model

class Controller():
    def __init__(self, width, height):
        self.root = Tk()
        self.root.resizable(False, False)
        self.width = width
        self.height = height
        self.model = Model()
        self.view = View(width, height, self.model.prosecutor.name, self.model.defendant.name)

    def run(self):
        self.view.run_button.config(command=self.execute_step)
        #Add name and starting content of both commitment stores
        Label(self.view.cs1_frame, text=self.model.prosecutor.name, font=("Helvetica", 14)).pack()
        Label(self.view.cs2_frame, text=self.model.defendant.name, font=("Helvetica", 14)).pack()

        Label(self.view.cs1_frame, text=self.model.prosecutor.get_facts(), font=("Helvetica", 8)).pack()
        Label(self.view.cs2_frame, text=self.model.defendant.get_facts(), font=("Helvetica", 8)).pack()

        Label(self.view.cs1_frame, text=self.model.prosecutor.get_rules(), font=("Helvetica", 8)).pack()
        Label(self.view.cs2_frame, text=self.model.defendant.get_rules(), font=("Helvetica", 8)).pack()


        self.root.mainloop()

    def execute_step(self):
        self.model.defendant.get_available_moves()

