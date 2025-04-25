import numpy as np

def sigmoid(x):
    return 1 / (1 + np.exp(-x))



class SimpleMLP:
    def __init__(self, N):
        self.N = N
        self.w1 = np.random.rand(N, N)
        self.b1 = np.zeros((1, N))
        self.w2 = np.random.rand(N, N)
        self.b2 = np.zeros((1, N))
        self.w3 = np.random.rand(N, 1)
        self.b3 = np.zeros((1, 1))

    def forward(self, x):
        self.z1 = sigmoid(np.dot(x, self.w1) + self.b1)
        self.z2 = sigmoid(np.dot(self.z1, self.w2) + self.b2)
        self.output = sigmoid(np.dot(self.z2, self.w3) + self.b3)
        return self.output

N = 4
mlp = SimpleMLP(N)
input_data = np.random.randint(0, 2, (1, N))
output = mlp.forward(input_data)

print("Input:", input_data)
print("Output:", output)
