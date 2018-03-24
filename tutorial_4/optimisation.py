# import pylab as pl
import matplotlib.pyplot as pl
import numpy as np
import inspect, os

__author__ = "Lech Szymanski"
__email__ = "lechszym@cs.otago.ac.nz"

#Output of coscos function y=w_0*cos(w_1*(x-w_2))+w_3*cos(w_4*(x-w_5))
#
#Params: x - array of N inputs
#        w - parameter vector
#
#Output: y - array of N ouptuts
def coscos_function(x,w):
    # Compute polynomial output
    y = w[0]*np.cos(w[1]*(x-w[2]))+w[3]*np.cos(w[4]*(x-w[5]))
    # Return optput as an nd-array (easier for plotting)
    return  np.squeeze(np.asarray(y))

#Derivative of coscos function with respect to its parameters
#
#Params: x - array of N inputs (1xN vector)
#        w - parameter vector (6x1 size, because there are 6 parameters)
#
#Output: dw - 6xN matrix of partial derivatives, each row is a derivative
#             for given parameter, each column are the derivatives for given
#             input
def coscos_function_derivative(x,w):
    dydw = np.ndarray((len(w), len(x)))
    dydw[0,:] = np.cos(w[1]*(x-w[2]))
    dydw[1,:] = np.multiply(-(x-w[2])*w[0,0],np.sin(w[1]*(x-w[2])))
    dydw[2,:] = w[1]*w[0,0]*np.sin(w[1]*(x-w[2]))
    
    dydw[3,:] = np.cos(w[4]*(x-w[5]))
    dydw[4,:] = np.multiply(-(x-w[5])*w[3,0],np.sin(w[4]*(x-w[5])))
    dydw[5,:] = w[4]*w[3,0]*np.sin(w[4]*(x-w[5]))
    
    return dydw

#Steepest gradient descent optimisation over a a non-linear model
#
#Params: x - 1xN input of training data
#        ytilde - 1xN desired output
#        w - initial guess of the parameter values
#        _alpha - learning rate
#        _nEpochs - number of epochs
#        f - model function f(x,w)
#        dfdw - function dfdw(x,w) that computes derivatives of f(x,w) wrt parameters
def optimise(x,ytilde,w,_alpha,_nEpochs,f,dfdw):
    #Get the number of samples in the training data
    N = np.matrix(x).shape[1]
    
    # Allocate array for cost values (used for plotting cost)
    J = np.ndarray((_nEpochs+1,1))

    # Compute the starting cost      
    y = f(x,w)
    error = y-ytilde
    J[0] = sum(error**2)
    print('Epoch 0: J=%.1f, sqrt(mean(J))=%.1f' % (J[0], np.sqrt(J[0]/N)));    

    # Iterate over the number of epochs
    for epoch in range(1,_nEpochs+1):
        # Compute the least squares gradient of the model using the provided
        # dfdw function
        dydw = np.matrix(dfdw(x,w))
        # For the update, divide the gradient by number of
        # data points to normalise it a bit.
        delta_w = dydw*np.matrix(error).T/N;
        # Compute the parameter update        
        w_new = w-_alpha*delta_w

        # Evalute model function for the new value of parameters using
        # the provided f(x,w), and compute the error and cost
        y = f(x,w_new)
        error = y-ytilde
        J[epoch] = sum(error**2)

        # If cost is not going down, stop training        
        if J[epoch]>=J[epoch-1]:
            print('Terminating optimisation because cost is going up\n');
            break;
        
        # If cost is goind down, keep the new parameter values 
        print('Epoch %d: J=%.1f, sqrt(mean(J))=%.1f' % (epoch, J[epoch], np.sqrt(J[epoch]/N)));
        w = w_new;        

    # Plot the cost over epochs
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
ytilde_train = y_tilde[I_train];
x_test = x[I_test];
ytilde_test = y_tilde[I_test];

#Number of epochs to train for
nEpochs = 2000;
#Learning rate
alpha = 0.01;
#Variance used for initial weight random initialisation (the larger the variance,
#the more random and larger the weight values)
winit_var = 2;

#Close any open figures, and start a new one
pl.close('all')
#Create a new (empty) figure
pl.figure()
pl.subplot(211)

print('Function fitting using steepest gradient descent')

#Pick initial values for parameters at random
w_init = np.matrix(np.random.randn(6, 1))*winit_var

#Optimise the model using least-squares non-linear optimisation.  
w=optimise(x_train,ytilde_train,w_init,alpha,nEpochs,coscos_function,coscos_function_derivative)


print('\nResults after optimisation:')

#Compute training output based on parameters found
y_train=coscos_function(x_train,w)
#Compute root mean squared error for training data
err_train=np.sqrt(sum((y_train -ytilde_train)**2)/N)
#Compute test output based on parameters found
y_test=coscos_function(x_test,w)
#Compute root mean squared error for test data
err_test=np.sqrt(sum((y_test -ytilde_test)**2)/N)
  
print('\n\tw=%s\n\t(mean squared train error = %.3f)\n\t(mean squared test error = %.3f)' % (w.T,err_train,err_test))

pl.subplot(212)
#Plot the training data
pl.plot(x_train,ytilde_train,'k.')

#Plot the poly and cos hypothesis found by regression
n=np.linspace(min(x),max(x),200)
pl.plot(n,coscos_function(n,w),'b-')
#pl.plot(n,cosines_function(n,w_cos),'g-')
pl.legend(['train','func'])
pl.xlabel('x')
pl.ylabel('y')

#Display the figure
pl.show()
