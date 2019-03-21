import worldObject
from learner import *
from world import *
from system_utility import *
from simulation import  *
from shared_policy_brain import  *
NUMBER_OF_AGENTS = 14
possibles_names = ['policy_complex_7x7','policy_complex_3x3','baseline_complex_7x7','baseline_complex_3x3',
             'intention_complex_7x7','intention_complex_3x3','MORL_complex_7x7','MORL_complex_3x3','goal_complex_3x3'
                   ,'goal_complex_7x7']
WORLD_NAME = 'MORL_complex_3x3'

VISION_X = 3
VISION_Y = 3


def get_settings():
    if "baseline" in WORLD_NAME:
        return False,False,False,False
    elif "goal" in WORLD_NAME:
        return False,True,False,False
    elif "policy" in WORLD_NAME:
        return False,False,True,True
    elif "intention" in WORLD_NAME:
        return False,False,True,False
    elif "MORL" in WORLD_NAME:
        return True,False,False,False

MORL , GOAL_COMMUNICATION, COMMUNICATION, SHARED_POLICY = get_settings()
REWARD_SHARING = True
EXPLORATION = 0.2
LEARNING_RATE = 0.001
DISCOUNT = 0.99
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
        self.width=18
        self.height = 18

        self.world = self.generate()

    def generate(self,argName=WORLD_NAME):
        self.name = argName
        # creating Obstacles
        new_obstacle_1 = obstacle(argType='wall', argId=-1, argWidth=2, argHight=2, argX=1, argY=6)
        new_obstacle_2 = obstacle(argType='wall', argId=-2, argWidth=2, argHight=1, argX=8, argY=2)
        new_obstacle_3 = obstacle(argType='wall', argId=-3, argWidth=2, argHight=2, argX=12, argY=6)
        new_obstacle_4 = obstacle(argType='wall', argId=-4, argWidth=2, argHight=2, argX=6, argY=9)
        new_obstacle_5 = obstacle(argType='wall', argId=-5, argWidth=2, argHight=1, argX=12, argY=11)
        new_obstacle_6 = obstacle(argType='wall', argId=-6, argWidth=2, argHight=2, argX=12, argY=16)
        new_obstacle_7 = obstacle(argType='wall', argId=-7, argWidth=2, argHight=2, argX=15, argY=2)
        new_obstacle_8 = obstacle(argType='wall', argId=-8, argWidth=2, argHight=1, argX=16, argY=11)

        self.obstacles.append(new_obstacle_1)
        self.obstacles.append(new_obstacle_2)
        self.obstacles.append(new_obstacle_3)
        self.obstacles.append(new_obstacle_4)
        self.obstacles.append(new_obstacle_5)
        self.obstacles.append(new_obstacle_6)
        self.obstacles.append(new_obstacle_7)
        self.obstacles.append(new_obstacle_8)

        # creating a goal
        new_goal_1 = goal(argColor='green', argId=100, argHight=3, argWidth=2, argX=9, argY=10)
        new_goal_2 = goal(argColor='green', argId=101, argHight=2, argWidth=4, argX=3, argY=3)
        self.goals.append(new_goal_1)
        self.goals.append(new_goal_2)
        # creating the agent
        num_agents=NUMBER_OF_AGENTS
        for i in range(1,num_agents+1):
            # creating the agent
            new_agent = agent(argId=i,argVisionX=VISION_X,argVisionY=VISION_Y)
            if not SHARED_POLICY:
                # creating the network of the agent
                new_agent.create_brain(argExploration=EXPLORATION, argDiscount=DISCOUNT, argLearning_rate=LEARNING_RATE,
                                   argHidden_size=HIDDEN_SIZE,argHidden_activation=HIDDEN_ACTIVATION,
                                   argOut_activation=OUT_ACTIVATION, argOutputSize=OUT_SIZE,
                                   argRewardSharing=REWARD_SHARING,create_load_mode="create",
                                   argCommunication=COMMUNICATION,argGoalCommunication=GOAL_COMMUNICATION,
                                       argMORL=MORL)

                new_agent.set_network_folder(WORLD_NAME)

                new_agent.save_network()
            # add the agent to the list
            self.agents.append(new_agent)

        if SHARED_POLICY:

            shared_brain = Policy_agent(argId=12, argVisionX=3, argVisionY=3)

            # creating the network of the agent
            shared_brain.shared_create_brain(argExploration=EXPLORATION, argDiscount=DISCOUNT, argLearning_rate=LEARNING_RATE,
                                   argHidden_size=HIDDEN_SIZE, argHidden_activation=HIDDEN_ACTIVATION,
                                   argOut_activation=OUT_ACTIVATION, argOutputSize=OUT_SIZE,
                                   argRewardSharing=REWARD_SHARING, create_load_mode="create",
                                   argCommunication=COMMUNICATION,
                                             argMORL=MORL,argGoalCommunication=GOAL_COMMUNICATION)

            shared_brain.set_network_folder(WORLD_NAME)

            shared_brain.save_network()


        self.world = world(argCreationMode="create",worldName=self.name)

        self.world.createWorld(argWidth=self.width,argHeigth=self.height, argObstacleList=self.obstacles, goalList=self.goals, argAgentList=self.agents)

        if SHARED_POLICY:
            self.world.set_shared_policy_brain(shared_brain)

        print(self.world.board)
        print(len(self.world.goals))
        print(len(self.world.agents))
        print(len(self.world.obstacles))
        self.world.check_validity()

        self.world.saveWorld(argWorldName=self.name,argShared_policy=SHARED_POLICY)

        #testing the world
        if not SHARED_POLICY:
            for i in self.world.agents:
                i.NN.__del__()
        else:
            self.world.shared_policy_brain.NN.__del__()

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

        new_world.loadWolrd(argName=self.name,argRewardSharing=REWARD_SHARING,argCommunication=COMMUNICATION,
                            argSharedPolicy=SHARED_POLICY,argMORL=MORL,argGoalcommunication=GOAL_COMMUNICATION)
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
