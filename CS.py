"""This class represents the commitment store. It can hold facts and rules. Furthermore, it can
check if a rule applies by either giving the rule conditions or rules to check, for a
simplified version of forward or backward chaining
"""
class CS():
    def __init__(self):
        self.facts = {}
        self.rules = {}

    #Add facts with their printable version as keys, for easy retrieval and removal
    def add_fact(self, fact):
        self.facts[fact.printable()] = fact

    #Remove a given fact, using the printable string as a key
    def remove_fact(self, fact):
        del self.facts[fact.printable()]

    def add_rule(self, rule):
        self.rules[rule.printable()] = rule

    def remove_rule(self, rule):
        del self.rules[rule.printable()]

    #Return the printable version of all the facts in the commitment store
    def get_printable_facts(self):
        self.fact_list = []
        for key in self.facts:
            self.fact_list.append(key)
        return "\n".join(self.fact_list)

    def get_printable_rules(self):
        self.rule_list = []
        for value in self.rules:
            self.rule_list.append(value)
        return "\n".join(self.rule_list)
