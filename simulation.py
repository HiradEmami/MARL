from learner import *
from world import *
from worldObject import *
from copy import copy
from shared_policy_brain import *
from pip._vendor.distlib.compat import raw_input
# TODO: self.PrepareCommunication should check if it is true, if so for all agents use the function to set communication


WIN_REWARD = 1.0
LOSE_REWARD = - 1.0
VISUALIZATION_FOLDER = 'test'
RANDOMIZATION = True

class simulation():
    def __init__(self,argWorld,argSteplimit,argDeveloperMode=False,argrewardSharing=False,argPRINT_DETAILS=False,
                 argMode="train",argVISUALIZATION=False,argcommunication = False,argSharedPolicy=False):
        self.world = argWorld
        #taking a copy of the starting board
        self.starting_board = self.copy_board(self.world.board)
        self.developerMode=argDeveloperMode
        self.print_details =argPRINT_DETAILS
        self.stepLimit=argSteplimit
        self.rewardSharing=argrewardSharing
        self.previous_collected_rewards=[]
        # placeholder to indicate if it is the first move that agents are taking
        self.first_move = True
        self.mode = argMode
        self.visualization=argVISUALIZATION
        self.communication = argcommunication
        self.shared_policy = argSharedPolicy


    #function to reset the grid and reset player information
    def reset_settings(self):
        if self.print_details:
            print("reseting")
            print("\nstarting board")
            self.print_boards(self.starting_board)
            print("\nworld board after simulation")
            self.print_boards(self.world.board)

        self.world.board = self.copy_board(self.starting_board)

        if  self.print_details:
            print("\nafter reset")
            self.print_boards(self.world.board)

        for i in range(len(self.world.agents)):
            self.world.agents[i].reset_agent()

        for j in range(len(self.world.goals)):
            self.world.goals[j].reset_goal()

        # placeholder to indicate if it is the first move that agents are taking
        self.first_move = True



    def run_one_simulation(self):
        # If print_details is set to True print some statements
        if self.print_details:
            print("\n###############################")
            print("#   Starting a new simulation #")
            print("###############################\n")

        num_steps=0
        simulation_state = "running_simulation"

        end_statement = "failed"
        if self.mode == "test" and RANDOMIZATION:
            self.world.test_randomization_prepration()
        while not(simulation_state== "finished"):

            remain=self.number_remaining_agents()

            if num_steps>=self.stepLimit:
                # If print_details is set to True print some statements
                if self.print_details:
                    print("Step Limit Reached!")
                    print("Number of remaining Agents: "+str(remain))
                    print("The Number of steps rich its limits\n# Performed Moves: "+str(num_steps)+
                          "\n# step limits: "+str(self.stepLimit))

                simulation_state="finished"

            elif remain == 0:
                # If print_details is set to True print some statements
                if self.print_details:
                    print("All agents arrived to their destination")
                    print("Number of remaining Agents: "+str(remain))
                simulation_state = "finished"

            else:
                self.do_one_step()
                num_steps += 1
                # If developermode is set to True , print information adn wait for user's input to continue
                if self.visualization:
                    continue_key = float(raw_input("Enter 1 to continue:"))
                    self.world.saveWorld(argWorldName=VISUALIZATION_FOLDER)
                if self.developerMode:
                    print(num_steps, self.stepLimit, simulation_state)
                    continue_key = float(raw_input("Enter 1 to continue:"))
        # If print_details is set to True print some statements
        if self.print_details:
            print("\n")
            print("#   Simulation Completed!   #")
            print("\n")
            print("Resetting simulation!")

        #evaluate the performance
        if not self.shared_policy:
            result, num_arrived, num_failed = self.evaluate_performance()
        else:
            result, num_arrived, num_failed = self.evaluate_performance_shared_policy()
        # Once the simulation is over, call to reset the world and agents
        self.reset_settings()

        # at the end return number of performed steps, updated world ,
        return num_steps , self.world , result, num_arrived, num_failed

    def evaluate_performance(self):
        num_failed=0
        num_arrived =0
        reward = []

        for i in self.world.agents:
            #updating the reward
            if i.state == "arrived":
                num_arrived +=1
                if self.mode == "train":
                    if not self.communication:
                        i.perform_final_update(argreward_1=WIN_REWARD)
                    else:
                        if i.arrived_at_goal == 1:
                            i.perform_final_update(argreward_1=WIN_REWARD,argreward_2=0)
                        elif i.arrived_at_goal == 2:
                            i.perform_final_update(argreward_1=0,argreward_2=WIN_REWARD)
                reward.append(WIN_REWARD)
            else:
                num_failed +=1
                if self.mode == "train":
                    if not self.communication:
                        i.perform_final_update(argreward_1=LOSE_REWARD)
                    else:
                        if i.arrived_at_goal == 1:
                            i.perform_final_update(argreward_1=LOSE_REWARD,argreward_2=0)
                        elif i.arrived_at_goal == 2:
                            i.perform_final_update(argreward_1=0,argreward_2=LOSE_REWARD)
                reward.append(LOSE_REWARD)

        # result can be success or fail
        result = None

        if num_arrived == len(reward):
            result = "successful"

        else:
            result = "fail"


        return result, num_arrived , num_failed

    def evaluate_performance_shared_policy(self):
        num_failed=0
        num_arrived =0
        reward = []
        added_reward_1 = 0
        added_reward_2 = 0
        for i in self.world.agents:
            #updating the reward
            if i.state == "arrived":
                num_arrived +=1
                if self.mode == "train":
                    if self.communication:
                        if i.arrived_at_goal == 1:
                            added_reward_1 += 0.1
                        elif i.arrived_at_goal == 2:
                            added_reward_2 += 0.1
                reward.append(WIN_REWARD)
            else:
                num_failed +=1
                added_reward_1 -= 0.1
                added_reward_2 -= 0.1
                reward.append(LOSE_REWARD)

        # result can be success or fail
        result = None

        if num_arrived == len(reward):
            result = "successful"
            if self.mode == "train":
                if not self.communication:
                    self.world.shared_policy_brain.perform_final_update(argreward_1=WIN_REWARD)
                else:
                    self.world.shared_policy_brain.perform_final_update(argreward_1=WIN_REWARD+added_reward_1,
                                                                        argreward_2=WIN_REWARD+added_reward_2)
        else:
            result = "fail"
            if self.mode == "train":
                if not self.communication:
                    self.world.shared_policy_brain.perform_final_update(argreward_1=LOSE_REWARD)
                else:
                    self.world.shared_policy_brain.perform_final_update(argreward_1=LOSE_REWARD+added_reward_1,
                                                                        argreward_2=LOSE_REWARD+added_reward_2)


        return result, num_arrived , num_failed
        

    # Function that connects the decision that agents make to the functions of performing and executing the actions
    def perform_move(self,argAgent,argMove):
        if argMove == "up":
            self.world.move_up(argPlayer=argAgent)
            if self.developerMode:
                print(self.world.board)
        elif argMove == "down":
            self.world.move_down(argPlayer=argAgent)
            if self.developerMode:
                print(self.world.board)
        elif argMove == "left":
            self.world.move_left(argPlayer=argAgent)
            if self.developerMode:
                print(self.world.board)
        elif argMove == "right":
            self.world.move_right(argPlayer=argAgent)
            if self.developerMode:
                print(self.world.board)
        elif argMove == "halt":
            if self.developerMode:
                print("the Move was Halt")

        if self.developerMode:
            self.world.saveWorld('test')

    def shared_update_agent_info(self,mainAgent, info):
        mainAgent.target_goal=info[0]
        mainAgent.communicate_target=info[1]
        mainAgent.communicate_goal_agents=info[2]
        mainAgent.total_agent=info[3]
        mainAgent.arrived_at_goal=info[4]
        mainAgent.previous_goal=info[5]
        return mainAgent

    # Function that makes all the agents that are not arrived to perform one action
    def do_one_step(self):
        self.prepare_communication()
        if (self.rewardSharing) and not(self.first_move):
            self.set_previous_rewards()
            for i in self.world.agents:
                if not  (i.state=="arrived"):
                    additional_reward= self.get_additional_reward(i.id)
                    if not self.shared_policy:
                        move, confidence = i.make_decision(argWGrid=self.world.board,argAdditionalReward=additional_reward)
                    else:
                        move, confidence, new_info = self.world.shared_policy_brain.shared_make_decision(argWGrid=self.world.board,
                                                           argAdditionalReward=additional_reward,argAgent=i)
                        i = self.shared_update_agent_info(mainAgent=i,info=new_info)
                    self.perform_move(argAgent=i,argMove=move)

        elif (self.rewardSharing) and (self.first_move):
            self.first_move = False
            for i in self.world.agents:
                 if not (i.state == "arrived"):
                    additional_reward =0
                    if not self.shared_policy:
                        move, confidence = i.make_decision(argWGrid=self.world.board,argAdditionalReward=additional_reward)
                    else:
                        move, confidence, new_info = self.world.shared_policy_brain.shared_make_decision(argWGrid=self.world.board,
                                                           argAdditionalReward=additional_reward,argAgent=i)
                        i = self.shared_update_agent_info(mainAgent=i,info=new_info)
                    self.perform_move(argAgent=i, argMove=move)
        else:
            for i in self.world.agents:
                if not (i.state == "arrived"):
                    if not self.shared_policy:
                        move, confidence = i.make_decision(argWGrid=self.world.board)
                    else:
                        move, confidence, new_info = self.world.shared_policy_brain.shared_make_decision(
                            argWGrid=self.world.board,
                            argAgent=i)
                        i = self.shared_update_agent_info(mainAgent=i, info=new_info)
                    #continue_key = float(raw_input("Enter 1 to continue:"))
                    self.perform_move(argAgent=i, argMove=move)
                    #print(move, i.positionX, i.positionY )

    def prepare_communication(self):
        if self.communication:
            targets = self.count_target_goals()
            goal_agent = self.count_agents_in_goal()
            for i in self.world.agents:
                i.set_communication_lists(argGoal_agents=goal_agent,argTarget=targets)


    # Function that counts how many agents are going to a goal
    def count_target_goals(self):
        goal_1 = 0
        goal_2 = 0
        for i in self.world.agents:
            if i.target_goal == 1:
                goal_1 += 1
            elif i.target_goal == 2:
                goal_2 += 1
        return [goal_1 , goal_2]

    def count_agents_in_goal(self):
        result = []
        for i in self.world.goals:
            result.append(i.num_agent)
        return result

    # The function for counting the number of remaining agents on the board
    def number_remaining_agents(self):
        count=0
        for i in self.world.agents:
            if not (i.state=="arrived"):
                count +=1
        if self.developerMode:
            print("Number of remaining agents:"+str(count))
        return count

    # Function to make a copy of the world's grid
    def copy_board(self,argboard):
        new_list=[]
        for i in range(len(argboard)):
            new_row=[]
            for j in range(len(argboard[0])):
                new_row.append(argboard[i][j])
            new_list.append(new_row)
        return new_list

    # Function to print the lists like a board
    def print_boards(self,list):
        for i in list:
            print(i)

    # Function that creates the list of previous rewards for reward sharing
    def set_previous_rewards(self):
        # Resetting the list to be empty again
        self.previous_collected_rewards =[]
        # For all the agents of the world append their previous reward to the list
        for i in self.world.agents:
            self.previous_collected_rewards.append(i.previous_reward)

        if self.developerMode:
            print(self.previous_collected_rewards,self.first_move)

    def get_additional_reward(self,agentID):
        agentNum = agentID - 1
        sum = 0
        for i in range(len(self.previous_collected_rewards)):
            if not (i == agentNum):
                sum += self.previous_collected_rewards[i]
        return sum / (len(self.previous_collected_rewards) - 1)

    def get_score(self):
        return 0