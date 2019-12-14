import matplotlib.pyplot as plt 
import numpy as np

n = 1024
X = np.random.normal(0,1,n)
Y = np.random.normal(0, 1, n)

T = np.arctan2(Y, X)


plt.scatter(X, Y, s=75, c = T,alpha=.5)

plt.xlim(-1.5, 1.5)
#plt.xticks(())  # ignore xticks
plt.ylim(-1.5, 1.5)
#plt.yticks(())  # ignore yticks

plt.figure()
n = 12
x = np.arange(n)
y1 = np.random.uniform(0.5,1, n)
plt.bar(x, y1)
plt.bar(x, -y1)

plt.xticks(())
for x, y in zip(x, y1):
 plt.text(x + 0.4, -y - 0.05, '%.2f' % y, ha='center', va='top')

plt.show()