from Move import *
from Fact import *
from random import randrange
import copy
class Agent():

    def __init__(self, name, state, strategy, commitment_store, move):
        self.name = name
        self.state = state
        self.strategy = strategy
        self.commitment_store = commitment_store
        self.last_move = move
        #Keep a list of possible rules for reasons that can be used to defend a claim
        self.reason_rules = []

    def set_opponent(self, opponent):
        self.opponent = opponent

    #Extract the set of possible moves at any turn
    def get_available_moves(self, opponent_move):
        if(self.last_move.agent != None):
            print("My last move:", self.last_move.printable(9))
        print("Opponent's last move:", opponent_move.printable(9))
        #If opponent claimed a new sentence, agent can choose
        #to question, deny, refuse or accept this sentence
        if(opponent_move.move_type == "claim" and self.last_move.move_type != "accept" and  self.last_move.move_type != "deny"
           and self.last_move.move_type != "withdraw"):
            possible_moves =  ["question", "deny", "accept"]
            sentence = opponent_move.sentence
            sentence.negation = not(sentence.negation)
            #If the negation of the sentence is already in the agent's commitment store,
            #then denial is not allowed!
            if(self.commitment_store.fact_in_CS(sentence)):
                possible_moves.remove("deny")
            sentence.negation = not(sentence.negation)
            return possible_moves

        # If opponent questioned a claim, agent has to search for a reason
        # that defends his claim

        elif (opponent_move.move_type == "question" and self.last_move.move_type != "accept" and self.last_move.move_type != "withdraw"):
            claim = opponent_move.sentence
            # Search the commitment store for rules that prove the claim
            # Get rules that prove the claim
            #print(claim.printable())
            reason_rules = self.commitment_store.prove_conclusion(claim)
            # for rule in reason_rules:
            # reasons.append(rule.conditions)
            # Select one of the possible reasons
            # Store rules that apply that can provide reasons
            self.reason_rules = reason_rules
            # If at least 1 reason is found, a reason move is possible
            if (len(reason_rules) > 0):
                return ["reason", "withdraw"]
            # Else, a claim cannot be defended and has to be withdrawn
            else:
                return ["withdraw"]

        # If opponent defends his claim with a reason,
        # the agent can choose to question this reason
        elif (opponent_move.move_type == "reason"):
            return ["question", "accept"]

        # If opponent questioned a reason, the agent has to search for a rule
        # that implies his reason
        elif (opponent_move.move_type == "question" and self.last_move.move_type == "reason"):
            return ["applies", "withdraw"]

        #If opponent denied the claim, this denial can be questioned,
        #or the original claim can be defended
        elif (opponent_move.move_type == "deny"):
            return ["question", "accept"]

        #If the agent has withdrawn a statement, the game reverts back to the parent dialogue.
        #If the opponent was questioning a claim in this parent dialogue, this means the
        #agent was claiming something. Therefore, the agent was not able to defend his claim
        #and should either provide a new defense or withdraw this claim too.
        elif (self.last_move.move_type == "withdraw" and opponent_move.move_type == "question"):
            return ["withdraw"]

        #Simular situation as above, except this time the agent has withdrawn his denial,
        #thus he has to either question or accept the original claim.
        elif(self.last_move.move_type == "withdraw" and opponent_move.move_type == "claim"):
            return ["accept"]

        #Same as the situation for withdraw. Either provide counter-arguments or accept
        #the parent claim too.
        elif (self.last_move.move_type == "accept" and opponent_move.move_type == "claim"):
            return ["accept"]

        #If the agent does not have any way to combat his opponent's claim, he can only accept
        #his opponent's claim.
        return ["accept"]


    def select_move(self, movelist, sentence):
        move_type = ""
        if(self.strategy == "dumb"):
            move_type = movelist[0]
        if(self.strategy == "random"):
            move_type = movelist[randrange(len(movelist))]
        if (move_type == "deny"):
            negated_sentence = Fact(sentence.predicate, sentence.args, sentence.negation)
            return Move(move_type, negated_sentence, self)
        return Move(move_type, sentence, self)


