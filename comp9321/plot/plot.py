import matplotlib.pyplot as plt 
import numpy as np

x = np.linspace(-3,3,50)
y1 = 2*x+1
y2 = x**2


plt.figure()
plt.plot(x,y1)
new_ticks = np.linspace(-1,10,6)
plt.xticks(new_ticks)#new unit on aixis
plt.yticks(new_ticks)
ax = plt.gca()
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')
ax.spines['bottom'].set_position(('data', 0))
ax.spines['left'].set_position(('data', 0))
x0 = 1
y0 = 2*x0+1
plt.scatter(x0, y0,s= 100, color = 'r')
#two types of comment
plt.annotate(r'$2x+1=%s$' % y0, xy=(x0, y0), xycoords='data', xytext=(+30, -30),
             textcoords='offset points', fontsize=16,
             arrowprops=dict(arrowstyle='->', connectionstyle="arc3,rad=.2"))
plt.text(-3.7, 3, r'$This\ is\ the\ some\ text. \mu\ \sigma_i\ \alpha_t$',
         fontdict={'size': 6, 'color': 'r'})
plt.show()

'''

plt.figure()
plt.plot(x, y2, label = 'fuck')
plt.plot(x,y1, color = 'red', linewidth = 2, label = 'me')
plt.legend()#图例
plt.xlim(-1, 3)
plt.ylim(-5,5)
plt.xlabel('fuck x')
plt.ylabel('fuck y')

new_ticks = np.linspace(-1,2,5)
plt.xticks(new_ticks)#new unit on aixis
plt.yticks([-2, -1, 0, 1], ['a', 'b', 'c', 'd'])

ax = plt.gca()
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')
ax.spines['bottom'].set_position(('data', 0))
ax.spines['left'].set_position(('data', 0))
plt.show()'''