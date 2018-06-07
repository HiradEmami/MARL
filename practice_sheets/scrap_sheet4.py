import numpy as np
import random as rd
from system_utility import flatten_list




def get_odds(argGrid):
    for i in range(len(argGrid)):
        for j in range(len(argGrid[0])):
            if argGrid[i][j]%2 == 1:
                argGrid[i][j]=1
            else:
                argGrid[i][j]=0
    return argGrid

def get_evens(argGrid):
    for i in range(len(argGrid)):
        for j in range(len(argGrid[0])):
            if argGrid[i][j]%2 == 0:
                argGrid[i][j]=1
            else:
                argGrid[i][j]=0
    return argGrid

def get_fives(argGrid):
    for i in range(len(argGrid)):
        for j in range(len(argGrid[0])):
            if argGrid[i][j]%5 == 0:
                argGrid[i][j]=1
            else:
                argGrid[i][j]=0
    return argGrid


def shape_input_layer(argObstacleList, argGoalList, argAgnetList):
    if not (len(argAgnetList)==len(argGoalList)) or not(len(argGoalList)==len(argObstacleList)):
        print("ERROR! The Sizes of The Lists Does not Match")
    else:
        counter=len(argObstacleList)+len(argGoalList)+len(argAgnetList)+2
        result_list = []
        for i in argObstacleList:
            result_list.append(i)
        for j in argGoalList:
            result_list.append(j)
        for k in argAgnetList:
            result_list.append(k)
        result_list.append(2)
        result_list.append(4)
        if not len(result_list) == counter:
            print("Failed to shape Input layer")
        else:
            return result_list





a = np.zeros((5,5),dtype=int)
counter= 1
for i in range(0,5):
    for j in range(0,5):
        a[i][j]=counter
        counter+=1

print(a)
print(get_odds(a))
print(get_evens(a))

b=flatten_list(get_evens(a))
c=flatten_list(get_odds(a))
d=flatten_list(get_fives(a))


p = shape_input_layer(b,c,d)
print(p)
print(len(b),len(c),len(d),len(p))

