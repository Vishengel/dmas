from Agent import *
from pyke import knowledge_engine

class Model():
    def __init__(self):
        #Create and init agents
        self.prosecutor = Agent("Prosecutor", "idle", "exhaustive", knowledge_engine.engine("prosecutor_knowledge"), "")
        self.defendant = Agent("Defendant", "idle", "exhaustive", knowledge_engine.engine("defendant"), "")
        self.prosecutor.set_opponent(self.defendant)
        self.defendant.set_opponent(self.prosecutor)
        self.dialogue_stack = []
        self.dialogue_history = []

        #Add starting facts
        self.prosecutor.commitment_store.add_case_specific_fact('facts', 'borrowed_from', ('defendant', 'prosecutor', 10000))
        self.prosecutor.commitment_store.add_case_specific_fact('facts', 'valid', ('rule', 'owes'))

        self.defendant.commitment_store.add_case_specific_fact('facts', 'borrowed_from', ('defendant', 'prosecutor', 10000))
        self.defendant.commitment_store.add_case_specific_fact('facts', 'valid', ('rule', 'owes'))

        #Add starting claim made by prosecutor
        self.prosecutor.commitment_store.add_case_specific_fact('facts', 'owes', ('defendant', 'prosecutor', 10000))

        """print("Prosecutor facts: ", self.prosecutor.get_facts())
        print("Defendant facts: ", self.defendant.get_facts())

        print("Prosecutor rules: ", "".join(self.prosecutor.get_rules().keys()))
        print("Defendant rules: ", self.defendant.get_rules())"""

        #print(self.defendant.commitment_store.prove_1_goal("facts.valid(rule, $rule_name)"))
