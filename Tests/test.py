import matplotlib.pyplot as plt
import numpy as np
import random

a=[0.1,0.2,0.3,0.4,0.5,0.6]
x=[1,2,3,4,5,6]

colors = np.random.rand(len(a))



seed=35607117
random.seed(seed)

plt.figure()
N = 18
y = np.zeros((N,))
x = np.array(list(range(N)))
colors = np.random.rand(N)
colors = np.array([i/N for i in list(range(N))])
colors1=np.zeros((N,3))
for i in range(N):
    colors1[i]=np.array([random.random(), random.random(), random.random()])

print(colors1)
colors2=np.zeros((6,3))
for i in range(6):
    colors2[i]=np.array([random.random(), random.random(), random.random()])

print(colors2)
area = 1#(30 * np.random.rand(N))**2  # 0 to 15 point radii

plt.scatter(x, y,  c=colors1)
plt.title(seed)
plt.scatter(x[0:6], y[0:6]-2, c=colors2)

#plt.scatter(x,a, 'o', c=colors)
plt.show()
# 35607117