from Move import *
from Fact import *
from random import randrange
class Agent():

    def __init__(self, name, state, strategy, commitment_store, move):
        self.name = name
        self.state = state
        self.strategy = strategy
        self.commitment_store = commitment_store
        self.move = move
        #Keep a list of possible reasons that can be used to defend a claim
        self.reasons = []

    def set_opponent(self, opponent):
        self.opponent = opponent

    #Extract the set of possible moves at any turn
    def get_available_moves(self, opponent_move):
        #If opponent claimed a new sentence, agent can choose
        #to question, deny, refuse or accept this sentence
        if(opponent_move.move_type == "claim"):
            possible_moves =  ["question", "deny", "accept"]
            sentence = opponent_move.sentence
            sentence.negation = not(sentence.negation)
            #If the negation of the sentence is already in the agent's commitment store,
            #then denial is not allowed!
            if(self.commitment_store.fact_in_CS(sentence)):
                possible_moves.remove("deny")
            sentence.negation = not(sentence.negation)
            return possible_moves

        #If opponent questioned a claim, agent has to search for a reason
        #that defends his claim
        if(opponent_move.move_type == "question"):
            claim = opponent_move.sentence
            # Search the commitment store for a reason for the made claim
            # Get rules that prove the claim
            reasons = []
            reason_rules = self.commitment_store.prove_conclusion(claim)
            for rule in reason_rules:
                reasons.append(rule.conditions)
                # Select one of the possible reasons
            #Store reasons
            self.reasons = reasons
            #If at least 1 reason is found, a reason move is possible
            if(len(reasons) > 0):
                return ["reason", "withdraw"]
            #Else, a claim cannot be defended and has to be withdrawn
            else:
                return ["withdraw"]



        return ["accept"]

    def select_move(self, movelist, sentence):
        move_type = ""
        if(self.strategy == "dumb"):
            move_type = movelist[0]
        if(self.strategy == "random"):
            move_type = movelist[randrange(len(movelist))]
        if (move_type == "deny"):
            negated_sentence = Fact(sentence.predicate, sentence.args, sentence.negation)
            return Move(move_type, negated_sentence)
        return Move(move_type, sentence)


