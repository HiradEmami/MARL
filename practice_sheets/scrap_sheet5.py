import numpy as np
import agent
from worldObject import *
from system_utility import *

board = np.zeros((10,10),dtype=int)
count=1


print(board)

ag=agent(argId=1)
ag.positionY=1
ag.positionX=1

ob= obstacle(ar)

vision=ag.get_observable_board(board)

print(vision)

print(len(vision),len(vision[0]))

ag.create_brain(argExploration=0.1, argDiscount=1, argLearning_rate=0.01, argHidden_size=30, argHidden_activation='sigmoid', argOut_activation='linear',argOutputSize=5)
print(ag.get_possible_moves(board))

move, confidence = ag.make_decision(argWGrid=board)

print(move,confidence)