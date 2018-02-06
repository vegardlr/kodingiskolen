import numpy as np
import matplotlib.pyplot as plt
x = np.linspace(-3,3,101)

plt.plot(x,np.exp(x),'b')
plt.plot(x,2.**x,'r')
plt.plot(x,10.**x,'g')
plt.xlim([-1,2])
plt.ylim([-1,10])
plt.grid()
plt.show()
