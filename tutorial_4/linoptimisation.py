#import pylab as pl
import matplotlib.pyplot as pl
import numpy as np
import inspect, os
import sys

__author__ = "Lech Szymanski"
__email__ = "lechszym@cs.otago.ac.nz"

#Bases of the polynomial function f_j(x)=x^j
#
#Params: x - array of N inputs
#        k - degree of the polynomial
#
#Output: y - array of N ouptuts
def polynomial_bases(x,k):
    # Number of points to evaluate the function on
    N = len(x)
    
    # (k+1)xN Matrix of base functions evaluations on input - each row 
    # corresponds to different base function, each column to evaluation of that 
    # function on given input
    F = np.ndarray((k+1, N))

    # For each row of F, compute that output of the base function
    # f_j(x)=x^j
    for j in range(0,k+1):
        F[j,] = x**j

    return  F


#Output of the polynomial function model y=w_0+w_1*x+w_2*x^2+...+w_k*x^k
#
#Params: x - array of N inputs
#        w - parameter vector
#
#Output: y - array of N ouptuts
#
#The polynomial degree k is derived from the length of the weigh vector
def polynomial_function(x,w):
    # Degree of the polynomial
    k = len(w)-1
    
    # Matrix of base functions evaluations on input - each row corresponds to 
    # different base function, each column to evaluation of that function
    # on given input
    F = polynomial_bases(x,k)

    # Compute polynomial output
    y = w.T*np.matrix(F)
    # Return optput as an nd-array (easier for plotting)
    return  np.squeeze(np.asarray(y))
    

#Bases of the cosines function f_j(x)=cos(j*x/pi)
#
#Params: x - array of N inputs
#        k - number of non-zero frequencies
#
#Output: y - array of N ouptuts
#
def cosines_bases(x,k):
    # Number of points to evaluate the function on
    N = len(x)
    
    # (k+1)xN Matrix of base functions evaluations on input - each row 
    # corresponds to different base function, each column to evaluation of that 
    # function on given input
    F = np.ndarray((k+1, N))

    # For each row of F, compute that output of the base function
    # f_j(x)=cos(j*x/pi)
    for j in range(0,k+1):
        F[j,] = np.cos(j/np.pi/4*(x+np.pi));

    return F


#Output of the cosines function model y=w_0+w_1*cos(x/pi)+w_2*cos(2*x/pi)...+w_k*cos(k*x/pi)
#
#Params: x - array of N inputs
#        w - parameter vector
#
#Output: y - array of N ouptuts
#
#The number of bases is derived from the length of the weigh vector
def cosines_function(x,w):
    # Number of bases
    k = len(w)-1
    
    # Matrix of base functions evaluations on input - each row corresponds to 
    # different base function, each column to evaluation of that function
    # on given input
    F = cosines_bases(x,k);

    # Compute the cos series otuput
    y = w.T*np.matrix(F)
    # Return optput as an nd-array (easier for plotting)
    return  np.squeeze(np.asarray(y))


#Steepest gradient descent optimisation over a linear model
#
#Params: F - input x after evaluation over base function of the linear model
#        ytilde - desired output
#        w - initial guess of the parameter values
#        _alpha - learning rate
#        _nEpochs - number of epochs
def optimise_lin(F,ytilde,w,_alpha,_nEpochs):
    # The number of rows in F matrix corresponds to number of base functions,
    # number of columns to the number of inputs   
    N = F.shape[1]
    
    # Allocate array for cost values (used for plotting cost)
    J = np.ndarray((_nEpochs+1,1))

    # Compute the starting cost    
    y = w.T*F
    error = y-ytilde
    J[0] = error*error.T
    print('Epoch 0 J=%.1f, sqrt(mean(J))=%.1f' % (J[0], np.sqrt(J[0]/N)));
    
    # Iterate over the number of epochs
    for epoch in range(1,_nEpochs+1):
        # Compute the least squares gradient of the model - for linear model
        # it's just matrix F times the error.  Divide it by number of
        # data points to normalise it a bit.
        delta_w = (F*np.matrix(error).T)/N;               
        # Update the parameters (negative gradient times learning rate)
        w_new = w-_alpha*delta_w

        # Compute the cost after update
        y = w_new.T*F
        error = y-ytilde
        J[epoch] = error*error.T

        # Stop optimisation if cost is not going down
        if J[epoch]>=J[epoch-1]:
            print('Terminating optimisation because cost is going up\n');
            break
                            
        # If cost went down, print current cost and keep the udpate
        print('Epoch %d: J=%.1f, sqrt(mean(J))=%.1f' % (epoch, J[epoch], np.sqrt(J[epoch]/N)));
        w = w_new
                    
    # Plot the RMS error over epochs
    pl.plot(np.linspace(0,epoch,epoch),np.sqrt(J[0:epoch]/N),'b-')
    pl.xlabel('Epoch')
    pl.ylabel('RMS error')

    return w



