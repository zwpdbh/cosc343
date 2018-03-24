import pylab as pl
import numpy as np
import time
import sys

__author__ = "Lech Szymanski"
__email__ = "lechszym@cs.otago.ac.nz"

class logsig:
    
    def f(self,v):
        y = 1/(1+np.exp(-v))
        return y

    def dfdv(self,y):
        return np.multiply(y,(1-y))

        
class tanh:
    
    def f(self,v):
        y = np.tanh(v)
        return y

    def dfdv(self,y):
        return np.multiply((1+y),(1-y))


class lin:
    
    def f(self,v):
        return v

    def dfdv(self,y):
        return np.ones(y.shape)

class softmax:
    
    def f(self,v):
        N = v.shape[1]
        y = np.exp(v)
        for i in range(0,N):
            y[:,i] /= y[:,i].sum()
                    
        return y

    def dfdv(self,y):
         return np.multiply(y,(1-y))

class relu:

    def f(self,v):
        U,N = v.shape
        y = v
        for i in range(0,N):
            for j in range(0,U):
                if(y[j,i] < 0):
                    y[j,i] = 0
                    
        return y

    def dfdv(self,y):
        U,N = y.shape
        dy = y
        for i in range(0,N):
            for j in range(0,U):
                if(dy[j,i] > 0):
                    dy[j,i] = 1
                    
        return dy

class MLP:

    def __init__(self, layer_sizes, f_activation='logsig',f_output='logsig',sigma=1):
        self.layer_sizes = layer_sizes
        self.num_layers = layer_sizes.size-1
        self.W = []
        self.b = []
        for l in range(1, self.layer_sizes.size):
            nInputs = self.layer_sizes[l-1]
            nNeurons = self.layer_sizes[l]            
            self.W.append(np.matrix(np.random.randn(nInputs,nNeurons))*sigma)
            self.b.append(np.matrix(np.random.randn(nNeurons,1))*sigma)
        if f_activation is 'logsig':
            self.f_activation = logsig()
        elif f_activation is 'tanh':
            self.f_activation = tanh()
        elif f_activation is 'relu':
            self.f_activation = relu()
        else:
            sys.exit('Unrecognised activation function \'' + f_activation + '\'.  Choose from \'logsig\',\'tanh\', or \'relu\'!')
        
        self.softmaxMode = False
        if f_output is 'logsig':
            self.f_output = logsig()
        elif f_output is 'tanh':
            self.f_output = tanh()
        elif f_output is 'lin':
            self.f_output = lin()
        elif f_output is 'relu':
            self.f_output = lin()
        elif f_output is 'softmax':
            if self.layer_sizes[-1]<=1:
                sys.exit('Softmax function requries output vector of size K>1!')
            self.f_output = softmax()   
            self.softmaxMode = True         
        else:
            sys.exit('Unrecognised output function \'' + f_output + '\'.  Choose from \'logsig\',\'tanh\',\'lin\', or \'softmax\'!')

                                
    def weights(self, layer):
        return self.W[layer-1]
    
    def biases(self, layer):
        return self.b[layer-1]

    def output_all_layers(self,x):
        y = []
        N = x.shape[1]
        for l in range(0, self.num_layers):
            W = self.W[l]
            b = self.b[l]
            if l==0:
                v = np.dot(W.T,x)
            else:
                v = np.dot(W.T,y[l-1])
            for i in range(0,N):
                v[:,i] -= b
                
            if l<self.num_layers-1:
                y.append(self.f_activation.f(v))
            else:
                y.append(self.f_output.f(v))        
        return y
        
    def output(self,x):
        y = self.output_all_layers(x)
        return y[-1]
        
    def output_labels(self,x):
        y = self.output(x)
        K = y.shape[0]
        if K==1:
            if isinstance(self.f_output,logsig):
                midPoint = 0.5;                
            else:
                midPoint = 0;
            N = y.shape[1]
            for i in range(0,N):
                if y[0,i]<midPoint:
                    y[0,i]=0
                else:
                    y[0,i]=1
        else:
            y = np.argmax(y,axis=0)
            
        return y
            
    def error(self,x,ytilde):
        y = self.output_labels(x)
        K = ytilde.shape[0]
        
        if K==1:
            e = y!=ytilde;        
        else:
            e = y!=np.argmax(ytilde,axis=0)

        e = e.sum()/ float(e.shape[1]) * 100
        return e
                              
    def backprop(self,x,ytilde):
        y = self.output_all_layers(x)
        dW = []
        db = []
        for l in range(0,self.num_layers):
            dW.append(np.zeros(self.W[l].shape))
            db.append(np.zeros(self.b[l].shape))

        if not self.softmaxMode:
            e = y[-1]-ytilde
            J = np.multiply(e,e).sum()
            dJ = e
        else:
            dJ = np.multiply(ytilde,y[-1]-1)+np.multiply(1-ytilde,y[-1])
            J = -(np.multiply(ytilde,np.log(y[-1]+1e-6))+np.multiply(1-ytilde,np.log(1-y[-1]+1e-6))).sum()


        for l in range(self.num_layers-1,-1,-1):
            dydv = self.f_activation.dfdv(y[l])
            dJdv = np.multiply(dydv,dJ)
                 
            if l==0:
                dW[l] = np.dot(x,dJdv.T)
            else:     
                dW[l] = np.dot(y[l-1],dJdv.T)
            db[l] = -np.matrix(dJdv.sum(axis=1))
            dJ = np.dot(self.W[l],dJdv)
                                                    
        return (dW, db, J)
                                                                                                                                                                                                                                                                                                        
                
    def train(self,x,ytilde,num_epochs,alpha=1e-05):
        #Create a new (empty) figure
        plfig = pl.figure(dpi=100)
        plax1 = plfig.add_subplot(211)
        plax2 = plfig.add_subplot(212)
        pl.ion()
        pl.show()
        plotStep = np.ceil(num_epochs / float(50));
        
        N = x.shape[1]
        J_cost = []
        J_class = []
        J_epochs = []
        for epoch in range(0,num_epochs):
            dW,db,J=self.backprop(x,ytilde)
            
            for l in range(0,self.num_layers):
                self.W[l] -= alpha/N*dW[l]
                self.b[l] -= alpha/N*db[l]                   

            if epoch == 0 or epoch == num_epochs - 1 or (epoch+1) % plotStep == 0:            
                if epoch > 0:  
                    plax1.lines.pop(0)
                    plax2.lines.pop(0)
                e = self.error(x,ytilde)
                J_cost.append(J)
                J_class.append(e)
                J_epochs.append(epoch+1)
                plax1.plot(J_epochs,J_cost,'b-')   
                plax2.plot(J_epochs,J_class,'b-')   
                pl.draw()
                plax1.set_xlim([0,epoch+1])
                plax1.set_ylim([0,max(J_cost)+1])
                plax1.set_ylabel('Cost (J)')
                plax2.set_xlim([0,epoch+1])
                plax2.set_ylim([0,101])
                plax2.set_xlabel('Epoch')
                plax2.set_ylabel('Misclassification (%)')
                time.sleep(0.1)
                pl.pause(0.0001)
                print('Epoch %d: cost=%f, classification error=%f%%' % (epoch+1,J_cost[-1],J_class[-1]))

#if __name__ == '__main__':
#    net = MLP(np.array([2, 8, 8, 1]),f_activation='logsig',f_output='logsig')
    #y=net.output(np.random.rand(2,7))
#    x = np.random.rand(2,7);
#    ytilde = np.random.rand(1,7);
#    net.train(x,ytilde,num_epochs=2000,alpha=0.1)