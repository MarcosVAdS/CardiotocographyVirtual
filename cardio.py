import matplotlib.pyplot as plt
import numpy as np
plt.yticks(np.arange(80, 250, 10))

fig, ax = plt.subplots()
fig.yticks(np.arange(80, 250, 10))
ax.yticks(np.arange(80, 250, 10))
ax.grid()

ax.axis((0, 1200, 0, 250))
plt.show()