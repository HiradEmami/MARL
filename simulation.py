
from agent import *
from world import *
from worldObject import *


class simulation():
    def __init__(self,argWorld,argDeveloperMode=False):
        self.state="initilization"
        self.world = argWorld
        self.developerMode=argDeveloperMode


    def run_one_simulation(self):
        num_steps=0
        simulation_state = "running_simulation"
        while not(simulation_state== "finished"):
            self.do_one_step()
            num_steps += 1
            if self.number_remaining_agents() == 0:
                simulation_state == "finished"
        return num_steps



    def do_one_step(self):
        for i in self.world.agents:
            if not  (i.state=="arrived"):
                #i.move(argWorld=self.world)
                print(2)

    #The function for counting the number of remaining agents on the board
    def number_remaining_agents(self):
        count=0
        for i in self.world.agents:
            if not (i.state=="arrived"):
                count +=1
        if self.developerMode: print("Number of remaining agents:"+str(count))
        return count