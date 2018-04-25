#The world class creates the 2-dimensional Grid
__author__='Hirad Emami Alagha - S3218139'

#required Libraries
import numpy as np
import tkinter as tk
import random as rd
import math
import agent
import os
from system_utility import *
from tkinter import *
from worldObject import *


class world():

    #there are three modes for the world:
    #   1) "Random" Mode generates a world with random dimension and obstacles
    #   2) "Create" Mode allows specific worlds to be generated
    #   3) "Load" Mode allows a previously generated world to be restored

    def __init__(self,argCreationMode):
        self.Mode = argCreationMode








    def loadWolrd(self,argName):
        load_world(argName)

    def saveWorld(self,argWorldName):
        save_world(argWorldName,self.board,self.obstacles)


    def generate_random_world(self):
        print("fse")

    def createWorld(self,argWidth,argHeigth, argObstacleInfo, argAgentInfo, goalInfo):
        #World Parameters
        self.width = argWidth
        self.height = argHeigth
        #creating empty world
        self.board=np.zeros((self.height,self.width),dtype=int)
        #getting the information about the goal, obstacles, and the payers
        self.obstacles= argObstacleInfo
        self.goals = goalInfo
        self.agents= argAgentInfo
        #placing obsticles and the goal on the grid
        self.place_objects(self.goals)
        self.place_objects(self.obstacles)









    #check weather the created world matches specified information
    def check_validity(self):
        #placeholder variables for counting agents, goals and obstacles (default = 0)
        num_obstacles = num_goals = num_agents = 0
        #looping through the entire board
        for i in range(self.height):
            for j in range(self.width):
                #if the value is less than zero we count that as an obstacle
                if self.board[i,j]<0:
                    num_obstacles +=1
                # if the value is more than 100 we count that as a goal
                elif self.board[i,j]>100:
                    num_goals +=1
                #if the value is between 1 and 99 we consider that an agent
                elif self.board[i,j]>0 and self.board[i,j]<100:
                    num_agents +=1

        #printing the result of validity check
        print("The resault of Validity Check")
        print("[# of agents, goals , Obstacles] is ",[num_agents,num_goals,num_obstacles])
        print("The required [# of agents, goals , Obstacles] is ",[len(self.agents),len(self.goals),len(self.obstacles)])

        #if they matched given values
        if(num_obstacles == len(self.obstacles)) and (num_goals == len(self.goals)) and (num_agents == len(self.agents)):
            print("The test was successfully, Right amount of objects are created")
            #Since the number of objects are correct, this function would validate the board
            return True
        elif(num_agents != len(self.agents)):
            print("The test was not successful. Missing Player!")
        elif(num_goals != len(self.goals)):
            print("The test was not successful. Missing Goal!")
        elif(num_obstacles != len(self.obstacles)):
            print("The test was not successful. Missing Obstacle!")
        #if either one of the objects were missing this function will invalidate the board
        return False


    #function for setting the goals on the grid
    def place_objects(self,object):
        #for each goal
        for i in range(len(object)):
            #calculate the margin that is half of the size of the goal
            margin_width = math.ceil(object[i].width/2)
            margin_height = math.ceil(object[i].height/2)
            #random position of object
            if(self.Mode == "Random"):
                foundLocation=False
                while not (foundLocation):
                    object[i].x = rd.randint(0, self.width - 1)
                    object[i].y = rd.randint(0, self.height - 1)
                    test=self.location_acceptable(margin_width,margin_height,object[i].x, object[i].y)
                    if(test):
                        foundLocation=True

                        for e in range(object[i].y,object[i].y+margin_height):
                            for q in range(object[i].x, object[i].x + margin_width):
                                self.board[e][q] = object[i].id
            else:
                test = self.location_acceptable(margin_width, margin_height, object[i].x, object[i].y)
                if (test):

                    self.board[object[i].y][object[i].x]=object[i].id
                    print((margin_height,margin_width))
                    for e in range(object[i].y, object[i].y + margin_height+1):
                        print(e)
                        for q in range(object[i].x, object[i].x + margin_width+1):
                            print(q)
                            self.board[e][q] = object[i].id
                            print(self.board[e][q])
                else:
                    print("There is an Error in the location of objects.")








    #function to test if the margines cross the border of the grid
    def margin_acceptable(self,sizeX,sizeY,positionX,positionY):
        if positionX+sizeX<self.width and positionY + sizeY < self.height:
            return True
        return False

    #function to test if the loction of the obstacle or goal is acceptable
    def location_acceptable(self,sizeX,sizeY,positionX,positionY):
        #we first check if the position of the
        margin_test=self.margin_acceptable(sizeX,sizeY,positionX,positionY)
        if not(margin_test):
            return False
        else:
            #even if the margines are acceptable, the tiles have to be empty for the object to occupy.
            #The easiest way to know if all the cells are empty is checking whether the sum of that patch is zero
            Sum = sum(sum(self.board[positionY:positionY+sizeY+1, positionX:positionX+sizeX+1]))
            if Sum != 0:
                return False
        return True




    def add_agents(self):
        print("fuck")

    #function for searching objects on the board
    def search_for_object(self,argObject):
        for i in range(self.height):
            for j in range(self.width):
                if self.board[i,j] == argObject.id:
                    return i,j
        print("Failed to find the object!")
        return None,None

    # The function for removing the goal from the work
    def remove_goal(self,argGoal):
        #First we find the position of Agent on the board
        x,y=self.search_for_object(argGoal)
        #if we failed to find the agent, we return False and none for its position
        if x is None or y is None:
            print("Failed to find Goal"+str(argGoal.id))
            return False,None,None
        #if we successfully found the goal
        else:
            if self.visualize:
                print("Goal " + str(argGoal.id) + "is removed")
            #Remove goal from the board
            self.board[x,y]= 0
            return True,x,y

    # The function for removing the obstacle from the work
    def remove_obstacle(self,argObstacle):
        # First we find the position of Agent on the board
        x, y = self.search_for_object(argObstacle)
        # if we failed to find the agent, we return False and none for its position
        if x is None or y is None:
            print("Failed to find Goal" + str(argObstacle.id))
            return False, None, None
        # if we successfully found the goal
        else:
            if self.visualize:
                print("Obstacle " + str(argObstacle.id) + "is removed")
            # Remove goal from the board
            self.board[x, y] = 0
            return True, x, y

    #The function for removing the agent from the work
    def remove_agent(self,argAgent):
        #First we find the position of Agent on the board
        x,y=self.search_for_object(argAgent)
        #if we failed to find the agent, we return False and none for its position
        if x is None or y is None:
            print("Failed to find player"+str(argAgent.id))
            return False,None,None
        #if we successfully found the agent
        else:
            if self.visualize:
                print("Player " + str(argAgent.id) + "is removed")
            #Remove Agent from the board
            self.board[x,y]= 0
            return True,x,y


if __name__=='__main__':
    print("__________EXAMPLE WORLD_________")
    width=10
    height=10
    numObstacle =1
    obstacleInfo=[]

    for i in range(numObstacle):
        obstacleInfo.append(('wall',1,2))

    agentInfo=[]
    agentInfo.append(2)

    print("your sample wolrld is created as:")
    world=world("Create",True)
    world.createWorld(width,height,obstacleInfo, agentInfo,agentInfo)
    print(world.obstacles)
    world.board[0,1] = -1
    print(world.board[0][1])
    world.check_validity()
    print(world.board)
    print("____________________________")