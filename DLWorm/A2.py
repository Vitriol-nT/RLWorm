from Module import *
import math
import random
import numpy as np

#Neural
class MLP2H:
    def __init__(self, input_size, h1_size, h2_size, output_size, eta=0.01, epochs=50000):
        self.eta = eta
        self.epochs = epochs

        # Weights & biases
        self.W1 = np.random.rand(input_size, h1_size)
        self.b1 = np.zeros((1, h1_size))

        self.W2 = np.random.rand(h1_size, h2_size)
        self.b2 = np.zeros((1, h2_size))

        self.W3 = np.random.rand(h2_size, output_size)
        self.b3 = np.zeros((1, output_size))

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def d_sigmoid(self, x):
        return x * (1 - x)

    def forward(self, x):
        self.a1 = self.sigmoid(x @ self.W1 + self.b1)
        self.a2 = self.sigmoid(self.a1 @ self.W2 + self.b2)
        self.out = self.sigmoid(self.a2 @ self.W3 + self.b3)
        return self.out

    def backward(self, x, y):
        # Output layer
        err3 = (y - self.out) * self.d_sigmoid(self.out)

        # Hidden layer 2
        err2 = (err3 @ self.W3.T) * self.d_sigmoid(self.a2)

        # Hidden layer 1
        err1 = (err2 @ self.W2.T) * self.d_sigmoid(self.a1)

        # Update weights & biases
        self.W3 += self.a2.T @ err3 * self.eta
        self.b3 += np.sum(err3, axis=0, keepdims=True) * self.eta

        self.W2 += self.a1.T @ err2 * self.eta
        self.b2 += np.sum(err2, axis=0, keepdims=True) * self.eta

        self.W1 += x.T @ err1 * self.eta
        self.b1 += np.sum(err1, axis=0, keepdims=True) * self.eta

    def train(self, x, y):
        for _ in range(self.epochs):
            self.forward(x)
            self.backward(x, y)

    def predict(self, x):
        return self.forward(x)

class agent2:
    def __init__(self, W1, F1, F2):
        self.W1 = W1
        self.F1= F1
        self.F2 = F2
        self.Objective = 1
        self.End = False
        self.movement_array = []

