"""This class represents the commitment store. It can hold facts and rules. Furthermore, it can
check if a rule applies by either giving the rule conditions or rules to check, for a
simplified version of forward or backward chaining
"""
from Fact import *

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

    #Ask the commitment store whether a given fact can be proven with the current facts and rules
    def prove_conclusion(self, fact):
        #Store rules that can prove the fact
        applicable_rules = []
        #Go through every rule
        #Check if the rule's conditions imply the fact (conclusion)
        #Return the conditions and rules corresponding to them
        for key,value in self.rules.items():
            rule = value
            conditions_proven = 0
            unified_conclusion = rule.conclusion.unify(fact)
            #If a rule is found where the conclusion matches the fact
            if(self.facts_match(unified_conclusion, fact)):
                #Check if conditions match facts in the commitment store
                for condition in rule.conditions:
                    # Unify the conditions of the match with the fact
                    unified_condition = condition.unify(fact)
                    for key,value in self.facts.items():
                        #Unify the found facts from the commitment_store with the query fact
                        unified_value = value.unify(fact)
                        #If the found fact matches the condition of the rule, increment
                        if(self.facts_match(unified_value, unified_condition)):
                            conditions_proven = conditions_proven + 1

            #If every condition is proven, the rule proves the conclusion based on the conditions
            #This doesn't allow for chaining (yet). Therefore, conditions have to be facts within the commitment store
            #already.
            if(conditions_proven == len(rule.conditions)):
                applicable_rules.append(rule)
        return applicable_rules

    #Returns true if two facts match
    def facts_match(self, fact1, fact2):
        #Check if the predicate name, arity and negation matches
        return (fact1.predicate == fact2.predicate and
           fact1.equal_args(fact2) and
            fact1.negation == fact2.negation)






