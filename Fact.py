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
