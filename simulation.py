from learner import *
from world import *
from worldObject import *
from copy import copy
from pip._vendor.distlib.compat import raw_input

class simulation():
    def __init__(self,argWorld,argSteplimit,argDeveloperMode=False,argrewardSharing=False):
        self.world = argWorld
        #taking a copy of the starting board
        self.starting_board = self.copy_board(self.world.board)
        self.developerMode=argDeveloperMode
        self.stepLimit=argSteplimit
        self.rewardSharing=argrewardSharing
        self.previous_collected_rewards=[]

    #function to reset the grid and reset player information
    def reset_settings(self):
        if self.developerMode:
            print("reseting")
            print("\nstarting board")
            self.print_boards(self.starting_board)
            print("\nworld board after simulation")
            self.print_boards(self.world.board)

        self.world.board = self.copy_board(self.starting_board)

        if  self.developerMode:
            print("\nafter reset")
            self.print_boards(self.world.board)

        for i in range(len(self.world.agents)):
            self.world.agents[i].reset_agent()

    def run_one_simulation(self):

        print("\n###############################")
        print("#   Starting a new simulation #")
        print("###############################\n")

        num_steps=0
        simulation_state = "running_simulation"
        while not(simulation_state== "finished"):

            remain=self.number_remaining_agents()

            if num_steps>=self.stepLimit:
                print("1 Number of remaining Agents: "+str(remain))
                print("The Number of steps rich its limits\n# Performed Moves: "+str(num_steps)+
                      "\n# step limits: "+str(self.stepLimit))
                simulation_state="finished"

            elif remain == 0:
                print("2 Number of remaining Agents: "+str(remain))
                simulation_state = "finished"

            else:
                self.do_one_step()
                num_steps += 1
                if self.developerMode:
                    print(num_steps, self.stepLimit, simulation_state)
                    continue_key = float(raw_input("Enter 1 to continue:"))

        print("\n")
        print("#   Simulation Completed!   #")
        print("\n")
        print("Resetting simulation!")
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
            if self.developerMode:
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

    def copy_board(self,argboard):
        new_list=[]
        for i in range(len(argboard)):
            new_row=[]
            for j in range(len(argboard[0])):
                new_row.append(argboard[i][j])
            new_list.append(new_row)
        return new_list

    def print_boards(self,list):
      for i in list:
          print(i)
