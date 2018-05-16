import worldObject
import agent
from world import *
from system_utility import *
from simulation import  *


class worldGenrator():
    def __init__(self):
        self.obstacles = []
        self.agents = []
        self.goals = []
        self.width, self.height = 8,10

        self.world = self.generate()


    def generate(self):
        #creating Obstacles
        new_obstacle_1 = obstacle(argType='wall',argId=-1,argWidth=2,argHight=4,argX=4,argY=10)
        new_obstacle_2 = obstacle(argType='wall', argId=-2, argWidth=1, argHight=2, argX=7, argY=3)
        self.obstacles.append(new_obstacle_1)
        self.obstacles.append(new_obstacle_2)
        #creating a goal
        new_goal = goal(argColor='green',argId=100,argHight=2,argWidth=2,argX=0,argY=0)
        self.goals.append(new_goal)

        #creating the agent
        new_agent = agent.agent(argId=2,argVisionX=5,argVisionY=5)
        self.agents.append(new_agent)

        self.world = world(argCreationMode="create")

        self.world.createWorld(argWidth=10,argHeigth=15,argObstacleInfo=self.obstacles, goalInfo=self.goals, argAgentInfo=self.agents)

        print(self.world.board)


    def get_world(self):
        return self.world


    def print(self,list):
        for i in list:
            print(i.id)


if __name__ == '__main__':
    world_generator= worldGenrator()
