import numpy as np
import math
from accuracy import *
from activation import *
from layer import *
from loss import *
from model import *
from optimizer import *

from generator import *

import matplotlib.pyplot as plt
from matplotlib import style


X, y = load_data('data')

net = Model()

net.add(Layer_Dense(1, 64))
net.add(Activation_ReLU())
net.add(Layer_Dense(64, 64))
net.add(Activation_ReLU())
net.add(Layer_Dense(64, 1))
net.add(Activation_Linear())

net.set(loss=Loss_MeanSquaredError(), optimizer=Optimizer_Adam(learning_rate=0.005, decay=1e-3), accuracy=Accuracy_Regression())
net.finalize()
net.train(X, y, epochs=10000)


X_test, y_test = generate(1000)
output = net.forward(X_test)
plt.plot(X_test, y_test)
plt.plot(X_test, output)
plt.show()


# Essentially, in reality, this network is abusing flaws in python's random library, and picking up on it's patterns. However, that's only because we're generating artificial data. With real data, things would be different.
# As with any AI, data is the most important part, and also the most time consuming. Since we don't have access to the data that Starbucks would have, we had to generate our own.