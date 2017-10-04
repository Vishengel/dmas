class Dialogue():
    def __init__(self, ID, sentence, agent, move):
        #Each dialogue has its own identifier
        self.ID = ID
        #The claim that starts the dialogue
        self.sentence = sentence
        #The agent whose turn it is to move
        self.turn = agent
        #The Dialogue is still open
        self.open = True
        #A dialogue is opened with a move
        #Alternatively, this variable stores the latest move made in the dialogue
        self.move = move


    def swap_turns(self, agent1, agent2):
        # Change turn to the other agent
        if (self.turn == agent1):
            self.turn = agent2
        else:
             self.turn = agent1



