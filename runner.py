

__author__='Hirad Emami Alagha - S3218139'

from worldObject import *
from learner import *
from world import *
from system_utility import *
from simulation import  *
from centralized_controller import *
from centralized_simulation import *
import math
import time


################################
#       Input of Variables       #
################################
LOAD_CREATE = "load"
WORLD_NAME='MORL_complex_7x7'
#WORLD_NAME = 'test_centralized'
TRAINING_TESTING = "training"
MARL_MODE = "decentralized"
#MARL_MODE = "centralized"

# Would save the world after training
SAVE_THE_SESSION = False
VISUALIZATION = False

def get_settings():
    if "baseline" in WORLD_NAME:
        return False,False,False,False
    elif "goal" in WORLD_NAME:
        return False,True,False,False
    elif "policy" in WORLD_NAME:
        return False,False,True,True
    elif "intention" in WORLD_NAME:
        return False,False,True,False
    elif "MORL" in WORLD_NAME:
        return True,False,False,False

MORL , GOAL_COMMUNICATION, COMMUNICATION, SHARED_POLICY = get_settings()

REWARD_SHARING = True
DEVELOPER_MODE = False      # Developer_mode controls huge prints and check to see if system is working correctly
PRINT_SIMULATION_DETAILS = False # Print_simulation_details prints more information about the simulation
PRINT_TEST_DETAILS = True

NUM_SIMULATION = 20000

EPOCHES = math.floor(0.05 * NUM_SIMULATION)
TRAINING_ACCURACY_RECORDER = 1000# number of simulations before one tick data is recorded

NUM_TEST = 100
STEP_LIMITS = 300
################################
#       End of Variables       #
################################

# The primary function to train the decentralized system
def decentralized_train():
    print("\nStarting Decentralized System:\n")
    # Loading the world and the agents
    new_world = world(argCreationMode=LOAD_CREATE)
    new_world.loadWolrd(argName=WORLD_NAME,argRewardSharing=REWARD_SHARING,argCommunication=COMMUNICATION,
                        argSharedPolicy=SHARED_POLICY,
                        argMORL=MORL,argGoalcommunication=GOAL_COMMUNICATION)
    training_accuracy = []
    testing_accuracy = []
    total_num_arrived = []
    total_num_failed = []
    num_successful= 0
    num_total = 0
    total_fail = 0

    for i in new_world.agents:
        i.set_total_agent_number(len(new_world.agents))

    if DEVELOPER_MODE:
        continue_key = float(raw_input("Enter 1 to continue: "))

    simulation_counter=0
    for i in range(NUM_SIMULATION):
        simulation_counter +=1
        num_total += 1
        # create a simulation session

        simulation_current = simulation(argWorld=new_world, argSteplimit= STEP_LIMITS,
                                  argDeveloperMode=DEVELOPER_MODE,argrewardSharing=REWARD_SHARING,
                                  argPRINT_DETAILS=PRINT_SIMULATION_DETAILS, argMode="train"
                                        ,argVISUALIZATION=VISUALIZATION
                                        ,argcommunication=COMMUNICATION
                                        ,argSharedPolicy=SHARED_POLICY,
                                        argMORL=MORL,argGoalCommunication=GOAL_COMMUNICATION)

        # getting some of the information back
        MoveCount , new_world, result, num_arrived, num_failed = simulation_current.run_one_simulation()

        if num_total == TRAINING_ACCURACY_RECORDER:
            acc = (num_successful / num_total) * 100
            training_accuracy.append(acc)
            num_total = 0
            num_successful = 0
            total_fail = 0

        else:
            if result == "successful":
                num_successful += 1
                print("success "+ str(num_successful) +", num_arrived, num_failed: "+str(num_arrived), str(num_failed)+
                      ", Move: "+str(MoveCount))

            else:
                total_fail +=1
                print("failed " + str(total_fail) + ", num_arrived, num_failed: " + str(num_arrived),
                      str(num_failed)+
                      ", Move: "+str(MoveCount))

        # print("In training the state of agent is " + new_world.agents[0].mode)
        if (i % EPOCHES)==0 and not i==0:
            print(result)
            progress = 100*(i/NUM_SIMULATION)
            print(str(progress)+"% Completed")
            test_accuracy, numArrived_agent,numFailed_agent = decentralized_test(argworld=new_world, argNumberofTest=NUM_TEST)
            testing_accuracy.append(test_accuracy)
            total_num_failed.append(numFailed_agent)
            total_num_arrived.append(numArrived_agent)
        # print("In training after the state of agent is "+new_world.agents[0].mode)

        if PRINT_SIMULATION_DETAILS:
            print("Finished", num_arrived ,num_failed , result)


    if SAVE_THE_SESSION:
        new_world.saveWorld(argWorldName=WORLD_NAME)
        for i in new_world.agents:
            i.save_network()



    print("\nTotal number of completed simulations: "+str(simulation_counter))
    print("\n Final test for the model")
    final_test_accuracy=decentralized_test(argworld=new_world, argNumberofTest=1)
    new_world.saveWorld(argWorldName=WORLD_NAME)
    testing_accuracy.append([100, final_test_accuracy])
    return testing_accuracy, training_accuracy

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
                                                           argVISUALIZATION=VISUALIZATION
                                     , argcommunication=COMMUNICATION,
                                     argSharedPolicy=SHARED_POLICY,
                                     argMORL=MORL, argGoalCommunication=GOAL_COMMUNICATION)
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
    return  accuracy, total_num_arrived, total_num_failed

