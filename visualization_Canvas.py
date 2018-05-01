__author__='Hirad Emami Alagha'

import numpy as np
import matplotlib.ticker as plticker
import matplotlib.animation as animation
import random as rd
import world as wd
import agent
from worldObject import *
from matplotlib import pyplot as plt
from matplotlib import colors
from system_utility import *




class visualization():
    def __init__(self,argWorld_file_name):

        self.file_name= argWorld_file_name
        self.grid = load_world(worldFOlder=self.file_name)
        self.width =len(self.grid[0])
        self.height= len(self.grid)
        self.color_map = colors.ListedColormap(['black', 'white', 'red', 'green'])
        self.color_bounds = [-6, 0, 1, 99, 105]
        self.norm = colors.BoundaryNorm(self.color_bounds, self.color_map.N)

        self.figure, self.ax = plt.subplots()
        # draw gridlines
        self.ax.grid(which='major', axis='both', linestyle='-', color='black', linewidth=2)

        self.ax.set_xlim(0, self.width)
        self.ax.set_ylim(self.height, 0)

        self.ax.set_xticks(np.arange(0, self.width, 1))
        self.ax.set_yticks(np.arange(0, self.height, 1))

    def animate(self,i):
        grid= load_world(worldFOlder=self.file_name)
        self.ax.imshow(grid,interpolation='nearest', cmap=self.color_map,
                       norm=self.norm,extent=[0, self.width, self.height, 0])


    def display(self):
        ani = animation.FuncAnimation(self.figure, self.animate, interval=1000)
        plt.show()







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