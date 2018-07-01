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


DEVELOPER_MODE = False      # Developer_mode controls huge prints and check to see if system is working correctly
PRINT_SIMULATION_DETAILS = False # Print_simulation_details prints more information about the simulation
TRAINING_TESTING = "training"
REWARD_SHARING = True

EPOCHES = 50
NUM_SIMULATION = 1000
STEP_LIMITS = 50

LOAD_CREATE = "load"
WORLD_NAME="test"



def train():
    new_world = world(argCreationMode=LOAD_CREATE)
    new_world.loadWolrd(argName=WORLD_NAME,argRewardSharing=REWARD_SHARING)

    if DEVELOPER_MODE:
        continue_key = float(raw_input("Enter 1 to continue: "))

    for i in range(NUM_SIMULATION):
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


if __name__ == '__main__':
    print("this")
    print(NUM_SIMULATION, DEVELOPER_MODE)
    train()