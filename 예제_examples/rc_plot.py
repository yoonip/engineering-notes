import numpy as np
import matplotlib.pyplot as plt

t = np.linspace(0.0, 0.01, 1001)
v = 3.3 * (1.0 - np.exp(-t / 0.001))
plt.plot(t * 1000, v)
plt.xlabel("Time [ms]")
plt.ylabel("Voltage [V]")
plt.grid(True)
plt.show()
