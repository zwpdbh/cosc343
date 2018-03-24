#These commands import some of the scipy libraries we'll be using. 
#import pylab as pl
import numpy as np
import matplotlib.pyplot as plt

#Define a uniformly spaced set of x values (n in total)
n=50
x=np.linspace(0,4,n)

#Define a set of corresponding y values
a=2; b=1
y=a*x+b;

#Close any open figures, and start a new one
#pl.close('all')
#Create a new (empty) figure
plt.figure()

#Plot the function (in greeen)
plt.plot(x,y,'g')

#Add a legend and axis labels
plt.legend(['my function'])
plt.xlabel('x')
plt.ylabel('y')

#Display the figure
plt.show()