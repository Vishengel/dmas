from Agent import *
from CS import *
from Fact import *
from Rule import *

class Model():
    def __init__(self):
        #Create and init agents
        self.prosecutor = Agent("Prosecutor", "idle", "exhaustive", CS(), "")
        self.defendant = Agent("Defendant", "idle", "exhaustive", CS(), "")
        self.prosecutor.set_opponent(self.defendant)
        self.defendant.set_opponent(self.prosecutor)
        self.dialogue_stack = []
        self.dialogue_history = []

        #Add starting facts
        first_fact = Fact('borrowed_from', ('defendant', 'prosecutor', 10000), True)
        self.prosecutor.commitment_store.add_fact(first_fact)
        self.defendant.commitment_store.add_fact(first_fact)

        #Add starting rules
        first_rule = Rule([Fact('borrowed_from', ('x', 'y', 'amount'), True),]
                          ,Fact('owes', ('x', 'y', 'amount'), True))
        self.prosecutor.commitment_store.add_rule(first_rule)
        self.defendant.commitment_store.add_rule(first_rule)






