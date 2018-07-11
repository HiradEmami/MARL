import world as wd
from worldObject import *
import learner,os
from tkinter import *
import time,random


from worldObject import *
from learner import *
from world import *
from system_utility import *
from simulation import  *


def perform_move(world, argAgent, argMove):
    if argMove == "up":
        world.move_up(argPlayer=argAgent)

    elif argMove == "down":
        world.move_down(argPlayer=argAgent)

    elif argMove == "left":
        world.move_left(argPlayer=argAgent)

    elif argMove == "right":
        world.move_right(argPlayer=argAgent)






# Would save the world after training
SAVE_THE_SESSION = True

DEVELOPER_MODE = False      # Developer_mode controls huge prints and check to see if system is working correctly
PRINT_SIMULATION_DETAILS = False # Print_simulation_details prints more information about the simulation
PRINT_TEST_DETAILS = False
TRAINING_TESTING = "training"

COMMUNICATION = False
REWARD_SHARING = False

EPOCHES = 50
NUM_SIMULATION = 500
NUM_TEST = 100
STEP_LIMITS = 60

LOAD_CREATE = "load"
WORLD_NAME="test"

file_name = "test"
file_name = "world_" + file_name
primaryDirectory='Saved_Worlds'

path=primaryDirectory + "/" + file_name

new_world = world(argCreationMode=LOAD_CREATE)
new_world.loadWolrd(argName=WORLD_NAME,argRewardSharing=REWARD_SHARING,argCommunication=COMMUNICATION)

for i in new_world.agents:
    i.mode = "testing"

successful = 0
failed = 0
total_num_arrived = 0
total_num_failed = 0


test_simulation =  simulation_current = simulation(argWorld=new_world, argSteplimit= STEP_LIMITS,
                                  argDeveloperMode=DEVELOPER_MODE,argrewardSharing=REWARD_SHARING,
                                  argPRINT_DETAILS=PRINT_SIMULATION_DETAILS, argMode="test",
                                                   argVISUALIZATION=True)
num_move, argworld, result, num_arrived, num_failed = simulation_current.run_one_simulation()
total_num_arrived += num_arrived
total_num_failed += num_failed
if result == "successful":
    successful += 1
else:
    failed += 1
accuracy = (successful/1)*100.0
print("\nFinal Test Accuracy: " + str(accuracy) + "%")


