from Agent import *

class Model():
    def __init__(self):
        self.prosecutor = Agent("p")
        self.defendant = Agent("d")
        self.dialogue_stack = []
        self.dialogue_history = []

        dialogue_content = "Claim:  owes(d, p, 1000)", "Question: owes(d, p, 1000)"
        self.dialogue_stack.append(dialogue_content)
        self.dialogue_history.append(dialogue_content)