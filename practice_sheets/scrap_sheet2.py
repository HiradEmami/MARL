import numpy as np
from world import *
from agent import *
import random as rd


a = np.zeros((10,10),dtype=int)


#evaluating each move
def get_possible_moves(argBoard):
    #check all 4 actions
    moves=[]
    moves.append(scarlet.try_move_up(argBoard))
    moves.append(scarlet.try_move_down(argBoard))
    moves.append(scarlet.try_move_left(argBoard))
    moves.append(scarlet.try_move_right(argBoard))
    #list of acceptable and rejected moves
    acceptable=[]
    rejected=[]
    #filling up the lists
    for i in moves:
        if i[0]:
            acceptable.append(i)
        else:
            rejected.append(i)
    #returning the acceptable and rejected moves
    return acceptable,rejected



def get_max_value_move(argOptions,argScores):
    if(len(scarlet.possible_moves)==0):
        print("NO Possible Move is Available")
    max=np.max(argScores)
    print(max)
    for i in range(len(argOptions)):
        if argOptions[i][1] == max:
            print(i)
            return i

scarlet=agent(argId=1,argVisionX=10,argVisionY=10,argMode="developer")

scarlet.positionX=3
scarlet.positionY=3
a[scarlet.positionY,scarlet.positionX]=1
a[3,2]=100
a[2,3]=-2
a[3,4]=4
a[4,3]=0
print(a)

scarlet.output_size=5
scarlet.possible_moves, rejectiop=scarlet.get_possible_moves(a)
print(scarlet.possible_moves)
print(rejectiop)

choice= rd.choice(scarlet.possible_moves)
print(choice[2])
print(len(choice))

scores=[100,50,30,70,45]

scarlet.output_size =5
options,scores=scarlet.get_move_options(scores)
print(options,scores)

print("best move:")
index, move, value=scarlet.get_max_value_move(argOptions=options,argScores=scores)
print(move)
print("value:"+str(value))

k=4
p=k
k=9
print(k,p)
