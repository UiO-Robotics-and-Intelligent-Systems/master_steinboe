
from scipy.stats import spearmanr
from scipy.stats import pearsonr
import numpy as np
import matplotlib.pyplot as plt


a = np.linspace(0, 16, num=100)
b= 2*(a-2)**2
plt.rc('font', size=20) 

plt.plot(a,b)
plt.xlabel("Number of cats in your room")
plt.ylabel("Fear (in percentage)")

plt.figure()

b=np.e**a
plt.plot(a,b)
plt.xlabel("number of dolphines")
plt.ylabel("fear")
plt.tight_layout()
plt.show()