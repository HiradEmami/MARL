import numpy as np
import tensorflow as tf
import os, time

os.environ['CUDA_VISIBLE_DEVICES'] = ''  # Disables GPU - likely more efficient when feeding one by one

# Possible activation functions
hid_act = {"linear": None, "sigmoid": tf.nn.sigmoid, "relu": tf.nn.relu}
out_act = {"linear": None, "softmax": tf.nn.softmax}


class NeuralNet():
    def __init__(self, input_size, hidden_size, output_size, learning_rate, hidden_activation, out_activation):
        print("\nTensorflow Network initializing...")

        self.session = tf.InteractiveSession()

        self.set_setting(hidden_activation, out_activation)

        self.learning_rate = learning_rate  # learningRate
        self.input_size = input_size  # size of input layer e.g. 64
        self.hidden_size = hidden_size  # size of Hidden Layer e.g. 50
        self.output_size = output_size  # size of outputlayer e.g. 60

        # Define the weights - uniformly randomly distributed
        self.hidden_weights = tf.Variable(
            tf.random_uniform([input_size, hidden_size], -0.5, 0.5))  # weights from input layer to hidden layer
        self.output_weights = tf.Variable(
            tf.random_uniform([hidden_size, output_size], -0.5, 0.5))  # weights from hidden layer to output layer

        # Define the biases - uniformly randomly distributed
        self.hidden_bias = tf.Variable(tf.random_uniform([hidden_size]))
        self.output_bias = tf.Variable(tf.random_uniform([output_size]))

        # Input and output layers - access when you know what you're doing
        self.input_layer = None
        self.output_layer = None

        # Backpropagation definitions
        self.X = tf.placeholder(tf.float32, [1, input_size])
        self.Y = tf.placeholder(tf.float32, [1, output_size])

        # Model definition
        self.logits = self.mlp(self.X)

        self.cost = tf.reduce_mean(tf.squared_difference(self.logits, self.Y))
        self.optimizer = self.optimizerFunc(learning_rate)
        self.train = self.optimizer.minimize(self.cost)

        # Initialize all TF variables
        self.session.run(tf.global_variables_initializer())

        # TensorFlow Writer & Saver
        self.writer = tf.summary.FileWriter("tf_summary", self.session.graph)
        self.writer.close()
        self.saver = tf.train.Saver()

        print("\nNetwork layout:\n  " + str(input_size) + "-" + str(hidden_size) + "-" + str(
            output_size) + "  with learning_rate=" + str(learning_rate) + "\n")


    def set_setting(self,hidden_activation,out_activation):
        self.optimizerFunc = tf.train.AdamOptimizer
        self.hidden_activation = hid_act[hidden_activation]
        self.output_activation = out_act[out_activation]
        self.activation = tf.nn.sigmoid  # Activation function for hidden layer - replace as needed


    # TensorFlow Graph representing the neural network
    def mlp(self, x):
        hidden_layer = tf.add(tf.matmul(x, self.hidden_weights), self.hidden_bias)
        if self.hidden_activation != None: hidden_layer = self.hidden_activation(
            hidden_layer)  # Apply activation function from initialized dict
        output_layer = tf.add(tf.matmul(hidden_layer, self.output_weights),
                              self.output_bias)  # Add or remove activation when needed
        if self.output_activation != None: self.output_activation(
            output_layer)  # Apply activation function from initialized dict
        return output_layer[0]

    # Computes output layer and stores it in 'self.outputLayer'
    def forward_propagation(self, input_data):
        # self.input_layer = tf.convert_to_tensor(np.array(input_data, np.float32).reshape(1, -1)) # Transform any array to tf [1, input_size]
        self.input_layer = np.array(input_data, np.float32).reshape(1, -1)
        self.output_layer = self.session.run(self.logits,
                                             feed_dict={self.X: self.input_layer})  # Compute the actual forward pass
        return self.output_layer

    # Updates weights using either the supplied input data, or the latest known if no input data is supplied
    def back_propagation(self, output_target, input_data=None):
        if input_data is not None:  # If backprop should take place with specific input data, then change the network's input layer
            self.input_layer = np.array(input_data, np.float32).reshape(1, -1)

        labels = np.array(output_target, np.float32).reshape(1, -1)  # Transform any array to np [1, input_size]
        _, cost = self.session.run([self.train, self.cost], feed_dict={self.X: self.input_layer, self.Y: labels})

    # print("tf error: " + str(cost))


    def saveNetwork(self, network_folder,checkpoint_name=None):
        # self.saver.save(self.session, './tf_checkpoints/' +str(network_folder)+ (
        # 'network.ckpt' if checkpoint_name == None else (str(checkpoint_name) + ".ckpt")))
        print(str(network_folder))
        self.saver.save(self.session, str(network_folder)+ (
            'network.ckpt' if checkpoint_name == None else (str(checkpoint_name) + ".ckpt")))

    def loadNetwork(self, network_folder,checkpoint_name=None):
        self.saver.restore(self.session, (
        tf.train.latest_checkpoint(str(network_folder)) if checkpoint_name == None else (
        './tf_checkpoints/' + str(checkpoint_name) + ".ckpt")))

        print("network loaded")

    # Remove the TF graph when object is deleted - leaks memory otherwise
    def __del__(self):
        tf.reset_default_graph()


# Network testing
if __name__ == '__main__':
    t_start = time.time()
    num_steps = 50

    nn = NeuralNet(2, 10, 1, learning_rate=.1,hidden_activation="sigmoid",out_activation="linear")

    # XOR
    x = [[0, 0], [0, 1], [1, 0], [1, 1]]
    target = [0, 1, 1, 0]

    for i in range(num_steps):
        for j in range(4):
            nn.forward_propagation(x[j])
            nn.back_propagation(target[j])

    for j in range(4):
        output = nn.forward_propagation(x[j])

        print("\ninput: \n  " + str(nn.input_layer[0]))
        # print("\nhidden: \n" + str(nn.hidden_layer.eval()))
        print("\n\noutput: \n  " + str(output))
        print("\ntarget: \n  " + str(np.array(target[j], np.float32).reshape(1, -1)[0]))
        print("\n")
    # print("\ninput to hidden: \n" + str(nn.hidden_weights.eval()))
    # print("\nhidden to output: \n" + str(nn.output_weights.eval()))
    # print("\nbiases: \n" + str(nn.hidden_bias.eval()))
    # print("\nbiases output: \n" + str(nn.output_bias.eval()))

    print("\n________________ DONE _______________\n    Running " + str(num_steps) + " steps took %.2f s" % (
    time.time() - t_start))