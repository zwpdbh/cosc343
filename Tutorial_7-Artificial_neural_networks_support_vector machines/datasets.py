from sklearn import datasets
import numpy as np
import pylab as pl
import MLP
from sklearn import svm
import sys

__author__ = "Lech Szymanski"
__email__ = "lechszym@cs.otago.ac.nz"

class dataset:
    
    xMin = 0
    xMax = 1

    def labelsToVectors(self,labels):
        N = labels.size
        labelSet = np.unique(labels)
        K = labelSet.size
        if K==2:
            y = np.zeros((1,N))
            for i in range(0,N):
                y[0,i]=labels[i]               
        else:
            y = np.zeros((K,N))
            for i in range(0,N):
                for k in range(0,K):
                    if labels[i]==labelSet[k]:
                        y[k,i]=1
                        break

        return y
            
    
    def vectorsToLabels(self,y):
        return np.argmax(y,axis=0)

    def split(self,x,target_labels,train_ratio):
        target_y = self.labelsToVectors(target_labels)
        
        #Total number of points in the dataset
        N = x.shape[1]

        #Create a random permutation of data sample indexes
        I = np.random.permutation(N)
        
        #Split the indexes into the training and testing indexes
        I_train = I[0:np.floor(train_ratio*N)]
        I_test = I[np.floor(train_ratio*N):N]

        self.x_test = x[:,I_test]
        self.target_y_test = target_y[:,I_test];
        self.target_labels_test = target_labels[I_test]
        
        self.x = x[:,I_train];
        self.target_y = target_y[:,I_train];
        self.target_labels = target_labels[I_train]

    def numInputs(self):
        return self.x.shape[0]
        
    def numClasses(self):
        return self.target_y.shape[0]

    def normalise(self, minVal=0, maxVal=1):
        self.xMin = self.x.min()-minVal
        self.x -= self.xMin      
        self.x_test -= self.xMin       
            
        self.xMax = self.x.max()/maxVal
        self.x /= self.xMax
        self.x_test /= self.xMax

    def show_classification(self,model):
        
        h = .02  # step size in the mesh

        # create a mesh to plot in
        M = self.numInputs()

        if M is not 2:
            print('Can\'t show classification plot on a dataset of %d-dimensions.' % (M))   
        else:
            plfig=pl.figure(dpi=100)
            plfig.add_subplot(111)

            x1_min, x1_max = self.x[0, :].min() - 0.1, self.x[0,:].max() + 0.1
            x2_min, x2_max = self.x[1, :].min() - 0.1, self.x[1,:].max() + 0.1
            xx1, xx2 = np.meshgrid(np.arange(x1_min, x1_max, h),
                           np.arange(x2_min, x2_max, h))
                     
            if isinstance(model,MLP.MLP):                                           
                y = model.output_labels(np.c_[xx1.ravel(), xx2.ravel()].T)
            elif isinstance(model,svm.SVC):
                y = model.predict(np.c_[xx1.ravel(), xx2.ravel()])
            else:
                sys.exit('Unrecognised model type!')
    
            y = np.squeeze(np.asarray(y.T))
            # Put the result into a color plot
            y = y.reshape(xx1.shape)
        
            pl.contourf(xx1, xx2, y, cmap=pl.cm.Paired, alpha=0.8)
            # Plot also the training points
            pl.scatter(self.x[0,:], self.x[1,:], c=self.target_labels.T, cmap=pl.cm.Paired)
            pl.xlabel('x1')
            pl.ylabel('x2')
            pl.xlim(xx1.min(), xx1.max())
            pl.ylim(xx2.min(), xx2.max())
            pl.xticks(())
            pl.yticks(())
            pl.show()


class dataset_spiral(dataset):
    
    def __init__(self, train_ratio=0.8):
        N = 120;

        x = np.zeros((2,N))
        t = np.zeros((1,N))    

        for i in range(0,N/2):
            delta = np.pi/8+i*0.2
            r = 2*delta+0.1
            x[0,i]=r*np.sin(delta)
            x[1,i]=r*np.cos(delta)
            t[0,i]=0
            
        for i in range(0,N/2):
            delta = np.pi/8+i*0.2
            r =-2*delta-0.1
            x[0,i+N/2]=r*np.sin(delta)
            x[1,i+N/2]=r*np.cos(delta)
            t[0,i+N/2]=1
    
        self.split(x,np.squeeze(np.asarray(t)),train_ratio)
        

class dataset_iris(dataset):

    def __init__(self, train_ratio=0.8, attributes=4):
        iris = datasets.load_iris()
        self.split(iris.data[:, :attributes].T,iris.target,train_ratio)
    
    
class dataset_digits(dataset):

    def __init__(self, train_ratio=0.8, n_class=10):
        digits = datasets.load_digits(n_class)
        self.split(digits.data.T,digits.target,train_ratio)
    
    def show_classification(self,model):
        pl.figure(dpi=100)

        N = self.x_test.shape[1]
        I = np.random.permutation(N)        
    
        nImages = 32
        if len(I)<nImages:
            nImages = len(I)

        for i in range(0,nImages):        
            ps=pl.subplot(4,8,i+1)
            ps.matshow(self.x_test[:,I[i]].reshape(8,8), cmap=pl.cm.gray)
            if isinstance(model,MLP.MLP):                                           
                label = model.output_labels(np.matrix(self.x_test[:,I[i]]).T)
            elif isinstance(model,svm.SVC):
                label = model.predict(np.matrix(self.x_test[:,I[i]]))
            else:
                sys.exit('Unrecognised model type!')
                
            ps.axis('off')
            pl.title(label)
        pl.show() 