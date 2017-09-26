from Agent import *

class Model():
    def __init__(self):
        self.prosecutor = Agent("p")
        self.defendant = Agent("d")
        self.dialogue_stack = ["Question: owes(d, p, 1000)"]
        self.dialogue_history = ["Claim:  owes(d, p, 1000)", "Question: owes(d, p, 1000)"]