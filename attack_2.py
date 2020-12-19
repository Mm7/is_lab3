import matplotlib.pyplot as plt
import numpy as np

import protocol

## Task 2: knowing a previous successful exchange, implement an
##         attack.

# Let's fix the length of the challenge.
l_c = 16

# Use these variables to store the results of the simulation.
l_k = np.arange(1, 20, 1)
compl = np.zeros_like(l_k)
succ_p = np.zeros_like(l_k, dtype=np.float32)

# Loop over all the possible key lengths and for each of them
# compute the attack complexity and success probability.
for i in range(len(l_k)):
    # Setup phase.
    k = protocol.random_key(l_k[i])

    # Let's simulate the legitimate exchange.
    n = 0
    _, eavesdropped_msgs, n = protocol.protocol(k, l_c, l_k[i], n)

    # Extract the interesting quantities from the exchange.
    eav_c = eavesdropped_msgs[1][0]
    eav_n = eavesdropped_msgs[1][1]
    eav_r = eavesdropped_msgs[2]

    eav_s_c = protocol.digit_dec_sum(eav_c)
    eav_s_t = eav_r / eav_s_c

    # Let's try to compute all the possible keys that can lead
    # to `eav_r` given `eav_n` and `eav_c`.
    keys = list()
    for tst_k in range(2**l_k[i]):
        t = eav_n + tst_k
        s_t = protocol.digit_dec_sum(t)

        if s_t == eav_s_t:
            keys.append(tst_k)

        # For each iteration increment the complexity counter.
        compl[i] += 1

    # The attacker knows that the key is in the set `keys`, thus,
    # assuming a uniform distribution, the success probability is
    # equal to the inverse of the size of the set of candidate keys.
    succ_p[i] = 1. / len(keys)

# Plot the success attack probability.
plt.figure()
plt.title('Task 2: success attack probability vs key length [l_c = %d]' % l_c)
plt.xlabel('Number of key bits')
plt.ylabel('Success attack probability [%]')
plt.grid()
plt.semilogy(l_k, succ_p * 100, '.')

# Plot the complexity.
plt.figure()
plt.title('Task 2: attack complexity vs key length [l_c = %d]' % l_c)
plt.xlabel('Number of key bits')
plt.ylabel('Number of iterations')
plt.grid()
plt.semilogy(l_k, compl, '.')

plt.show()

