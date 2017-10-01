class Rule():
    def __init__(self, conditions, conclusion):
        self.conditions = conditions
        self.conclusion = conclusion

    #Return a nice, printable rule string
    def printable(self):
        condition_list = []
        for condition in self.conditions:
            condition_list.append(condition.printable())
        return " ∧ ".join(condition_list) + " -> " + self.conclusion.printable()