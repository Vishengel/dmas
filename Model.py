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
        #second_fact = Fact('owes', ('defendant', 'prosecutor', 10000), True)
        second_fact = Fact('hate', ('defendant', 'prosecutor'), False)
        third_fact = Fact('brothers', ('defendant', 'prosecutor'),False)
        fourth_fact = Fact('loves', ('defendant','prosecutor'), True)
        self.prosecutor.commitment_store.add_fact(first_fact)
        self.prosecutor.commitment_store.add_fact(second_fact)
        self.prosecutor.commitment_store.add_fact(third_fact)
        self.prosecutor.commitment_store.add_fact(fourth_fact)

        self.defendant.commitment_store.add_fact(first_fact)



        #Add starting rules
        first_rule = Rule([Fact('borrowed_from', ('x', 'y', 'amount'), True), Fact('hate', ('x', 'y'), False),
                           Fact('brothers', ('x', 'y'), False)]
                          ,Fact('owes', ('x', 'y', 'amount'), True), 'valid')
        second_rule = Rule([Fact('loves', ('x', 'y'),True)], Fact('owes', ('x', 'y', 'amount'),True),'valid')
        self.prosecutor.commitment_store.add_rule(first_rule)
        self.defendant.commitment_store.add_rule(first_rule)
        self.prosecutor.commitment_store.add_rule(second_rule)







