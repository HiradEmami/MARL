from pip._vendor.distlib.compat import raw_input

__author__='Hirad Emami Alagha - S3218139'

from worldObject import *
from learner import *
from world import *
from system_utility import *
from simulation import  *
from centralized_controller import *
from centralized_simulation import *
import math

################################
#       Input of Variables       #
################################
LOAD_CREATE = "load"
WORLD_NAME="test"
TRAINING_TESTING = "training"
MARL_MODE = "decentralized"

# Would save the world after training
SAVE_THE_SESSION = False
VISUALIZATION = False

COMMUNICATION = False
REWARD_SHARING = False

DEVELOPER_MODE = False      # Developer_mode controls huge prints and check to see if system is working correctly
PRINT_SIMULATION_DETAILS = False # Print_simulation_details prints more information about the simulation
PRINT_TEST_DETAILS = False

NUM_SIMULATION = 3000

EPOCHES = math.floor(0.05 * NUM_SIMULATION)

NUM_TEST = 100
STEP_LIMITS = 100
################################
#       End of Variables       #
################################

# The primary function to train the decentralized system
def decentralized_train():
    print("\nStarting Decentralized System:\n")
    # Loading the world and the agents
    new_world = world(argCreationMode=LOAD_CREATE)
    new_world.loadWolrd(argName=WORLD_NAME,argRewardSharing=REWARD_SHARING,argCommunication=COMMUNICATION)

    if DEVELOPER_MODE:
        continue_key = float(raw_input("Enter 1 to continue: "))

    simulation_counter=0
    for i in range(NUM_SIMULATION):
        simulation_counter +=1
        # create a simulation session

        simulation_current = simulation(argWorld=new_world, argSteplimit= STEP_LIMITS,
                                  argDeveloperMode=DEVELOPER_MODE,argrewardSharing=REWARD_SHARING,
                                  argPRINT_DETAILS=PRINT_SIMULATION_DETAILS, argMode="train"
                                        ,argVISUALIZATION=VISUALIZATION)
        # getting some of the information back
        num_move, new_world, result, num_arrived, num_failed = simulation_current.run_one_simulation()


        # print("In training the state of agent is " + new_world.agents[0].mode)
        if (i % EPOCHES)==0 and not i==0:
            print(result)
            print(str(100*(i/NUM_SIMULATION))+"% Completed")
            decentralized_test(argworld=new_world, argNumberofTest=NUM_TEST)
        # print("In training after the state of agent is "+new_world.agents[0].mode)

        if PRINT_SIMULATION_DETAILS:
            print("Finished", num_move , num_arrived ,num_failed , result)


    if SAVE_THE_SESSION:
        new_world.saveWorld(argWorldName=WORLD_NAME)
        for i in new_world.agents:
            i.save_network()



    print("\nTotal number of completed simulations: "+str(simulation_counter))
    print("\n Final test for the model")
    decentralized_test(argworld=new_world, argNumberofTest=1)
    new_world.saveWorld(argWorldName=WORLD_NAME)

def decentralized_test(argworld, argNumberofTest):
  #setting the mode to testing

    # print("In testing after change the state of agent is " + argworld.agents[0].mode)
    successful = 0
    failed = 0
    total_num_arrived = 0
    total_num_failed = 0
    for i in argworld.agents:
        i.mode="testing"

    if PRINT_TEST_DETAILS:
        print("\nTesting ...")

    for i in range(argNumberofTest):

        test_simulation = simulation(argWorld=argworld, argSteplimit= STEP_LIMITS,
                                  argDeveloperMode=DEVELOPER_MODE,argrewardSharing=REWARD_SHARING,
                                  argPRINT_DETAILS=PRINT_SIMULATION_DETAILS, argMode="test",
                                                           argVISUALIZATION=VISUALIZATION)
        num_move, argworld, result, num_arrived, num_failed = test_simulation.run_one_simulation()


        total_num_arrived += num_arrived
        total_num_failed += num_failed
        if result == "successful":
            successful += 1
        else:
            failed += 1
    accuracy = (successful/argNumberofTest)*100.0
    if PRINT_TEST_DETAILS:
        print("\n"+str(argNumberofTest)+" Completed!\nTotal successful simulations: "
            +str(successful)+"\nTotal failed simulations: "+str(failed)+"\nTotal number of agents that arrived: "+
            str(total_num_arrived)+ "\nTotal number of lost agents: "+str(total_num_failed))
    print("\nFinal Test Accuracy: "+str(accuracy)+"%")

    for i in argworld.agents:
        i.mode = "training"
    # print("In testing after second change the state of agent is " + argworld.agents[0].mode)

def centralized_train():
    print("\nStarting Centralized System:\n")

def centralized_test():
    print('This')

if __name__ == '__main__':
    print("Epoches: "+str(EPOCHES))
    if MARL_MODE == "decentralized":
        decentralized_train()
    elif MARL_MODE == "centralized":
        centralized_train()
