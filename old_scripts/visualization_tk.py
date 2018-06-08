__author__='Hirad Emami Alagha - S3218139'

#required Libraries and Classes
import world
import tkinter as tk
from tkinter import *


##visualization class that provides graphical representation of the 2D grid
##including the obsticles, agents and the goal
class visualization(tk.Tk):
    ##primary Root of visualization in tkinter is passed by argRoot
    def __init__(self,argWorld,argtk):
        #cell scaling value given the size of the world
        #the size of the window will be static 600x600 for square worlds
        #the size of the window will be either 700x400 or 700x400 for worlds that are rectangle
        self.world=argWorld
        self.frame_widthScale, self.frame_heightScale = self.calculateTheScale(height=self.world.height, width=self.world.width)
        #the root of tkinter
        self.master = argtk
        #name and size of the window
        # name and size of the window
        self.master.title("MARL - Simulation Display")
        print(self.world.width * self.frame_widthScale, self.world.height * self.frame_heightScale)
        #the main frame initialization and setting the size of the window based on the scale and the size of the world
        self.frame = Canvas(self.master, height=(self.world.height * self.frame_heightScale),
                            width=(self.world.width * self.frame_widthScale))

        self.render()

    def calculateTheScale(self,height, width):
        # if the world is square
        if (height == width):
            return 600 / width, 600 / height
        # if the world's height is bigger than the width
        elif (height > width):
            return 400 / width, 700 / height
        # if the world's width is bigger than the hight
        else:
            return 700 / width, 400 / height

    #Rendering THe Grid
    def render(self):
        for i in range(self.world.height):
            for j in range(self.world.width):
                type=self.set_type(self.world.board[i][j])
                self.draw_cell(type,i,j)

    def draw_cell(self,argType,i,j):
        color=self.set_color(argType)
        self.frame.create_rectangle(j * self.frame_widthScale, i * self.frame_heightScale,
                                    (j + 1) * self.frame_widthScale, (i + 1) * self.frame_heightScale,
                                    fill=color, width=1, outline="gray1")

    def set_color(self,argType):
        colors = {
            "agent": "light sky blue",
            "obstacle": "black",
            "goal": "green",
            "empty": "white"
        }
        return colors.get(argType,"white")

    def set_type(self,argValue):
        if argValue<0:
            return "obstacle"
        elif argValue == 0:
            return "empty"
        elif argValue>0 and argValue<100:
            return "agent"
        elif argValue > 99:
            return "goal"
