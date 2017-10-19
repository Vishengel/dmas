from Agent import *

class Judge(Agent):
    def __init__(self, name, state, strategy, commitment_store, move):
        super().__init__(name, state, strategy, commitment_store, move)

    def arbiter_call(self, rule):
        return self.commitment_store.rule_in_CS(rule)


