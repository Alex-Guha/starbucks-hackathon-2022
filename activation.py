import numpy as np
import math

# Sets any neuron output that is below 0 to 0
class Activation_ReLU:
	# Forward pass
	def forward(self, inputs, training):
		self.inputs = inputs
		self.output = np.maximum(0, inputs)
	# Gradient calculation
	def backward(self, dvalues):
		self.dinputs = dvalues.copy()
		self.dinputs[self.inputs <= 0] = 0
	# For model use
	def predictions(self, outputs):
		return outputs

class Activation_Softmax:
	# Forward pass
	def forward(self, inputs, training):
		self.inputs = inputs
		exp_values = np.exp(inputs - np.max(inputs, axis=1, keepdims=True))
		probabilities = exp_values / np.sum(exp_values, axis=1, keepdims=True)
		self.output = probabilities
	# Gradient calculation
	def backward(self, dvalues):
		self.dinputs = np.empty_like(dvalues)
		for index, (single_output, single_dvalues) in enumerate(zip(self.output, dvalues)):
			single_output = single_output.reshape(-1, 1)
			jacobian_matrix = np.diagflat(single_output) - np.dot(single_output, single_output.T)
			self.dinputs[index] = np.dot(jacobian_matrix, single_dvalues)
	# For model use
	def predictions(self, outputs):
		return np.argmax(outputs, axis=1)