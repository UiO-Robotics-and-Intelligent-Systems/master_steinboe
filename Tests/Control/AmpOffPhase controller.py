
import matplotlib.pyplot as plt
import numpy as np
import random

def k(t,a,ps,b,p):
    return a*np.tanh(4*np.sin(p*(t+ps)))+b


def amplitude(v,w):
    return (v-w)/2

def verticalPhase(v,w):
    return (v+w)/2

# 100 linearly spaced numbers
t = np.linspace(-2,2,1000)

# the function, which is y = x^2 here
p=1#2*np.pi # periode = 2pi/p
a=1 # amplitude
ps=0 # phase shift
b=0  # vertical shift
y1= k(t,a,ps,b, p)


def sin(t,a,ps,b,p):
    return a*np.sin(p*(t+ps))+b

p=2*np.pi
a=0.5
ps=ps-1
b=0
y2=k(t,a,ps,b,p)



p=2*np.pi
a=1
ps=0
b=0
y3=sin(t,a,ps,b,p)

#title="a="+str(a)+", o="+str(ps)+", b="+str(b)
#plt.title(title)

#plt.plot(t,y1, 'g')
#plt.plot(t,y2, 'b')
#plt.plot(t,y3, 'r')

def minMaxPhase(t,v,w,ps,p=2*np.pi):
    # t - timestep, v and w - used to find amplitude and vertical phase, periode=2pi/p
    a = amplitude(v,w)
    b = verticalPhase(v,w)
    return a*np.tanh(4*np.sin(p*(t+ps)))+b

p=2*np.pi
a = 1 
ps=0
b= 0

s = sin(t,a,ps,b,p)
v = -0.25
w = -0.75
ps=0.25
mmp=minMaxPhase(t,v,w,ps,p)
plt.plot(t,s)
plt.plot(t,mmp)
# plot random MinMaxPhase
"""
nrOfGraphs=1
for i in range(nrOfGraphs):
    params = []
    nrOfParams=6
    for i in range(nrOfParams):
        params.append(random.uniform(-1, 1))

    #randomMinMax = minMaxPhase(t,*params,p)
    #plt.plot(t, randomMinMax)

    
    randomMinMax = minMaxPhase(t,params[0],params[1],params[2],p)
    plt.plot(t, randomMinMax)
    randomMinMax = minMaxPhase(t,params[0],params[1],params[2]+(-0.95)/2,p)
    plt.plot(t, randomMinMax)
    randomMinMax = minMaxPhase(t,params[0],params[1],params[2]+(0.95)/2,p)
    plt.plot(t, randomMinMax)

"""
# show the plot
plt.show()

# se side 75 fra Tønnes sin master