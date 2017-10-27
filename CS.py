"""This class represents the commitment store. It can hold facts and rules. Furthermore, it can
check if a rule applies by either giving the rule conditions or rules to check, for a
simplified version of forward or backward chaining
"""
from Fact import *
from Rule import *
import copy
class CS():
    def __init__(self):
        self.facts = {}
        self.rules = {}

    #Add facts with their printable version as keys, for easy retrieval and removal
    def add_fact(self, fact):
        self.facts[fact.printable()] = fact

    #Remove a given fact, using the printable string as a key
    def remove_fact(self, fact):
        try:
            del self.facts[fact.printable()]
        except:
            print("No such fact exists in this CS.")

    #Check if a fact is already present in the CS
    def fact_in_CS(self, fact):
        return fact.printable() in self.facts

    def add_rule(self, rule):
        rule.number = len(self.rules) + 1
        self.rules[rule.printable()] = rule

    def remove_rule(self, rule):
        try:
            del self.rules[rule.printable()]
        except:
            print("No such rule exists in this CS.")


    def add(self, sentence):
        if (isinstance(sentence, Fact)):
            self.add_fact(sentence)
        else:
            self.add_rule(sentence)

    def remove(self, sentence):
        if (isinstance(sentence, Fact)):
            self.remove_fact(sentence)
        else:
            self.remove_rule(sentence)


    # Check if a rule is already present in the CS
    def rule_in_CS(self, rule):
        return rule.printable() in self.rules

    def in_CS(self, sentence):
        if (isinstance(sentence, Fact)):
            return self.fact_in_CS(sentence)
        else:
            claim = copy.copy(sentence)
            claim.property = "valid"
            return self.rule_in_CS(sentence)

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

    #Check if the commitment store contains an accepted reason for the given sentence
    def contains_reason(self, sentence):
        for key, facts in self.facts.items():
            if(facts.claim != None):
                if(facts.claim.printable() == sentence.printable()):
                    return True
        return False

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
            """if(not(isinstance(value, Fact))):
                continue"""
            try:
                unified_conclusion = rule.conclusion.unify(fact)
            except:
                print("WARNING: CAN'T UNIFY!")
                continue
            #If a rule is found where the conclusion matches the fact
            #The rule also has to be a valid rule
            if(self.facts_match(unified_conclusion, fact) and rule.property == "valid"):
                #print(unified_conclusion.printable())
                #Check if conditions match facts in the commitment store
                for condition in rule.conditions:
                    #print("condition: ",condition.printable())
                    # Unify the conditions of the match with the fact
                    unified_condition = condition.unify(fact)
                    print(unified_condition.printable())
                    for key,value in self.facts.items():
                        #print("Fact:", value.printable())
                        #print("Condition: ", unified_condition.printable())
                        #If the found fact matches the condition of the rule, increment
                        #check if the two facts are actually facts and not rules!
                        if(isinstance(value, Fact) and self.facts_match(value, unified_condition)):
                            conditions_proven = conditions_proven + 1
                            #print("Condition proven!")
                            break
                        
            #If every condition is proven, the rule proves the conclusion based on the conditions
            #This doesn't allow for chaining (yet). Therefore, conditions have to be facts within the commitment store
            #already.
            #print("conditions_proven:", conditions_proven)
            if(conditions_proven == len(rule.conditions)):
                applicable_rules.append(rule)
        return applicable_rules

    def prove_rule_exclusion(self, rule):
        #print("TOTAL RULE:",rule.printable())
        # Store rules that can prove the excluded rule
        applicable_rules = []
        # Go through every rule
        # Check if the rule's conditions imply the fact (conclusion)
        # Return the conditions and rules corresponding to them
        for key, value in self.rules.items():
            rule = value
            conditions_proven = 0
            excluded_rule = rule.conclusion
            #Check if this conclusion is a rule with the 'excluded' property
            if (excluded_rule.property == "excluded"):
                # Check if conditions match facts in the commitment store
                for condition in rule.conditions:
                    if(not(self.fact_in_CS(condition))):
                        break
                    else:
                         conditions_proven = conditions_proven + 1

            # If every condition is proven, this means that the exclusion rule is applies
            if (conditions_proven == len(rule.conditions)):
                applicable_rules.append(rule)
        return applicable_rules




    #Returns true if two facts match
    def facts_match(self, fact1, fact2):
        #print("Fact 1:", fact1.printable())
        #print("Fact 2:", fact2.printable())
        #Check if the predicate name, arity and negation matches
        return (fact1.predicate == fact2.predicate and
           fact1.equal_args(fact2) and
            fact1.negation == fact2.negation)





