import copy
import numpy as np
import network as network
import sys, os
import random

class controller():
    def __init__(self,argMode="train",argStepCost=-0.1):
        # the State of the player can be:
        #   1) "initialized"
        #   3) "progressing : selecting next action
        #   4) "waiting for the action"
        #   2) "arrived"
        self.state="initialized"
        # mode defines if the agent is "training" or "testing" or "developer"
        self.mode = argMode
        # counter of number of moves
        self.move_count = 0
        # cost of every action
        self.step_cost = argStepCost
        self.network_folder = None
        self.reward_Sharing=False
        self.previous_reward=0

    def set_network_folder(self,world_name):
        primaryDirectory = 'Saved_Worlds'
        outputDirect = primaryDirectory + '/world_' + str(world_name)
        agent_folder = str("meta_agent/")
        second_root = str(outputDirect)+'/tf_checkpoints/'
        final_root = str(second_root)+str(agent_folder)

        self.create_necessary_folders(primaryDirectory,outputDirect,second_root,final_root)
        self.network_folder=final_root

    def save_network(self):
        self.NN.saveNetwork(network_folder=self.network_folder)

    def create_necessary_folders(self, primaryDirectory, outputDirect, second_root, final_root):
        if not os.path.exists(primaryDirectory):
            print("creating The primary folder under " + primaryDirectory)
            os.makedirs(primaryDirectory)
            print(" The Folder for all saved worlds is created! \n The directory is : " + primaryDirectory)

        if not os.path.exists(outputDirect):
            print("creating The primary folder under " + outputDirect)
            os.makedirs(outputDirect)

        if not os.path.exists(second_root):
            print("creating The TF Checkpoint folder under " + second_root)
            os.makedirs(second_root)

        if not os.path.exists(final_root):
            print("creating The agent folder to save the network " + final_root)
            os.makedirs(final_root)

    def build_network(self, argboard_width, argboard_height, argExploration, argDiscount, argLearning_rate,
                      argHidden_size,argHidden_activation,argOut_activation, argOutputSize = 5,
                      create_load_mode = "create",argRewardSharing = False):
        # the primary neural network
        self.hidden_size = argHidden_size
        self.learning_rate = argLearning_rate
        self.hidden_activation = argHidden_activation
        self.out_activation = argOut_activation
        # the size of input and output layers
        self.reward_Sharing = argRewardSharing

        self.board_height = argboard_height
        self.board_width = argboard_width

        self.input_size = (self.board_height * self.board_width * 3) + 2
        print("Length of input: " + str(self.input_size))

        self.output_size = argOutputSize
        # defining the network
        if create_load_mode == "create":
            print("Creating the network for the centralized controller: ")
        else:
            print("Loading the network for the centralized controller: ")

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
        self.previous_input_layer = None

        # the function for selecting the next action
    def reset_meta_agent(self):
        # reseting the number of moves
        self.move_count = 0
        # setting back the state of the agent
        self.state = "initialized"
        # setting the location of the agents back to default values
        #set previous result to zero again
        self.previous_reward = 0


    def make_decision(self, argWGrid, argAgent,argAdditionalReward=None):
        # The portion of the grid that is observed by the agent currently, will be passed as argWGrid
        # This matrix is flattened to be used as the input layer of the Q-learning network
        current_agent = argAgent
        input_grid = argWGrid
        obstacle_board = self.get_obstacle_grid(argGrid=input_grid)
        agent_board = self.get_agent_grid(argGrid=input_grid,argAgent=current_agent)
        goal_board = self.get_goal_grid(argGrid=input_grid)
        self.input_layer = self.shape_input_layer(argObstacleList=obstacle_board, argGoalList=goal_board,
                                                  argAgnetList=agent_board,argAgent=current_agent)
        self.possible_moves, self.rejected_moves = self.get_possible_moves(argBoard=argWGrid,argAgent=current_agent)

        ####################
        #  print statement #
        ####################
        # print("Agent "+str(self.id)+" At position ("+str(self.positionX)+","+str(self.positionY)+")")
        # print("Observed grid: ")
        # print(observabl_grid)
        # print("List of Possible Moves")
        # print(self.possible_moves)
        ########################

        # the confidance is a scalar value between 0 and 1 which determins the certainty of the agent
        self.confidence = -1
        # if the mode is set at training/developer we use the following steps
        # note that this would only work if the state is not initialized
        # THis means no attempt at back prop if it is the first step
        if not (self.mode == "testing") and not (self.state == "initialized"):
            # we first obtain our previous input layer by copying the input of NN
            previous_input_layer = copy.copy(self.NN.input_layer)  # previous state (s0)
            previous_output_layer = copy.copy(self.NN.output_layer)  # previous expected reward (r1)

            # Obtain network's current output (a1)
            _, new_confidence, _ = self.get_best_move()

            # Calculate actual reward
            # if we had to use rewardsharing we will get the additional reward that is provided
            if self.reward_Sharing:
                reward = self.get_reward(additional_reward=argAdditionalReward)
            else:  # Otherwise we dont have any additional reward a.k.a = 0
                reward = self.get_reward()

            previous_output_layer[self.previous_index] = (self.discount * new_confidence) + reward
            # assigining the previous reward so that simulation uses that for reward sharing if needed
            self.previous_reward = reward

            # Backpropagate actual reward
            # print("backprop", self.id)
            self.NN.back_propagation(previous_output_layer, input_data=previous_input_layer)
        else:
            self.state = "Progressing"

        # training : this statement selects the move
        if not (self.mode == "testing"):
            # first we try a chance on a random move for exploration
            if random.uniform(0, 1) < self.exploration:
                index, move = self.get_random_move()
                output_layer = self.NN.forward_propagation(self.input_layer)
                self.confidence = output_layer[index]

                # Use network forward pass
            else:
                index, self.confidence, move = self.get_best_move()

        # testing
        else:
            # first we try a chance on a random move for exploration
            if random.uniform(0, 1) < 0.05:
                index, move = self.get_random_move()
                output_layer = self.NN.forward_propagation(self.input_layer)
                self.confidence = output_layer[index]
            else:
                # j ust simply forward pass to obtain the move
                index, self.confidence, move = self.get_best_move()

        # uodating counter values and previous index variable
        self.previous_index = index
        self.move_count += 1

        return move, self.confidence

    def get_reward(self, additional_reward=0):
        reward = self.step_cost + additional_reward
        return reward

    def perform_final_update(self, argreward):

        # we first obtain our previous input layer by copying the input of NN
        previous_input_layer = copy.copy(self.NN.input_layer)  # previous state (s0)
        previous_output_layer = copy.copy(self.NN.output_layer)  # previous expected reward (r1)

        # Obtain network's current output (a1)
        _, new_confidence, _ = self.get_best_move()

        # Calculate actual reward
        # if we had to use rewardsharing we will get the additional reward that is provided

        reward = argreward

        # previous_output_layer[self.previous_index] = (self.discount * new_confidence) + reward
        previous_output_layer[self.previous_index] = reward
        # assigining the previous reward so that simulation uses that for reward sharing if needed
        self.previous_reward = reward

        # Backpropagate actual reward
        # print("backprop", self.id)
        self.NN.back_propagation(previous_output_layer, input_data=previous_input_layer)

    # Using a forward pass, find the best move along with its index and confidence (= output node value)
    def get_best_move(self):
        # first we obtain the network's output using forward propogation given the input layer
        # print("forwardPass",self.id)
        network_rewards = copy.copy(self.NN.forward_propagation(self.input_layer))
        # Obtain the output nodes (rewards) corresponding with legal moves
        # this returns two list :
        #  1) the options =(moves, score) eg, [('up',5),('left',4)]
        #  2) the scores =[network output value] eg, [5,4]
        options,scores = self.get_move_options(argOutputlayer=network_rewards)
        # we call the function that finds the index, move and value given the options for the best move
        index, move, value =  self.get_max_value_move(argOptions=options,argScores=scores)
        # returning the result for selecting the best move
        return index, value, move

    # Function that returns a list of confidence
    def get_move_options(self,argOutputlayer):
        # We first take a copy of the output layer
        output=copy.copy(argOutputlayer)
        # Checking if the output layer's size matches what we specified
        if not (len(output) ==self.output_size):
            print("ERROR!!! OUTPUT LAYER DOES NOT HAVE ACCEPTABLE SIZE")
            print(len(output), self.output_size)
        # Placeholder variable that stores the score of the corresponding accepted move in a list
        scores=[]
        options=[]
        # we loop through all the possible moves
        for i in self.possible_moves:
            move_index = self.move_to_index(argMove=i[2])
            temp = (i[2], output[move_index])
            options.append(temp)
            scores.append(output[move_index])
        return options,scores

    # function for selecting move with max value , it returns the index of the move with the highest value
    def get_max_value_move(self,argOptions, argScores):
        if len(self.possible_moves) == 0:
            print("NO Possible Move is Available")
        max = np.max(argScores)
        for index in range(len(argOptions)):
            if argOptions[index][1] == max:
                # it returns the index of the item, the move and the value of the move
                return index, argOptions[index][0], argOptions[index][1]

    def get_random_move(self):
        randomChoice = random.choice(self.possible_moves)
        index = self.move_to_index(randomChoice[2])
        return index, randomChoice[2]

    # function that takes a move and returns it's corresponding index in output layer
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

    # function that takes an index of output layer and returns the corresponding move
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

    def try_move_up(self, argboard,argAgent):
        if (argAgent.positionY - 1) > -1:
            if argboard[argAgent.positionY - 1][ argAgent.positionX] == 0:
                # self.move_up(argAgent)
                # self.agents[index].positionY -=1
                return True, "empty", "up"
            elif argboard[argAgent.positionY - 1][ argAgent.positionX] > 99:
                return True, "goal", "up"
            elif argboard[argAgent.positionY - 1][ argAgent.positionX] < 0:
                return False, "obstacle", "up"
            else:
                return False, "occupied", "up"
        else:
            return False, "out_of_range", "up"

    def try_move_down(self, argboard,argAgent):
        height=len(argboard)
        if (argAgent.positionY + 1) < height:
            if argboard[argAgent.positionY + 1][ argAgent.positionX] == 0:
                # self.move_left(argAgent)
                # self.agents[index].positionY += 1
                return True, "empty", "down"
            elif argboard[argAgent.positionY + 1][argAgent.positionX] > 99:
                return True, "goal", "down"
            elif argboard[argAgent.positionY + 1][argAgent.positionX] < 0:
                return False, "obstacle", "down"
            else:
                return False, "occupied", "down"
        else:
            return False, "out_of_range", "down"

    def try_move_left(self, argboard,argAgent):
        if (argAgent.positionX - 1) > -1:
            if argboard[argAgent.positionY][ argAgent.positionX - 1] == 0:
                # self.move_left(argAgent)
                # self.agents[index].positionX -=1
                return True, "empty", "left"
            elif argboard[argAgent.positionY][ argAgent.positionX - 1] > 99:
                return True, "goal", "left"
            elif argboard[argAgent.positionY][ argAgent.positionX - 1] <0:
                return False, "obstacle", "left"
            else:
                return False, "occupied", "left"
        else:
            return False, "out_of_range", "left"

    def try_move_right(self, argboard,argAgent):
        width=len(argboard[0])
        if (argAgent.positionX + 1) < width:
            if argboard[argAgent.positionY][argAgent.positionX + 1] == 0:
                # self.move_right(argAgent)
                # self.agents[index].positionX +=1
                return True, "empty", "right"
            elif argboard[argAgent.positionY][argAgent.positionX + 1] > 99:
                return True, "goal", "right"
            elif argboard[argAgent.positionY][argAgent.positionX + 1] < 0:
                return False, "obstacle", "right"
            else:
                return False, "occupied", "right"
        else:
            return False, "out_of_range", "right"

    # evaluating each move
    def get_possible_moves(self,argBoard,argAgent):
        # check all 4 actions
        moves = []
        moves.append(self.try_move_up(argBoard,argAgent))
        moves.append(self.try_move_down(argBoard,argAgent))
        moves.append(self.try_move_left(argBoard,argAgent))
        moves.append(self.try_move_right(argBoard,argAgent))
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
        if len(acceptable)>=1:
            rejected.append(halt_move)
        else:
            acceptable.append(halt_move)

        # returning the acceptable and rejected moves
        if not (len(acceptable)+len(rejected)==self.output_size):
            print("ERROR! the sum of accepted and rejected are bigger than output layer size:\n")
            print("Output_layer: "+str(self.output_size)+" ,accepted: "+str(len(acceptable))+" ,rejected: "+str(len(rejected)))
        return acceptable, rejected


    def get_obstacle_grid(self,argGrid):
        new_list=[]
        for i in range(len(argGrid)):
            for j in range(len(argGrid[0])):
                if argGrid[i][j]<0:
                    new_list.append(1)
                else:
                    new_list.append(0)
        return new_list


    def get_goal_grid(self,argGrid):
        new_list = []
        for i in range(len(argGrid)):
            for j in range(len(argGrid[0])):
                if argGrid[i][j]>99:
                    new_list.append(1)
                else:
                    new_list.append(0)
        return new_list

    def get_agent_grid(self,argGrid,argAgent):
        new_list = []
        for i in range(len(argGrid)):
            for j in range(len(argGrid[0])):
                if argGrid[i][j]>0 and argGrid[i][j]<100:
                    if argGrid[i][j]==argAgent.id:
                        new_list.append(0)
                    else:
                        new_list.append(1)
                else:
                    new_list.append(0)
        return new_list

    def set_scale_parameters(self, argBoardWidth, argBoardHeight ,argScaleMin, argScaleMax):
        self.max_x_scale = argBoardWidth -1
        self.max_y_scale = argBoardHeight -1
        self.scale_max = argScaleMax
        self.scale_min = argScaleMin

    def scale(self,argNum, argMin, argMax, scale_max=2, scale_min=0):
        return ((scale_max - scale_min) * ((argNum - argMin) / (argMax - argMin))) + scale_min

    #function to shape the input layer
    def shape_input_layer(self,argObstacleList, argGoalList, argAgnetList,argAgent):
        #if the three generated lists are not in the same size theree should be an error
        if not (len(argAgnetList) == len(argGoalList)) or not (len(argGoalList) == len(argObstacleList)):
            print("ERROR! The Sizes of The Lists Does not Match")
        else:
            # If we had communication between agents we have to add two nods to the input layer

            counter = len(argObstacleList) + len(argGoalList) + len(argAgnetList) + 2

            result_list = []
            for i in argObstacleList:
                result_list.append(i)
            for j in argGoalList:
                result_list.append(j)
            for k in argAgnetList:
                result_list.append(k)

            # Adding the scaled Position X and position Y
            node_x= self.scale(argNum=argAgent.positionX,argMin=0, argMax=self.max_x_scale,
                               scale_max=self.scale_max,scale_min=self.scale_min)

            node_y= self.scale(argNum=argAgent.positionY,argMin=0, argMax=self.max_y_scale,
                               scale_max=self.scale_max,scale_min=self.scale_min)

            result_list.append(node_x)
            result_list.append(node_y)

            counter = len(argObstacleList) + len(argGoalList) + len(argAgnetList) + 2


            if not len(result_list) == counter:
                print("Failed to shape Input layer")
            else:
                return result_list


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

    def create_necessary_folders(self,primaryDirectory,outputDirect,second_root,final_root):
        if not os.path.exists(primaryDirectory):
            print("creating The primary folder under " + primaryDirectory)
            os.makedirs(primaryDirectory)
            print(" The Folder for all saved worlds is created! \n The directory is : " + primaryDirectory)

        if not os.path.exists(outputDirect):
            print("creating The primary folder under " + outputDirect)
            os.makedirs(outputDirect)

        if not os.path.exists(second_root):
            print("creating The TF Checkpoint folder under " + second_root)
            os.makedirs(second_root)

        if not os.path.exists(final_root):
            print("creating The agent folder to save the network " + final_root)
            os.makedirs(final_root)
