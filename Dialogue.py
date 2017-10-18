class Dialogue():
    def __init__(self, ID, sentence, agent, move):
        #Each dialogue has its own identifier
        self.ID = ID
        #The claim that starts the dialogue
        self.sentence = sentence
        #The agent who started the dialogue / is the proponent
        self.proponent = agent
        #The Dialogue is still open
        self.open = True
        #A dialogue is opened with a move
        #Alternatively, this variable stores the latest move made in the dialogue
        self.move = move
        #A dialogue contains two list, keeping track of the moves that have been
        #performed by each party in this dialogue
        self.prosecutor_move_list = []
        self.defendant_move_list = []

        #Keep track of the last moves performed by both parties
        self.last_prosecutor_move = None
        self.last_defendant_move = None
        #Keep track of how many sub-dialogues have been opened in this dialogue
        self.subdialogues = 0


    def swap_turns(self, agent1, agent2):
        # Change turn to the other agent
        if (self.move.agent == agent1):
            self.turn = agent2
        else:
             self.turn = agent1



