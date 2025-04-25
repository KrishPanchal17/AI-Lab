import numpy as np

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def sigmoid_derivative(x):
    return x * (1 - x)

class NeuralNetwork:
    def __init__(self, input_size, hidden1, hidden2, output_size, learning_rate):
        self.lr = learning_rate
        self.w1 = np.random.rand(input_size, hidden1)
        self.b1 = np.zeros((1, hidden1))
        self.w2 = np.random.rand(hidden1, hidden2)
        self.b2 = np.zeros((1, hidden2))
        self.w3 = np.random.rand(hidden2, output_size)
        self.b3 = np.zeros((1, output_size))

    def forward(self, X):
        self.z1 = sigmoid(np.dot(X, self.w1) + self.b1)
        self.z2 = sigmoid(np.dot(self.z1, self.w2) + self.b2)
        self.output = sigmoid(np.dot(self.z2, self.w3) + self.b3)
        return self.output

    def backward(self, X, y):
        output_error = y - self.output
        d_output = output_error * sigmoid_derivative(self.output)
        z2_error = d_output.dot(self.w3.T)
        d_z2 = z2_error * sigmoid_derivative(self.z2)
        z1_error = d_z2.dot(self.w2.T)
        d_z1 = z1_error * sigmoid_derivative(self.z1)
        self.w3 += self.z2.T.dot(d_output) * self.lr
        self.b3 += np.sum(d_output, axis=0, keepdims=True) * self.lr
        self.w2 += self.z1.T.dot(d_z2) * self.lr
        self.b2 += np.sum(d_z2, axis=0, keepdims=True) * self.lr
        self.w1 += X.T.dot(d_z1) * self.lr
        self.b1 += np.sum(d_z1, axis=0, keepdims=True) * self.lr

    def train(self, X, y, epochs=10000):
        for _ in range(epochs):
            self.forward(X)
            self.backward(X, y)


X = np.array([
    [0, 0],
    [0, 1],
    [1, 0],
    [1, 1]
])

y = np.array([[0], [1], [1], [0]])


nn = NeuralNetwork(input_size=2, hidden1=4, hidden2=4, output_size=1, learning_rate=0.1)


nn.train(X, y, epochs=10000)


predictions = nn.forward(X)
print("Predictions after training:")
print(np.round(predictions, 2))
