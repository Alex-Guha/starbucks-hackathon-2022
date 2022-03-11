import numpy as np
import math

class Accuracy:
	def calculate(self, predictions, y):
		comparisons = self.compare(predictions, y)
		accuracy = np.mean(comparisons)
		self.accumulated_sum += np.sum(comparisons)
		self.accumulated_count += len(comparisons)
		return accuracy
	def calculate_accumulated(self):
		accuracy = self.accumulated_sum / self.accumulated_count
		return accuracy
	def new_pass(self):
		self.accumulated_count = 0
		self.accumulated_sum = 0

class Accuracy_Categorical(Accuracy):
	def __init__(self, *, binary=False):
		self.binary = binary
	def init(self, y):
		pass
	def compare(self, predictions, y):
		if not self.binary and len(y.shape) == 2:
			y = np.argmax(y, axis=1)
		return predictions == y