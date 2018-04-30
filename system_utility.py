__author__ ='Hirad Emami Alagha'

#importing required libraries
import numpy as np
import os,time
from world import *

#global variables
primaryDirectory='Saved_Worlds'

def save_world(argWorldName,board, obstacles):
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


#the save function that specifically saves the world, this function is also used for visualization
def save_grid(outputDirect,board):
    # saving the main grid
    file_1 = open(outputDirect + "/world.txt", 'w')
    # the primary loop for grid
    for i in range(len(board)):
        for j in range(len(board[i])):
            # writing the values of cells
            file_1.write(str(board[i, j]) + " ")
        file_1.write("\n")
    # closing the file
    file_1.close()

def save_info(outputDirect,agents,obsticals,goals,world):
    # saving the main info file
    file = open(outputDirect + "/info.txt", 'w')
    # the primary loop for basic information
    file.write(str(len(agents))+" "+str(len(obstacle))+" "+str(len(goals)))
    file.write("\n")
    file.write(str(world.height)+" "+str(world.height))
    
    # closing the file
    file.close()



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
#   2) Or with the complete format of
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
            inputFile=  open(path+"/"+file, 'r')

            input_files.append(inputFile)

    print("_________Files Imported_________")
    grid=read_world(open(path+"/world.txt",'r'))
    return grid

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