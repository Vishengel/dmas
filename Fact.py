class Fact():
    def __init__(self, predicate, args, negation):
        self.predicate = predicate
        self.args = args
        self.negation = not(negation)
        #possible properties: reason()
        self.property = ""
        #A fact can be a reason for a specific claim
        self.claim = ""
        #Possible property is 'reason-for' or 'reason-against'


    #Return a nice, printable fact string
    def printable(self):
        negation_symbol = ''
        if(self.negation):
            negation_symbol = '¬'
        if(self.property == "reason-for"):
            if(self.claim.negation):
                claim_negation = "¬"
            else:
                claim_negation = ""
            return ("reason(%s%s%s, %s%s%s, pro)" % (negation_symbol,self.predicate, self.args,
                                           claim_negation, self.claim.predicate, self.claim.args))

        return ("%s%s%s" % (negation_symbol,self.predicate, self.args))

    #Return the fact in the form reason(reason_for, claim, pro)
    #or (reason_against, claim, con)


    # Set arguments of one predicate to the arguments of the other one(very simple unification)
    #To prevent changing the original rule/fact, create new fact and return it, unified
    def unify(self, fact):
        altered_fact = Fact(self.predicate, self.args, not(self.negation))
        #Only assign the arguments that this fact can hold
        #Example unification:
        #unify(hates(x, y), owes(defendant, prosecutor, 10000)) = hates(defendant, prosecutor)
        #and ABSOLUTELY NOT hates(defendant, prosecutor, 10000) !!!!
        #This implies that order in the args is very important!
        #This may need to be adjusted when this becomes a problem...
        altered_fact.args = fact.args[:len(self.args)]
        return altered_fact

    #Returns true if both facts have the same arguments
    def equal_args(self, fact2):
        #Sentences are not equal if they don't have the same amount of arguments
        if(len(self.args) != len(fact2.args)):
            return False
        for i in range(len(fact2.args)):
            if(self.args[i] != fact2.args[i]):
                return False
        return True