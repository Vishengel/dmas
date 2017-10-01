from tkinter import *
from View import View
from Model import Model
from Fact import *
from Rule import *
from CS import *

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
        #Add name and starting content of both commitment stores
        Label(self.view.cs1_frame, text=self.model.prosecutor.name, font=("Helvetica", 14)).pack()
        Label(self.view.cs2_frame, text=self.model.defendant.name, font=("Helvetica", 14)).pack()
        Label(self.view.cs1_frame, textvariable=self.left_cs_string, font=("Helvetica", 8)).pack()
        Label(self.view.cs2_frame, textvariable=self.right_cs_string, font=("Helvetica", 8)).pack()
        #Set starting facts and rules to defendant and prosecutor labels
        self.left_cs_string.set(self.model.prosecutor.commitment_store.get_printable_facts() + "\n"
                                + self.model.prosecutor.commitment_store.get_printable_rules())
        self.right_cs_string.set(self.model.defendant.commitment_store.get_printable_facts() + "\n"
                                + self.model.defendant.commitment_store.get_printable_rules())
        self.root.mainloop()


    def execute_step(self):
        #Prove that the claim 'owes('defendant', 'prosecutor', 10000) holds
        test_fact = Fact('owes', ('defendant', 'prosecutor', 10000), True)
        applicable_rules = self.model.prosecutor.commitment_store.prove_conclusion(test_fact)
        self.print_prove(applicable_rules, test_fact)
        #Prove the negated fact
        test_fact.negation = not(test_fact.negation)
        applicable_rules = self.model.prosecutor.commitment_store.prove_conclusion(test_fact)
        self.print_prove(applicable_rules, test_fact)


    #Update the contents of the commitment stores and the dialogue frame
    def update_labels(self):
        self.left_cs_string.set(self.model.prosecutor.commitment_store.get_printable_facts() + "\n"
                                + self.model.prosecutor.commitment_store.get_printable_rules())
        self.right_cs_string.set(self.model.defendant.commitment_store.get_printable_facts() + "\n"
                                 + self.model.defendant.commitment_store.get_printable_rules())


    #If a fact can be proven, print the rules and its conditions that prove that fact
    def print_prove(self, applicable_rules, fact):
        print("-----------------------------------------------------------")
        print("I'm trying to prove: ", fact.printable())
        if (len(applicable_rules) == 0):
            print("This fact cannot be proven from the current facts and rules.")
        else:
            applicable_rules[0].conditions[0].unify(fact)
            for rule in applicable_rules:
                print("The following rule proves this claim: \n", rule.printable())
                print("Because the following conditions are facts in the commitment store:")
                for condition in rule.conditions:
                    print("- ", condition.unify(fact).printable())
        print()












