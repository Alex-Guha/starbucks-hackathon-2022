import numpy as np
import math, pickle, copy, time
from layer import *
from activation import *
from activation_loss import *
from optimizer import *
from accuracy import *
from loss import *
import matplotlib.pyplot as plt
from matplotlib import style

class Model:
	def __init__(self):
		self.layers = []
		self.plot_data = {'time':[], 'accuracy':[], 'loss':[], 'val_loss':[], 'val_acc':[], 'lr':[]}
		self.softmax_classifier_output = None
	def add(self, layer):
		self.layers.append(layer)
	def set(self, *, loss, optimizer, accuracy):
		if loss is not None:
			self.loss = loss
		if optimizer is not None:
			self.optimizer = optimizer
		if accuracy is not None:
			self.accuracy = accuracy
	def train(self, X, y, *, epochs=1, batch_size=None, print_every=1, validation_data=None):
		self.accuracy.init(y)
		train_steps = 1
		if validation_data is not None:
			val_steps = 1
			X_val, y_val = validation_data
		if batch_size is not None:
			train_steps = len(X) // batch_size
			if train_steps * batch_size < len(X):
				train_steps += 1
			if validation_data is not None:
				val_steps = len(X_val) // batch_size
				if val_steps * batch_size < len(X_val):
					val_steps += 1
		for epoch in range(1, epochs+1):
			self.loss.new_pass()
			self.accuracy.new_pass()
			for step in range(train_steps):
				if batch_size is None:
					batch_X = X
					batch_y = y
				else:
					batch_X = X[step*batch_size:(step+1)*batch_size]
					batch_y = y[step*batch_size:(step+1)*batch_size]
				output = self.forward(batch_X, training=True)
				data_loss, reg_loss = self.loss.calculate(output, batch_y, include_regularization=True)
				loss = data_loss + reg_loss
				predictions = self.output_layer_activation.predictions(output)
				accuracy = self.accuracy.calculate(predictions, batch_y)
				self.backward(output, batch_y)
				self.optimizer.pre_update_params()
				for layer in self.trainable_layers:
					self.optimizer.update_params(layer)
				self.optimizer.post_update_params()
				if not step % print_every or step == train_steps - 1:
					print(f'step: {step}, acc: {accuracy:.3f}, loss: {loss:.3f} (data_loss: {data_loss:.3f}, reg_loss: {reg_loss:.3f}), lr: {self.optimizer.current_learning_rate}')
					self.plot_data['time'].append(time.time())
					self.plot_data['accuracy'].append(accuracy)
					self.plot_data['loss'].append(loss)
					self.plot_data['lr'].append(self.optimizer.current_learning_rate)
					if validation_data is not None:
						val_loss, val_acc = self.evaluate(*validation_data, batch_size=batch_size)
						self.plot_data['val_acc'].append(val_acc)
						self.plot_data['val_loss'].append(val_loss)
			epoch_data_loss, epoch_reg_loss = self.loss.calculate_accumulated(include_regularization=True)
			epoch_loss = epoch_data_loss + epoch_reg_loss
			epoch_accuracy = self.accuracy.calculate_accumulated()
			print(f'training, epoch: {epoch}, acc: {epoch_accuracy:.3f}, loss: {epoch_loss:.3f} (data_loss: {epoch_data_loss:.3f}, reg_loss: {epoch_reg_loss:.3f}), lr: {self.optimizer.current_learning_rate}')
		if validation_data is not None:
			self.plot()
	# Validate model during training
	def evaluate(self, X_val, y_val, *, batch_size=None):
		val_steps = 1
		if batch_size is not None:
			val_steps = len(X_val) // batch_size
			if val_steps * batch_size < len(X_val):
				val_steps += 1
		self.loss.new_pass()
		self.accuracy.new_pass()
		for step in range(val_steps):
			if batch_size is None:
				batch_X = X_val
				batch_y = y_val
			else:
				batch_X = X_val[step*batch_size:(step+1)*batch_size]
				batch_y = y_val[step*batch_size:(step+1)*batch_size]
			output = self.forward(batch_X, training=False)
			self.loss.calculate(output, batch_y)
			predictions = self.output_layer_activation.predictions(output)
			self.accuracy.calculate(predictions, batch_y)
		val_loss = self.loss.calculate_accumulated()
		val_acc = self.accuracy.calculate_accumulated()
		print(f'validation, acc: {val_acc:.3f}, loss: {val_loss:.3f}')
		return val_loss, val_acc
	# Predict on new data, outside of training
	'''
	Using this with:
	confidences = model.predict(X)
	predictions = model.output_layer_activation.predictions(confidences)
	'''
	def predict(self, X, *, batch_size=None):
		prediction_steps = 1
		if batch_size is not None:
			prediction_steps = len(X) // batch_size
			if prediction_steps * batch_size < len(X):
				prediction_steps += 1
		output = []
		for step in range(prediction_steps):
			if batch_size is None:
				batch_X = X
			else:
				batch_X = X[step*batch_size:(step+1)*batch_size]
			batch_output = self.forward(batch_X, training=False)
			output.append(batch_output)
		return np.vstack(output)
	# Plot the results of training
	def plot(self):
		style.use("ggplot")
		fig = plt.figure()
		ax1 = plt.subplot2grid((3,1), (0,0))
		ax2 = plt.subplot2grid((3,1), (1,0), sharex=ax1)
		ax3 = plt.subplot2grid((3,1), (2,0), sharex=ax1)
		ax1.plot(self.plot_data['time'], self.plot_data['accuracy'], label='acc')
		ax1.plot(self.plot_data['time'], self.plot_data['val_acc'], label='val_acc')
		ax1.legend(loc=2)
		ax2.plot(self.plot_data['time'], self.plot_data['loss'], label='loss')
		ax2.plot(self.plot_data['time'], self.plot_data['val_loss'], label='val_loss')
		ax2.legend(loc=2)
		ax3.plot(self.plot_data['time'], self.plot_data['lr'], label='learning_rate')
		ax3.legend(loc=2)
		plt.show()
	def finalize(self):
		self.input_layer = Layer_Input()
		layer_count = len(self.layers)
		self.trainable_layers = []
		for i in range(layer_count):
			if i == 0:
				self.layers[i].prev = self.input_layer
				self.layers[i].next = self.layers[i+1]
			elif i < layer_count - 1:
				self.layers[i].prev = self.layers[i-1]
				self.layers[i].next = self.layers[i+1]
			else:
				self.layers[i].prev = self.layers[i-1]
				self.layers[i].next = self.loss
				self.output_layer_activation = self.layers[i]
			if hasattr(self.layers[i], 'weights'):
				self.trainable_layers.append(self.layers[i])
		if self.loss is not None:
			self.loss.remember_trainable_layers(self.trainable_layers)
		if isinstance(self.layers[-1], Activation_Softmax) and isinstance(self.loss, Loss_CategoricalCrossEntropy):
			self.softmax_classifier_output = Activation_Softmax_Loss_CategoricalCrossEntropy()
	def forward(self, X, training):
		self.input_layer.forward(X, training)
		for layer in self.layers:
			layer.forward(layer.prev.output, training)
		return layer.output
	def backward(self, output, y):
		if self.softmax_classifier_output is not None:
			self.softmax_classifier_output.backward(output, y)
			self.layers[-1].dinputs = self.softmax_classifier_output.dinputs
			for layer in reversed(self.layers[:-1]):
				layer.backward(layer.next.dinputs)
			return
		self.loss.backward(output, y)
		for layer in reversed(self.layers):
			layer.backward(layer.next.dinputs)
	# Returns parameters - array of tuple array of weight array and array of biases. The weight array contains an array of each individual neuron's weights [layer1(weights[neuron1[], neuron2[], ..., neuron64[]], [biases[neuron1, neuron2, ..., neuron64]]), layer2([weights],[[biases]])]
	def get_parameters(self):
		parameters = []
		for layer in self.trainable_layers:
			parameters.append(layer.get_parameters())
		return parameters
	# Initialize a model with saved parameters
	def set_parameters(self, parameters):
		for parameter_set, layer in zip(parameters, self.trainable_layers):
			layer.set_parameters(*parameter_set)
	# Saves weights and biases to a file
	def save_parameters(self, path):
		with open(path, 'wb') as f:
			pickle.dump(self.get_parameters(), f)
	# Load parameters from a file
	def load_parameters(self, path):
		with open(path, 'rb') as f:
			self.set_parameters(pickle.load(f))
	# Save the model for further training
	def save(self, path):
		model = copy.deepcopy(self)
		model.loss.new_pass()
		model.accuracy.new_pass()
		model.input_layer.__dict__.pop('output', None)
		model.loss.__dict__.pop('dinputs', None)
		for layer in model.layers:
			for property in ['inputs', 'output', 'dinputs', 'dweights', 'dbiases']:
				layer.__dict__.pop(property, None)
		with open(path, 'wb') as f:
			pickle.dump(model, f)
	# Load a saved model from a file
	@staticmethod
	def load(path):
		with open(path, 'rb') as f:
			model = pickle.load(f)
		return model