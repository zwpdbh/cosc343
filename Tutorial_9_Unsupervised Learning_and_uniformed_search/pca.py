# Code to demo Principal Components Analysis (PCA) on some simple image data
# 
# Written in Python.  See http://www.python.org/
# Placed in the public domain.
# Alistair Knott <alik@cs.otago.ac.nz>

import numpy as np
import matplotlib.pyplot as plt
import sklearn
import sklearn.preprocessing
from scipy import randn
from scipy.cluster.vq import kmeans, vq
from matplotlib import cm

import backprop_network as bp

#Create two template matrices with dimensions dim*dim
dim=4
template1=np.array([[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]])
template2=np.array([[1,0,0,0],[1,0,0,0],[1,0,0,0],[1,0,0,0]])

#Flatten each template into a 1D array
pattern1 = template1.reshape((1,dim*dim))
pattern2 = template2.reshape((1,dim*dim))

#Create num training instances of each pattern
num_instances = 20
noise_level=.0
pattern1_data = np.repeat(pattern1,num_instances,0)
pattern1_noise = randn(num_instances, dim*dim)
pattern1_data = pattern1_data + noise_level*pattern1_noise
pattern2_data = np.repeat(pattern2,num_instances,0)
pattern2_noise = randn(num_instances, dim*dim)
pattern2_data = pattern2_data + noise_level*pattern2_noise

#Normalise the data so it has a mean of zero. (This is an important prerequisite for PCA!)
mu1 = np.mean(pattern1_data)
pattern1_data = np.subtract(pattern1_data, mu1)
mu2 = np.mean(pattern2_data)
pattern2_data = np.subtract(pattern2_data, mu2)

#Close all currently open figures
plt.close('all')
#train
def show_training_images():
    #Create a figure showing the training data as images
    plt.figure()
    plt.suptitle('Training instances.\n\nTop row is pattern1 (white diagonal line running top-left -> bottom-right)\n\nBottom row is pattern 2 (white vertical line on lhs of image)\n')
    image_number = 1
    for dataset in np.array([pattern1_data,pattern2_data]):
        if num_instances < 3:
            num_shown_instances = num_instances
        else:
            num_shown_instances = 3
        for instance in range(num_shown_instances):
            plt.subplot(2,num_shown_instances,image_number)
            plt.xticks(())
            plt.yticks(())
            plt.imshow(dataset[instance].reshape((dim,dim)), interpolation='nearest', cmap="bone")
            image_number +=1
    plt.subplots_adjust(top=.8)
    plt.show()

def plot_raw_data_in_sampled_dimensions():
    #Create a figure showing plots of the training data in randomly selected pairs of dimensions
    plt.figure()
    plt.suptitle('Plots showing the training data in randomly selected pairs of dimensions\n\nPattern 1 in red; Pattern2 in blue')
    for plotnum in range(0,10):
        plt.subplot(2,5,plotnum)
        #Pick two dimensions at random
        while True:
            dimensions = np.random.randint(15,size=2)
            if dimensions[0] != dimensions[1]:
                break
        plt.xlabel('d%d' % dimensions[0])
        plt.ylabel('d%d' % dimensions[1])
        plt.xticks(np.arange(-1,1.1,1))
        plt.yticks(np.arange(-1,1.1,1))
        plt.scatter(pattern1_data[:,dimensions[0]],pattern1_data[:,dimensions[1]], color="red")
        plt.scatter(pattern2_data[:,dimensions[0]],pattern2_data[:,dimensions[1]], color="blue")
    plt.tight_layout()
    plt.subplots_adjust(top=.8)
    plt.show()

