from learner import *
from world import *
from worldObject import *
from copy import copy
from pip._vendor.distlib.compat import raw_input

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

            if num_steps>=self.stepLimit:
                simulation_state="finished"

            remain=self.number_remaining_agents()
            if remain == 0:
                simulation_state = "finished"

            self.do_one_step()
            num_steps += 1
            if self.developerMode:
                print(num_steps,self.stepLimit,simulation_state)
                continue_key = float(raw_input("Enter 1 to continue:"))

        self.reset_settings()
        return num_steps , self.world


    def perform_move(self,argAgent,argMove):
        if argMove == "up":
            self.world.move_up(argPlayer=argAgent)
            if self.developerMode:
                print(self.world.board)
        elif argMove == "down":
            self.world.move_down(argPlayer=argAgent)
            if self.developerMode:
                print(self.world.board)
        elif argMove == "left":
            self.world.move_left(argPlayer=argAgent)
            if self.developerMode:
                print(self.world.board)
        elif argMove == "right":
            self.world.move_right(argPlayer=argAgent)
            if self.developerMode:
                print(self.world.board)
        elif argMove == "halt":
            print("the Move was Halt")

        if self.developerMode:
            self.world.saveWorld('test')


    def do_one_step(self):
        for i in self.world.agents:
            if not  (i.state=="arrived"):
                move, confidence=i.make_decision(argWGrid=self.world.board)
                self.perform_move(argAgent=i,argMove=move)


    #The function for counting the number of remaining agents on the board
    def number_remaining_agents(self):
        count=0
        for i in self.world.agents:
            if not (i.state=="arrived"):
                count +=1
        if self.developerMode:
            print("Number of remaining agents:"+str(count))
        return count