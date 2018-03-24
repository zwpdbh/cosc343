#import pylab as pl
import matplotlib.pyplot as pl

import numpy as np
from scipy import randn, optimize  

#First hypothesis function - a line that takes two parameters
def f1(x, w1, w2):
    return w1/x + w2 + 100

#Second hypotheis function - a quadratic that takes three parameters
def f2(x, w1, w2, w3):
    return w1/(x*x) + w2/x + w3

# def f2(x, w1, w2, w3):
# 	return w1 + w2/x + w3*log(x)

# My own guess
def f3(x, a, b, c):
    return a*x*x*x + b*x*x + c*x


#Define a uniformly spaced set of x values (n in total)
n=20
x = np.linspace(1, 20, n)

#Define a set of corresponding y values, according to a quadratic function function
# w1_true=2; w2_true=1; w3_true=4   #True parameters of the function
# y_tilde=w1_true*x*x+w2_true*x+w3_true;  #True output of the function



#add some Gaussian noise to each value of the true output
# y_with_noise=y_tilde+randn(n)

#Fraction of data used for training - 0.8 corresponds to 80% of the data
#being used for train set and 20% for test set
# pTrain = 0.8;

#Create a random permutation of data sample indexes
# I = np.random.permutation(n);
#Split the indexes into the training and testing indexes
# Itrain = I[1:np.floor(pTrain*n)];
# Itest = I[np.floor(pTrain*n)+1:n];
#Select training and test sets
xtrain=np.linspace(1, 20, n)
ytrain = np.loadtxt("training_for_depth.txt")            
# xtrain = x[Itrain]                                                  # ? how to get array of data based on another two array
# ytrain = y_with_noise[Itrain]
# xtest = x[Itest]
# ytest = y_with_noise[Itest]
xtest =np.linspace(1, 20, n)
ytest = np.loadtxt("testing_for_depth.txt")

#Use scipy's curve_fit method to fit data to two different hypothesis
#functions.  The first arguemtn is the hypothesis function, then
#input data and observed output.  The [0] at the end of the funciton instructs
#python just to return the first element of the multi-variable return from 
#curve_fit - the estimated parameters.
params1 = optimize.curve_fit(f1,xtrain,ytrain)[0]
params2 = optimize.curve_fit(f2,xtrain,ytrain)[0]

params3 = optimize.curve_fit(f3, xtrain, ytrain)[0]

# Compute the otuput of the first hypothesis
y_hypothesis1 = f1(xtrain,params1[0],params1[1])
# Compute the output of the second hypothesis
y_hypothesis2 = f2(xtrain,params2[0],params2[1],params2[2])

y_h3 = f3(xtrain, params3[0], params3[1], params3[2])

#Compute the mean squared train and test error
err1=sum((y_hypothesis1 -ytrain)**2)/n
err1test=sum((f1(xtest,params1[0],params1[1])-ytest)**2)/n

errMyTest = sum((f3(xtest, params3[0], params3[1], params3[2]))**2)/n
errMyTrain = sum((y_h3-ytrain)**2)/n

err2=sum((y_hypothesis2-ytrain)**2)/n
err2test=sum((f2(xtest,params2[0],params2[1],params2[2])-ytest)**2)/n

#Print out results of regression analysis 
print('Function fitting using curve_fit')
print('hypothesis1: parameters: w1=%.2f w2=%.2f\n\t(mean squared train error = %.3f)\n\t(mean squared test error = %.3f)' % (params1[0],params1[1],err1,err1test))
print('hypothesis2: parameters: w1=%.2f w2=%.2f, w3=%.2f\n\t(mean squared train error = %.3f)\n\t(mean squared test error = %.3f)' % (params2[0],params2[1],params2[2],err2,err2test))

print
print("h3: parameters: a=%.2f b=%.2f c=%.2f" % (params3[0], params3[1], params3[2]));
print("mean test squared for h3: %.2f" % errMyTest);
print("mean train squared for h3: %.2f" % errMyTrain);

#Close any open figures, and start a new one
pl.close('all')
#Create a new (empty) figure
pl.figure()

#Plot the original function, the training data, and the hypothesis found by regression
# pl.plot(x,y_tilde,'g')
pl.plot(xtrain,ytrain,'k.')
pl.plot(xtest,ytest,'c.')
pl.plot(x,f1(x,params1[0],params1[1]),'r-')
pl.plot(x,f2(x,params2[0],params2[1],params2[2]),'b-')
pl.plot(x,f3(x, params3[0], params3[1], params3[2]), 'c-')
# pl.legend(['original','train', 'test', 'hypothesis 1', 'hypothesis 2', 'h3'])
pl.legend(['train', 'test', 'h1', 'h2', 'h3'])
pl.xlabel('x')
pl.ylabel('y')



#Display the figure
pl.show()