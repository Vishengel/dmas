from Agent import *
from Witness import *
from Interrogator import *

class Model():
    def __init__(self):
        self.agents = []
        self.num_agents = 5
        self.state = "init"

    def start_simulation(self, width, height):
        print("Simulation initialized!")
        #Create witness agents
        xpos = int(width / self.num_agents)
        ypos = int(height /  10)
        for i in range(self.num_agents):
            self.agents.append(Witness(xpos * i + 5, ypos))
        #Create interrogator agent
        self.agents.append(Interrogator(width / 2, height / 2) )



    def play(self):
        pass