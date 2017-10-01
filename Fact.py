class Fact():
    def __init__(self, predicate, args, negation):
        self.predicate = predicate
        self.args = args
        self.negation = not(negation)

    #Return a nice, printable fact string
    def printable(self):
        negation_symbol = ''
        if(self.negation):
            negation_symbol = '¬'
        return ("%s%s%s" % (negation_symbol,self.predicate, self.args))

    # Set arguments of one predicate to the arguments of the other one(very simple unification)
    #To prevent changing the original rule/fact, create new fact and return it, unified
    def unify(self, fact):
        #make copy
        altered_fact = Fact(self.predicate, self.args, not(self.negation))
        altered_fact.args = fact.args
        return altered_fact

    #Returns true if both facts have the same arguments
    def equal_args(self, fact2):
        for i in range(len(fact2.args)):
            if(self.args[i] != fact2.args[i]):
                return False
        return True