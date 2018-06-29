

##########################################################
#                       Scaling                          #
##########################################################
def scale(argNum,argMin,argMax,scale_max=2,scale_min=0):
    return ((scale_max - scale_min)*((argNum-argMin)/(argMax-argMin)))+scale_min


min=0
max=9
num =9
print(scale(num,min,max,scale_max=2,scale_min=0))

##########################################################
#                       save net                         #
##########################################################
def wload_network_structure(file):
    # reading all the lines in the file
    lines = file.readlines()
    print(lines)
    parameters=[]
    for i in lines:
        temp=i.split("\n")
        parameters.append(temp[0])
    print(parameters)

    hidden_size=int(parameters[0])
    learning_rate=float(parameters[1])
    hidden_activation=str(parameters[2])
    out_activation=str(parameters[3])
    output_size=int(parameters[4])
    exploration=float(parameters[5])
    discount=int(parameters[6])

    return hidden_size, learning_rate, hidden_activation, out_activation, output_size, exploration, discount


from learner import *
from system_utility import *

sample_agent = agent(argId=1)
sample_agent.create_brain(argExploration=0.2, argDiscount=1, argLearning_rate=0.001, argHidden_size=50,
                   argHidden_activation='sigmoid', argOut_activation='linear',argOutputSize=5)


argWorldName='test'
out='Saved_Worlds'+'/world_'+str(argWorldName)

save_network_structure(out,argAgent=sample_agent)
hidden_size, learning_rate, hidden_activation, out_activation, output_size, exploration, discount= \
    wload_network_structure(open(out+"/brain.txt",'r'))
print(hidden_size, learning_rate, hidden_activation, out_activation, output_size, exploration, discount)
print(sample_agent.NN.output_layer)
sampleINput=[1,2,3,4,5,6,7,8,9,1,2,3,4,5,6,7,8,9,1,2,3,4,5,6,7,8,9,1,2]
sampleINput2=[1,2,3,4,5,4,7,2,9,1,1,3,4,5,6,7,8,9,1,2,3,4,5,6,7,8,9,1,2]
print(sample_agent.NN.input_size)
sample_agent.NN.forward_propagation(sampleINput)
print(sample_agent.NN.output_layer)
sample_agent.NN.forward_propagation(sampleINput2)
print(sample_agent.NN.output_layer)
sample_agent.NN.saveNetwork()
sample_agent.NN.loadNetwork()
sample_agent.NN.forward_propagation(sampleINput)
print(sample_agent.NN.output_layer)

sample_agent.NN.__del__()

print("FUCK1")
sample_agent2 = agent(argId=2)
sample_agent2.create_brain(argExploration=0.2, argDiscount=1, argLearning_rate=0.001, argHidden_size=50,
                   argHidden_activation='sigmoid', argOut_activation='linear',argOutputSize=5)
print("FUCK2")
sample_agent2.NN.loadNetwork()
print("FUCK3")
print(sample_agent2.NN.output_layer)
print("FUCK4")
sample_agent2.NN.forward_propagation(sampleINput)
print("FUCK5")
print(sample_agent2.NN.output_layer)
