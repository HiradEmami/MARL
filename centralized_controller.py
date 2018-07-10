import copy
import numpy as np
import network as network
import sys, os
import random

class controller():
    def __init__(self,argExploration, argDiscount, argLearning_rate, argHidden_size, argHidden_activation,
                     argOut_activation,argOutputSize = 5,create_load_mode = "create",
                     argRewardSharing = False):
        # the primary neural network
        self.hidden_size = argHidden_size
        self.learning_rate = argLearning_rate
        self.hidden_activation = argHidden_activation
        self.out_activation = argOut_activation
        # the size of input and output layers
        self.reward_Sharing = argRewardSharing


        self.input_size = (self.vision_x * self.vision_y * 3) + 2 + 2
        self.input_size = (self.vision_x * self.vision_y *3)+ 2

        self.output_size=argOutputSize
        # defining the network
        if create_load_mode =="create":
            print("Creating the network for agent "+str(self.id)+": ")
        else:
            print("Loading the network for agent " + str(self.id) + ": ")

        self.NN = network.NeuralNet(self.input_size, self.hidden_size, self.output_size, self.learning_rate,
                                    self.hidden_activation, self.out_activation)
        if create_load_mode == "load":
            self.NN.loadNetwork(network_folder=self.network_folder)
        # setting the exploration and discount of the network
        self.exploration = argExploration
        self.discount = argDiscount
        # for back prop we need to store :
        #   1) the index of the output layer that corresponds to the move we chose
        self.previous_index = None
