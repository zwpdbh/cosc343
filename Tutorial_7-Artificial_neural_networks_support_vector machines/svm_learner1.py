import pylab as pl
from sklearn import svm
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

# Create and train a support vector machine with traing error penalty C=1 and
# a linear (taking raw input as the feature) kernel
# C: linear, rbf, poly
svm_model = svm.SVC(gamma=35, kernel='rbf', C=20, verbose=True).fit(dset.x.T, dset.target_labels)

# Compute the output labels based on the training set...
labels = svm_model.predict(dset.x.T)
# ...and compare them to target labels...
e = labels != dset.target_labels
# ...and compute the training classificaiton error (as %)
e = e.sum()/ float(len(e)) * 100

# Compute the output labels based on the test set...
labels_test = svm_model.predict(dset.x_test.T)
# ...and compare them to test target labels...
e_test = labels_test != dset.target_labels_test
# ...and compute the test classificaiton error (as %)
e_test = e_test.sum()/ float(len(e_test)) * 100

print('\nTraining classification error: %f%%' % e)
print('Test classification error: %f%%' % e_test)

# Show visualisation of the training
dset.show_classification(model=svm_model)