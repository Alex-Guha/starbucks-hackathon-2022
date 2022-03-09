import numpy as np
import math

# Normal Dense Layer
class Layer_Dense:
	# Initialize the weights as a random array of size inputs by neurons, and the biases as an array of zeros
	def __init__(self, n_inputs, n_neurons, weight_reg_l1=0, bias_reg_l1=0, weight_reg_l2=0, bias_reg_l2=0):
		self.weights = 0.10 * np.random.randn(n_inputs, n_neurons)
		self.biases = np.zeros((1, n_neurons))
		# Regularization initialization
		self.weight_reg_l1 = weight_reg_l1
		self.bias_reg_l1 = bias_reg_l1
		self.weight_reg_l2 = weight_reg_l2
		self.bias_reg_l2 = bias_reg_l2
	# Simple dot product of inputs and weights, then adding the biases
	def forward(self, inputs, training):
		self.inputs = inputs
		self.output = np.dot(inputs, self.weights) + self.biases
	# Calculate the gradients on weights and biases and regularization
	def backward(self, dvalues):
		self.dweights = np.dot(self.inputs.T, dvalues)
		self.dbiases = np.sum(dvalues, axis=0, keepdims=True)
		if self.weight_reg_l1 > 0:
			dL1 = np.ones_like(self.weights)
			dL1[self.weights < 0] = -1
			self.dweights += self.weight_reg_l1 * dL1
		if self.weight_reg_l2 > 0:
			self.dweights += 2 * self.weight_reg_l2 * self.weights
		if self.bias_reg_l1 > 0:
			dL1 = np.ones_like(self.biases)
			dL1[self.biases < 0] = -1
			self.dbiases += self.bias_reg_l1 * dL1
		if self.bias_reg_l2 > 0:
			self.dbiases += 2 * self.bias_reg_l2 * self.biases
		self.dinputs = np.dot(dvalues, self.weights.T)
	# Returns weights and biases for model
	def get_parameters(self):
		return self.weights, self.biases
	# Initializes weights and biases for model
	def set_parameters(self, weights, biases):
		self.weights = weights
		self.biases = biases

# Input Layer for model use
class Layer_Input:
	def forward(self, inputs, training):
		self.output = inputs

# Dropout helps mitigate overfitting by preventing memorization, not allowing the network to become too reliant on any particular neuron
class Layer_Dropout:
	def __init__(self, rate):
		self.rate = 1 - rate
	# Just sets some of the inputs to zero randomly
	def forward(self, inputs, training):
		self.inputs = inputs
		if not training:
			self.output = inputs.copy()
			return
		self.binary_mask = np.random.binomial(1, self.rate, size=inputs.shape) / self.rate
		self.output = inputs * self.binary_mask
	# Gradient calculation
	def backward(self, dvalues):
		self.dinputs = dvalues * self.binary_mask
