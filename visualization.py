__author__='Hirad Emami Alagha'

import numpy as np
import matplotlib.ticker as plticker
import random as rd
import world as wd
import agent
from worldObject import *
from matplotlib import pyplot as plt
from matplotlib import colors




if __name__ =='__main__':
    obstacles = []
    obstacle1 = obstacle("wall", argWidth=2, argHight=2, argX=5, argY=5, argId=-1)
    obstacle2 = obstacle("swamp", 3, 3, 10, 10, -2)

    obstacles.append(obstacle1)
    obstacles.append(obstacle2)

    goals = []
    goa11 = goal("red", argWidth=2, argHight=3, argX=3, argY=3, argId=100)
    goa12 = goal("blue", argWidth=2, argHight=2, argX=17, argY=11, argId=101)

    goals.append(goa11)
    goals.append(goa12)

    agents = []
    agen1 = agent.agent(argId=1)
    agen2 = agent.agent(argId=2)

    agents.append(agen1)
    agents.append(agen2)

    world = wd.world("Create")
    world.createWorld(argWidth=20, argHeigth=20, argObstacleInfo=obstacles, argAgentInfo=agents, goalInfo=goals)
    print(world.board)