__author__ = 'Hirad Emami Alagha - s3218139'

from copy import copy
import numpy as np
import network as network
import sys, random


class agent():
    def __init__(self,argId, argExploration, argDiscount, argLearning_rate, argHidden_size, argHidden_activation, argOut_activation,argMode="train"):
        #the position of the agent on grid
        self.positionX=0
        self.positionY=0
        #the id of the agent
        self.id = argId
        #the vision of the agent, portion of the word it observs
        self.vision_x = 0
        self.vision_y = 0
        #the State of the player can be:
        #   1) "initialized"
        #   3) "searching"
        #   2) "Finished"
        self.state="initialized"
        #mode defines if the agent is training or testing
        self.mode = argMode
        #the primary neural network
        self.hidden_size = argHidden_size
        self.learning_rate = argLearning_rate
        self.hidden_activation = argHidden_activation
        self.out_activation = argOut_activation

        self.NN = network.NeuralNet(64, self.hidden_size, 4, self.learning_rate, self.hidden_activation, self.out_activation)

    def move(self,argWGrid):
        print("fart")
