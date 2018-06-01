import worldObject
from agent import *
from world import *
from system_utility import *
from simulation import  *


class worldGenrator():
    def __init__(self):
        self.obstacles = []
        self.agents = []
        self.goals = []
        self.width, self.height = 10,15

        self.world = self.generate()


    def generate(self):
        #creating Obstacles
        new_obstacle_1 = obstacle(argType='wall',argId=-1,argWidth=2,argHight=2,argX=1,argY=6)
        new_obstacle_2 = obstacle(argType='wall', argId=-2, argWidth=2, argHight=2, argX=6, argY=7)
        self.obstacles.append(new_obstacle_1)
        self.obstacles.append(new_obstacle_2)
        #creating a goal
        new_goal_1 = goal(argColor='green',argId=100,argHight=3,argWidth=1,argX=0,argY=0)
        new_goal_2 = goal(argColor='green',argId=101,argHight=3,argWidth=1,argX=9,argY=11)
        self.goals.append(new_goal_1)
        self.goals.append(new_goal_2)
        #creating the agent
        num_agents=8
        for i in range(1,num_agents+1):
            new_agent = agent(argId=i,argVisionX=3,argVisionY=3)
            self.agents.append(new_agent)

        self.world = world(argCreationMode="create")

        self.world.createWorld(argWidth=self.width,argHeigth=self.height, argObstacleList=self.obstacles, goalList=self.goals, argAgentList=self.agents)

        print(self.world.board)
        print(len(self.world.goals))
        print(len(self.world.agents))
        print(len(self.world.obstacles))
        self.world.check_validity()

        self.world.saveWorld(argWorldName='test')
        new_world = world(argCreationMode="load")
        new_world.loadWolrd(argName='test')

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
