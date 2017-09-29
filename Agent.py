class Agent():

    def __init__(self, name, state, strategy, commitment_store, move):
        self.name = name
        self.state = state
        self.strategy = strategy
        self.commitment_store = commitment_store
        #self.commitment_store.activate('rules')
        self.move = move

    def set_opponent(self, opponent):
        self.opponent = opponent

    #Extract the set of possible moves at any turn
    def get_available_moves(self, ):
        #Generate the full movelist
        movelist = [
        "withdraw", "accept", "question,", "pass", "deny", "refuse",
        "claim", "reason_for", "reason_against", "valid", "apply",
        "applicable", "exclude"]
        #Apply game-rules to filter the list
        if(self.opponent.state == "claiming"):
            movelist.remove("withdraw")
            movelist.remove("pass")
            movelist.remove("claim")
            movelist.remove("reason_for")
            movelist.remove("valid")
            movelist.remove("apply")
            movelist.remove("applicable")
            movelist.remove("exclude")

        if(self.opponent.state == "deny"):
            movelist = ["question", "reason_for"]

        return movelist

    #Return a list containing all the facts from the agent's commitment store
    def get_facts(self):
        return "\n".join(self.commitment_store.get_kb('facts').dump_specific_facts())
        #print("FIX THIS:")
       # print(self.commitment_store.get_kb('facts').dump_specific_facts())
        #return self.commitment_store.get_kb('facts').dump_specific_facts()
    def get_rules(self):
        (self.commitment_store.get_rb('rules').get_rules().get('owes'))
        return self.commitment_store.get_rb('rules').get_rules()

