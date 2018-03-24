# import pylab as pl
import matplotlib.pyplot as pl
import numpy as np
import inspect, os

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

#Least squares closed form solution for a linear model
# y=w_0*f_0(x)+w_1*f_1(x)+...+w_k*f_k(x)
#
# Params: F - base functions evaluated on the input
#         ytilde - desired outputs
#
# Output: w - parameters computed from he least squares fit
def linearLS_params(F,ytilde):

    # Typecast F to numpy matrix
    F = np.matrix(F);

    # Compute parameters using least squares solution (same formula as
    # given in Lecture 7)
    w = np.matrix((F * F.T).I * F * np.matrix(ytilde).T)
    
    return w


#Load data from file found in the same directory where this script resides
workingDir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) 
#npzfile = np.load(os.path.join(workingDir, "t4dataset1.npz"))
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

# Select the degree of the polynomial function
k_poly = 10;

#Compute the least squares solution to the regression problem using
#k_poly-degree polynomial
w_poly=linearLS_params(polynomial_bases(x_train,k_poly),y_tilde_train)

#Compute training output based on parameters found
y_poly_train=polynomial_function(x_train,w_poly)
#Compute root mean squared error for training data
err_poly_train=np.sqrt(sum((y_poly_train -y_tilde_train)**2)/N)
#Compute test output based on parameters found
y_poly_test=polynomial_function(x_test,w_poly)
#Compute root mean squared error for test data
err_poly_test=np.sqrt(sum((y_poly_test -y_tilde_test)**2)/N)

# Select the number of bases used in the cosines function
k_cos = 4;

#Compute the least squares solution to the regression problem using
#k_cos bases
w_cos=linearLS_params(cosines_bases(x_train,k_poly),y_tilde_train)

#Compute training output based on parameters found
y_cos_train=cosines_function(x_train,w_cos)
#Compute root mean squared error for training data
err_cos_train=np.sqrt(sum((y_cos_train -y_tilde_train)**2)/N)
#Compute test output based on parameters found
y_cos_test=cosines_function(x_test,w_cos)
#Compute root mean squared error for test data
err_cos_test=np.sqrt(sum((y_cos_test -y_tilde_test)**2)/N)

#Print out results of regression analysis for the two models
print('Function fitting using least-squares')
print('polynomial k=%d:\n\tw=%s\n\t(mean squared train error = %.3f)\n\t(mean squared test error = %.3f)' % (k_poly,w_poly.T,err_poly_train,err_poly_test))
print('cos series k=%d:\n\tw=%s\n\t(mean squared train error = %.3f)\n\t(mean squared test error = %.3f)' % (k_cos, w_cos.T,err_cos_train,err_cos_test))

#Close any open figures, and start a new one
pl.close('all')
#Create a new (empty) figure
pl.figure()

#Plot the training data
pl.plot(x_train,y_tilde_train,'k.')

#Plot the poly and cos hypothesis found by regression
n=np.linspace(min(x),max(x),200)
pl.plot(n,polynomial_function(n,w_poly),'b-')
pl.plot(n,cosines_function(n,w_cos),'g-')
pl.legend(['train','poly k=' + str(k_poly), 'cos k=' + str(k_cos)])
pl.xlabel('x')
pl.ylabel('y')

#Display the figure
pl.show()
