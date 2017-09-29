from Controller import *
from pyke import knowledge_engine



def main():
    simulation = Controller(600,500)
    simulation.run()
    """
    csd = knowledge_engine.engine("defendant_knowledge")
    csp =  knowledge_engine.engine("prosecutor_knowledge")
    csd.reset()
    csp.reset()
    #my_engine.prove_1_goal('facts.owes($defendant, prosecutor, 10000)')
    csd.add_case_specific_fact('facts', 'borrowed_from', ('defendant', 'prosecutor', 10000))
    csd.add_case_specific_fact('facts', 'borrowed_from', ('defendant', 'prosecutor', 30000))
    csp.add_case_specific_fact('facts', 'borrowed_from', ('defendant', 'prosecutor', 999))

    csd.activate('rules')
    #get facts
    print("Defendant: ")
    defendant_facts = csd.get_kb('facts').dump_specific_facts()
    print(defendant_facts)

    print("Prosecutor: ")
    prosecutor_facts = csp.get_kb('facts').dump_specific_facts()
    print(prosecutor_facts)


    #get rules
    #print(csd.get_rb('rules').get_rules())

    print(csd.prove_1_goal('facts.owes(defendant, prosecutor, 10000)'))

    defendant_facts = csd.get_kb('facts').dump_specific_facts()
    print(defendant_facts)




    #csd.get_kb('facts').dump_universal_facts()
    #my_engine.prove_1_goal('family.son_of(paul, leon)')
"""

if __name__ == '__main__':
    main()

