class Move():
    def __init__(self, move_type, sentence):
        self.move_type = move_type
        self.sentence = sentence

    def printable(self, dialogue_ID, current_agent):
        if(self.move_type == "pass"):
            return "%s. %s -  %s" % (dialogue_ID, current_agent.name, self.move_type)
        else:
            return "%s. %s -  %s: %s" % (dialogue_ID, current_agent.name, self.move_type, self.sentence.printable())




