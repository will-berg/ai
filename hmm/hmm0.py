# Goal: find the probability distribution of the next observation

from functions import *


# Read input
A = read_matrix()
B = read_matrix()
PI = read_matrix()

# Calculate probability distribution of next emission (2 stages)
M1 = matrix_mult(PI, A)
M2 = matrix_mult(M1, B)

# Print answer
print(str(len(M2)) + ' ' + str(len(M2[0])), end=' ')
for i in range(0, len(M2[0])):
    print(M2[0][i], end=' ')
print()