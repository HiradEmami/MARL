__author__='Hirad Emami Alagha - S3218139'

#required Libraries and Classes
import world
import tkinter as tk
from tkinter import *


##visualization class that provides graphical representation of the 2D grid
##including the obsticles, agents and the goal
class visualization(tk.Tk):
    ##primary Root of visualization in tkinter is passed by argRoot
    def __init__(self,argWorld):
        #cell scaling value given the size of the world
        #the size of the window will be static 600x600 for square worlds
        #the size of the window will be either 700x400 or 700x400 for worlds that are rectangle
        self.world=argWorld
        self.frame_widthScale, self.frame_heightScale = self.calculateTheScale(height=self.world.height, width=self.world.width)
        #the root of tkinter
        self.master = tk.Tk()
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

                self.frame.create_rectangle(j * self.frame_widthScale, i * self.frame_heightScale,
                                            (j + 1) * self.frame_widthScale, (i + 1) * self.frame_heightScale,
                                            fill="white", width=1, outline="gray1")

    def display_simulation(self):
        self.frame.grid(row=0, column=0)
        self.master.mainloop()

    def createWidgets(self):
        self.QUIT = Button(self)
        self.QUIT["text"] = "QUIT"
        self.QUIT["fg"]   = "red"
        self.QUIT["command"] =  self.quit

        self.QUIT.pack({"side": "left"})

        self.hi_there = Button(self)
        self.hi_there["text"] = "Hello",
        self.hi_there["command"] = self.say_hi

        self.hi_there.pack({"side": "left"})


if __name__ == '__main__':
    print("__________EXAMPLE WORLD_________")
    width = 5
    height = 10
    numObsticles = 2
    obsticleInfo = []

    for i in range(numObsticles):
        obsticleInfo.append(('wall', 1, 2))

    print("your sample wolrld is created as:")
    world = world.world(width, height, numObsticles, obsticleInfo)
    print(world.board)
    print(world.obsticle_info)
    print("____________________________")

    root = Tk()
    app = visualization(world, argRoot=root)
    app.mainloop(root)
    root.destroy()
