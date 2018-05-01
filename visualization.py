__author__='Hirad Emami Alagha'

import numpy as np
import matplotlib.ticker as plticker
import matplotlib.animation as animation
import random as rd
import world as wd
import agent,sys
from worldObject import *
from matplotlib import pyplot as plt
from matplotlib import colors
from system_utility import *


file_name = "test"
grid = load_world(worldFOlder=file_name)
width = len(grid[0])
height = len(grid)
color_map = colors.ListedColormap(['black', 'white', 'red', 'green'])
color_bounds = [-6, 0, 1, 99, 105]
norm = colors.BoundaryNorm(color_bounds, color_map.N)

figure, ax = plt.subplots()
# draw gridlines
ax.grid(which='major', axis='both', linestyle='-', color='black', linewidth=2)

ax.set_xlim(0, width)
ax.set_ylim(height, 0)

ax.xaxis.set_tick_params(labeltop='on',labelbottom="off")

ax.set_xticks(np.arange(0,width, 1))
ax.set_yticks(np.arange(0,height, 1))


def animate(i):
    grid = load_world(worldFOlder=file_name)
    ax.imshow(grid, interpolation='nearest', cmap=color_map,
                   norm=norm, extent=[0, width,height, 0])

ani = animation.FuncAnimation(figure, animate, interval=500)
plt.show()

