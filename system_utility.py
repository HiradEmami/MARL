__author__ ='Hirad Emami Alagha'

#importing required libraries
import numpy as np
import os,time
from world import *
from worldObject import *
from learner import *



#global variables
primaryDirectory='Saved_Worlds'

def save_world(argWorldName,board, obstacles, agents, goals, width, height):
#The primary Directory for worlds is a folder called Saved_worlds

        #The output folder to save all the information of the world is saved as:
        #world+(the user-given name)+ width + height + number of obstacles
        outputDirect = primaryDirectory+'/world_'+str(argWorldName)

        #if the primary path of Saved_worlds does not exist create a new folder
        if not os.path.exists(primaryDirectory):
            print("creating The primary folder under " + primaryDirectory)
            os.makedirs(primaryDirectory)
            print(" The Folder for all saved worlds is created! \n The directory is : " + primaryDirectory)
        else:
             print("Creating new Save File!")

        # if the main path of particular world does not exist create a new folder
        if not os.path.exists(outputDirect):
            print("creating The primary folder under " + outputDirect)
            os.makedirs(outputDirect)
        else:
            print("The new world is saved in MARL/: " + outputDirect)
        #call function to save the world file
        save_grid(outputDirect=outputDirect,board=board)
        save_info(outputDirect=outputDirect,obstacles=obstacles,agents=agents,goals=goals,height=height,width=width)


#the save function that specifically saves the world, this function is also used for visualization
def save_grid(outputDirect,board):
    # saving the main grid
    file_1 = open(outputDirect + "/world.txt", 'w')
    # the primary loop for grid
    for i in range(len(board)):
        for j in range(len(board[i])):
            # writing the values of cells
            file_1.write(str(board[i] [j]) + " ")
        file_1.write("\n")
    # closing the file
    file_1.close()

def save_info(outputDirect,agents,obstacles,goals,height,width):
    # saving the main info file
    file = open(outputDirect + "/info.txt", 'w')
    # the primary loop for basic information
    file.write(str(len(agents)) + " " + str(len(obstacles)) + " " + str(len(goals))+"\n")
    file.write(str(height) + " " + str(width)+"\n")

    for i in range(len(agents)):
        print(len(agents),"TEST")
        file.write(str(agents[i].id)+" "+str(agents[i].vision_x)+" "+str(agents[i].vision_y)+" "
                   +str(agents[i].positionX)+" "+str(agents[i].positionY)+" "+str(agents[i].step_cost)+" "
                   +str(agents[i].mode)+"\n")
        print(str(agents[i].id)+" "+str(agents[i].vision_x)+" "+str(agents[i].vision_y)+" "
                   +str(agents[i].positionX)+" "+str(agents[i].positionY)+" "+str(agents[i].step_cost)+" "
                   +str(agents[i].mode)+"\n")

    for i in range(len(obstacles)):
        file.write(str(obstacles[i].id)+" "+str(obstacles[i].width)+" "+str(obstacles[i].height)+" "+str(obstacles[i].x)
                   +" "+str(obstacles[i].y)+" "+str(obstacles[i].type)+"\n")

    for i in range(len(goals)):
        file.write(str(goals[i].id)+" "+str(goals[i].width)+" "+str(goals[i].height)+" "+str(goals[i].x)+" "+
                   str(goals[i].y)+" "+str(goals[i].color)+"\n")
    
    # closing the file
    file.close()