#Load data from file found in the same directory where this script resides
workingDir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) 
npzfile = np.load(os.path.join(workingDir, "t4dataset2.npz"))
# Extract input and target output samples
x = npzfile['x'];
y_tilde = npzfile['y_tilde'];

#Fraction of data used for training - 0.8 corresponds to 80% of the data
#being used for train set and 20% for test set
pTrain = 0.8;

#Total number of points in the dataset
N = len(x)
#Create a random permutation of data sample indexes
I = np.random.permutation(N);
#Split the indexes into the training and testing indexes
I_train = I[1:np.floor(pTrain*N)];
I_test = I[np.floor(pTrain*N)+1:N];
#Create training and test sets
x_train = x[I_train];
y_tilde_train = y_tilde[I_train];
x_test = x[I_test];
y_tilde_test = y_tilde[I_test];

#Number of epochs to train for
nEpochs = 1000;
# Learning rate
alpha = 0.01;
# Polynomial/coscos function degree
k = 3;

using_poly = True
#If you're using poly function, leave the following line commetented out, 
#otherwise uncomment it
#using_poly = False

#Close any open figures, and start a new one
pl.close('all')
#Create a new (empty) figure
pl.figure()
pl.subplot(211);

print('Function fitting using steepest gradient descent')


if using_poly:
    #Evaluate base functions over input for polynomial model
    F = polynomial_bases(x_train,k);
    pl.title('Poly training (k=' + str(k) + ', alpha=' + str(alpha) + ')' );
else:
    #Evaluate base functions over input for cosines model
    F = cosines_bases(x_train,k);
    pl.title('Cos training (k=' + str(k) + ', alpha=' + str(alpha) + ')' );

#Choose the initial value of parametrs at random
w_init = np.matrix(np.random.randn(k+1, 1))
#Compute the least squares solution to the regression problem using steepest
#gradient algorithm
w=optimise_lin(F,y_tilde_train,w_init,alpha,nEpochs)


print('\nResults after optimisation')
if using_poly:
    #Compute training output based on parameters found
    y_train=polynomial_function(x_train,w)
    #Compute root mean squared error for training data
    err_train=np.sqrt(sum((y_train -y_tilde_train)**2)/N)
    #Compute test output based on parameters found
    y_test=polynomial_function(x_test,w)
    #Compute root mean squared error for test data
    err_test=np.sqrt(sum((y_test -y_tilde_test)**2)/N)
    sys.stdout.write('poly')
else:
    #Compute training output based on parameters found
    y_train=cosines_function(x_train,w)
    #Compute root mean squared error for training data
    err_train=np.sqrt(sum((y_train -y_tilde_train)**2)/N)
    #Compute test output based on parameters found
    y_test=cosines_function(x_test,w)
    #Compute root mean squared error for test data
    err_test=np.sqrt(sum((y_test -y_tilde_test)**2)/N)
    sys.stdout.write('cosines')
    

print(' k=%d:\n\tw=%s\n\t(mean squared train error = %.3f)\n\t(mean squared test error = %.3f)' % (k,w.T,err_train,err_test))

#Plot the training data
pl.subplot(212)
pl.plot(x_train,y_tilde_train,'k.')

#Plot the hypothesis found by regression
n=np.linspace(min(x),max(x),200)
pl.plot(n,polynomial_function(n,w),'b-')
pl.legend(['train','k=' + str(k)])
pl.xlabel('x')
pl.ylabel('y')

#Display the figure
pl.show()
