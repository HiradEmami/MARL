__author__ = 'Hirad Emami Alagha - s3218139'

from copy import copy
import numpy as np
import network as network
import sys, random
from system_utility import *


class agent():
    #An agent is initialized using:
    #   1)   An integer "id"
    #   2)   The Extent of it's vision = (argVisionY, argVisionX)  #The default value is set at 5
    #   3)   Mode = that can be training, testing
    def __init__(self,argId,argVisionX=5,argVisionY=5,argMode="train"):
        #the position of the agent on grid
        self.positionX=0
        self.positionY=0
        #the id of the agent
        self.id = argId
        #the vision of the agent, portion of the word it observs
        self.vision_x = argVisionX
        self.vision_y = argVisionY
        #Calculating the margine of his vision using "set_margines" function
        self.set_margines()
        #The area of the board that agent sees is set at 0
        self.vision = []
        #the State of the player can be:
        #   1) "initialized"
        #   3) "selecting next action"
        #   4) "waiting for the action"
        #   2) "arrived"
        self.state="initialized"
        #mode defines if the agent is training or testing or developer
        self.mode = argMode

    #The Create_brain function creates the primary neural netwokr that the agent is using the given
    #parameters. The function is called after creation of the agent
    def create_brain(self,argExploration, argDiscount, argLearning_rate, argHidden_size, argHidden_activation, argOut_activation,argInputLayerSize,argOutputSize=4):
        #the primary neural network
        self.hidden_size = argHidden_size
        self.learning_rate = argLearning_rate
        self.hidden_activation = argHidden_activation
        self.out_activation = argOut_activation
        #the size of input and output layers
        self.input_size=argInputLayerSize
        self.output_size=argOutputSize
        #defining the network
        self.NN = network.NeuralNet(self.input_size, self.hidden_size, self.output_size, self.learning_rate, self.hidden_activation, self.out_activation)
        #the memory of agent's moves as a dictionary with capacity of 100 moves
        self.memory = [dict() for x in range(100)]  # Containing all moves it played during the game
        self.move_count = 0

    #Set_margines function updates the extent that agent sees from the board
    def set_margines(self):
        self.marginx = (int)((self.vision_x - 1) / 2)
        self.marginY = (int)((self.vision_y - 1) / 2)

    #update_the vision of player
    def get_observable_board(self,argBoard):
        if self.mode =="developer":
            return argBoard
        else:
            #calculating the boundaries
            y0 = max(0, self.positionY - self.marginY)
            y1 = min(len(argBoard), self.positionY + self.marginY + 1)
            x0 = max(0, self.positionX - self.marginx)
            x1 = min(len(argBoard[0]), self.positionX + self.marginx + 1)
            #calculating the boundaries
            return argBoard[y0:y1, x0:x1]


    #the function for selecting the next action
    def make_decision(self,argWGrid):
        #The portion of the grid that is observed by the agent currently, will be passed as argWGrid
        #This matrix is flattened to be used as the input layer of the Q-learning network
        self.input_layer=flatten_list(argWGrid)
        self.possible_moves, self.rejected_moves = self.get_possible_moves(argBoard=argWGrid)

    def try_move_up(self, argboard):
        if (self.positionY - 1) > -1:
            if argboard[self.positionY - 1, self.positionX] == 0:
                # self.move_up(argAgent)
                # self.agents[index].positionY -=1
                return True, "empty", "up"
            elif argboard[self.positionY - 1, self.positionX] > 99:
                return True, "goal", "up"
            elif argboard[self.positionY - 1, self.positionX] < 0:
                return False, "obstacle", "up"
            else:
                return False, "occupied", "up"
        else:
            return False, "out_of_range", "up"

    def try_move_down(self, argboard):
        height=len(argboard)
        if (self.positionY + 1) < height:
            if argboard[self.positionY + 1, self.positionX] == 0:
                # self.move_left(argAgent)
                # self.agents[index].positionY += 1
                return True, "empty", "down"
            elif argboard[self.positionY + 1, self.positionX] > 99:
                return True, "goal", "down"
            elif argboard[self.positionY + 1, self.positionX] < 0:
                return False, "obstacle", "down"
            else:
                return False, "occupied", "down"
        else:
            return False, "out_of_range", "down"

    def try_move_left(self, argboard):
        if (self.positionX - 1) > -1:
            if argboard[self.positionY, self.positionX - 1] == 0:
                # self.move_left(argAgent)
                # self.agents[index].positionX -=1
                return True, "empty", "left"
            elif argboard[self.positionY, self.positionX - 1] > 99:
                return True, "goal", "left"
            elif argboard[self.positionY, self.positionX - 1] <0:
                return False, "obstacle", "left"
            else:
                return False, "occupied", "left"
        else:
            return False, "out_of_range", "left"

    def try_move_right(self, argboard):
        width=len(argboard[0])
        if (self.positionX + 1) < width:
            if argboard[self.positionY, self.positionX + 1] == 0:
                # self.move_right(argAgent)
                # self.agents[index].positionX +=1
                return True, "empty", "right"
            elif argboard[self.positionY, self.positionX + 1] > 99:
                return True, "goal", "right"
            elif argboard[self.positionY, self.positionX + 1] < 0:
                return False, "obstacle", "right"
            else:
                return False, "occupied", "right"
        else:
            return False, "out_of_range", "right"

    # evaluating each move
    def get_possible_moves(self,argBoard):
        # check all 4 actions
        moves = []
        moves.append(self.try_move_up(argBoard))
        moves.append(self.try_move_down(argBoard))
        moves.append(self.try_move_left(argBoard))
        moves.append(self.try_move_right(argBoard))
        # list of acceptable and rejected moves
        acceptable = []
        rejected = []
        # filling up the lists
        for i in moves:
            if i[0]:
                acceptable.append(i)
            else:
                rejected.append(i)
        # returning the acceptable and rejected moves
        return acceptable, rejected