def centralized_train():
    print("\nStarting Centralized System:\n")
    # Loading the world and the agents
    new_world = world(argCreationMode=LOAD_CREATE)
    new_world.loadWolrd(argName=WORLD_NAME,argRewardSharing=REWARD_SHARING,argCommunication=COMMUNICATION,
                        argCentralized=True)
    for i in new_world.agents:
        i.set_total_agent_number(len(new_world.agents))

    training_accuracy = []
    testing_accuracy = []
    num_successful = 0
    num_total = 0

    if DEVELOPER_MODE:
        continue_key = float(raw_input("Enter 1 to continue: "))

    simulation_counter=0
    for i in range(NUM_SIMULATION):
        simulation_counter +=1
        num_total += 1
        # create a simulation session

        simulation_current = centralized_simulation(argWorld=new_world, argSteplimit= STEP_LIMITS,
                                  argDeveloperMode=DEVELOPER_MODE,argrewardSharing=REWARD_SHARING,
                                  argPRINT_DETAILS=PRINT_SIMULATION_DETAILS, argMode="train"
                                        ,argVISUALIZATION=VISUALIZATION)
        # getting some of the information back
        num_move, new_world, result, num_arrived, num_failed = simulation_current.run_one_simulation()

        if num_total == TRAINING_ACCURACY_RECORDER:
            acc = (num_successful / num_total ) * 100
            training_accuracy.append(acc)
            num_total = 0
            num_successful = 0
        else:
            if result == "successful":
                num_successful += 1

        # print("In training the state of agent is " + new_world.agents[0].mode)
        if (i % EPOCHES)==0 and not i==0:
            print(result)
            progress = 100*(i/NUM_SIMULATION)
            print(str(progress)+"% Completed")
            test_accuracy = centralized_test(argworld=new_world, argNumberofTest=NUM_TEST)
            testing_accuracy.append([progress, test_accuracy])
        # print("In training after the state of agent is "+new_world.agents[0].mode)

        if PRINT_SIMULATION_DETAILS:
            print("Finished", num_move , num_arrived ,num_failed , result)


    if SAVE_THE_SESSION:
        new_world.saveWorld(argWorldName=WORLD_NAME)
        for i in new_world.agents:
            i.save_network()



    print("\nTotal number of completed simulations: "+str(simulation_counter))
    print("\n Final test for the model")
    final_test_accuracy=centralized_test(argworld=new_world, argNumberofTest=1)
    new_world.saveWorld(argWorldName=WORLD_NAME, argCentralized=True, argMetaAgent=new_world.centralized_meta_agent)
    testing_accuracy.append([100,final_test_accuracy])

    return testing_accuracy , training_accuracy

