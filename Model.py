from Agent import *
from CS import *
from Fact import *
from Rule import *
from Judge import *

class Model():
    def __init__(self):
        #Create and init agents
        #Agents are initialized with initial empty moves, to prevent None errors
        self.prosecutor = Agent("Prosecutor", "idle", "dumb", CS(), Move("", None, None))
        self.defendant = Agent("Defendant", "idle", "dumb", CS(), Move("", None, None))
        self.judge = Judge("Judge", "", "", CS(), None)
        self.prosecutor.set_opponent(self.defendant)
        self.defendant.set_opponent(self.prosecutor)
        self.dialogue_stack = []
        self.dialogue_history = []
        self.dialogue_history_natural = []

        #Add starting facts
        first_fact = Fact('borrowed_from', ('Defendant', 'Prosecutor', 10000), True)
        self.prosecutor.commitment_store.add_fact(first_fact)
        self.prosecutor.commitment_store.add(Fact('older_than', ('loan', '30'), True))
        self.defendant.commitment_store.add_fact(first_fact)
        #self.defendant.commitment_store.add_fact( Fact('owes', ('Defendant', 'Prosecutor', 10000), False) )

        #Add starting rules
        starting_rule = Rule([Fact('borrowed_from', ('x', 'y', 'amount'), True)]
                          ,Fact('owes', ('x', 'y', 'amount'), True), 'valid')
        self.prosecutor.commitment_store.add(starting_rule)
        self.defendant.commitment_store.add(starting_rule)

        self.defendant.commitment_store.add(Rule([Fact('loves', ('x', 'y'), True)]
                          ,Fact('owes', ('x', 'y', 'amount'), False), 'valid'))

        self.defendant.commitment_store.add(Rule([Fact('older_than', ('loan','30'), True)]
                                                 , Rule([Fact('borrowed_from', ('x', 'y', 'amount'), True)]
                          ,Fact('owes', ('x', 'y', 'amount'), True), 'excluded'),'valid'))


        self.defendant.commitment_store.add(Fact('loves', ('Defendant', 'Prosecutor'), True))
        self.defendant.commitment_store.add(Fact('older_than', ('loan','30'), True))

        self.judge.commitment_store.add(Rule([Fact('older_than', ('loan', '30'), True)]
                                             , Rule([Fact('borrowed_from', ('x', 'y', 'amount'), True)]
                                                    , Fact('owes', ('x', 'y', 'amount'), True), 'excluded'),
                                             'valid'))

        self.game_over = False

    #Add the dialogue moves as text to both the logical and natural language frames
    def add_dialogue_content(self, move, dialogue_ID):
        self.dialogue_history.append(move.printable(dialogue_ID))
        move_components = [dialogue_ID, move.agent.name, move.move_type]
        for argument in move.sentence.args:
            move_components.append(argument)
        #Change natural language version of dialogue move depending on move type
        if (move.move_type == "claim"):
            self.dialogue_history_natural.append("%s. %s: ")
        elif(move.move_type == "question"):
            self.dialogue_history_natural.append("%s. %s: Why?" % (dialogue_ID, move.agent))

    def remove_repeating_moves(self, movelist, current_dialogue):
        for move in movelist:
            if (current_dialogue.turn == self.prosecutor):
                if(move in current_dialogue.prosecutor_move_list):
                    movelist.remove(move)
            else:
                if (move in current_dialogue.defendant_move_list):
                    movelist.remove(move)
        return movelist








