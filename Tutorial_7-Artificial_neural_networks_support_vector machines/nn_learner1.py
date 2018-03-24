import pylab as pl
import numpy as np
import MLP
import datasets

__author__ = "Lech Szymanski"
__email__ = "lechszym@cs.otago.ac.nz"

#Close any open figures, and start a new one
pl.close('all')

# Import some data to play with
#dset = datasets.dataset_spiral()
dset = datasets.dataset_iris(attributes=2)
#dset = datasets.dataset_digits(n_class=10)
# Normalise the data so to values between 0 and 1
dset.normalise(minVal=0,maxVal=1)

# Create a multi-layer perceptron network, with 2-dim input, single hindden
# layer of 4 neurons and 3-neuron output.  Specify hidden neurons' activation
# function as logistic and the output neurons' activation function as 
# logistic sigmoid.  Set the variance of the parameter (weights and biases)
# initialisation to 0.1
nn_model = MLP.MLP(layer_sizes=np.array([2, 8, 3]),f_activation='tanh',f_output='logsig', sigma=0.2)

# Train the network on the sample dataset for 500 epochs using learning rate 
# of 0.1
nn_model.train(dset.x,dset.target_y,num_epochs=4000,alpha=0.1)

# Compute the output labels based on the training set...
labels = nn_model.output_labels(dset.x)
# ...and compare them to target labels...
e = labels != dset.target_labels
# ...and compute the training classificaiton error (as %)
e = e.sum()/ float(e.shape[1]) * 100

# Compute the output labels based on the test set...
labels_test = nn_model.output_labels(dset.x_test)
# ...and compare them to test target labels...
e_test = labels_test != dset.target_labels_test
# ...and compute the test classificaiton error (as %)
e_test = e_test.sum()/ float(e_test.shape[1]) * 100

print('Training classification error: %f%%' % e)
print('Test classification error: %f%%' % e_test)

# Show visualisation of the training
dset.show_classification(model=nn_model)