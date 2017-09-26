from Agent import *

class Model():
    def __init__(self):
        self.prosecutor = Agent("p", "drinking", "", "", "")
        self.defendant = Agent("d", "smoking", "", "", "")
        self.prosecutor.set_opponent(self.defendant)
        self.defendant.set_opponent(self.prosecutor)
        self.dialogue_stack = []
        self.dialogue_history = []

        dialogue_content = "Claim:  owes(d, p, 1000)", "Question: owes(d, p, 1000)"
        self.dialogue_history.append(dialogue_content)