import matplotlib.pyplot as plt
import numpy as np
from timeit import timeit

import protocol

## Task 2: knowing a previous successful exchange, implement an
##         attack.

# List of possible challenge and key lengths.
l_c = [8, 16, 24]
l_k = np.arange(1, 17, 1)

# Use these variables to store the results of the simulation.
compl = np.zeros((len(l_c), len(l_k)))
succ_p = np.zeros((len(l_c), len(l_k)), dtype=np.float32)

# Repeat the simulation `sim_cnt` times to average the results.
sim_cnt = 100

for j in range(len(l_c)):
    for i in range(len(l_k)):
        def single_run():
            # Setup phase.
            k = protocol.random_key(l_k[i])

            # Let's simulate the legitimate exchange.
            n = np.random.randint(0, 100)
            _, eavesdropped_msgs, n = protocol.protocol(k, l_c[j], l_k[i], n)

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

            # The attacker knows that the key is in the set `keys`.
            picked_k = np.random.choice(keys)

            def attacker_step_3(c, n):
                s_c = protocol.digit_dec_sum(c)
                t = picked_k + n
                s_t = protocol.digit_dec_sum(t)

                return s_t * s_c

            accepted, _, _ = protocol.protocol(k, l_c[j], l_k[i], n + 24, attacker_step_3)

            succ_p[j,i] += accepted

        compl[j,i] = timeit(single_run, number=sim_cnt)

compl /= sim_cnt
succ_p /= (sim_cnt)

# Plot the success attack probability.
plt.figure()
plt.title('Task 2: success attack probability vs key length')
plt.xlabel('Number of key bits')
plt.ylabel('Success attack probability [%]')
plt.grid()

for i in range(len(l_c)):
    plt.plot(l_k, succ_p[i]*100, label='l_c = %d' % l_c[i])
plt.legend()

# Plot the complexity.
plt.figure()
plt.title('Task 2: attack complexity vs key length')
plt.xlabel('Number of key bits')
plt.ylabel('Time per iteration [ms]')
plt.grid()

for i in range(len(l_c)):
    plt.plot(l_k, compl[i] * 1e3, label='l_c = %d' % l_c[i])
plt.legend()

plt.show()

