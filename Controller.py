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
        self.view.reset_button.config(command=self.reset)
        # Create TKINTER text variables for updating the Label contents
        self.left_cs_string = StringVar()
        self.right_cs_string = StringVar()

        #Create starting / main move
        self.main_claim = Fact('owes', ('Defendant', 'Prosecutor', 10000), True)
        starting_move = Move('claim',  self.main_claim, self.model.prosecutor)
        self.model.prosecutor.last_move = starting_move
        #If a sentence is claimed, it has to be added to the commitment store!
        self.model.prosecutor.commitment_store.add_fact( self.main_claim)
        #Create main dialogue
        self.current_dialogue = Dialogue('1',  self.main_claim, self.model.prosecutor,
                                 starting_move)
        self.current_dialogue.prosecutor_move_list.append(starting_move.move_type)
        self.current_dialogue.last_prosecutor_move = starting_move

        #Add starting move string to dialogue frame
        self.model.add_dialogue_content(self.current_dialogue.move,self.current_dialogue.ID)

        self.update_text()
        #Change turns
        self.current_dialogue.swap_turns(self.model.prosecutor, self.model.defendant)
        #Add dialogue to dialogue stack
        self.model.dialogue_stack.append(self.current_dialogue)
        self.root.mainloop()


    def execute_step(self):
        if(not(self.model.game_over)):
            #Current agent makes a move, based on the available move list and his opponent's last move
            if(self.current_dialogue.turn == self.model.prosecutor):
                movelist = self.current_dialogue.turn.get_available_moves(self.current_dialogue.last_defendant_move,
                                                                      self.current_dialogue.proponent)
            else:
                movelist = self.current_dialogue.turn.get_available_moves(self.current_dialogue.last_prosecutor_move,
                                                                      self.current_dialogue.proponent)

            # Remove moves that were already performed by this agent in this dialogue, because
            # repetition of same moves in a dialogue is not allowed
            #Set the latest agent move of the dialogue to the current move
            movelist = self.model.remove_repeating_moves(movelist, self.current_dialogue)

            #print("%s can make the following moves in dialogue %s:" % (self.current_dialogue.turn.name, self.current_dialogue.ID), movelist)
            #Based on the move list, select an appropriate move according to the agent's strategy
            #Add this move to one of the two agent's latest move, in this dialogue
            move = self.current_dialogue.turn.select_move(movelist, self.current_dialogue.sentence)
            if (self.current_dialogue.turn == self.model.prosecutor):
                self.current_dialogue.last_prosecutor_move = move
            else:
                self.current_dialogue.last_defendant_move = move


            #Add move to the dialogue's list of moves for this agent
            if(self.current_dialogue.turn == self.model.prosecutor):
                self.current_dialogue.prosecutor_move_list.append(move.move_type)
            else:
                self.current_dialogue.defendant_move_list.append(move.move_type)

            #Set the new move to be the latest move done by the agent
            self.current_dialogue.turn.last_move = move
           # print( self.current_dialogue.turn.last_move.printable( self.current_dialogue.ID,
                                                  #self.current_dialogue.turn))
            #Execute the chosen move in the dialogue game
            self.execute_move(move, self.current_dialogue.turn)
            #Set the dialogue to the appropriate next one before the next turn
            #unless no more dialogues are left in the stack

            #print("Dialogue:", self.current_dialogue.ID)
            #print("P:", self.current_dialogue.prosecutor_move_list)
            #print("D:", self.current_dialogue.defendant_move_list)


            if (not(self.model.game_over)):
                self.current_dialogue = self.model.dialogue_stack[-1]
            #If the main claim is no longer in the commitment store of the prosecutor,
            #the game is over and the defendant has won
            if( not(self.model.prosecutor.commitment_store.fact_in_CS(self.main_claim))):
                print("Prosecutor's main claim is gone!")
                self.model.game_over = True
            self.update_text()

        else:
            self.view.run_button['state'] = 'disabled'
            #When the game is over, announce the winner of the dialogue game
            if(self.model.defendant.last_move.move_type == "accept"):
                self.model.dialogue_history.append("%s won the dialogue game." % (self.model.prosecutor.name))
            else:
                self.model.dialogue_history.append("%s won the dialogue game." % (self.model.defendant.name))
            self.update_text()


    #Execute the move selected by an agent
    def execute_move(self, move, agent):

        if(move.move_type == "arbiter"):
            self.model.dialogue_stack.pop()
            self.model.dialogue_stack[-1].swap_turns(self.model.prosecutor, self.model.defendant)

            judgement = self.model.judge.arbiter_call(move.sentence)
            #If the judge decides that a rule is valid, add the rule to both parties' commitment store
            if(judgement == True):
                self.model.dialogue_history.append("%s. %s" % (self.current_dialogue.ID, "Judge: this rule is valid."))
                self.model.prosecutor.commitment_store.add_rule(move.sentence)
                self.model.defendant.commitment_store.add_rule(move.sentence)

                #BIG PATCH! NO IDEA WHY THIS WORKS.... ;_______________________________;
                if (self.current_dialogue.turn == self.model.prosecutor):
                    self.model.dialogue_stack[-1].turn = self.model.defendant
                else:
                    self.model.dialogue_stack[-1].turn = self.model.prosecutor

            #Else, remove the rule from both parties' commitment store
            else:
                self.model.dialogue_history.append("%s. %s" % (self.current_dialogue.ID, "Judge: this rule is NOT valid."))
                self.model.prosecutor.commitment_store.remove_rule(move.sentence)
                self.model.defendant.commitment_store.remove_rule(move.sentence)



        elif(move.move_type == "accept-arbiter"):
            self.model.dialogue_history.append(self.current_dialogue.move.printable(self.current_dialogue.ID))

        #If agent accepts the opponent's claim..
        elif(move.move_type == "accept" or move.move_type == "withdraw"):
            #Add opponent's claim to agent's commitment store
            #when accepting
            if(move.move_type == "accept"):
                agent.commitment_store.add_fact(move.sentence)
                #If the negation of this claim exist, remove this claim
                if(isinstance(move.sentence,Fact)):
                    negated_sentence = Fact(move.sentence.predicate, move.sentence.args, move.sentence.negation)
                    #print("Sentence:", move.sentence.printable())
                    #print("Negated sentence:", negated_sentence.printable())

                    agent.commitment_store.remove_fact(negated_sentence)
                agent.commitment_store.add_fact(move.sentence)

            #Remove own claim when withdrawing
            else:
                agent.commitment_store.remove_fact(move.sentence)

            #The sub dialogue concerning this claim is now closed.
            #Remove it from the dialogue stack and return to the parent dialogue.
            self.model.dialogue_stack.pop()
            self.current_dialogue.move = move
            # Make new move show-able on the screen
            self.model.dialogue_history.append(self.current_dialogue.move.printable(self.current_dialogue.ID))

            #Change the sentence of the parent dialogue to be the acceptance of
            #that dialogue's claim as well
            #HOWEVER: If there are no dialogues left in the stack,
            #this means that the game is over.
            if(len(self.model.dialogue_stack) > 0):
                #Agent who accepts or withdraws can still make another move
                #print( self.model.dialogue_stack[-1].move.printable(self.model.dialogue_stack[-1].ID))
                self.model.dialogue_stack[-1].turn = self.current_dialogue.turn
            else:
                self.model.game_over = True


        #Defend the claim made earlier
        elif (move.move_type == "reason"):
            #Choose a reason to defend the earlier claim from the list of possible reasons
            #FOR NOW, CHOOSE FIRST ONE
            reason = self.current_dialogue.turn.reason_rules[0].conditions[0]
            reason =  reason.unify(move.sentence)
            reason.property = "reason-for"
            reason.claim = move.sentence
            #Create a sub dialogue about this reason
            move.sentence =  reason
            self.add_sub_dialogue(move)

        elif (move.move_type == "applies"):
            # Get a rule that has the reason as a conclusion
            # Get the first rule for now
            # Copy the rule to prevent the original rule from being changed
            rule = copy.copy(self.current_dialogue.turn.reason_rules[0])
            rule.property = "applies"
            move.sentence = rule
            self.add_sub_dialogue(move)


        elif (move.move_type == "question"):
            # Set dialogue move to the new move
            self.current_dialogue.move = move
            # Make new move show-able on the screen
            self.model.dialogue_history.append(self.current_dialogue.move.printable(self.current_dialogue.ID))

            self.current_dialogue.swap_turns(self.model.prosecutor, self.model.defendant)

        elif (move.move_type == "deny" or move.move_type == "arbiter"):
                self.add_sub_dialogue(move)

        elif(move.move_type == "valid"):
            rule = copy.copy(self.current_dialogue.turn.reason_rules[0])
            rule.property = "valid"
            move.sentence = rule
            self.add_sub_dialogue(move)

    def add_sub_dialogue(self, move):
        old_dialogue_ID = self.current_dialogue.ID
        # Add denied sentence to proponent's commitment store
        self.current_dialogue.turn.commitment_store.add_fact(move.sentence)
        # old_sentence = self.current_dialogue.sentence
        # negated_sentence = Fact(old_sentence.predicate, old_sentence.args, old_sentence.negation)
        # print(negated_sentence.printable())
        new_sub_dialogue = Dialogue(old_dialogue_ID + "-" + str(1 + self.current_dialogue.subdialogues) , move.sentence,
                                    self.current_dialogue.turn, move)
        #The proponent of the claim that starts this sub-dialogue's move is recorded
        if(self.current_dialogue.turn == self.model.prosecutor):
            new_sub_dialogue.last_prosecutor_move = move
        else:
            new_sub_dialogue.last_defendant_move = move

        self.model.dialogue_history.append(new_sub_dialogue.move.printable(new_sub_dialogue.ID))

        self.current_dialogue.subdialogues = self.current_dialogue.subdialogues + 1

        # Change turn to the other agent
        new_sub_dialogue.swap_turns(self.model.prosecutor, self.model.defendant)
        # Add newly created dialogue to the dialogue stack
        self.model.dialogue_stack.append(new_sub_dialogue)


    #Update the contents of the commitment stores and the dialogue frame
    def update_text(self):
        self.view.dialogue_text.config(state='normal')
        self.view.dialogue_text.delete(1.0, END)
        self.view.dialogue_text.insert(END, "\n".join(self.model.dialogue_history) + "\n")
        self.view.dialogue_text.config(state='disabled')

        self.view.cs1_text.config(state='normal')
        self.view.cs1_text.delete(1.0, END)
        self.view.cs1_text.insert(END, self.model.prosecutor.commitment_store.get_printable_facts() + "\n"
                                + self.model.prosecutor.commitment_store.get_printable_rules() + "\n")
        self.view.cs1_text.config(state='disabled')

        self.view.cs2_text.config(state='normal')
        self.view.cs2_text.delete(1.0, END)
        self.view.cs2_text.insert(END, self.model.defendant.commitment_store.get_printable_facts() + "\n"
                                 + self.model.defendant.commitment_store.get_printable_rules() + "\n")
        self.view.cs1_text.config(state='disabled')

    def reset(self):
        self.model = Model()
        self.update_text()
        self.view.run_button['state'] = 'normal'
        self.run()

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












