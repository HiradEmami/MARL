from pip._vendor.distlib.compat import raw_input

__author__='Hirad Emami Alagha - S3218139'

from worldObject import *
from learner import *
from world import *
from system_utility import *
from simulation import  *

#TODO: Visualization should be completely fixed
#TODO: Reward Shaping
#TODO: Rewards

SAVE_THE_SESSION = False

DEVELOPER_MODE = False      # Developer_mode controls huge prints and check to see if system is working correctly
PRINT_SIMULATION_DETAILS = False # Print_simulation_details prints more information about the simulation
TRAINING_TESTING = "training"

COMMUNICATION = False
REWARD_SHARING = False

EPOCHES = 50
NUM_SIMULATION = 20000
STEP_LIMITS = 60

LOAD_CREATE = "load"
WORLD_NAME="test"



def train():
    new_world = world(argCreationMode=LOAD_CREATE)
    new_world.loadWolrd(argName=WORLD_NAME,argRewardSharing=REWARD_SHARING,argCommunication=COMMUNICATION)

    if DEVELOPER_MODE:
        continue_key = float(raw_input("Enter 1 to continue: "))
    counter=0
    for i in range(NUM_SIMULATION):
        counter +=1
        # create a simulation session
        simulation_current = simulation(argWorld=new_world, argSteplimit= STEP_LIMITS,
                                  argDeveloperMode=DEVELOPER_MODE,argrewardSharing=REWARD_SHARING,
                                  argPRINT_DETAILS=PRINT_SIMULATION_DETAILS)
        # getting some of the information back
        num_move, new_world = simulation_current.run_one_simulation()

        if (i % EPOCHES)==0:
            print(str(100*(i/NUM_SIMULATION))+"% Completed")

        if PRINT_SIMULATION_DETAILS:
            print("Finished", num_move)

    if SAVE_THE_SESSION:
        new_world.saveWorld(argWorldName=WORLD_NAME)

    print("\nTotal number of completed simulations: "+str(counter))
if __name__ == '__main__':
    print("this")
    print(NUM_SIMULATION, DEVELOPER_MODE)
    train()