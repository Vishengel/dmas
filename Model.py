from Agent import *
from CS import *
from Fact import *
from Rule import *
from Judge import *

class Model():
    def __init__(self, caseID):
        #Create and init agents
        #Agents are initialized with initial empty moves, to prevent None errors
        self.prosecutor = Agent("Prosecutor", "idle", "dumb", CS(), Move("", None, None))
        self.defendant = Agent("Defendant", "idle", "dumb", CS(), Move("", None, None))
        self.judge = Judge("Judge", "", "", CS(), None)
        self.prosecutor.set_opponent(self.defendant)
        self.defendant.set_opponent(self.prosecutor)
        self.dialogue_stack = []
        self.dialogue_history = []
        self.dialogue_history_natural = []

        #Populate the commitment stores with facts and rules
        self.build_commitment_stores(caseID)
        self.game_over = False

    def build_commitment_stores(self, caseID):
        if caseID == "loan":
            first_fact = Fact('borrowed_from', ('Defendant', 'Prosecutor', 10000), True)
            self.prosecutor.commitment_store.add_fact(first_fact)
            self.prosecutor.commitment_store.add(Fact('older_than', ('loan', '30'), True))
            self.defendant.commitment_store.add_fact(first_fact)
            #self.defendant.commitment_store.add_fact( Fact('owes', ('Defendant', 'Prosecutor', 10000), False) )

            #Add starting rules
            starting_rule = Rule([Fact('borrowed_from', ('x', 'y', 'amount'), True)]
                              ,Fact('owes', ('x', 'y', 'amount'), True), 'valid')
            self.prosecutor.commitment_store.add(starting_rule)
            self.defendant.commitment_store.add(starting_rule)
            """
            self.defendant.commitment_store.add(Rule([Fact('loves', ('x', 'y'), True)]
                              ,Fact('owes', ('x', 'y', 'amount'), False), 'valid'))
            """
            self.defendant.commitment_store.add(Rule([Fact('older_than', ('loan','30'), True)]
                                                     , Rule([Fact('borrowed_from', ('x', 'y', 'amount'), True)]
                              ,Fact('owes', ('x', 'y', 'amount'), True), 'excluded'),'valid'))


            self.defendant.commitment_store.add(Fact('loves', ('Defendant', 'Prosecutor'), True))
            self.defendant.commitment_store.add(Fact('older_than', ('loan','30'), True))

            self.judge.commitment_store.add(Rule([Fact('older_than', ('loan', '30'), True)]
                                                 , Rule([Fact('borrowed_from', ('x', 'y', 'amount'), True)]
                                                        , Fact('owes', ('x', 'y', 'amount'), True), 'excluded'),
                                                 'valid'))

        if caseID == "contract":
            first_fact = Fact('offer_was_heard', ('Defendant', 'Prosecutor'), True)
            self.prosecutor.commitment_store.add(first_fact)
            self.defendant.commitment_store.add_fact(first_fact)

            second_fact = Fact('written_agreement', ('Defendant', 'Prosecutor'), False)
            self.prosecutor.commitment_store.add(second_fact)
            self.defendant.commitment_store.add(second_fact)

            third_fact = Fact('provided_after_written_phase', ('document',), True)
            self.prosecutor.commitment_store.add(third_fact)
            self.defendant.commitment_store.add(third_fact)

            #self.defendant.commitment_store.add_fact( Fact('owes', ('Defendant', 'Prosecutor', 10000), False) )

            fourth_fact = Fact('documented_insanity', ('Defendant',), True)
            self.defendant.commitment_store.add(fourth_fact)
            self.judge.commitment_store.add(fourth_fact)

            fifth_fact = Fact('insane_during_offer', ('Defendant',),True)
            self.defendant.commitment_store.add(fifth_fact)

            #Add starting rules
            first_rule = Rule([first_fact]
                              ,Fact('valid_contract', ('party_1', 'party_2'), True), 'valid')
            self.prosecutor.commitment_store.add(first_rule)
            self.defendant.commitment_store.add(first_rule)

            second_rule = Rule([third_fact]
                              ,Fact('admissable', ('document',), False), 'valid')
            self.prosecutor.commitment_store.add(second_rule)
            self.judge.commitment_store.add(second_rule)

            third_rule = Rule([Fact('insane_during_offer', ('party_1',), True)],
                              Fact('valid_contract', ('party_1', 'party_2'), False),'valid')
            self.defendant.commitment_store.add(third_rule)
            self.judge.commitment_store.add(third_rule)

            fourth_rule = Rule([Fact('documented_insanity', ('party_1', 'document'), True)],
                                Fact('insane_during_offer', ('party_1',),True), "valid")
            self.defendant.commitment_store.add(fourth_rule)
            self.judge.commitment_store.add(fourth_rule)



    #Add the dialogue moves as text to both the logical and natural language frames
    def add_dialogue_content(self, move, dialogue_ID):
        self.dialogue_history.append(move.printable(dialogue_ID))
        move_components = [dialogue_ID, move.agent.name, move.move_type]
        for argument in move.sentence.args:
            move_components.append(argument)
        #Change natural language version of dialogue move depending on move type
        if (move.move_type == "claim"):
            self.dialogue_history_natural.append("%s. %s: ")
        elif(move.move_type == "question"):
            self.dialogue_history_natural.append("%s. %s: Why?" % (dialogue_ID, move.agent))

    def remove_repeating_moves(self, movelist, current_dialogue):
        #print("Unfiltered movelist:", movelist)
        remove_list = []
        for move in movelist:
            #print(movelist)
            if (current_dialogue.turn == self.prosecutor):
                if(move in current_dialogue.prosecutor_move_list):
                    remove_list.append(move)
            else:
                if (move in current_dialogue.defendant_move_list):
                    remove_list.append(move)

        for move in remove_list:
            if move in movelist:
                movelist.remove(move)
        return movelist









