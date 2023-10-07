# Goal: learn the parameters of the HMM model (A, B, pi)
# This is accomplished with the Baum-Welch algorithm:
#   1. Initialize (A, B, pi)
#   2. Compute alpha, beta, di-gamma and gamma
#   3. Re-estimate (A, B, pi)
#   4. Go to 2 until convergence

from functions import *
import math


# Read input
a = read_matrix()
b = read_matrix()
pi = read_matrix()[0]
T, O = read_observations()

N = len(a) # Number of states
M = len(b[0]) # Number of different possible observations

max_iterations = 50
old_log_prob = -999999 # A very large negative number

for iterations in range(1, max_iterations):
    # Compute alpha, beta, di-gamma and gamma
    c, alpha = alpha_pass(a, b, pi, T, O)
    beta = beta_pass(a, b, T, O, c)
    di_gamma, gamma = compute_gamma(a, b, T, O, alpha, beta)

    # Re-estimate pi
    for i in range(0, N):
        pi[i] = gamma[0][i]

    # Re-estimate a
    for i in range(0, N):
        denom = 0
        for t in range(0, T-1):
            denom += gamma[t][i]
        for j in range(0, N):
            numer = 0
            for t in range(0, T-1):
                numer += di_gamma[t][i][j]
            denom += EPSILON
            a[i][j] = numer/denom

    # Re-estimate b
    for i in range(0, N):
        denom = 0
        for t in range(0, T):
            denom += gamma[t][i]
        for j in range(0, M):
            numer = 0
            for t in range(0, T):
                if O[t] == j:
                    numer += gamma[t][i]
            denom += EPSILON
            b[i][j] = numer/denom
    
    # Compute log(P[O|λ])
    log_prob = 0
    for i in range(0, T):
        log_prob = log_prob + math.log(c[i] + EPSILON)
    log_prob = -log_prob

    # Break if the model has converged (i.e. we are done)
    if iterations < max_iterations and log_prob > old_log_prob:
        old_log_prob = log_prob
    else:
        break

# Print answer
print(len(a), end = ' ')
print(len(a[0]), end = ' ')
for i in range(0, len(a)):
    for j in range(0, len(a[0])):
        print(round(a[i][j], 6), end = ' ')
print()

print(len(b), end = ' ')
print(len(b[0]), end = ' ')
for i in range(0, N):
    for j in range(0, M):
        print(round(b[i][j], 6), end = ' ')
print()