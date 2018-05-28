__author__ = 'Hirad Emami Alagha - s3218139'

import copy
import numpy as np
import network as network
import sys
import random



#TODO: I should add the halt move properly to the network and every other function
#TODO: I should make the functions for performing the moves properly

class agent():
    #An agent is initialized using:
    #   1)   An integer "id"
    #   2)   The Extent of it's vision = (argVisionY, argVisionX)  #The default value is set at 5
    #   3)   Mode = that can be training, testing
    def __init__(self,argId,argVisionX=3,argVisionY=3,argMode="train",argStepCost=0.1):
        #the position of the agent on grid
        self.positionX=0
        self.positionY=0
        #placeholder for the initial position
        self.default_positionX=0
        self.default_positionY=0
        #the id of the agent
        self.id = argId
        #setting the cost of
        #the vision of the agent, portion of the word it observs
        self.vision_x = argVisionX
        self.vision_y = argVisionY
        #Calculating the margine of his vision using "set_margines" function
        self.set_margines()
        #The area of the board that agent sees is set at 0
        self.vision = []
        #the State of the player can be:
        #   1) "initialized"
        #   3) "progressing : selecting next action
        #   4) "waiting for the action"
        #   2) "arrived"
        self.state="initialized"
        #mode defines if the agent is "training" or "testing" or "developer"
        self.mode = argMode
        #counter of number of moves
        self.move_count = 0

    #the function to reset the agent back to the initial state to start the simulation again
    def reset_agent(self):
        #reseting the number of moves
        self.move_count = 0
        #setting back the state of the agent
        self.state = "initialized"
        #setting the location of the agents back to default values
        self.positionX = self.default_positionX
        self.positionY = self.default_positionY

    #setter for the default values
    def set_default_positions(self):
        self.default_positionY = self.positionY
        self.default_positionX = self.positionX

    def set_position(self,posY,posX):
        self.positionX= posX
        self.positionY=posY

    #The Create_brain function creates the primary neural netwokr that the agent is using the given
    #parameters. The function is called after creation of the agent
    def create_brain(self,argExploration, argDiscount, argLearning_rate, argHidden_size, argHidden_activation, argOut_activation,argOutputSize=5):
        #the primary neural network
        self.hidden_size = argHidden_size
        self.learning_rate = argLearning_rate
        self.hidden_activation = argHidden_activation
        self.out_activation = argOut_activation
        #the size of input and output layers
        self.input_size=self.vision_x * self.vision_y
        self.output_size=argOutputSize
        #defining the network
        self.NN = network.NeuralNet(self.input_size, self.hidden_size, self.output_size, self.learning_rate, self.hidden_activation, self.out_activation)
        #setting the exploration and discount of the network
        self.exploration = argExploration
        self.discount = argDiscount
        #for back prop we need to store :
        #   1) the index of the output layer that corresponds to the move we chose
        self.previous_index = None

    #Set_margines function updates the extent that agent sees from the board
    # for example if the vision is 3x3 it means the agent is at a center of a square
    #and the agent sees one tile in every dimension
    def set_margines(self):
        self.marginx = (int)((self.vision_x - 1) / 2)
        self.marginY = (int)((self.vision_y - 1) / 2)

    #update_the vision of player
    def get_observable_board(self,argBoard):
        #if we are using developer mode we only return the entire board
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
        observabl_grid = self.get_observable_board(argBoard=argWGrid)
        obstacle_board = self.get_obstacle_grid(argGrid=observabl_grid)
        agent_board= self.get_agent_grid(argGrid=observabl_grid)
        goal_board= self.get_goal_grid(argGrid=observabl_grid)
        self.input_layer=self.shape_input_layer(argObstacleList=obstacle_board, argGoalList=goal_board, argAgnetList=agent_board)
        self.possible_moves, self.rejected_moves = self.get_possible_moves(argBoard=argWGrid)
        #the confidance is a scalar value between 0 and 1 which determins the certainty of the agent
        self.confidence = -1
        #if the mode is set at training/developer we use the following steps
        #note that this would only work if the state is not initialized
        #THis means no attempt at back prop if it is the first step
        if not(self.mode == "testing") and not (self.state == "initialized"):
            #we first obtain our previous input layer by copying the input of NN
            previous_input_layer = copy.copy(self.NN.input_layer)  # previous state (s0)
            previous_output_layer = copy.copy(self.NN.output_layer)  # previous expected reward (r1)

            # Obtain network's current output (a1)
            _, new_confidence, _ = self.get_best_move()

            # Calculate actual reward
            previous_output_layer[self.previous_index] = self.discount * new_confidence

            # Backpropagate actual reward
            self.NN.back_propagation(previous_output_layer, input_data=previous_input_layer)
        else:
            self.state = "Progressing"

        #training : this statement selects the move
        if not (self.mode == "testing"):
            #first we try a chance on a random move for exploration
            if random.uniform(0,1) < self.exploration:
                index, move = self.get_random_move()
                output_layer = self.NN.forward_propagation(self.input_layer)
                self.confidence = output_layer[index]
                # Use network forward pass
            else:
                index, confidence, move = self.get_best_move()

        #testing
        else:
            #just simply forward pass to obtain the move
            index, confidence, move = self.get_best_move()

        #uodating counter values and previous index variable
        self.previous_index = index
        self.move_count += 1

        return move, confidence

    # Update the weights
    def final_update(self, opponent_score, own_score):
        if self.mode == "train":
            corrected_output_layer = copy.copy(self.NN.output_layer)
            if opponent_score < own_score:
                corrected_output_layer[self.previous_index] = 1
            elif opponent_score == own_score:
                corrected_output_layer[self.previous_index] = 0
            elif opponent_score > own_score:
                corrected_output_layer[self.previous_index] = -1
            self.NN.back_propagation(corrected_output_layer)
        # Reset things after a round
        self.reset_agent()

    # Using a forward pass, find the best move along with its index and confidence (= output node value)
    def get_best_move(self):
        # first we obtain the network's output using forward propogation given the input layer
        network_rewards = copy.copy(self.NN.forward_propagation(self.input_layer))
        # obtain the output nodes (rewards) corresponding with legal moves
        #this returns two list :
        #  1) the options =(moves, score) eg, [('up',5),('left',4)]
        #  2) the scores =[network output value] eg, [5,4]
        options,scores = self.get_move_options(argOutputlayer=network_rewards)
        #we call the function that finds the index, move and value given the options for the best move
        index, move, value =  self.get_max_value_move(argOptions=options,argScores=scores)
        #returning the result for selecting the best move
        return index, value, move

    #function that returns a list of confidence
    def get_move_options(self,argOutputlayer):
        #we first take a copy of the output layer
        output=copy.copy(argOutputlayer)
        #checking if the output layer's size matches what we specified
        if not (len(output) ==self.output_size):
            print("ERROR!!! OUTPUT LAYER DOES NOT HAVE ACCEPTABLE SIZE")
            print(len(output), self.output_size)
        #placeholder variable that stores the score of the corresponding accepted move in a list
        scores=[]
        options=[]
        #we loop through all the possible moves
        for i in self.possible_moves:
            move_index = self.move_to_index(argMove=i[2])
            temp = (i[2], output[move_index])
            options.append(temp)
            scores.append(output[move_index])
        return options,scores

    #function for selecting move with max value , it returns the index of the move with the highest value
    def get_max_value_move(self,argOptions, argScores):
        if (len(self.possible_moves) == 0):
            print("NO Possible Move is Available")
        max = np.max(argScores)
        for index in range(len(argOptions)):
            if argOptions[index][1] == max:
                #it returns the index of the item, the move and the value of the move
                return index, argOptions[index][0], argOptions[index][1]


    def get_random_move(self):
        randomChoice = random.choice(self.possible_moves)
        index = self.move_to_index(randomChoice[2])
        return index, randomChoice[2]

    #function that takes a move and returns it's corresponding index in output layer
    def move_to_index(self,argMove):
        if argMove=="up":
            return 0
        elif argMove == "down":
            return 1
        elif argMove == "left":
            return 2
        elif argMove == "right":
            return 3
        elif argMove == "halt":
            return 4

    #function that takes an index of output layer and returns the corresponding move
    def index_to_move(self,argIndex):
        if argIndex == 0:
            return "up"
        elif argIndex == 1:
            return "down"
        elif argIndex == 2:
            return "left"
        elif argIndex == 3:
            return "right"
        elif argIndex == 4:
            return "halt"



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
        #creating halt move manually:
        halt_move = (True,"halt","halt")
        #since Halting is always possible , it is automatically added to the acceptable moves
        acceptable.append(halt_move)
        # returning the acceptable and rejected moves
        if not (len(acceptable)+len(rejected)==self.output_size):
            print("ERROR! the sum of accepted and rejected are bigger than output layer size:\n")
            print("Output_layer: "+str(self.output_size)+" ,accepted: "+str(len(acceptable))+" ,rejected: "+str(len(rejected)))
        return acceptable, rejected


    def get_obstacle_grid(self,argGrid):
        for i in range(len(argGrid)):
            for j in range(len(argGrid[0])):
                if argGrid[i][j]<0:
                    argGrid[i][j]=1
                else:argGrid[i][j]=0
        result = self.flatten_list(argGrid)
        return result


    def get_goal_grid(self,argGrid):
        for i in range(len(argGrid)):
            for j in range(len(argGrid[0])):
                if argGrid[i][j]>99:
                    argGrid[i][j]=1
                else:
                    argGrid[i][j]=0
        result = self.flatten_list(argGrid)
        return result

    def get_agent_grid(self,argGrid):
        for i in range(len(argGrid)):
            for j in range(len(argGrid[0])):
                if argGrid[i][j]>0 and argGrid[i][j]<100:
                    if argGrid[i][j]==self.id:
                        argGrid[i][j] = 0
                    else:
                        argGrid[i][j] = 1
                else:
                    argGrid[i][j]=0
        result=self.flatten_list(argGrid)
        return result

    def shape_input_layer(self,argObstacleList, argGoalList, argAgnetList):
        if not (len(argAgnetList) == len(argGoalList)) or not (len(argGoalList) == len(argObstacleList)):
            print("ERROR! The Sizes of The Lists Does not Match")
        else:
            counter = len(argObstacleList) + len(argGoalList) + len(argAgnetList)+2
            result_list = []
            for i in argObstacleList:
                result_list.append(i)
            for j in argGoalList:
                result_list.append(j)
            for k in argAgnetList:
                result_list.append(k)

            result_list.append(self.positionX)
            result_list.append(self.positionY)

            if not len(result_list) == counter:
                print("Failed to shape Input layer")
            else:
                return result_list

    # function to that takes a 2d list and returns a flat array
    def flatten_list(self,argList):
        # flat arraty
        flat_array = []
        for i in range(len(argList)):
            for j in range(len(argList[0])):
                flat_array.append(argList[i][j])
        # returning the 1d Flattened array
        return flat_array

    # function that takes the flattened array and returns the 2d array
    def convert_2d(self,argFlatList, argWidth, argHeight):
        list = np.zeros((argHeight, argWidth), dtype=int)
        if (argWidth * argHeight == len(argFlatList)):
            counter = 0
            for i in range(0, argHeight):
                for j in range(0, argWidth):
                    list[i][j] = argFlatList[counter]
                    counter += 1
        else:
            print("The list is not convertable to 2d")
        return list