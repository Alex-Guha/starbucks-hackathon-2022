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

class Accuracy_Regression(Accuracy):
	def __init__(self):
		self.precision = None
	def init(self, y, reinit=False):
		if self.precision is None or reinit:
			self.precision = np.std(y) / 250
	def compare(self, predictions, y):
		return np.absolute(predictions - y) < self.precision