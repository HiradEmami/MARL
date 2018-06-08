import world as wd
from worldObject import *
import learner,os
from tkinter import *
import time,random


initial=True
if initial:
    obstacles = []
    obstacle1 = obstacle("wall", argWidth=2, argHight=2, argX=4, argY=4, argId=-1)
    obstacle2= obstacle("wall",argWidth=2, argHight=2, argX=6, argY=8, argId=-2)

    obstacles.append(obstacle1)
    obstacles.append(obstacle2)


    goals = []
    goa11 = goal("red", argWidth=1, argHight=1, argX=8, argY=9, argId=100)
    goa12 = goal("blue", argWidth=4, argHight=4, argX=0, argY=0, argId=101)

    goals.append(goa11)
    goals.append(goa12)

    agents = []
    num_agents =8
    for i in range(num_agents):
        a=learner.agent(argId=i+1)
        agents.append(a)

    world = wd.world("Create")
    world.createWorld(argWidth=10, argHeigth=15, argObstacleInfo=obstacles, argAgentInfo=agents, goalInfo=goals)
    print(world.board)
    world.saveWorld(argWorldName="test")
    print("hello")
    test=True
    counter = 0

    while(test):

        counter=random.randint(0,3)
        if counter==0:
            counter +=1
            time.sleep(0.5)
        elif counter == 1:
            world.try_move_left(agents[4])
            world.saveWorld(argWorldName="test")
            time.sleep(0.5)
        elif counter == 2:
            world.try_move_up(agents[4])
            world.saveWorld(argWorldName="test")
            time.sleep(0.5)
        else:
            world.try_move_right(agents[4])
            world.saveWorld(argWorldName="test")
            time.sleep(0.5)















