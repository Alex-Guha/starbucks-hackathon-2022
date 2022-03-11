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


X, y = load_data('data_100')
X = np.array(X)
y = np.array(y)

X_val, y_val = generate(100, 110)
X_val = np.array(X)
y_val = np.array(y)

net = Model()

net.add(Layer_Dense(6, 64))
net.add(Activation_ReLU())
net.add(Layer_Dense(64, 64))
net.add(Activation_ReLU())
net.add(Layer_Dense(64, 24))
net.add(Activation_Softmax())

net.set(loss=Loss_CategoricalCrossEntropy(), optimizer=Optimizer_Adam(decay=5e-5), accuracy=Accuracy_Categorical())
net.finalize()
net.train(X, y, epochs=1, batch_size=300, print_every=10, validation_data=(X_val, y_val))
