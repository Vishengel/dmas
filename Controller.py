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
        # Create TKINTER text variables for updating the Label contents
        self.left_cs_string = StringVar()
        self.right_cs_string = StringVar()
        self.left_cs_string.set(self.model.prosecutor.get_facts())
        self.right_cs_string.set(self.model.defendant.get_facts())

        #Add name and starting content of both commitment stores
        Label(self.view.cs1_frame, text=self.model.prosecutor.name, font=("Helvetica", 14)).pack()
        Label(self.view.cs2_frame, text=self.model.defendant.name, font=("Helvetica", 14)).pack()

        Label(self.view.cs1_frame, textvariable = self.left_cs_string, font=("Helvetica", 8)).pack()
        Label(self.view.cs2_frame, textvariable = self.right_cs_string, font=("Helvetica", 8)).pack()

        Label(self.view.cs1_frame, text=self.model.prosecutor.get_rules(), font=("Helvetica", 8)).pack()
        Label(self.view.cs2_frame, text=self.model.defendant.get_rules(), font=("Helvetica", 8)).pack()


        self.root.mainloop()

    def execute_step(self):
        try:
            self.model.prosecutor.commitment_store.prove_1_goal('prosecutor_rules.owes(defendant, prosecutor, 10000)')
            self.model.prosecutor.commitment_store.add_case_specific_fact('prosecutor_facts', 'owes', ('defendant', 'prosecutor', 10000))
            self.left_cs_string.set(self.model.prosecutor.get_facts())

        except:
            print("Nope :-)")




        #print(self.model.defendant.get_rules())
        #print(self.model.prosecutor.get_rules())
        #print(self.model.defendant.get_facts())
        #print(self.model.prosecutor.get_facts())
        #self.model.defendant.get_available_moves()

