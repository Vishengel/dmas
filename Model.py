from Agent import *
from CS import *
from Fact import *
from Rule import *

class Model():
    def __init__(self):
        #Create and init agents
        #Agents are initialized with initial empty moves, to prevent None errors
        self.prosecutor = Agent("Prosecutor", "idle", "dumb", CS(), Move("", None))
        self.defendant = Agent("Defendant", "idle", "dumb", CS(), Move("", None))
        self.prosecutor.set_opponent(self.defendant)
        self.defendant.set_opponent(self.prosecutor)
        self.dialogue_stack = []
        self.dialogue_history = []

        #Add starting facts
        first_fact = Fact('borrowed_from', ('Defendant', 'Prosecutor', 10000), True)
        self.prosecutor.commitment_store.add_fact(first_fact)
        self.defendant.commitment_store.add_fact(first_fact)
        #self.defendant.commitment_store.add_fact( Fact('owes', ('Defendant', 'Prosecutor', 10000), False) )

        #Add starting rules
        starting_rule = Rule([Fact('borrowed_from', ('x', 'y', 'amount'), True)]
                          ,Fact('owes', ('x', 'y', 'amount'), True), 'valid')
        self.prosecutor.commitment_store.add_rule(starting_rule)
        self.defendant.commitment_store.add_rule(starting_rule)








