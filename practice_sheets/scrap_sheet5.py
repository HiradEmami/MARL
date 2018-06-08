import numpy as np
import learner
from worldObject import *
from system_utility import *
from world import *

board = np.zeros((10,10),dtype=int)
count=1
ob = obstacle(argId=-2,argWidth=2,argHight=2,argX=2,argY=1,argType="wall")

gl= goal(argId=100,argWidth=2,argHight=2,argColor="green",argX=0,argY=2)

for i in range(ob.height):
    for j in range(ob.width):
        board[ob.y+i][ob.x+j]=ob.id

for i in range(gl.height):
    for j in range(gl.width):
        board[gl.y+i][gl.x+j]=gl.id



ag=agent(argId=1)
ag.positionY=1
ag.positionX=1


ag2=agent(argId=3)
ag2.positionX=2
ag2.positionY=0

board[ag.positionY][ag.positionX]=ag.id
board[ag2.positionY][ag2.positionX]=ag2.id
print(board)


vision=ag.get_observable_board(board)

print(vision)

obstacle_grid=ag.get_obstacle_grid(vision)
goal_grid=ag.get_goal_grid(vision)
agent_grid=ag.get_agent_grid(vision)

print("goal grid")
print(goal_grid)
print("Obstacle Grid")
print(obstacle_grid)
print("agent grid")
print(agent_grid)
print("example flat")
#print(ag.flatten_list(ag.get_goal_grid(vision)))
print("input")
print(ag.shape_input_layer(argObstacleList=obstacle_grid,argGoalList=goal_grid,argAgnetList=agent_grid))

ag.create_brain(argExploration=0.1, argDiscount=1, argLearning_rate=0.01, argHidden_size=30, argHidden_activation='sigmoid', argOut_activation='linear',argOutputSize=5)
print(ag.get_possible_moves(board))

move, confidence = ag.make_decision(argWGrid=board)

print(move,confidence)