from pip._vendor.distlib.compat import raw_input

__author__='Hirad Emami Alagha - S3218139'

from worldObject import *
from learner import *
from world import *
from system_utility import *
from simulation import  *

#TODO: Visualization should be completely fixed
#TODO: Check if Agents make decision and move properly
#TODO: Check if agnets have problem with moving out of index or wrong possible moves

#TODO: Reward Shaping
#TODO: Rewards

DEVELOPER_MODE = False
TRAINING_TESTING = "training"
REWARD_SHARING = True

EPOCHES = 10
NUM_SIMULATION = 100
STEP_LIMITS = 1000

LOAD_CREATE = "load"
WORLD_NAME="test"


def train():
    new_world = world(argCreationMode=LOAD_CREATE)
    new_world.loadWolrd(argName=WORLD_NAME,argRewardSharing=REWARD_SHARING)

    if DEVELOPER_MODE:
        continue_key = float(raw_input("Enter 1 to continue: "))

    for i in range(NUM_SIMULATION):
        simulation_e = simulation(argWorld=new_world, argSteplimit= STEP_LIMITS, argDeveloperMode=DEVELOPER_MODE)
        num_move, new_world = simulation_e.run_one_simulation()
        print("Finished", num_move)


if __name__ == '__main__':
    print("this")
    print(NUM_SIMULATION, DEVELOPER_MODE)
    train()