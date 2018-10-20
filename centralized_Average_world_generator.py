import worldObject
from learner import *
from world import *
from system_utility import *
from simulation import  *

NUMBER_OF_AGENTS = 7
WORLD_NAME = 'centralized_average_entire'

REWARD_SHARING = False
COMMUNICATION = False

EXPLORATION = 0.2
LEARNING_RATE = 0.001
DISCOUNT = 0.99
HIDDEN_ACTIVATION = 'sigmoid'
OUT_ACTIVATION = 'linear'
HIDDEN_SIZE = 100
OUT_SIZE = 5

RANDOMIZATION_TEST = False

class worldGenrator():
    def __init__(self):
        self.obstacles = []
        self.agents = []
        self.goals = []
        self.width = 14
        self.height = 14

        self.world = self.generate()

    def generate(self, argName=WORLD_NAME):
        self.name = argName
        # creating Obstacles
        new_obstacle_1 = obstacle(argType='wall', argId=-1, argWidth=2, argHight=2, argX=1, argY=6)
        new_obstacle_2 = obstacle(argType='wall', argId=-2, argWidth=2, argHight=1, argX=8, argY=2)
        new_obstacle_3 = obstacle(argType='wall', argId=-3, argWidth=2, argHight=2, argX=12, argY=6)
        new_obstacle_4 = obstacle(argType='wall', argId=-4, argWidth=2, argHight=2, argX=6, argY=9)
        new_obstacle_5 = obstacle(argType='wall', argId=-5, argWidth=2, argHight=1, argX=12, argY=11)

        self.obstacles.append(new_obstacle_1)
        self.obstacles.append(new_obstacle_2)
        self.obstacles.append(new_obstacle_3)
        self.obstacles.append(new_obstacle_4)
        self.obstacles.append(new_obstacle_5)

        # creating a goal
        new_goal_1 = goal(argColor='green', argId=100, argHight=3, argWidth=1, argX=9, argY=10)
        new_goal_2 = goal(argColor='green', argId=101, argHight=2, argWidth=2, argX=3, argY=3)
        self.goals.append(new_goal_1)
        self.goals.append(new_goal_2)
        # creating the agent
        num_agents=NUMBER_OF_AGENTS
        for i in range(1,num_agents+1):
            # creating the agent
            new_agent = agent(argId=i,argVisionX=3,argVisionY=3)
            # add the agent to the list
            self.agents.append(new_agent)

        # create the meta agent
        meta_centralized_agent = controller()
        # creating the network of the Meta agent
        meta_centralized_agent.build_network(argExploration=EXPLORATION, argDiscount=DISCOUNT, argLearning_rate=LEARNING_RATE,
                               argHidden_size=HIDDEN_SIZE,argHidden_activation=HIDDEN_ACTIVATION,
                               argOut_activation=OUT_ACTIVATION, argOutputSize=OUT_SIZE,
                               argRewardSharing=REWARD_SHARING,create_load_mode="create"
                                             ,argboard_width=self.width, argboard_height=self.height)

        meta_centralized_agent.set_network_folder(WORLD_NAME)

        meta_centralized_agent.save_network()

        self.world = world(argCreationMode="create",worldName=self.name)

        self.world.createWorld(argWidth=self.width,argHeigth=self.height, argObstacleList=self.obstacles, goalList=self.goals, argAgentList=self.agents)

        self.world.set_meta_controller_agent(argMetaController=meta_centralized_agent)

        print(self.world.board)
        print(len(self.world.goals))
        print(len(self.world.agents))
        print(len(self.world.obstacles))
        self.world.check_validity()

        self.world.saveWorld(argWorldName=self.name,argCentralized=True,argMetaAgent=self.world.centralized_meta_agent)

        #testing the world

        self.world.centralized_meta_agent.NN.__del__()
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


        new_world.loadWolrd(argName=self.name,argRewardSharing=REWARD_SHARING,argCommunication=COMMUNICATION
                            ,argCentralized=True)
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
