from Move import *
from Fact import *
from Rule import *
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
        self.exclusion_rules = []

    def set_opponent(self, opponent):
        self.opponent = opponent


    #Extract the set of possible moves at any turn
    def get_available_moves(self, opponent_move, claim_proponent):
        print("%s is now moving. Last move: %s" % (self.name, self.last_move.move_type))
        print("Opponent %s's last move is %s." % (opponent_move.agent.name,opponent_move.move_type))
        #print("Last opponent move was: %s" % (opponent_move.move_type))
        #print("Last opponent:", opponent_move.move_type)
        possible_moves = []

        if (opponent_move.move_type == "valid"):
            possible_moves = ["question", "accept"]
            if(self.commitment_store.rule_in_CS(opponent_move.sentence)):
                possible_moves.remove("question")
            #print(possible_moves)


        # If the opponent claims that a rule applies, the agent can question this, or claim that this rule is
        # excluded
        elif (opponent_move.move_type == "applies" and self.last_move.move_type != "accept"):
            possible_moves = ["excluded", "question", "accept"]
            self.reason_rules = self.commitment_store.prove_rule_exclusion(opponent_move.sentence)
            #If no exclusion rules are present, exclusion move is not possible
            if(len(self.reason_rules ) == 0):
                possible_moves.remove("excluded")
            #print(self.exclusion_rules[0].printable() )


        #If opponent has accepted an exclusion of the agent's  rule, withdraw the applicability of this rule
        elif (opponent_move.move_type == "excluded" and self.last_move.move_type == "accept"):
            possible_moves = ["withdraw"]

        #If opponent claims that the agent's rule is excluded, this can be questioned or accepted
        elif (opponent_move.move_type == "excluded"):
            possible_moves = ["question", "accept"]


        #If opponent claimed a new sentence, agent can choose
        #to question, deny, refuse or accept this sentence
        elif(opponent_move.move_type == "claim"):
            possible_moves =  ["deny", "question", "accept"]

            #A rule cannot be denied
            if(isinstance(opponent_move.sentence, Rule)):
                possible_moves.remove("deny")

           #Try to prove the negation of the claim, to see if denial is possible
            claim = copy.copy(opponent_move.sentence)
            claim.negation = not(claim.negation)
            reason_rules = self.commitment_store.prove_conclusion(claim)
            self.reason_rules = reason_rules
            if (len(reason_rules) == 0):
                possible_moves.remove("deny")

            #If agent has already accepted a reason for a claim, he can no longer deny this claim
            claim.negation = not(claim.negation)
            if(self.commitment_store.contains_reason(claim)):
                possible_moves.remove("deny")




        # If opponent questioned a reason, the agent has to search for a rule
        # that implies his reason.
        # OR:
        # #If opponent questioned an exclusion claim of a rule, find a rule that applies that excludes this rule
        elif (opponent_move.move_type == "question" and (self.last_move.move_type == "reason" or self.last_move.move_type == "excluded")):
            # return ["applies", "withdraw"]
            possible_moves = ["applies", "withdraw"]
            #if(self.last_move.move_type == "excluded"):
                #possible_moves.remove("applies")

        #If opponent questioned an apply claim, the agent has to point to the validity of the rule that applies
        elif(opponent_move.move_type == "question" and (self.last_move.move_type == "applies" or self.last_move.move_type == "excluded") ):

            possible_moves = ["valid", "withdraw"]
            # Check if if the validity of the rule is in the commitment store
            valid_rule = Rule(opponent_move.sentence.conditions, opponent_move.sentence.conclusion, "valid")
            if ( not(self.commitment_store.rule_in_CS(valid_rule)) ):
                possible_moves.remove("valid")

        #If opponent questioned a validity claim, the agent can make a call to the arbiter to verify the validity
        #of the rule
        elif (opponent_move.move_type == "question" and self.last_move.move_type == "valid"):
            possible_moves = ["arbiter", "withdraw"]


        # If opponent questioned a claim, agent has to search for a reason
        # that defends his claim
        elif (opponent_move.move_type == "question" or opponent_move.move_type == "question-fact"):
            possible_moves = ["reason", "arbiter", "withdraw"]
            if(opponent_move.move_type == "question"):
                possible_moves.remove("arbiter")
            claim = opponent_move.sentence
            #claim.property = ""
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
            #print(len(reason_rules))
            if (len(reason_rules) == 0):
                #return ["reason", "withdraw"]
                possible_moves.remove("reason")
            # Else, a claim cannot be defended and has to be withdrawn


        # If opponent defends his claim with a reason,
        # the agent can choose to question this reason, or question
        #the states fact in the rezson.
        elif (opponent_move.move_type == "reason"):
            #return ["question", "accept"]
            possible_moves = ["question", "question-fact", "accept"]
            reason = copy.copy(opponent_move.sentence)
            reason.property = ""
            # Questioning the fact in the reason can only be done if the fact
            # is not established
            if (self.commitment_store.fact_in_CS(reason)):
                possible_moves.remove("question-fact")

        #If opponent denied the claim, this denial can be questioned,
        #or the original claim can be defended
        elif (opponent_move.move_type == "deny"):
            #return ["question", "accept"]
            possible_moves = ["question", "accept"]

        #If the agent does not have any way to combat his opponent's claim, he can only accept
        #his opponent's claim.
        else:
            possible_moves = ["accept"]



        if(self.last_move.move_type == "withdraw" and claim_proponent.name != self.name):
            if("withdraw" in possible_moves):
                possible_moves.remove("withdraw")
                possible_moves.append("accept")
        elif(self.last_move == "accept" and claim_proponent.name != self.name):
            if ("withdraw" in possible_moves):
                possible_moves.remove("withdraw")
                possible_moves.append("accept")


        return possible_moves


    def select_move(self, movelist, sentence):
        if("valid" in movelist):
            return Move("valid", sentence, self)
        move_type = ""
        if(self.strategy == "dumb"):
            move_type = movelist[0]
        if(self.strategy == "random"):
            move_type = movelist[randrange(len(movelist))]
        if (move_type == "deny"):
            negated_sentence = Fact(sentence.predicate, sentence.args, sentence.negation)
            return Move(move_type, negated_sentence, self)
        return Move(move_type, sentence, self)



