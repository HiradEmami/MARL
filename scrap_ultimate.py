import  os


WORLD_NAME="test"
MARL_MODE = "decentralized"
COMMUNICATION = False
NUM_SIMULATION = 300

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
        file_1.write(str(final_results[i][0]) + "% : "+str(final_results[i][1])+"%")
        file_1.write("\n")
    # closing the file
    file_1.close()



P = []
A = 5
V = 52
S = [A,V]
P.append(S)
print(P)


restult_example = [[5.0, 100.0], [10.0, 100.0], [15.0, 100.0], [20.0, 94.0], [25.0, 100.0], [30.0, 100.0], [35.0, 92.0], [40.0, 100.0], [45.0, 100.0], [50.0, 87.0], [55.00000000000001, 100.0], [60.0, 99.0], [65.0, 97.0], [70.0, 98.0], [75.0, 98.0], [80.0, 100.0], [85.0, 99.0], [90.0, 100.0], [95.0, 80.0]]

save_results(restult_example)