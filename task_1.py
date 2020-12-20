import matplotlib.pyplot as plt
import numpy as np
from timeit import timeit

import protocol

## TASK1: implement the protocol and evaluate the speed.

# List of possible challenge and key lengths.
l_c = [8, 16, 24]
l_k = np.arange(1, 60, 1)

# Use these variables to store the results of the simulation.
compl = np.zeros((len(l_c), len(l_k)))

for j in range(len(l_c)):
    for i in range(len(l_k)):
        # Init the counter.
        n = np.random.randint(0, 100)

        # Setup phase.
        k = protocol.random_key(l_k[i])

        def single_run():
            # Let's simulate a legitimate exchange.
            _, eavesdropped_msgs, _ = protocol.protocol(k, l_c[j], l_k[i], n)

        # Adjust for execution time.
        iterations = 4000
        compl[j,i] = timeit(single_run, number=iterations) / iterations

# Plot the success attack probability.
plt.figure()
plt.title('Task 1: time complexity vs key length')
plt.xlabel('Number of key bits')
plt.ylabel('Time per authentication [us]')
plt.grid()

for i in range(len(l_c)):
    plt.plot(l_k, compl[i] * 1e6, label='l_c = %d' % l_c[i])
plt.legend()
plt.show()
