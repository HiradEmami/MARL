__author__ = 'Hirad Emami Alagha - s3218139'

from copy import copy
import numpy as np
import network as network
import sys, random


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
        #   3) "searching"
        #   2) "Finished"
        self.state="initialized"
        #mode defines if the agent is training or testing
        self.mode = argMode

    #The Create_brain function creates the primary neural netwokr that the agent is using the given
    #parameters. The function is called after creation of the agent
    def create_brain(self,argBoard,argExploration, argDiscount, argLearning_rate, argHidden_size, argHidden_activation, argOut_activation):
        #the primary neural network
        self.hidden_size = argHidden_size
        self.learning_rate = argLearning_rate
        self.hidden_activation = argHidden_activation
        self.out_activation = argOut_activation
        #defining the network
        self.NN = network.NeuralNet(64, self.hidden_size, 4, self.learning_rate, self.hidden_activation, self.out_activation)

    #Set_margines function updates the extent that agent sees from the board
    def set_margines(self):
        self.marginx = (int)((self.vision_x - 1) / 2)
        self.marginY = (int)((self.vision_y - 1) / 2)

    #update_the vision of player
    def update_vision(self,argBoard):
        #calculating the boundaries
        y0 = max(0, self.positionY - self.marginY)
        y1 = min(len(argBoard), self.positionY + self.marginY + 1)
        x0 = max(0, self.positionX - self.marginx)
        x1 = min(len(argBoard[0]), self.positionX + self.marginx + 1)
        #calculating the boundaries
        return argBoard[y0:y1, x0:x1]

    def move(self,argWGrid):
        print("will be added")
