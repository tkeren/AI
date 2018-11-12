import random
from PIL import Image
import numpy
from scipy import *
from numpy import *
import random
import mnist_loader



from scipy import ndimage as ndi
import numpy as np


class Network():
    def __init__(self, layers):
        # input: array representing the number of neurons in each layer the first representing the input
        self.layers = layers
        self.Nlayers = len(layers)
        # creates biases for layer 2 and 3 with normal distribution N(0,1)
        self.biases = [np.random.randn(y, 1) for y in layers[1:]]

        #creates matrix of weights between layer 1->2 and 2->3 with N(0,1)
        #[[[weight*30]*784][[weight*30]*10]]
        self.weights = [np.random.randn(y, x) for x, y in zip(layers[:-1], layers[1:])] #[(784,30)(30,10)]



    def newguess(self, filename):
        #converts image to grayscae array
        img = Image.open(filename).convert('L')
        imga = np.array(img)
        #flattn array
        temp = np.asarray(imga).reshape(-1)
        a = np.zeros((784, 1))
        #for each dark pixel get relative value from 0-1
        for x in range(len(temp)):
            if temp[x] < 255:
                a[x][0] = abs(temp[x] - 255.0) / 255.0
        #predict using current biases and weigths
        result = self.FeedForward(a)
        print (result)
        detected = np.argmax(result)
        print("The detected digit is: " + str(detected) + " with - " + str(result[detected] * 100.0) + "% accuracy")

    def FeedForward(self, a):
        #applies weights and biases to layers and uses the sigmoid function to output prediction
        group = zip(self.biases, self.weights)
        for g in group:
            b = g[0]
            w = g[1]
            a = sigmoid(np.dot(w,a)+b)
        return a

    def train(self, Tdata, periodNum, samples, LC, test_data = None):

        n = len(Tdata)
        for i in range(periodNum):
            #shuffle samples
            random.shuffle(Tdata)
            #create samples of sample sizes
            sample = [ Tdata[j:j+samples] for j in range(0, n, samples)]

            #gradients decent for each sample
            for s in sample:
                self.updateSample(s, LC)
            #if test_data, show evaluation score after every iteration
            if test_data:
                print("Epoch " + str(i) + ": " + str(self.evaluate(test_data)) + ' / '+ str(len(test_data)))

            else:
                print ("Epoch " + str(i) + " + complete")


    def evaluate(self, test_data):
        #return sum of correctly classified images
        sum = 0
        for t in test_data:
            x = t[0]
            y = t[1]
            add = np.argmax(self.FeedForward(x))
            if add == y:
                sum+=1

        return sum

    def updateSample(self, sample, LC):
        #using backpropagation to update the weights and biases of the network
        W = [np.zeros(w.shape) for w in self.weights]
        B = [np.zeros(b.shape) for b in self.biases]
        for x,y in sample:
            #gets partial derivative of cost function over biases and weights
            deltaW, deltaB = self.backProp(x, y)
            W = [nw+dw for nw, dw in zip(W, deltaW)]
            B = [nb + db for nb, db in zip(B, deltaB)]
        #minimizes cost function
        self.weights = [w-(LC/len(sample))*nw for w, nw in zip(self.weights, W)]
        self.biases = [b-(LC/len(sample))*nb for b, nb in zip(self.biases, B)]


    def backProp(self, x, y):
        deltaW = [np.zeros(w.shape) for w in self.weights]
        deltaB = [np.zeros(b.shape) for b in self.biases]
        activation = x
        activations = [x]
        storeZ = []
        for b, w in zip(self.biases, self.weights):
            z = np.dot(w, activation) + b
            storeZ.append(z)
            activation = sigmoid(z)
            activations.append(activation)

        d = self.delta(activations[-1], y) * dsigmoid(storeZ[-1])
        deltaB[-1] = d
        deltaW[-1] = np.dot(d, activations[-2].transpose())

        for l in range (2, self.Nlayers):
            z = storeZ[-l]
            ds = dsigmoid(z)
            d = np.dot(self.weights[-l+1].transpose(), d) * ds
            deltaB[-l] = d
            deltaW[-l] = np.dot(d, activations[-l-1].transpose())
        return (deltaW, deltaB)



    def delta(self, output, y):
        #error
        return(output-y)


def dsigmoid(x):
    #returns derivative of sigmoid
    return sigmoid(x)*(1-sigmoid(x))






def sigmoid(x):
    #returns sigmoid function
    return 1.0/(1.0 + np.exp(-x))





net = Network([784, 30, 10])
training_data, validation_data, test_data = mnist_loader.load_data_wrapper()

net.train(training_data, 30, 10, 3.0, test_data=test_data)

