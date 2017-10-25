import copy
class Rule():
    def __init__(self, conditions, conclusion, property):
        self.conditions = conditions
        self.conclusion = conclusion
        self.property = property
        self.number = 0

    #Return a nice, printable rule string
    def printable(self):
        condition_list = []
        for condition in self.conditions:
            condition_list.append(condition.printable())
        return self.property + "( " +  " ∧ ".join(condition_list) + " -> " + self.conclusion.printable() + " )"



