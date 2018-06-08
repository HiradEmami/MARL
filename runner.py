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
#TODO: The save and load functions need some serious update
#TODO: Reward Shaping
#TODO: Rewards
DEVELOPER_MODE = False

new_world = world(argCreationMode="load")
new_world.loadWolrd(argName="test")

if DEVELOPER_MODE:
    continue_key = float(raw_input("Enter 1 to continue: "))



for i in new_world.agents:
    i.create_brain(argExploration=0.2, argDiscount=1, argLearning_rate=0.001, argHidden_size=50,
                   argHidden_activation='sigmoid', argOut_activation='linear',argOutputSize=5)



num_simulations =1
for i in range(num_simulations):
    simulation_e = simulation(argWorld=new_world, argSteplimit=15, argDeveloperMode=True)
    num_move, new_world = simulation_e.run_one_simulation()
    print("Finished", num_move)