def pca():
    #Run PCA on the training data, and plot it in a coordinate space given by the first 2 principal components.
    #Return the datapoints in this coordinate space.
    
    #First combine the two types of data into a single dataset
    combined_data = np.concatenate((pattern1_data, pattern2_data), axis=0)
    
    #Do PCA on the combined input data. 
    eigenvectors, eigenvalues, V = np.linalg.svd(combined_data.T, full_matrices=False)
    
    #Now project the two types of data into the principal component space
    projected_pattern1_data = np.dot(pattern1_data, eigenvectors)
    projected_pattern2_data = np.dot(pattern2_data, eigenvectors)
    
    sigma = projected_pattern1_data.std(axis=0).mean()
    #print(eigenvectors)

    #Get the first two components of each pattern   
    pattern1_pc1s = projected_pattern1_data[:,0]
    pattern1_pc2s = projected_pattern1_data[:,1]
    pattern2_pc1s = projected_pattern2_data[:,0]
    pattern2_pc2s = projected_pattern2_data[:,1]
    
    #Plot the patterns in the space of the first two principal components
    fig, ax = plt.subplots()
    ax.scatter(pattern1_pc1s,pattern1_pc2s, color="red")
    ax.scatter(pattern2_pc1s,pattern2_pc2s, color="blue")
    #ax.scatter(projected_pattern1_data[:,0],projected_pattern1_data[:,1], color="red")
    #ax.scatter(projected_pattern2_data[:,0],projected_pattern2_data[:,1], color="blue")
    plt.show()
    
    return(np.array([pattern1_pc1s,pattern1_pc2s,pattern2_pc1s,pattern2_pc2s]))

def demo():
    show_training_images()
    plot_raw_data_in_sampled_dimensions()
    pca()
            
def train_autoassociative_network_on_patterns():
    
    combined_patterns = np.concatenate((pattern1_data, pattern2_data), axis=0)
    
    #scale patterns to fall between 0 and 1 
    min_max_scaler = sklearn.preprocessing.MinMaxScaler(feature_range=(0, 1))
    scaled_patterns = min_max_scaler.fit_transform(combined_patterns, (2*num_instances,dim*dim))

    print scaled_patterns
    
    #Create an array containing training data for the network. The targets are a copy of the inputs.
    tmp=np.expand_dims(combined_patterns, axis=1)
    network_training_data = np.concatenate((tmp,tmp), axis=1)
    
    # create a network with two input, two hidden, and one output nodes
    n = bp.NN(dim*dim, 2, dim*dim)
    # train it with some patterns
    n.train(network_training_data, epochs=200)
    
    plt.figure()
    plt.subplot(1,2,1)
    plt.xticks(())
    plt.yticks(())
    arr1 = np.array(n.wo[0])
    plt.imshow(arr1.reshape((dim,dim)), interpolation='nearest', cmap="bone")
    plt.subplot(1,2,2)
    plt.xticks(())
    plt.yticks(())
    arr2 = np.array(n.wo[1])
    plt.imshow(arr2.reshape((dim,dim)), interpolation='nearest', cmap="bone")
    plt.show()
    

    n.weights()
    # test it
    #n.test(network_training_data)
    
def kmeans_test():
    
    #Run PCA on the image data    
    projected_patterns = pca()
    
    #Combine the returned classes into a single dataset
    combined_pc1s = np.concatenate((projected_patterns[0], projected_patterns[2]), axis=0)
    combined_pc2s = np.concatenate((projected_patterns[1], projected_patterns[3]), axis=0)
    kmeans_inputs = np.matrix([combined_pc1s,combined_pc2s]).transpose()
    
    #Run k-means on the combined data  
    number_of_clusters = 2.  
    cluster_centroids, error = kmeans(kmeans_inputs, number_of_clusters)
    idx, _ = vq(kmeans_inputs, cluster_centroids)
    
    #Plot the data, using different shades of grey for points from different clusters
    fig, ax = plt.subplots()
    color = [str((item+1)/number_of_clusters) for item in idx]
    ax.scatter(combined_pc1s.transpose(),combined_pc2s.transpose(), s=50, c=color)
    plt.show()

    print 'Categories found by k-means:' 
    print idx