def centralized_test(argworld, argNumberofTest):
    # setting the mode to testing

    # print("In testing after change the state of agent is " + argworld.agents[0].mode)
    successful = 0
    failed = 0
    total_num_arrived = 0
    total_num_failed = 0

    argworld.centralized_meta_agent.mode = "testing"

    if PRINT_TEST_DETAILS:
        print("\nTesting ...")

    for i in range(argNumberofTest):

        test_simulation = centralized_simulation(argWorld=argworld, argSteplimit=STEP_LIMITS,
                                     argDeveloperMode=DEVELOPER_MODE, argrewardSharing=REWARD_SHARING,
                                     argPRINT_DETAILS=PRINT_SIMULATION_DETAILS, argMode="test",
                                     argVISUALIZATION=VISUALIZATION)
        num_move, argworld, result, num_arrived, num_failed = test_simulation.run_one_simulation()

        total_num_arrived += num_arrived
        total_num_failed += num_failed
        if result == "successful":
            successful += 1
            #print("success")
        else:
            failed += 1
            #print("fail")
    accuracy = (successful / argNumberofTest) * 100.0
    if PRINT_TEST_DETAILS:
        print("\n" + str(argNumberofTest) + " Completed!\nTotal successful simulations: "
              + str(successful) + "\nTotal failed simulations: " + str(
            failed) + "\nTotal number of agents that arrived: " +
              str(total_num_arrived) + "\nTotal number of lost agents: " + str(total_num_failed))
    print("\nFinal Test Accuracy: " + str(accuracy) + "%")
    argworld.centralized_meta_agent.mode ="training"
        # print("In testing after second change the state of agent is " + argworld.agents[0].mode)
    return accuracy

def save_results(final_results):
    #create the results folder if it is not there
    if not os.path.exists("Results/"):
        print("creating The primary folder under " + "Results/")
        os.makedirs("Results/")
        print(" The Folder for all saved worlds is created! \n The directory is : " + "Results/")

    #create communication stamp
    communication_var = None
    if COMMUNICATION:
        communication_var = "comm"
    else:
        communication_var = "NOcomm"
    #create the file name
    result_file_name = "Results/"+WORLD_NAME +"_"+ MARL_MODE +"_"+ communication_var +"_"+ str(NUM_SIMULATION)+".txt"
    #create the file
    file_1 = open(result_file_name, 'w')
    #save small world information
    file_1.write("World Name: " + WORLD_NAME+"\n")
    file_1.write("System type: " + MARL_MODE + "\n")
    file_1.write("Number of simulations: " + str(NUM_SIMULATION) + "\n")
    file_1.write("Communication: " + communication_var + "\n")
    file_1.write("_________________________________________\n")
    #saving the results
    file_1.write(str(0) + "% : " + str(0) + "%\n")
    # the primary loop for results
    for i in range(len(final_results)):
        # writing the values of cells
        if final_results[i][0] == 55.00000000000001:
            final_results[i][0] = 55.0
        file_1.write(str(final_results[i][0]) + "% : "+str(final_results[i][1])+"%")
        file_1.write("\n")
    # closing the file
    file_1.close()


if __name__ == '__main__':
    starting_time = time.time()
    print("Epoches: "+str(EPOCHES))
    if MARL_MODE == "decentralized":
       testing_accuracy,training_accuracy = decentralized_train()
    elif MARL_MODE == "centralized":
        testing_accuracy,training_accuracy = centralized_train()

    save_results(testing_accuracy)
    print("\nTotal progress :\n")
    print(testing_accuracy)
    print(training_accuracy)
    end_time= time.time() - starting_time

    print("\nTotal runtime:     \t{:.1f}".format(end_time) + " s")