# PRIVATE function for importing the info file and converting them to appropriate lists
def read_info(argFile):

    # reading all the lines in the file
    lines = argFile.readlines()

    lengths=lines[0].split(" ")
    len_agent = int(lengths[0])
    len_obstacles=int(lengths[1])
    len_goals=int(lengths[2])

    worldinfo=lines[1].split(" ")
    world_height=int(worldinfo[0])
    world_width=int(worldinfo[1])

    #print(len_agent,len_obstacles,len_goals,height,width)

    print(len(lines))
    agents=[]
    goals=[]
    obstacles=[]

    line_counter=2
    num_agent=1
    num_goal=1
    num_obstacle=1

    while(num_agent<len_agent+1):
        info = lines[line_counter].split(" ")
        id = int(info[0])
        vision_x = int(info[1])
        vision_y = int(info[2])
        positionX = int(info[3])
        positionY = int(info[4])
        step_cost = float(info[5])
        temp= str(info[6])
        temp2 = temp.split("\n")
        mode = temp2[0]



        new_agent = agent(argId=id, argVisionX=vision_x, argVisionY=vision_y, argPosX=positionX, argPosY=positionY,
                          argStepCost=step_cost, argMode=mode)
        print(id, vision_x, vision_y, positionX, positionY,
              step_cost, mode)
        agents.append(new_agent)
        line_counter+=1
        num_agent+=1

    while(num_goal<len_goals+1):
        info=lines[line_counter].split(" ")
        print(info)
        id=int(info[0])
        width=int(info[1])
        height=int(info[2])
        x=int(info[3])
        y=int(info[4])
        temp=str(info[5])
        temp2=temp.split("\n")
        type=temp2[0]
        new_obstacle= obstacle(argType=type,argId=id,argWidth=width,argHight=height,argX=x,argY=y)
        num_goal+=1
        line_counter+=1

        obstacles.append(new_obstacle)
        print(type,id,width,height,x,y)


    while(num_obstacle<len_obstacles+1):
        info = lines[line_counter].split(" ")
        id = int(info[0])
        width = int(info[1])
        height = int(info[2])
        x = int(info[3])
        y = int(info[4])
        temp=str(info[5])
        temp2=temp.split("\n")
        color=temp2[0]
        print(color, id, width, height, x, y)
        new_goal = goal(argColor=color, argId=id, argWidth=width, argHight=height, argX=x, argY=y)

        goals.append(new_goal)
        num_obstacle+=1
        line_counter+=1

    return world_width,world_height,agents,obstacles,goals


# PRIVATE function for importing the world file and converting it to matrix
def read_world(argFile):
    # reading all the lines in the file
    lines = argFile.readlines()
    # Creating an empty Grid
    grid = []
    for i in lines:
        cells = i.split(" ")
        # the last element will be empty which we remove
        cells = cells[:-1]
        temp=[]
        for i in cells:
            temp.append((int)(i))
        grid.append(temp)
    #returning the grid
    return grid

#the main load utility function: as the argument it takes the "worldFolder" name. This can be either :
#   1) Just the given world name like "world1"
#   2) Or with the complete format of world_worldName
def load_world(worldFOlder):
    #if the user has given only the name
    if not(worldFOlder.startswith("world_")):
        worldFOlder = "world_"+worldFOlder
    #creating the complete path to folder
    path=primaryDirectory + "/" + worldFOlder
    #counting number of files found and terminating uppon missing files
    num_files = len(os.listdir(path))
    if num_files <1:
        print("Files are missing!")
        return None
    #reading the files
    print('Reading input Files from ' + path + " folder:")
    input_files= []
    for i, file in enumerate(os.listdir(path)):
        if file.endswith('.txt'):
            inputFile=  path+"/"+file
            input_files.append(inputFile)

    print("_________Files Imported_________")
    board=read_world(open(path+"/world.txt",'r'))
    width, height, agents, obstacles, goals =read_info(open(path+"/info.txt",'r'))

    return board , width, height, agents, obstacles, goals

def calculateTheScale(height,width):
    #if the world is square
    if(height == width):
        return 600/width, 600/height
    # if the world's height is bigger than the width
    elif(height>width):
        return 400 / width, 700 / height
    # if the world's width is bigger than the hight
    else:
        return 700 / width, 400 / height

#function to that takes a 2d list and returns a flat array
def flatten_list(argList):
    #flat arraty
    flat_array=[]
    for i in range(len(argList)):
        for j in range(len(argList[0])):
            flat_array.append(argList[i][j])
    #returning the 1d Flattened array
    return flat_array

#function that takes the flattened array and returns the 2d array
def convert_2d(argFlatList,argWidth,argHeight):
    list=np.zeros((argHeight,argWidth),dtype=int)
    if (argWidth*argHeight==len(argFlatList)):
        counter = 0
        for i in range(0, argHeight):
            for j in range(0, argWidth):
                list[i][j] = argFlatList[counter]
                counter += 1
    else:
        print("The list is not convertable to 2d")
    return list