from agent import *
from world import *
from worldObject import *
from copy import copy


class simulation():
    def __init__(self,argWorld,argSteplimit,argDeveloperMode=False):

        self.world = argWorld
        #taking a copy of the starting board
        self.starting_board = copy(self.world.board)
        self.developerMode=argDeveloperMode
        self.stepLimit=argSteplimit

    #function to reset the grid and reset player information
    def reset_settings(self):
        self.world.board = copy(self.starting_board)
        for i in range(len(self.world.agents)):
            self.world.agents[i].reset_agent()

    def run_one_simulation(self):
        num_steps=0
        simulation_state = "running_simulation"
        while not(simulation_state== "finished"):
            self.do_one_step()
            num_steps += 1
            if (self.number_remaining_agents() == 0) or (num_steps == self.stepLimit):
                simulation_state == "finished"

        self.reset_settings()
        return num_steps , self.world


    #TODO: have to implement how to make one step of simulation and agents making decision and moving
    def do_one_step(self):
        for i in self.world.agents:
            if not  (i.state=="arrived"):
                move, confidence=i.make_decision(argWGrid=self.world.board)



    #The function for counting the number of remaining agents on the board
    def number_remaining_agents(self):
        count=0
        for i in self.world.agents:
            if not (i.state=="arrived"):
                count +=1
        if self.developerMode: print("Number of remaining agents:"+str(count))
        return count