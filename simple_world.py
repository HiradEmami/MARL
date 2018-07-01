import worldObject
from learner import *
from world import *
from system_utility import *
from simulation import  *

NUMBER_OF_AGENTS = 1
WORLD_NAME = 'test'

REWARD_SHARING = False
COMMUNICATION = False

class worldGenrator():
    def __init__(self):
        self.obstacles = []
        self.agents = []
        self.goals = []
        self.width=8
        self.height = 8

        self.world = self.generate()


    def generate(self,argName=WORLD_NAME):
        self.name = argName
        # creating Obstacles
        new_obstacle_1 = obstacle(argType='wall',argId=-1,argWidth=1,argHight=1,argX=1,argY=6)
        self.obstacles.append(new_obstacle_1)
        # creating a goal
        new_goal_1 = goal(argColor='green',argId=100,argHight=1,argWidth=2,argX=0,argY=0)
        self.goals.append(new_goal_1)

        # creating the agent
        num_agents=NUMBER_OF_AGENTS
        for i in range(1,num_agents+1):
            # creating the agent
            new_agent = agent(argId=i,argVisionX=3,argVisionY=3)

            # creating the network of the agent
            new_agent.create_brain(argExploration=0.2, argDiscount=1, argLearning_rate=0.001, argHidden_size=50,
                   argHidden_activation='sigmoid', argOut_activation='linear',
                                   argOutputSize=5,argRewardSharing=REWARD_SHARING,create_load_mode="create",
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


        new_world.loadWolrd(argName=self.name,argRewardSharing=REWARD_SHARING,argCommunication=COMMUNICATION)

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
