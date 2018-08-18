import worldObject
from learner import *
from world import *
from system_utility import *
from simulation import  *

NUMBER_OF_AGENTS = 4
WORLD_NAME = 'test_centralized'

REWARD_SHARING = False
COMMUNICATION = False

EXPLORATION = 0.2
LEARNING_RATE = 0.001
DISCOUNT = 1
HIDDEN_ACTIVATION = 'sigmoid'
OUT_ACTIVATION = 'linear'
HIDDEN_SIZE = 50
OUT_SIZE = 5

RANDOMIZATION_TEST = False

class worldGenrator():
    def __init__(self):
        self.obstacles = []
        self.agents = []
        self.goals = []
        self.width=10
        self.height = 15

        self.world = self.generate()


    def generate(self,argName=WORLD_NAME):
        self.name = argName
        # creating Obstacles
        new_obstacle_1 = obstacle(argType='wall',argId=-1,argWidth=2,argHight=2,argX=1,argY=6)
        new_obstacle_2 = obstacle(argType='wall', argId=-2, argWidth=2, argHight=2, argX=6, argY=7)
        self.obstacles.append(new_obstacle_1)
        self.obstacles.append(new_obstacle_2)
        # creating a goal
        new_goal_1 = goal(argColor='green',argId=100,argHight=3,argWidth=1,argX=0,argY=0)
        new_goal_2 = goal(argColor='green',argId=101,argHight=3,argWidth=1,argX=9,argY=11)
        self.goals.append(new_goal_1)
        self.goals.append(new_goal_2)
        # creating the agent
        num_agents=NUMBER_OF_AGENTS
        for i in range(1,num_agents+1):
            # creating the agent
            new_agent = agent(argId=i,argVisionX=3,argVisionY=3)

            # creating the network of the agent
            new_agent.create_brain(argExploration=EXPLORATION, argDiscount=DISCOUNT, argLearning_rate=LEARNING_RATE,
                                   argHidden_size=HIDDEN_SIZE,argHidden_activation=HIDDEN_ACTIVATION,
                                   argOut_activation=OUT_ACTIVATION, argOutputSize=OUT_SIZE,
                                   argRewardSharing=REWARD_SHARING,create_load_mode="create",
                                   argCommunication=COMMUNICATION)

            new_agent.set_network_folder(WORLD_NAME)

            new_agent.save_network()
            # add the agent to the list
            self.agents.append(new_agent)

        self.world = world(argCreationMode="create",worldName=self.name)

        self.world.createWorld(argWidth=self.width,argHeigth=self.height, argObstacleList=self.obstacles, goalList=self.goals, argAgentList=self.agents)

        print(self.world.board)
        print(len(self.world.goals))
        print(len(self.world.agents))
        print(len(self.world.obstacles))
        self.world.check_validity()

        self.world.saveWorld(argWorldName=self.name)

        #testing the world
        for i in self.world.agents:
            i.NN.__del__()
        new_world = world(argCreationMode="load")
        if RANDOMIZATION_TEST:
            print("\n##########################")
            print("     Test Randomization Check")
            print("##########################\n")
            print("Before Randomization:")
            print(self.world.board)
            print("Randomized:")
            self.world.test_randomization_prepration()
            print(self.world.board)
            print("Restored:")
            for i in self.world.agents:
                i.reset_agent()
            self.world.board = self.world.default_board
            print(self.world.board)


        new_world.loadWolrd(argName=self.name,argRewardSharing=REWARD_SHARING,argCommunication=COMMUNICATION)
        for i in new_world.agents:
            print(i.default_positionX,i.default_positionY)
        new_world.print_the_world()

    def get_world(self):
        return self.world

    def print(self,list):
        for i in list:
            print(i.id)

    def check_save_load(self,saveBoard,loadBoard):
        if not(len(saveBoard)==len(loadBoard)):
            print("the save and load differ in height")
        if not(len(saveBoard[0])==len(loadBoard[0])):
            print("the save and load differ in width")
        test = True
        for i in range(len(saveBoard)):
            for j in range(len(saveBoard[1])):
                if not(saveBoard[i][j] == loadBoard[i][j]):
                    test = False
        return test
if __name__ == '__main__':
    world_generator= worldGenrator()