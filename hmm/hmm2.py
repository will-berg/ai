# Goal: estimate the state sequence with the most likely state sequence
# This is accomplished with the Viterbi algorithm

from functions import *


# Read input
A = read_matrix()
B = read_matrix()
PI = read_matrix()[0]
T, O = read_observations()

N = len(A) # Number of states

# δ_t(i) is the probability of having observed o_1:t and being in state i at time t,
# given the most likely preceeding state x_j
delta = []
delta.append([])

# δ_1(i)
for i in range(0, N):
    delta[0].append(B[i][O[0]]*PI[i])

# delta_idx tells us the state that most likely preceded state i at time t
# We can use this to backtrack once we get the most likely final state from δ
delta_idx = [[0 for _ in range(0, N)] for _ in range(0, T-1)]

# δ_2:T(i)
for t in range(1, T):
    delta.append([])
    for i in range(0, N):
        partial_delta = []
        for j in range(0, N):
            partial_delta.append(A[j][i]*delta[t-1][j]*B[i][O[t]])
        delta[t].append(max(partial_delta))
        # compute delta_idx[t][i]
        current_max = 0
        current_j = 0
        for j in range(0, N):
            next_value = A[j][i]*delta[t-1][j]*B[i][O[t]]
            if next_value > current_max:
                current_max = next_value
                current_j = j
        delta_idx[t-1][i] = current_j

# This is where we backtrack using delta and delta_idx

path = [0 for _ in range(0, T)] # The most likely state sequence

# Compute X*_T; the most likely state at the last time step
curr_j = 0
curr_max = 0
for j in range(0, N):
    next = delta[T-1][j]
    if next > curr_max:
        curr_j = j
        curr_max = next
path[T-1] = curr_j

# Compute X*_1:T-1 by repeatedly finding the most likely preceding state
for t in range(T-2, -1, -1):
    path[t] = delta_idx[t][path[t+1]]

for i in range(0, len(path)):
    print(path[i], end = ' ')
print()