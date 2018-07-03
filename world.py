# The world class creates the 2-dimensional Grid
# It holds lists of all the Obstacles, Agents, Goals
# It has the primary board of the game and has all the objects coded in the matrix
# It has functions for saving itself or load a pre-built world
# You can randomize a world, or load a world or use the create mode that builds the world based on given info
# It also holds functions for moving the agent in the board
__author__='Hirad Emami Alagha - S3218139'

# Required Libraries
import numpy as np
import tkinter as tk
import random as rd
import math
from learner import *
import os
from system_utility import *
from tkinter import *
from worldObject import *
import copy

#Global
SCALE_BETWEEN_MIN = 0
SCALE_BETWEEN_MAX = 2
RAND=-1

class world():

    #there are three modes for the world:
    #   1) "Random" Mode generates a world with random dimension and obstacles
    #   2) "Create" Mode allows specific worlds to be generated
    #   3) "Load" Mode allows a previously generated world to be restored

    def __init__(self,argCreationMode,worldName=None):
        self.Mode = argCreationMode
        self.name = worldName

    #Function to load the entire world
    def loadWolrd(self,argName,argRewardSharing, argCommunication):

        print("\n#######################")
        print("Loading the World : "+str(argName))
        print("#######################\n")

        # Getting the following information from the saved files
        self.board, self.width, self.height, self.agents, self.obstacles, self.goals,self.name = load_world(argName)

        print("World name: " + self.name)
        print("World Width: "+str(self.width))
        print("World Height: "+str(self.height))

        # Copying the board for the reset
        print("Making a copy of the grird ...")
        self.default_board = copy.copy(self.board)

        #creating the structure of the network
        for i in self.agents:
            i.set_scale_parameters(argBoardWidth=self.width, argBoardHeight=self.height ,
                                   argScaleMin=SCALE_BETWEEN_MIN, argScaleMax=SCALE_BETWEEN_MAX)

        self.run_scale_test()

        outputDirect = 'Saved_Worlds' + '/world_' + str(argName)
        hidden_size, learning_rate, hidden_activation, out_activation, output_size, exploration, discount = \
            load_network_structure(open(outputDirect + "/brain.txt", 'r'))

        print("\nLoading Network Structures ...")
        print("hidden_size, learning_rate, hidden_activation, out_activation, output_size, exploration, discount")
        print(hidden_size, learning_rate, hidden_activation, out_activation, output_size, exploration, discount)

        for i in self.agents:
            i.set_network_folder(self.name)
            i.create_brain(argExploration=exploration, argDiscount=discount, argLearning_rate=learning_rate,
                           argHidden_size=hidden_size,argHidden_activation=hidden_activation,
                           argOut_activation='linear', argOutputSize=5,
                           argRewardSharing=argRewardSharing,create_load_mode="load",
                           argCommunication=argCommunication)


    def run_scale_test(self):
        print("\nRunning a test for scale:\n")
        node_x = self.agents[0].scale(argNum=self.agents[0].positionX, argMin=0, argMax=self.agents[0].max_x_scale,
                            scale_max=self.agents[0].scale_max, scale_min=self.agents[0].scale_min)

        node_y = self.agents[0].scale(argNum=self.agents[0].positionY, argMin=0, argMax=self.agents[0].max_y_scale,
                            scale_max=self.agents[0].scale_max, scale_min=self.agents[0].scale_min)

        print("With a world that is "+str(self.width)+ " in width and "+str(self.height)+" in height ...\n"
                + "the pisition of the first agent with (x,y) as : (" + str(self.agents[0].positionX)+","
              + str(self.agents[0].positionY)+") is scaled to ("+str(node_x)+","+str(node_y)+") to be " +
              "between "+str(self.agents[0].scale_min)+" and "+str(self.agents[0].scale_max)+".")

        print("\ntest completed:\n")

    def saveWorld(self,argWorldName):
        save_world(argWorldName,width=self.width,height=self.height,goals=self.goals,agents=self.agents,
                   obstacles=self.obstacles,board=self.board)


    def generate_random_world(self):
        print("fse")

    #creating the world manually
    def createWorld(self,argWidth,argHeigth, argObstacleList, argAgentList, goalList,argAgent_Location_Constraint=True):
        #World Parameters
        self.width = argWidth
        self.height = argHeigth
        #creating empty world
        self.board=np.zeros((self.height,self.width),dtype=int)
        #getting the information about the goal, obstacles, and the payers
        self.obstacles= argObstacleList
        self.goals = goalList
        self.agents= argAgentList
        #placing obsticles and the goal on the grid
        self.place_objects(self.goals)
        self.place_objects(self.obstacles)
        self.place_agents(argMargine_constraint=argAgent_Location_Constraint)
        #taking a copy of the world
        self.default_board = copy.copy(self.board)


    def place_agents(self,argMargine_constraint=True):
        if argMargine_constraint:
            for i in self.agents:
                foundLocation = False
                while not (foundLocation):
                    #picking a random position of the agent
                    i.positionX = rd.randint(0, self.width - 1)
                    i.positionY = rd.randint(0, self.height - 1)
                    if (self.board[i.positionY][i.positionX] == 0):
                        #updating the board
                        self.board[i.positionY][i.positionX] = i.id
                        #setting the default value for the agents
                        i.set_default_positions()
                        foundLocation = True




    def move_up(self,argPlayer):
        # print("up")
        i,j=self.search_for_object(argPlayer)
        self.board[i][j]=0
        #if it the tile is a goal change the state of the state to arrived
        self.check_player(argPlayer)
        if self.board[i-1][j]>99:
            argPlayer.state = "arrived"
        else:
            self.board[i-1][j]=argPlayer.id
        argPlayer.positionY =  argPlayer.positionY - 1
    def move_down(self,argPlayer):
        # print("down")
        i,j=self.search_for_object(argPlayer)
        self.board[i][j]=0
        # if it the tile is a goal change the state of the state to arrived
        self.check_player(argPlayer)
        if self.board[i+1][j]>99:
            argPlayer.state="arrived"
        else:
            self.board[i+1][j]=argPlayer.id
        argPlayer.positionY = argPlayer.positionY + 1
    def move_right(self,argPlayer):
        # print("right")
        i,j=self.search_for_object(argPlayer)
        self.board[i][j]=0
        self.check_player(argPlayer)
        # if it the tile is a goal change the state of the state to arrived
        if self.board[i][j+1]>99:
            argPlayer.state ="arrived"
        else:
            self.board[i][j+1]=argPlayer.id
        argPlayer.positionX = argPlayer.positionX + 1
    def move_left(self,argPlayer):
        # print("left")
        i,j=self.search_for_object(argPlayer)
        self.board[i][j]=0
        self.check_player(argPlayer)
        # if it the tile is a goal change the state of the state to arrived
        if self.board[i][j-1]>99:
            argPlayer.state="arrived"
        else:
            self.board[i][j - 1] = argPlayer.id
        argPlayer.positionX = argPlayer.positionX - 1


    #a search function that returns the index of an object in a list
    def find_object_index(self,object,list):
        for i in range(len(list)):
            if list[i].id == object.id:
                return i

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
                elif self.board[i,j]>99:
                    num_goals +=1
                #if the value is between 1 and 99 we consider that an agent
                elif self.board[i,j]>0 and self.board[i,j]<100:
                    num_agents +=1

        #printing the result of validity check
        print("The resault of Validity Check")
        print("[# tiles of agents, goals , Obstacles] is ",[num_agents,num_goals,num_obstacles])
        print("[# of agents, goals , Obstacles] is ",[len(self.agents),len(self.goals),len(self.obstacles)])

        obstacle_counter= 0
        for i in self.obstacles:
            obstacle_counter += i.width * i.height

        goal_counter= 0
        for i in self.goals:
            goal_counter += i.width * i.height
        #if they matched given values
        if(num_obstacles == obstacle_counter) and (num_goals == goal_counter) and (num_agents == len(self.agents)):
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
    def check_player(self,argPlayer):
        temp = rd.randint(0,250)
        if temp<RAND:
            print("PROC")
            argPlayer.state="arrived"
    #function for setting the objects on the grid
    def place_objects(self,object):
        #for each object
        for i in range(len(object)):
            #calculate the margin of the object
            margin_width = object[i].width
            margin_height = object[i].height
            #random position of object
            if(self.Mode == "Random"):
                #placeholder variable to know whether we found an acceptable location for the object
                foundLocation=False
                #while we did not find an acceptable location we try new random places on board
                while not (foundLocation):
                    #the (x,y) saved in the object classes indicate the top -left cell coordinate
                    #this means (x,y) of an agent with width and height 1 , is just the one cell it occupies
                    #however, (x,y) of a wall with hight = width = 2 is the coordinate of the top left cell of
                    #the 4 cells in the 2x2 matricies it occupies
                    #Here we first select a random position for the object's starting cell
                    object[i].x = rd.randint(0, self.width - 1)
                    object[i].y = rd.randint(0, self.height - 1)
                    #we call the "location acceptable" function that takes the random positions and calculated margine
                    #and determine it is possible for the object to be placed there . It returns a boolean accordingly
                    test=self.location_acceptable(margin_width,margin_height,object[i].x, object[i].y)
                    #if the location was acceptable:
                    if(test):
                        #set the boolean to true
                        foundLocation=True
                        #The cell we have is the top left cell from the object, thus we have to fill out also the other
                        #cells. We use loop to cover the
                        for e in range(object[i].y,object[i].y+object[i].height+1):
                            for q in range(object[i].x, object[i].x + object[i].width+1):
                                self.board[e][q] = object[i].id
            else:
                test = self.location_acceptable(margin_width, margin_height, object[i].x, object[i].y)
                if (test):
                    self.board[object[i].y][object[i].x]=object[i].id
                    for e in range(object[i].y, object[i].y + margin_height):
                        for q in range(object[i].x, object[i].x + margin_width):
                            self.board[e][q] = object[i].id
                else:
                    print("There is an Error in the location of objects.")

    #function to test if the margines cross the border of the grid
    def margin_acceptable(self,sizeX,sizeY,positionX,positionY):
        if positionX+sizeX<self.width+1 and positionY + sizeY < self.height+1:
            return True
        return False

    #function to test if the loction of the obstacle or goal is acceptable
    def location_acceptable(self,sizeX,sizeY,positionX,positionY):
        #we first check if the position of the
        margin_test=self.margin_acceptable(sizeX,sizeY,positionX,positionY)
        if not(margin_test):
            print("The location is exceeds the board. This selected location is not acceptable", (positionX, positionY))
            return False
        else:
            #even if the margines are acceptable, the tiles have to be empty for the object to occupy.
            #The easiest way to know if all the cells are empty is checking whether the sum of that patch is zero
            Sum = sum(sum(self.board[positionY:positionY+sizeY, positionX:positionX+sizeX]))
            if Sum != 0:
                print("The location is occupied. This selected location is not acceptable",(positionX,positionY))
                return False
        return True

    #function for searching objects on the board
    def search_for_object(self,argObject):
        for i in range(self.height):
            for j in range(self.width):
                if self.board[i][j] == argObject.id:
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
            for i in range(x,argGoal.height+1):
                for j in range(y,argGoal.width+1):
                    self.board[i][j]=0
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
            for i in range(x, argObstacle.height + 1):
                for j in range(y, argObstacle.width + 1):
                    self.board[i][j] = 0
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

    def print_the_world(self):
        print("###################")
        print("World Information")
        print("width: "+str(self.width)+"   ,    height :"+str(self.height))
        print("###################")
        print("      agents    ")
        print("###################")
        for i in self.agents:
            print("\nid:"+str(i.id)+"\nvis_x:"+str(i.vision_x)+"\nvis_y:"+str(i.vision_y)+"\nx:"+str(i.positionX)+
                  "\ny:"+str(i.positionY)+"\nstep_cost:"+str(i.step_cost))
        print("###################")
        print("      goals    ")
        print("###################")
        for i in self.goals:
            print("\nid:"+str(i.id)+"\ncolor:"+str(i.color)+"\nwidth:"+str(i.width)+"\nheight:"+str(i.height)+
                  "\nx:"+str(i.x)+"\ny:"+str(i.y))
        print("###################")
        print("      obstacles    ")
        print("###################")
        for i in self.obstacles:
            print("\nid:"+str(i.id)+"\ncolor:"+str(i.type)+"\nwidth:"+str(i.width)+"\nheight:"+str(i.height)+
                  "\nx:"+str(i.x)+"\ny:"+str(i.y))


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