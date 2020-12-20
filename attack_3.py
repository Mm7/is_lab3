import matplotlib.pyplot as plt
import numpy as np
from timeit import timeit

import protocol

## Task 3: knowing nothing more than what is publicy available,
##         an attacker has to authenticate into the system.

# List of possible challenge and key lengths.
l_c = [8, 16, 24]
l_k = np.arange(1, 32, 1)

# Use these variables to store the results of the simulation.
compl = np.zeros((len(l_c), len(l_k)))
succ_p = np.zeros((len(l_c), len(l_k)), dtype=np.float32)

# Repeat the simulation `sim_cnt` times to average the results.
sim_cnt = 20000

for j in range(len(l_c)):
    for i in range(len(l_k)):
        def single_run():
            # Setup phase.
            k = protocol.random_key(l_k[i])
            n = np.random.randint(0, 100)

            # `s_t` must be a number in the range:
            # [1, 9 * (floor(log10(2^l_k + n)) + 1)].
            upp_bound = 9 * (np.floor(np.log10(2**l_k[i]) + n) + 1)

            # Let's simulate a (desperate) attack.
            def attacker_step_3(c, n):
                s_c = protocol.digit_dec_sum(c)
                s_t = np.random.randint(0, upp_bound)

                return s_t * s_c

            accepted, _, _ = protocol.protocol(k, l_c[j], l_k[i], n, attacker_step_3)

            succ_p[j,i] += accepted

        compl[j,i] = timeit(single_run, number=sim_cnt)

compl /= sim_cnt
succ_p /= sim_cnt

# Plot the success attack probability.
plt.figure()
plt.title('Task 3: success attack probability vs key length')
plt.xlabel('Number of key bits')
plt.ylabel('Success attack probability [%]')
plt.grid()

for i in range(len(l_c)):
    plt.plot(l_k, succ_p[i]*100, label='l_c = %d' % l_c[i])
plt.legend()

# Plot the complexity.
plt.figure()
plt.title('Task 3: attack complexity vs key length')
plt.xlabel('Number of key bits')
plt.ylabel('Time per iteration [us]')
plt.grid()

for i in range(len(l_c)):
    plt.plot(l_k, compl[i] * 1e6, label='l_c = %d' % l_c[i])
plt.legend()

plt.show()

