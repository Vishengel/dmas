class Move():
    def __init__(self, move_type, sentence, agent):
        self.move_type = move_type
        self.sentence = sentence
        self.agent = agent


    def printable(self, dialogue_ID):
        if(self.move_type == "pass"):
            return "%s. %s -  %s" % (dialogue_ID, self.agent.name, self.move_type)
        else:
            return "%s. %s -  %s: %s" % (dialogue_ID, self.agent.name, self.move_type, self.sentence.printable())




