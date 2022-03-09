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

# Literally just returns the values
class Activation_Linear:
	# Forward pass
	def forward(self, inputs, training):
		self.inputs = inputs
		self.output = inputs
	# Gradient calculation
	def backward(self, dvalues):
		self.dinputs = dvalues.copy()
	# For model use
	def predictions(self, outputs):
		return outputs