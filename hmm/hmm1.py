# Goal: find, and print, the probability of the observation sequence O_1:T
# This is accomplished with the forward algorithm/α-pass

from functions import *


# Read input
A  = read_matrix()
B  = read_matrix()
PI = read_matrix()[0]
T, O  = read_observations()

N = len(A) # Number of states

alpha = [] # α_t(i) = probability of being in state i at time t, and having observed o_1:t

alpha.append([]) # α_1(i)

# Compute α_1(i)
for i in range(0, N):
    alpha[0].append(PI[i] * B[i][O[0]])

# Compute α_t(i) for t = 1..T
for t in range(1, T):
    alpha.append([])
    for i in range(0, N):
        alpha[t].append(0)
        # 
        for j in range(0, N):
            alpha[t][i] += alpha[t-1][j] * A[j][i]
        alpha[t][i] *= B[i][O[t]]

# Compute (and print) p = P(O|λ) by marginalizing over the states
p = 0
for i in range(0, N):
    p += alpha[T-1][i]

print(p)