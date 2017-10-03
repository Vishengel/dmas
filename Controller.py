from tkinter import *
from View import View
from Model import Model
from Fact import *
from Rule import *
from CS import *
from Dialogue import *
from Move import *

class Controller():
    def __init__(self, width, height):
        self.root = Tk()
        self.root.resizable(False, False)
        self.width = width
        self.height = height
        self.model = Model()
        self.view = View(width, height)

    def run(self):
        self.view.run_button.config(command=self.execute_step)
        # Create TKINTER text variables for updating the Label contents
        self.dialogue_content = StringVar()
        self.left_cs_string = StringVar()
        self.right_cs_string = StringVar()

        #Create entry field
        self.entry = Entry(self.view.button_frame)
        self.entry.pack(side = LEFT)
        self.entry.insert(0, 1)

        #Add the content of the dialogue game to the dialog frame
        Label(self.view.dialog_frame, text="Dialog viewer", font=("Helvetica", 10),
              textvariable=self.dialogue_content).pack()
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

        #Create starting move
        starting_claim = Fact('owes', ('Defendant', 'Prosecutor', 10000), True)
        starting_move = Move('claim', starting_claim)
        self.model.prosecutor.last_move = starting_move
        #If a sentence is claimed, it has to be added to the commitment store!
        self.model.prosecutor.commitment_store.add_fact(starting_claim)
        #Create main dialogue
        self.current_dialogue = Dialogue('1', starting_claim, self.model.prosecutor,
                                 starting_move)
        #Add starting move string to dialogue frame
        self.model.dialogue_history.append(self.current_dialogue.move.printable(self.current_dialogue.ID,
                                                                           self.current_dialogue.turn))
        self.update_labels()
        #Change turns
        self.current_dialogue.swap_turns(self.model.prosecutor, self.model.defendant)
        #Add dialogue to dialogue stack
        self.model.dialogue_stack.append(self.current_dialogue)
        self.root.mainloop()


    def execute_step(self):
        steps = int(self.entry.get())
        #No more than 100 steps at a time!
        if(steps <= 100):
            for i in range(steps):
                #Current agent makes a move, based on the available move list
                movelist = self.current_dialogue.turn.get_available_moves(self.current_dialogue.move)
                #Based on the move list, select an appropriate move according to the agent's strategy
                move = self.current_dialogue.turn.select_move(movelist, self.current_dialogue.sentence)
                #print(move.printable(self.current_dialogue.ID, self.current_dialogue.turn))
                #Set the new move to be the latest move done by the agent
                self.current_dialogue.turn.last_move = move
                #Execute the chosen move in the dialogue game
                self.execute_move(move, self.current_dialogue.turn)
                #Set the dialogue to the appropriate next one before the next turn
                self.current_dialogue = self.model.dialogue_stack[-1]
                self.update_labels()



    #Execute the move selected by an agent
    def execute_move(self, move, agent):
        #Defend the claim made earlier
        if (move.move_type == "reason"):
            #Choose a reason to defend the earlier claim from the list of possible reasons
            #FOR NOW, CHOOSE FIRST ONE
            self.current_dialogue.turn.reasons[0][0] = self.current_dialogue.turn.reasons[0][0].unify(move.sentence)
            self.current_dialogue.turn.reasons[0][0].property = "reason-for"
            self.current_dialogue.turn.reasons[0][0].claim = move.sentence
            #Create a sub dialogue about this reason
            move.sentence =  self.current_dialogue.turn.reasons[0][0]
            self.add_sub_dialogue(move)

        elif (move.move_type != "claim" and move.move_type != "deny" and move.move_type != "refuse"):
            # Set dialogue move to the new move
            self.current_dialogue.move = move
            # Make new move show-able on the screen
            self.model.dialogue_history.append(self.current_dialogue.move.printable(self.current_dialogue.ID,
                                                                                    self.current_dialogue.turn))
            self.current_dialogue.swap_turns(self.model.prosecutor, self.model.defendant)
        else:
            if(move.move_type == "deny"):
                self.add_sub_dialogue(move)




    def add_sub_dialogue(self, move):
        old_dialogue_ID = self.current_dialogue.ID
        # Add denied sentence to proponent's commitment store
        self.current_dialogue.turn.commitment_store.add_fact(move.sentence)
        # old_sentence = self.current_dialogue.sentence
        # negated_sentence = Fact(old_sentence.predicate, old_sentence.args, old_sentence.negation)
        # print(negated_sentence.printable())
        new_sub_dialogue = Dialogue(old_dialogue_ID + "-1", move.sentence,
                                    self.current_dialogue.turn, move)
        self.model.dialogue_history.append(new_sub_dialogue.move.printable(new_sub_dialogue.ID,
                                                                           new_sub_dialogue.turn))
        # Change turn to the other agent
        new_sub_dialogue.swap_turns(self.model.prosecutor, self.model.defendant)
        # Add newly created dialogue to the dialogue stack
        self.model.dialogue_stack.append(new_sub_dialogue)


    #Update the contents of the commitment stores and the dialogue frame
    def update_labels(self):
        self.dialogue_content.set("\n".join(self.model.dialogue_history))
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
                print("The following rule proves this claim: \n- ", rule.printable())
                print("Because the following conditions are facts in the commitment store:")
                for condition in rule.conditions:
                    print("\t- ", condition.unify(fact).printable())
        print()












