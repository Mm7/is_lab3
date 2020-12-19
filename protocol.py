from random import randint

# Constants.
ID_A = 12345

# Some utils.
def random_key(l_k):
    return randint(1, 2**l_k - 1)

def random_challenge(l_c):
    return randint(1, 2**l_c - 1)

# Given an integer `n`. Return the base-10 sum its digits.
def digit_dec_sum(n):
    s = 0

    while n > 0:
        s += n % 10
        n //= 10

    return s


## Protocol implementation.

# Assuming that A, B exchanged the key `k` during the setup
# phase, this function implements the protocol described in the
# assignment.
#
# The parameter `n` is the last value for the counter. If not
# provided if defaults to `0`.
#
# The B side is computed automatically. On the other hand
# the message sent by A during the step 3 can be customized: by providing
# the function `a_res` (signature: [c,n] -> r) an user can decide
# how A responds to B in the 3rd step, this way it is very easy to
# implement an attack without rewriting all the code for the protocol.
# If such function is not provided, by default the legitimate response
# is implemented.
#
# The last two parameters are the length of key `l_k` and of the
# challenge `l_c`.
#
# The returned values are:
#   `accept`: a boolean which is `True` if B accepts A.
#   `msgs`: all the messages that were exchanged over the public
#           channel.
#   `n`: the new value for the `n` counter.
def protocol(k, l_c, l_k, n=0, a_res=None):
    # As a convention, let's name `step_i` the message sent
    # in the ith step.

    # Step 1: A -> B
    step_1 = ID_A

    # Step 2: B -> A
    c = random_challenge(l_c)
    n += 1

    step_2 = (c, n)

    # Step 3: A -> B

    # Implement the legitimate rensponse. Not needed here if
    # `a_res` is not `None`, but it'll be used in the next step,
    # so compute it anyway.
    s_c = digit_dec_sum(c)
    t = k + n
    s_t = digit_dec_sum(t)

    s = s_c * s_t
    leg_r = s

    if a_res is None:
        # Use the legitimate response.
        r = leg_r
    else:
        # Use the user provided function to compute the response.
        r = a_res(c, n)

    step_3 = r

    # Step 4:
    accept = leg_r == r
    msgs = [step_1, step_2, step_3]

    return accept, msgs, n


## If called directly run some tests.
if __name__ == '__main__':
    # If A is legitimate, then `accept` must be always `True`.
    # Run some randomized tests to confirm that.
    n = randint(0, 100)
    for _ in range(1000):
        accept, _, n = protocol(random_key(16), 16, 16, n)
        assert accept

    # Run a small example.
    k = 12345
    l_c = 16
    l_k = 16
    n = 98765

    print('Secret key: %d' % k)
    print('l_c: %d' % l_c)
    print('l_k: %d' % l_k)
    print('n: %d' % n)
    print('### simulation ###')

    accept, msgs, n = protocol(k, l_c, l_k, n)

    print('A->B: ' + str(msgs[0]))
    print('B->A: ' + str(msgs[1]))
    print('A->B: ' + str(msgs[2]))

    print('Is A authenticated: ' + str(accept))
    print('New n value: %d' % n)

